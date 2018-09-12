#!/usr/bin/python
# -*- coding: utf-8 -*-

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