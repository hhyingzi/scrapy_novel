import scrapy

class TempSpiderSpider(scrapy.Spider):
    name = 'temp_spider'
    allowed_domains = ['m.zmccx.com', 'm.tycqzw.net']
    start_urls = ['http://m.tycqzw.net/69_69296/all.html']

    def parse(self, response):
        yield scrapy.Request(response.url, self.debug_response())

        # print('提示：', response.text)
        chapters = response.xpath(".//div[@id='chapterlist']//p")
        for chapter in chapters:
            print(chapter)
            print("chapter: ", chapter.xpath(".//text()").get())
            print("href: ", chapter.xpath(".//@href").get())

    def debug_response(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)