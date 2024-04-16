#!/bin/sh

echo $GZCTF_FLAG > /usr/share/nginx/html/flag

nginx -g 'daemon off;'