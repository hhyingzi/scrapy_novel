import logging

import scrapy
import novel.items as items
import re
from scrapy import signals
import pymongo
import configparser

class TianyuContentSpider(scrapy.Spider):
    name = 'tianyu_content_spider'
    allowed_domains = ['m.tycqzw.net']
    content_logger = logging.getLogger("ContentSpiderLogger")

    novel_name = None  # 小说名称

    def __init__(self):
        self.novel_name = None

        # 加载配置文件
        config = configparser.ConfigParser()
        config.read('mypass.ini')

        # 加载数据库配置
        self.mongo_host = config.get('mongodb', 'mongo_host')
        self.mongo_port = int(config.get('mongodb', 'mongo_port'))
        self.mongo_username = config.get('mongodb', 'mongo_username')
        self.mongo_password = config.get('mongodb', 'mongo_password')
        self.authSource = 'admin'  # 用于登录的数据库，需要指定为用户凭据所在位置
        self.db_novel = 'novel'  # 用于写入业务数据的数据库

        # 日志
        self.content_logger = logging.getLogger("ContentSpiderLogger")

        # 建立数据库连接
        self.client = pymongo.MongoClient(host=self.mongo_host,
                                          port=self.mongo_port,
                                          username=self.mongo_username,
                                          password=self.mongo_password,
                                          authSource=self.authSource)
        # 指定 database: novel
        self.db = self.client[self.db_novel]
        # 指定 collection
        self.novel_info_collection = self.db['novel_info']  # novel_info 用于预览小说
        self.content_collection = self.db['content']  # content 用于存储小说具体章节

        # 验证数据库连接
        try:
            self.client.admin.command('ping')
            self.content_logger.info("MongoDB connect successful.")
        except pymongo.errors.ConnectionFailure:
            self.content_logger.error("Mongodb server not available! 服务器无法连接！")
            exit(1)
        except pymongo.errors.OperationFailure:
            self.content_logger.error(
                f'Mongodb Authentication faild! 认证失败！ user:{self.mongo_username}, db:{self.authSource}')
            exit(1)

    def start_requests(self):
        # 获取小说名称
        self.novel_name = "满唐华彩"
        # 根据小说名称，查找 novel_info
        novel_info_query = self.novel_info_collection.find_one({
            'title': self.novel_name
        })
        # 获取章节列表：chapter_name, chapter_url,
        for chapter in novel_info_query['chapters'][:]:
            chapter_meta = {
                "chapter_name": chapter['chapter_name'],
                'chapter_index': chapter['chapter_index'],
                "book_name": self.novel_name,
                "chapter_url": chapter['chapter_url'],
                "content": ""
            }
            yield scrapy.Request(chapter_meta["chapter_url"], meta=chapter_meta, callback=self.parse)


    def parse(self, response):
        self.content_logger.info( f"Parsing content. Url={response.url}.")
        chapter_meta = response.meta

        content = response.xpath(".//div[@id='chaptercontent']//text()").getall()
        content = "".join(content)
        chapter_meta['content'] += content
        # 迭代至下一页
        if ("继续阅读" in content):
            nextpage_url = 'http://' + self.allowed_domains[0] + response.xpath(".//a[@id='pt_next']/@href").get()
            yield scrapy.Request(nextpage_url, callback=self.parse, meta=chapter_meta)
        else:
            chapter_item = items.ChapterItem()
            chapter_item['chapter_name'] = chapter_meta['chapter_name']
            chapter_item['chapter_index'] = chapter_meta['chapter_index']
            chapter_item['book_name'] = chapter_meta['book_name']
            chapter_item['chapter_url'] = chapter_meta['chapter_url']
            chapter_item['content'] = chapter_meta['content']
            yield chapter_item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TianyuContentSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self):
        self.content_logger.info(f"ContentSpider opened: id={id(self)}")

    def spider_closed(self, spider):
        self.content_logger.info(f"ContentSpider closed: id={id(self)}")
