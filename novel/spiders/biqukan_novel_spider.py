import logging

import scrapy
from novel.items import NovelItem, ChapterItem
import re
from scrapy import signals

class NovelSpider(scrapy.Spider):
    name = 'biqukan_novel_spider'
    allowed_domains = ['www.biqukan8.cc']

    start_urls = [
        'https://www.biqukan8.cc/34_34697/'  # 《班花》天朝书生，目录页
    ]
    novel_logger = logging.getLogger("TianyuNovelSpiderLogger")

    # 将小说信息存入数据库
    def parse(self, response):
        self.novel_logger.info(f"Parsing novel info. Url={response.url}.")
        novel_item = NovelItem()
        novel_item['title'] = response.xpath(".//div[@class='info']/h2/text()").get()  # 标题
        novel_item['author'] = re.search("作者：(.*)", response.xpath(".//div[@class='small']/span[1]/text()").get())[1]  # 作者
        novel_item['last_chapter'] = response.xpath(".//div[@class='small']/span[6]/a/text()").get()  # 最近更新章节
        update_date_text = response.xpath(".//div[@class='small']/span[5]/text()").get()
        novel_item['update_date'] = re.search("更新时间：(.*)", update_date_text).group(1)  # 最近更新日期
        novel_item['platform'] = '笔趣看：www.biqukan8.cc'  # 小说所在平台
        novel_item['platform_url'] = response.url  # 小说主页地址

        # 获取所有章节
        self.novel_logger.info(f"Parsing chapter list. Url={response.url}.")
        novel_item['chapters'] = []

        # 章节集合
        chapter_item = ChapterItem()

        chapters = response.xpath(".//dd[preceding-sibling::dt[2]]")
        chapter_index = 1;
        for chapter in chapters[:]:
            chapter_item['chapter_name'] = chapter.xpath(".//text()").get()  # 章节名
            chapter_item['chapter_url'] = 'http://' + self.allowed_domains[0] + chapter.xpath(".//@href").get()  # 章节url
            novel_item['chapters'].append({
                'chapter_index': chapter_index,
                'chapter_name': chapter_item['chapter_name'],
                'chapter_url': chapter_item['chapter_url']
            })
            chapter_index += 1
        yield novel_item

    # 设置爬虫日志
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NovelSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self):
        self.novel_logger.info(f"NovelSpider opened: id={id(self)}")

    def spider_closed(self, spider):
        self.novel_logger.info(f"NovelSpider closed: id={id(self)}")
