# 搭建 anaconda3 环境
FROM continuumio/anaconda3
ENV LANG C.UTF-8

COPY .condarc ~/.condarc
RUN conda clean -i
RUN conda create -n spider
RUN activate spider
RUN conda install scrapy selenium pymongo

# 工作目录
WORKDIR /novel

# 启动
ENTRYPOINT python ./novel/main.py
