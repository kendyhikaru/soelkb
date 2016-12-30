package sparkexample;

import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.VoidFunction;

import org.apache.spark.streaming.Durations;

import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.api.java.JavaPairInputDStream;
import org.apache.spark.streaming.api.java.JavaDStream;


import scala.Tuple2;

// import org.apache.spark.streaming.kafka010.*;
import org.apache.spark.streaming.kafka.KafkaUtils;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import kafka.serializer.StringDecoder;

import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import static org.apache.spark.sql.functions.col;


public class Hello {
  public static void main(String[] args) throws Exception {
  	SparkSession spark = SparkSession
            .builder()
            .master("local[2]")
            .appName("Log Analyzer Streaming SQL")
            .getOrCreate();    
    JavaSparkContext sc = new JavaSparkContext(spark.sparkContext());
    JavaStreamingContext jssc = new JavaStreamingContext(sc, Durations.seconds(10));
	SQLContext sqlContext = new SQLContext(sc);

	Set<String> topicsSet = new HashSet<>(Arrays.asList("suricata-alert".split(",")));
    Map<String, String> kafkaParams = new HashMap<>();
    kafkaParams.put("metadata.broker.list", "kafka:9092");

    // Create direct kafka stream with brokers and topics
    JavaPairInputDStream<String, String> messages = KafkaUtils.createDirectStream(
        jssc,
        String.class,
        String.class,
        StringDecoder.class,
        StringDecoder.class,
        kafkaParams,
        topicsSet
    );
    JavaDStream<String> lines = messages.map(new Function<Tuple2<String, String>, String>() {
      @Override
      public String call(Tuple2<String, String> tuple2) {
        return tuple2._2();
      }
    });
    // Convert json to Dataset
    final List<Dataset<Row>> datasetArray = new ArrayList<Dataset<Row>>();
    lines.foreachRDD(new VoidFunction<JavaRDD<String>>() {
        @Override
        public void call(JavaRDD<String> rdd) {

          	Dataset<Row> allDf = sqlContext.read().json(rdd);
            // Check if have > 0 rows
            if(allDf.count() > 0)
            {
                allDf.createOrReplaceTempView("allDf");
                Dataset<Row> df = spark.sql("SELECT src_ip, src_port, dest_port, dest_ip, alert.severity, alert.signature_id, alert.signature, proto, flow_id FROM allDf");
                datasetArray.add(df);
            }
            
        }
	});
    System.out.println("Size: "+datasetArray.size());
    // Union to one dataset to group by
	jssc.start();              // Start the computation
	jssc.awaitTermination();   // Wait for the computation to terminate

  }
}
