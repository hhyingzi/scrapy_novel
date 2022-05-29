from scrapy.crawler import CrawlerProcess  # 用于开启spider进程
from scrapy.utils.project import get_project_settings  # 用于加载项目配置

from spiders import qidian
from spiders import zongheng

process = CrawlerProcess(get_project_settings())
process.crawl(qidian.QidianSpider)  # 进程1
process.crawl(zongheng.ZonghengSpider)  # 进程2
process.start()



# from scrapy import cmdline
# cmdline.execute('scrapy crawl qidian'.split())
# cmdline.execute('scrapy crawl zongheng'.split())
# cmdline.execute('scrapy crawl TianYu_spider'.split())