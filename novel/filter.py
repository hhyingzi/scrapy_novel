from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

# 自定义去重过滤器
# 原因：默认的去重过滤器，只根据 URL 过滤。但是有的小说网站（bqg123），章节内容的URL是相同的，只是GET请求参数不同，结果后续章节被过滤掉了。

# 在 Settings 中增加设置，类似于：DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
class MyDupeFilter(BaseDupeFilter):
    """
    覆盖默认去重过滤器。
    - 默认去重过滤器仅使用 URL 作为判断依据。
    - 本过滤器除判断 URL 外，还进一步根据 GET 请求的参数，作为判断依据。若参数不同，则不认为相同。

    尚未完成。
    """
    def __init__(self, path=None):
        self.seen = set()
        self.file = None

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        fingerprint = self.request_fingerprint(request)
        if fingerprint in self.seen:
            return True
        self.seen.add(fingerprint)
        return False

    def request_fingerprint(self, request):
        # Generate a unique fingerprint for the request
        # You can customize the fingerprint generation logic here
        return request_fingerprint(request)