FROM node:lts-alpine

WORKDIR /app
COPY . /app
RUN npm install --registry=https://registry.npmmirror.com --production

CMD ["node", "app.js"]