#!/bin/bash
echo $GZCTF_FLAG > /flag
chmod 400 /flag
export GZCTF_FLAG=""
chmod u+s /usr/bin/date

useradd tomcat
chown -R tomcat:tomcat /usr/local/tomcat
su -c "/usr/local/tomcat/bin/catalina.sh run" tomcat