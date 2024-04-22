#!/bin/sh
mv /app/images/* /tmp/
rm -rf /app/images
echo $GZCTF_FLAG > /flag
node app.js