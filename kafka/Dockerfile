FROM java:8
RUN apt-get clean cache && apt-get update
RUN useradd kafka -m
RUN adduser kafka sudo
RUN apt-get install -y zookeeperd vim
RUN mkdir -p /data/
WORKDIR /data
COPY kafka_2.11-0.10.1.0.tgz /data
RUN tar -xvzf kafka_2.11-0.10.1.0.tgz
RUN mv kafka_2.11-0.10.1.0 kafka
RUN rm -rf /data/kafka/config/server.properties
COPY conf/server.properties /data/kafka/config/server.properties