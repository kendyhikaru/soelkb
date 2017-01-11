FROM logstash:5.0
RUN echo "Start install Logstash"
COPY GeoLite2-City.mmdb /opt
#RUN logstash-plugin install logstash-output-kafka
COPY elastic5-ossec-template.json /etc/logstash/elastic5-ossec-template.json
COPY wait-for-es.sh /
RUN chmod 755 /wait-for-es.sh