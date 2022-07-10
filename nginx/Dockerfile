FROM jwilder/nginx-proxy

RUN rm /etc/nginx/conf.d/default.conf
COPY vhost.d/default
COPY nginx.conf /etc/nginx/conf.d
