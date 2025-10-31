# 《少妇白洁》小说爬虫
import logging

import scrapy
from novel.items import NovelItem, ChapterItem
import re
from scrapy import signals

class NovelSpider(scrapy.Spider):
    name = 'sfbj_spider'
    allowed_domains = ['m.41nr.com']
    start_urls = [
        'https://m.41nr.com/book/7553/',  # 少妇白洁
    ]
    novel_logger = logging.getLogger("ShaoFuBaiJieLogger")
    chapter_index = 1;

    # 介绍页
    def parse(self, response):
        self.novel_logger.info(f"Parsing novel info. Url={response.url}.")
        novel_item = NovelItem()
        novel_item['title']= '少妇白洁'  # 标题
        novel_item['author'] = '无'  # 作者
        novel_item['platform'] = self.allowed_domains[0]  # 小说所在平台
        novel_item['platform_url'] = self.start_urls[0]  # 小说主页地址
        novel_item['chapters'] = []  # 章节列表
        self.novel_item_cache = novel_item

        # 获取第一篇文章的url
        first_chapter_link = response.xpath("/html/body/div[@class='cover']/ul[@class='chapter']/li/a/@href").extract_first()
        first_chapter_absolute_link = response.urljoin(first_chapter_link)

        # 从第一页开始解析
        yield scrapy.Request(url=first_chapter_absolute_link, callback=self.parse_contents)

    # 解析章节正文
    def parse_contents(self, response):
        page_title = response.xpath("/html/body[@id='nr_body']/div[2]/div[@id='nr_title']/text()").get()  # 获取页面中的标题
        page_content = response.xpath("/html/body[@id='nr_body']/div[2]/div[@id='nr']/div//text()").getall()  # 获取所有文本
        page_content = '\n'.join(page_content)
        next_link = response.xpath("/html/body[@id='nr_body']/div[2]/div[@class='nr_page'][2]/table/tbody/tr/td[@class='next']/a[@id='pb_next']/@href").get()
        next_page_absolute_url = response.urljoin(next_link)
        chapter_item = ChapterItem()
        chapter_item['chapter_index'] = self.chapter_index
        self.chapter_index = self.chapter_index + 1
        chapter_item['chapter_name'] = page_title
        chapter_item['book_name'] = self.novel_item_cache['title']
        chapter_item['chapter_url'] = response.url
        chapter_item['content'] = page_content
        self.novel_item_cache['chapters'].append(chapter_item)

        # 下一页如果是目录页，则说明没有文章了
        if next_page_absolute_url == self.start_urls[0]:
            return
        # 访问下一页文章
        yield scrapy.Request(url=next_page_absolute_url, callback=self.parse_contents)

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



