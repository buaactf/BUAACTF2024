FROM nikolaik/python-nodejs:python3.9-nodejs21-slim
WORKDIR /app
COPY app /app
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install seedrandom
EXPOSE 3001
CMD ["python", "app.py"]
