import scrapy
from items import TempItem

class TempSpiderSpider(scrapy.Spider):
    name = 'temp_spider'
    allowed_domains = ['www.nowcoder.com']
    start_urls = ['https://www.nowcoder.com/exam/oj?page=1&tab=SHELL%E7%AF%87&topicId=195']

    def parse(self, response):
        temp_item = TempItem()

        items = response.xpath('//*[@id="jsApp"]/main/div[2]/div[1]/div[2]/div[3]/div[2]/div/div/div/div/div[2]/div/div[3]/table/tbody/tr')
        for item in items:
            temp_item['title_num'] = item.xpath(".//td[2]//span/text()").extract_first()
            temp_item['title_content'] = item.xpath(".//td[3]//a//text()").extract_first().strip()
            print("["+temp_item['title_num']+"]" + "(#"+temp_item['title_num'].lower()+"-" + temp_item['title_content']+")")
