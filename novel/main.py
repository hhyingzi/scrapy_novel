from scrapy.crawler import CrawlerProcess  # 用于开启spider进程
from scrapy.utils.project import get_project_settings  # 用于加载项目配置

# 天域
from spiders.tianyu import tianyu_novel_spider, tianyu_content_spider

# bqg123
from spiders.bqg123 import bqg123_novel_spider, bqg123_content_spider

process = CrawlerProcess(get_project_settings())

# 天域
# process.crawl(tianyu_novel_spider.NovelSpider) # info
process.crawl(tianyu_content_spider.TianyuContentSpider) # content


# bqg123
# process.crawl(bqg123_novel_spider.NovelSpider) # info
# process.crawl(bqg123_content_spider.ContentSpider)

process.start()