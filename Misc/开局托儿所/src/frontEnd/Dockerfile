FROM node:14-slim
COPY app /app
WORKDIR /app
RUN npm install -g serve
EXPOSE 3000
CMD ["serve","-s","/app"]
