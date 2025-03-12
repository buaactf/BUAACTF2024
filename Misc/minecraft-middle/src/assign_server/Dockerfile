FROM python:3.9-slim
RUN apt-get clean
RUN apt-get update -y && apt-get install -y screen && apt-get install -y libicu-dev
WORKDIR /app
COPY app .
EXPOSE 25553
CMD ["python", "-u", "app.py"]