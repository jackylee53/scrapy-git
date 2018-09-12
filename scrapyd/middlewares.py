# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .user_agents import user_agents

class UserAgentMiddleware(object):
    """ 换User-Agent """
    def process_request(self, request, spider):
        agent = random.choice(user_agents)
        request.headers["User-Agent"] = agent

class ScrapydSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
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


class ScrapydDownloaderMiddleware(object):
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

# middlewares下载中间件
# 导入随机数模块,目的是从IPPOOL中挑选一个IP
import random

# 从setting文件中引入设置好的IP
from scrapyd.settings import IPPOOL

# 导入官方文档HttpProxyMiddleware对应的模块
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

class IPPOOLS(HttpProxyMiddleware):
    def __init__(self, ip=''):
        self.ip = ip
    # process_request方法进行请求处理
    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print("当前使用的IP是" + thisip["ipaddr"])
        request.meta["proxy"] = "http://" + thisip["ipaddr"]

# 实现BrowserCookiesMiddleware,直接访问浏览器中的cookie
import browsercookie
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware

class BrowserCookiesMiddleWare(CookiesMiddleware):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.load_browser_cookies()

    def load_browser_cookies(self):
        # 加载chrome浏览器的cookie
        jar = self.jars['chrome']
        chrome_cookiejar = browsercookie.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)

        # 加载firefox浏览器的cookie
        jar = self.jars['firefox']
        firefox_cookiejar = browsercookie.firefox()
        for cookie in firefox_cookiejar:
            jar.set_cookie(cookie)