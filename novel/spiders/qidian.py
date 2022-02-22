import scrapy
from novel.items import NovelItem
import re

class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com/']
    start_urls = [
        'https://book.qidian.com/info/1030870265/',  # 明克街13号
        'https://book.qidian.com/info/1032837638/',  # 金手指拍卖会
    ]

    def parse(self, response):
        novel_item = NovelItem()
        novel_item['title'] = response.xpath("//div[normalize-space(@class='book-detail-wrap center990')]/div[normalize-space(@class='book-information cf')]/div[normalize-space(@class='book-info')]/h1/em/text()").extract_first()
        novel_item['author'] = response.xpath("//div[normalize-space(@class='book-detail-wrap center990')]/div[normalize-space(@class='book-information cf')]/div[normalize-space(@class='book-info')]/h1//a/text()").extract_first()
        novel_item['last_chapter'] = response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/text()").extract_first()

        alt = response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/@alt").extract_first()
        search_result = re.search("首发时间：(.*)章节字数", alt)
        date_result = search_result.group(1).strip()
        novel_item['update_date'] = date_result

        novel_item['novel_url'] = "https://" + response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/@href").extract_first()
        print(novel_item)
