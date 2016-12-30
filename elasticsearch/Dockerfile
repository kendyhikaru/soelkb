FROM elasticsearch:2.4
RUN echo "Start install ElasticSearch"
COPY elasticsearch-HQ-master.zip /tmp
RUN plugin install file:///tmp/elasticsearch-HQ-master.zip
RUN echo "deb http://packages.elastic.co/curator/4/debian stable main" > /etc/apt/sources.list.d/es.list
RUN apt-get clean cache && apt-get update
RUN apt-get install elasticsearch-curator
COPY ./logging.yml /usr/share/elasticsearch/config/logging.yml
COPY etc/cron.daily /etc/cron.daily
