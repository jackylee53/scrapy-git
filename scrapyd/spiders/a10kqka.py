# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class A10kqkaSpider(scrapy.Spider):
    name = '10kqka'
    allowed_domains = ['d.10jqka.com.cn']
    start_urls = ['http://d.10jqka.com.cn/v6/time/gzs_N225/last.js']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})

    def parse(self, response):
        
        for sel in response.css('div.quote'):
            quote = sel.css('span.text::text').extract_first()
            author = sel.css('small.author::text').extract_first()
            # splashquites = SplashQuotesItem()
            # splashquites['quote'] = quote
            # splashquites['author'] = author
            print("quote")
            print("quote", quote)
            yield {'quote': quote, 'author': author}
        href = response.css('li.next a::attr(href)').extract_first()
        if href:
            url = response.urljoin(href)
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})

