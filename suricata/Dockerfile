FROM ubuntu:trusty
RUN echo "Start install Suricata"
RUN apt-get clean cache && apt-get update
RUN apt-get -y install build-essential libpcre3 libpcre3-dbg libpcre3-dev autoconf automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev libjansson4 pkg-config libgeoip1 libgeoip-dev wget build-essential vim python-pip python-dev git python-pip python-dev logrotate oinkmaster
ENV VER 3.1
WORKDIR /opt
COPY suricata-3.1.tar.gz /opt 
RUN tar -xvzf "suricata-$VER.tar.gz" 
WORKDIR "/opt/suricata-$VER" 
RUN ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-geoip
RUN make
RUN make install 
RUN ldconfig
RUN mkdir -p /etc/suricata/rules
COPY conf/suricata.yaml /etc/suricata/suricata.yaml
RUN cp threshold.config /etc/suricata/
RUN mkdir -p /var/log/suricata/
COPY etc/logrotate.d/suricata /etc/logrotate.d/suricata
RUN chmod 644 /etc/logrotate.d/*
RUN echo "Config ET Rule"
COPY etc/oinkmaster.conf /etc/oinkmaster.conf
RUN oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules





