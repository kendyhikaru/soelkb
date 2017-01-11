FROM elasticsearch:5.0.0
RUN echo "Start install ElasticSearch For Wazuh"
RUN echo "deb http://packages.elastic.co/curator/4/debian stable main" > /etc/apt/sources.list.d/es.list
RUN apt-get clean cache && apt-get update
RUN apt-get install elasticsearch-curator
COPY ./logging.yml /usr/share/elasticsearch/config/logging.yml
COPY etc/cron.daily /etc/cron.daily
