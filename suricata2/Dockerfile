FROM ubuntu:trusty
RUN echo "Start install Suricata"
RUN apt-get update
RUN apt-get -y install build-essential libpcre3 libpcre3-dbg libpcre3-dev autoconf automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev libjansson4 pkg-config libgeoip1 libgeoip-dev wget build-essential
ENV VER 3.1
RUN wget "http://www.openinfosecfoundation.org/download/suricata-$VER.tar.gz" 
RUN tar -xvzf "suricata-$VER.tar.gz" 
WORKDIR "/suricata-$VER" 
RUN ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-geoip
RUN make
RUN make install 
RUN ldconfig
RUN mkdir -p /etc/suricata
COPY conf/suricata.yaml /etc/suricata

