# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import re

import scrapy.http
from scrapy import signals
import random
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import logging

class NovelSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NovelDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agent_list = [
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
             "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
             "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
             "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
             "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def process_request(self, request, spider):
        request.headers['User_Agent'] = random.choice(self.user_agent_list)
        return None


from selenium import webdriver
from scrapy.http import HtmlResponse

class SeleniumMiddleware:
    def __init__(self):
        # chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        from selenium.webdriver.chrome.service import Service
        service = Service(executable_path=r"C:\Users\12921\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        #self.browser = webdriver.Remote(command_executor='http://47.110.147.155:4444',desired_capabilities={'browserName': 'chrome'})
        self.driver.delete_all_cookies()
        self.novel_logger = logging.getLogger("MiddlewareLogger")

    def process_request(self, request, spider):
        self.novel_logger.info(f'Selenium id={id(self)} fetch：{request.url}')
        self.driver.get(request.url)
        url = request.url
        body = self.driver.page_source
        # 如果网页乱码，那么自己定义解码方式，本示例为 gbk
        return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='gbk', status=200)
        # return HtmlResponse(url=url, body=body, request=request, encoding=' utf-8', status=200)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # This method is used by Scrapy to create your spiders.
        selenium_middleware = cls()
        crawler.signals.connect(selenium_middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(selenium_middleware.spider_closed, signal=signals.spider_closed)
        return selenium_middleware

    def spider_opened(self, spider):
        self.novel_logger.info(f'Selenium id={id(self)} start.')

    def spider_closed(self, spider):
        self.driver.quit()
        self.novel_logger.info(f'Selenium id={id(self)} closed.')


class ResponseDecodeMiddleware:
    """将非 utf-8 编码的 response 进行正确 decode。"""
    def __init__(self):
        self.logger = logging.getLogger("ResponseDecodeMiddlewareLogger")
    def process_response(self, request, response, spider):
        encoding_html = response.xpath(".//meta/@content").get()
        if 'charset' not in encoding_html:
            return response
        # 响应编码非 utf-8 时，需改变其解码方式
        page_encoding = re.search("charset=(.*)", encoding_html)[1].strip()  # 'gbk'
        # 默认的 utf8 没问题
        if 'utf' in page_encoding.lower():
            return response
        # 笔趣看8：返回的 html 说是 gbk 编码，实际上是 utf-8。需用 utf-8 对内容解码。
        elif 'gb' in page_encoding.lower():
            self.logger.info(f"Response.encoding is {page_encoding}. Now convert to utf-8.")
            # 创建一个新的 TextResponse 对象，并指定其编码为 gbk，以使用 gbk 来解码。
            text_response = scrapy.http.TextResponse(
                url=response.url,
                status=response.status,
                headers=response.headers,
                body=response.body,
                encoding='utf-8'
            )
            return text_response
        else:
            self.logger.info(f"Response.encoding is {page_encoding}.")
            raise BaseException

