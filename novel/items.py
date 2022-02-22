# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 小说介绍
class NovelItem(scrapy.Item):
    # 小说标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()

    # 最新章节名
    last_chapter = scrapy.Field()
    # 更新时间
    update_date = scrapy.Field()

    # 小说链接
    novel_url = scrapy.Field()

# 小说目录
class CatalogItem(scrapy.Item):
    # 小说标题
    title = scrapy.Field()
    # 目录
    catalog = scrapy.Field()

# 章节内容
class ContentItem(scrapy.Item):
    # 章节标题
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()




