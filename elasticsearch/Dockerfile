FROM elasticsearch:2.4
RUN echo "Start install ElasticSearch"
RUN plugin install royrusso/elasticsearch-HQ
RUN plugin install delete-by-query
RUN apt-get clean cache && apt-get update
RUN apt-get -y install python-pip
RUN pip install elasticsearch-curator
COPY etc/cron.daily /etc/cron.daily

