import scrapy
from novel.items import NovelItem
import re
from logging import getLogger


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com']
    start_urls = [
        'https://book.qidian.com/info/1030870265/',  # 明克街13号
        'https://book.qidian.com/info/1032837638/',  # 金手指拍卖会
        'https://book.qidian.com/info/1030224513/',  # 我为截教仙
        'https://book.qidian.com/info/1021617576/',  # 夜的命名术
        'https://book.qidian.com/info/1025901449/',  # 我的治愈系游戏
        'https://book.qidian.com/info/1031299526/',  # 一品丹仙
        # '',  # 陆地键仙，纵横小说网
        'https://book.qidian.com/info/1029006481/',  # 不科学御兽
        'https://book.qidian.com/info/1031563172/',  # 丧失拿我当空气
        'https://book.qidian.com/info/1027714068/',  # 复活帝国
        'https://book.qidian.com/info/1030433215/',  # 我成了女反派的跟班
        'https://book.qidian.com/info/1024483590/',  # 当系统泛滥成灾
        # '',  # 我在菜市口斩妖除魔那些年
        'https://book.qidian.com/info/1027440366/',  # 视死如归魏君子
        'https://book.qidian.com/info/1031587468/',  # 修仙就是这样子的
    ]

    def parse(self, response):
        novel_item = NovelItem()
        try:
            novel_item['title'] = response.xpath("//div[normalize-space(@class='book-detail-wrap center990')]/div[normalize-space(@class='book-information cf')]/div[normalize-space(@class='book-info')]/h1/em/text()").extract_first()

            novel_item['author'] = response.xpath("//div[normalize-space(@class='book-detail-wrap center990')]/div[normalize-space(@class='book-information cf')]/div[normalize-space(@class='book-info')]/h1//a/text()").extract_first()

            novel_item['last_chapter'] = response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/text()").extract_first()

            alt = response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/@alt").extract_first()
            search_result = re.search("首发时间：(.*)章节字数", alt)
            date_result = search_result.group(1).strip()
            novel_item['update_date'] = date_result

            novel_item['pretty_update_date'] = response.xpath("//li[@class='update']/div[@class='detail']/p[1]/em/text()").extract_first()  # <number>小时前

            # novel_item['novel_url'] = "https://" + response.xpath("//div[@id='j-catalogWrap']/div[@class='volume-wrap']/div[last()]//li[last()]/h2[@class='book_name']/a/@href").extract_first()
        except BaseException:
            logger = getLogger()
            logger.debug('Item parse fail.')

        yield novel_item


