FROM nginx
RUN echo "Start install Nginx"
RUN apt-get update && apt-get install -y apache2-utils curl
RUN htpasswd -b -c /etc/nginx/htpasswd.users kibanaadmin fsoc@123
RUN mkdir -p /var/log/nginx/soelk/
COPY wait-for-es.sh /
RUN chmod 755 /wait-for-es.sh
EXPOSE 80
