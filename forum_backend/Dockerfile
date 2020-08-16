FROM python:3.7
LABEL maintainer="zengzhengrong"
ENV PYTHONUNBUFFERED 1
ENV TZ='Asia/Shanghai'
RUN mkdir /api
WORKDIR /api
COPY . /api

EXPOSE 8000 5555

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

