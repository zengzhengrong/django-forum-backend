FROM python:3.7
LABEL maintainer="zengzhengrong"
ENV PYTHONUNBUFFERED 1

RUN mkdir /api
WORKDIR /api
COPY . /api

RUN rm -f /etc/localtime \
    && ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

RUN ["chmod", "+x", "/api/entrypoint.sh"]
RUN ["chmod", "+x", "/api/wait-for-it.sh"]
EXPOSE 8000 5555

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

