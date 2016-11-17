FROM ubuntu:trusty
RUN echo "Start install Suricata"
RUN apt-get clean cache && apt-get update
RUN apt-get -y install build-essential libpcre3 libpcre3-dbg libpcre3-dev autoconf automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev libjansson4 pkg-config libgeoip1 libgeoip-dev wget build-essential vim python-pip python-dev git python-pip python-dev
ENV VER 3.1
RUN wget "http://www.openinfosecfoundation.org/download/suricata-$VER.tar.gz" 
RUN tar -xvzf "suricata-$VER.tar.gz" 
WORKDIR "/suricata-$VER" 
RUN ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-geoip
RUN make
RUN make install 
RUN ldconfig
RUN mkdir -p /etc/suricata/rules
COPY conf/suricata.yaml /etc/suricata/suricata.yaml
COPY etc/suricata /etc/init.d/suricata
RUN chmod 755 /etc/init.d/suricata
RUN mkdir -p /var/log/suricata/
RUN service suricata start
RUN echo "Install Scirius"
WORKDIR /opt
RUN wget https://github.com/StamusNetworks/scirius/archive/scirius-1.1.13.tar.gz
RUN tar xvf scirius-1.1.13.tar.gz
WORKDIR /opt/scirius-scirius-1.1.13
RUN pip install --upgrade six
RUN pip install -r requirements.txt
RUN pip install django-revproxy
RUN python manage.py migrate --noinput
COPY scirius.json /tmp
RUN python manage.py loaddata /tmp/scirius.json
RUN python manage.py createcachetable my_cache_table
RUN python manage.py addsource "ETOpen Ruleset" https://rules.emergingthreats.net/open/suricata-3.0/emerging.rules.tar.gz http sigs
RUN python manage.py addsource "SSLBL abuse.ch" https://sslbl.abuse.ch/blacklist/sslblacklist.rules http sig
RUN python manage.py addsource "PT Research Ruleset" https://github.com/ptresearch/AttackDetection/raw/master/pt.rules.tar.gz http sigs
RUN python manage.py defaultruleset "Default SELKS ruleset"
RUN python manage.py disablecategory "Default SELKS ruleset" stream-events
RUN python manage.py addsuricata suricata "Suricata on SELKS" /etc/suricata/rules "Default SELKS ruleset"
RUN python manage.py updatesuricata
COPY settings.py /opt/scirius-scirius-1.1.13/scirius/settings.py





