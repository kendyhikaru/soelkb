from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json, urllib2, urllib, datetime
def check_Index_Exists(host, port, index):
	url = "http://{0}:{1}/{2}?pretty".format(host,port,index)
	try:
		urllib2.urlopen(url)
		return True
	except urllib2.HTTPError as err:
		if(err.code == 404):
			return False
		else:
			print(err.code)
			return False
def insert_ES(host, port, index, data):
	url = "http://{0}:{1}/{2}/message".format(host,port,index)
	jsonValue = json.dumps(data).encode('utf8')
	data2 = urllib.urlencode(data)
	req = urllib2.Request(url=url, data=jsonValue)
	req.get_method = lambda: 'POST'
	f = urllib2.urlopen(req)
	response = f.read()
	print(response)
def create_Object(src_ip,src_port,dest_port,dest_ip,proto,signature_id,signature,severity,num,flow_ids,timestamps,message):
	tmp = {
		"@timestamp":datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),
		"ip_src_addr":src_ip,
		"ip_src_port":list(set(src_port)),
		"ip_dst_port":list(set(dest_port)),
		"ip_dst_addr":dest_ip,
		"protocol":proto,
		"type":"Network IDS",
		"timestamps":timestamps,
		"message": message,
		"extra_info":
		{
			"number_related": num,
			"flow_ids":flow_ids,
			"signature_id":signature_id,
			"signature":signature,
			"severity":severity
		}
	}
	return tmp
def save_To_ES(data):
	pass
if __name__ == "__main__":
	spark = SparkSession\
		.builder\
		.appName("StructuredKafkaProcessing")\
		.getOrCreate()
	batchDuration = 60*(1) #Duration
	# Stream Kafka context
	context = spark.sparkContext
	context.setLogLevel("WARN")
	ssc = StreamingContext(context, batchDuration)
	kvs = KafkaUtils.createDirectStream(ssc, ["suricata-alert"], {"metadata.broker.list": "kafka:9092"})
	lines = kvs.map(lambda x: x[1])
	# Create dateframe for each rdd
	def rdd_Process(rdd):
		allDf = spark.read.json(rdd)
		allDf.createOrReplaceTempView("allDf")
		if(allDf.count() > 0):
			df1 = spark.sql("SELECT src_ip, src_port, dest_port, dest_ip, alert.severity AS severity, alert.signature_id AS signature_id , alert.signature AS signature, proto, flow_id, timestamp, alert.category AS category FROM allDf")
			df1.createOrReplaceTempView("df")
			#Aggreantation
			alerts = spark.sql("SELECT src_ip, COLLECT_LIST(src_port) AS src_port, COLLECT_LIST(dest_port) AS dest_port, dest_ip, proto, signature_id, signature, severity, COUNT(*) AS num, COLLECT_LIST(flow_id) AS flow_ids, COLLECT_LIST(timestamp) AS timestamps, category FROM df GROUP BY signature_id, src_ip, dest_port, dest_ip, proto, signature, severity, category").collect();
			for alert in alerts:
				message = "{0}: {1} from {2} to {3} {4} times".format(alert["category"],alert["signature"],alert["src_ip"],alert["dest_ip"],alert["num"])
				alert_line = (create_Object(alert["src_ip"],alert["src_port"],alert["dest_port"],alert["dest_ip"],alert["proto"],alert["signature_id"], alert["signature"], alert["severity"], alert["num"], alert["flow_ids"], alert["timestamps"],message))
				# print(alert_line)
				insert_ES("elasticsearch",9200,"alert",alert_line)
	lines.foreachRDD(rdd_Process)

	ssc.start()
	print("Start Spark Streaming")
	# insert_ES("elasticsearch",9200,"alert",{"aa":"Fds"})
	ssc.awaitTermination()
