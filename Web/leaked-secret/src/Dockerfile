FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY robots.txt /usr/share/nginx/html/robots.txt
COPY nginx.conf /usr/share/nginx/html/secret.conf
COPY start.sh /
RUN chmod +x start.sh
WORKDIR /

CMD ["./start.sh"]