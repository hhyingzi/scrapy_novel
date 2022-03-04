from scrapy import cmdline

# 数据来源：起点，纵横中文网
cmdline.execute('scrapy crawl qidian'.split())
cmdline.execute('scrapy crawl zongheng'.split())


# cmdline.execute('scrapy crawl TianYu_spider'.split())