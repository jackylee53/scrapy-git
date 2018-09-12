# -*- coding: utf-8 -*-
"""
模拟登录
"""

import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = 'Login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    # 解析登录后下载的页面,本例子中为用户个人信息页面
    def parse(self, response):
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        yield dict(zip(keys, values))

    # 登录流程
    login_url = "http://example.webscraping.com/places/default/user/login"
    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    # 登录页面的解析函数,构造FormRequest对象提交表单
    def login(self, response):
        fb = {'email': 'liushuo@webscraping.com', 'password': '12345678'}
        yield FormRequest.from_response(response, formdata=fb, callback=self.parse_login)

    # 登录成功,继续爬取start_urls页面
    def parse_login(self, response):
        if 'Welcome Liu' in response.text:
            yield from super().start_requests()