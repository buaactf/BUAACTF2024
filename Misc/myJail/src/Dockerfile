FROM python:3.9-slim
RUN apt-get clean
RUN apt-get update -y && apt-get install -y ncat
COPY src.py /app/src.py
COPY flag /FlAg_1s_H3re
WORKDIR /app
EXPOSE 8888
CMD ncat -l 8888 -c "python src.py" -k