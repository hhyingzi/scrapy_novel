import logging

import scrapy
from novel.items import NovelItem, ChapterItem
import re
from scrapy import signals

class NovelSpider(scrapy.Spider):
    name = 'tianyu_novel_spider'
    allowed_domains = ['m.tycqzw.net']

    start_urls = [
        # 末尾要加 /
        'http://m.tycqzw.net/152_152242/',  # 喜欢捉弄人的老婆很可恶啊
    ]
    novel_logger = logging.getLogger("TianyuNovelSpiderLogger")

    def parse(self, response):
        self.novel_logger.info(f"Parsing novel info. Url={response.url}.")
        novel_item = NovelItem()
        novel_item['title'] = response.xpath(".//span[@class='title']/text()").get()  # 标题
        novel_item['author'] = response.xpath(".//p[@class='author']/text()").get()  # 作者
        novel_item['last_chapter'] = response.xpath(".//div[@class='directoryArea']/p[1]/a/text()").get()  # 最近更新章节
        update_date_text = response.xpath(".//h2[@class='str-over-dot']/a/text()").get()
        novel_item['update_date'] = re.search("更新：(.*)", update_date_text).group(1)  # 最近更新日期
        novel_item['platform'] = '天域小说网'  # 小说所在平台
        novel_item['platform_url'] = response.url  # 小说主页地址
        # 获取所有章节
        yield scrapy.Request(url=f"{self.start_urls[0]}/all.html", callback=self.parse_chapters, meta={'novel_item': novel_item})

    # 从目录页，解析所有章节
    def parse_chapters(self, response):
        self.novel_logger.info(f"Parsing chapter list. Url={response.url}.")

        novel_item = response.meta['novel_item']
        novel_item['chapters'] = []

        # 章节集合
        chapter_item = ChapterItem()

        chapters = response.xpath(".//div[@id='chapterlist']//p")
        chapter_index = 1;
        for chapter in chapters[1:]:  # 第一个元素不是章节
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
