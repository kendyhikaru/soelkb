FROM java:8
RUN apt-get update && apt-get install -y vim maven net-tools netcat
COPY spark-2.0.2-bin-hadoop2.7.tgz /tmp
WORKDIR /tmp
RUN tar xvf spark-2.0.2-bin-hadoop2.7.tgz 
RUN mv spark-2.0.2-bin-hadoop2.7 spark
RUN cp -R spark /srv/
RUN mkdir -p /workdir/app1
WORKDIR /workdir/app1
#RUN mvn dependency:resolve
