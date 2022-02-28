import scrapy
from novel.items import NovelItem
import re
from logging import getLogger

class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['book.zongheng.com']
    start_urls = [
        'http://book.zongheng.com/book/1005752.html'  # 陆地键仙
    ]

    def parse(self, response):
        novel_item = NovelItem()
        try:
            novel_item['title'] = response.xpath("//div[@class='book-name']/text()").extract_first().strip()

            novel_item['author'] = response.xpath("//div[@class='au-name']/a/text()").extract_first()

            novel_item['last_chapter'] = response.xpath("//div[@class='book-new-chapter']/div[@class='tit']/a/text()").extract_first()

            catalog_url = response.xpath("//a[@class='all-catalog']/@href").extract_first()
            yield scrapy.Request(url=catalog_url, callback=self.parse_catalog, cb_kwargs=dict(novel_item=novel_item))
            # yield response.follow(url=catalog_url, callback=self.parse_catalog, cb_kwargs=dict(novel_item=novel_item))

            alt = response.xpath("//div[@class='book-new-chapter']/div[@class='time']").extract_first()  # <number>小时前
            search_result = re.search("· ([0-9]*.*前)", alt)
            pretty_date_result = search_result.group(1).strip()
            novel_item['pretty_update_date'] = pretty_date_result

            # novel_item['novel_url'] = "//div[@class='book-new-chapter']/div[@class='tit']/a/@href").extract_first()
        except BaseException:
            logger = getLogger()
            logger.debug('Item parse fail.')

        # yield novel_item
        # print('now', novel_item)

    def parse_catalog(self, response, novel_item):
        alt = response.xpath("//div[@class='volume-list']/div[last()]/ul/li[last()]/a/@title").extract_first()
        search_result = re.search("更新时间：(.*)", alt)
        date_result = search_result.group(1).strip()
        novel_item['update_date'] = date_result
        # print('sec', novel_item)
        yield novel_item


