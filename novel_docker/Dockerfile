# 搭建 anaconda3 环境
FROM continuumio/anaconda3
ENV LANG C.UTF-8

COPY .condarc /root/.condarc
RUN conda clean -i && conda info | grep "user config\|channel" && sleep 5 && conda install scrapy selenium pymongo pytz

# 工作目录
WORKDIR /novel

# 启动
ENTRYPOINT python ./novel/main.py
