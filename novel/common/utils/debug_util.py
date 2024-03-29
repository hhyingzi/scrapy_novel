# 一个用于调试的模板，复制粘贴参考用，不直接运行
def parse(self, response):
    from scrapy.shell import inspect_response
    inspect_response(response, self)
    exit(0)


def cmdrun():
    # from scrapy import cmdline
    # cmdline.execute('scrapy crawl qidian'.split())
    # cmdline.execute('scrapy crawl TianYu_spider'.split())
    pass


def processrun():
    from scrapy.crawler import CrawlerProcess  # 用于开启spider进程
    from scrapy.utils.project import get_project_settings  # 用于加载项目配置
    # from spiders import tianyu_novel_spider
    # from spiders import tianyu_content_spider

    process = CrawlerProcess(get_project_settings())

    # 天域
    # process.crawl(tianyu_novel_spider.NovelSpider) # 爬取小说信息
    # process.crawl(tianyu_content_spider.TianyuContentSpider)  # 爬取章节内容信息(诡电脑)

    process.start()
    pass
