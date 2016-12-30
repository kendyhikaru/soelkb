FROM kibana:4
RUN echo "Start install Kibana4"
RUN apt-get update && apt-get install -y netcat git-core curl net-tools
RUN kibana plugin -i elastic/timelion
RUN git clone https://github.com/StamusNetworks/KTS.git
WORKDIR KTS
RUN patch -p1 -d /opt/kibana/  < /KTS/patches/kibana-integer.patch
RUN patch -p1 -d /opt/kibana/  < /KTS/patches/timelion-integer.patch
RUN echo 0 > /frist_boot
RUN mkdir -p /var/log/kibana/
COPY wait-for-es.sh /
RUN chmod 755 /wait-for-es.sh


