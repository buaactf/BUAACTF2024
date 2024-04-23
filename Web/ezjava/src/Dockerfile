FROM tomcat:8.5.92

COPY ezjava-1.0-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war
COPY serialkiller.xml /etc/serialkiller.xml
COPY root.sh /root/root.sh

CMD ["/root/root.sh"]