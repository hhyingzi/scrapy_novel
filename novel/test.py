from pipelines import MongoPipeline
from scrapy import cmdline

def print_overview():
    MongoPipeline().print_overview()


if __name__ == '__main__':
    print_overview()
    # cmdline.execute('scrapy crawl qidian'.split())














