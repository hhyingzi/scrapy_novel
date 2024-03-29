# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from typing import List

# 小说介绍
# class NovelItem(scrapy.Item):
#     # 小说名
#     title = scrapy.Field()
#     # 作者
#
#     author = scrapy.Field()
#
#     # 最新章节名
#     last_chapter = scrapy.Field()
#     # 更新日期和时间
#     update_date = scrapy.Field()
#     pretty_update_date = scrapy.Field()
#
#     # 小说链接
#     # novel_url = scrapy.Field()
#
# class TempItem(scrapy.Item):
#     title_num = scrapy.Field()
#     title_content = scrapy.Field()

class NovelItem(scrapy.Item):
    title = scrapy.Field()  # 小说名称
    author = scrapy.Field()  # 作者
    update_date = scrapy.Field()  # 最近更新时间
    platform = scrapy.Field()  # 该小说内容，被爬取的平台，例如天域小说网等。
    platform_url = scrapy.Field()  # 小说在该平台的 url 页
    chapters = scrapy.Field()  # [{chapter_index, chapter_name，chapter_url}] 是{索引号，章节名，url} 组成的列表
    # 爬虫业务计算该字段
    last_chapter = scrapy.Field()  # 最近更新章节。 = chapters[-1].chapter_name

    # 业务字段，非爬虫提供。
    read_chapter: str = scrapy.Field()  # 最近阅读章节的标题（由后端修改）
    invalid_chapter_list = scrapy.Field()  # 无效章节标题列表，待执行定时任务，进行删除
    new_chapter_list = scrapy.Field()  # 待爬取的章节列表。格式为 {章节标题，章节索引号，章节url}。
    # 需要先在 chapters 中维护好这些内容，再加入此列表。

class ChapterItem(scrapy.Item):
    chapter_index = scrapy.Field()  # 章节序号
    chapter_name = scrapy.Field()  # 章节标题
    book_name = scrapy.Field()  # 书名（非爬虫提供，书名）
    # update_time = scrapy.Field()  # 章节更新时间
    chapter_url = scrapy.Field()  # 章节url
    content = scrapy.Field()  # 章节内容
