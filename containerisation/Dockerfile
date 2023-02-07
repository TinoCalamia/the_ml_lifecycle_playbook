FROM python:3.9.10-slim
LABEL maintainer="your_mail@gmail.com" service=service_name

COPY requirements.txt ./

# Install python packages
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install --no-cache-dir --upgrade --upgrade-strategy=eager -r requirements.txt
RUN pip install jupyterlab
