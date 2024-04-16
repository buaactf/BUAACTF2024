FROM node:lts-alpine as build

WORKDIR /build
COPY . /build
# RUN npm install vue --registry=https://registry.npmmirror.com
# RUN npm install axios --registry=https://registry.npmmirror.com
# RUN npm install pinia --registry=https://registry.npmmirror.com
RUN npm install --registry=https://registry.npmmirror.com
RUN npm run build

FROM nginx:stable-alpine as deploy

RUN rm -rf /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html
COPY --from=build /build/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
