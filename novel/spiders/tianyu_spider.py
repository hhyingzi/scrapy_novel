import scrapy
from novel.items import NovelItem


class NovelSpiderSpider(scrapy.Spider):
    name = 'TianYu_spider'
    allowed_domains = ['m.zmccx.com']

    # start_urls = ['https://m.zmccx.com']  # 主站
    start_urls = ['https://m.zmccx.com/mybook.php']  # 书架
    custom_settings = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "m.zmccx.com",
        "Referer": "https://m.zmccx.com/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }

    # tianyu login info
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "m.zmccx.com",
            "Referer": "https://m.zmccx.com/",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }
    login_url = "https://m.zmccx.com/login.php"
    post_url = "https://m.zmccx.com/login.php"
    booklist_url = "https://m.zmccx.com/mybook.php"
    cookies = {
        "UM_distinctid": "17ea8e4e602751-00f73c9c90ee35-f791539-1fa400-17ea8e4e603e64",
        "username": "User",
        "identity-frontend": "1fd695bb7ff34b54d94f3786abc17cb38433e5833fe8855dd66dd983a9bf0420a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A18%3A%22%5B49179%2C%22%22%2C2592000%5D%22%3B%7D",
        "PHPSESSID": "8cvs3et0d9f5ccglkhke0ncn83",
        "CNZZDATA1280630367": "326847757-1643508673-%7C1643792442",
        "Hm_lvt_8864929e24dc8d5d318b9b675ee61d96": "1643511081,1643794078",
        "Hm_lpvt_8864929e24dc8d5d318b9b675ee61d96": "1643794284"
    }
    post_data = {
        'LoginForm[username]': 'hhyingzi',
        'LoginForm[password]': 'fghf1098',
        'login_hold': '1'
    }

    def start_requests(self):
        yield scrapy.FormRequest(url=self.post_url, formdata=self.post_data, headers=self.headers, callback=self.after_login)

    def after_login(self, login_response):
        yield scrapy.Request(url=self.booklist_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # 判断是否为登录页
        title = response.xpath(".//span[@class='title']/text()").extract_first()

        if title == "天域小说网会员登录":
            print("需要登录")
            self.start_requests()
        else:
            self.book_list_parse(response)  # 解析书架

    def book_list_parse(self, response):
        novel_list = response.xpath(".//div[@class='slide-item list1']/div[@class='hot_sale']")
        for i_item in novel_list:
            novel_item = NovelItem()  # 实例化NovelItem类

            novel_item['novel_title'] = i_item.xpath("./a/p[@class='title']/text()").extract_first().strip()
            novel_item['novel_url'] = self.allowed_domains[0] + i_item.xpath("./a/@href[1]").extract_first()
            novel_item['autor'] = i_item.xpath("./a/p[@class='author']/text()").extract_first().strip()
            novel_item['last_chapter'] = i_item.xpath("./p[@class='author'][1]/a/text()").extract_first().strip()

            print(novel_item)


