# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # 小说标题
    novel_title = scrapy.Field()

    # 小说链接
    novel_url = scrapy.Field()

    # 作者
    autor = scrapy.Field()

    # 最新章节名
    last_chapter = scrapy.Field()
