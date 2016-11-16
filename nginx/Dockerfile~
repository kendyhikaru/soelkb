FROM nginx
RUN echo "Start install Nginx"
RUN apt-get update && apt-get install -y apache2-utils
RUN htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
