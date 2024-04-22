FROM node:alpine

WORKDIR /app

COPY . .

RUN npm set registry https://registry.npmmirror.com/ && \
    npm install && \
    chmod +x start.sh

CMD ["/bin/sh", "/app/start.sh"]