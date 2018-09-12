# -*- coding: utf-8 -*-

import scrapy
from scrapyd.items import ScrapydMoreInfoItem
from scrapy.linkextractors import LinkExtractor

class BookstoresmoreinfoSpider(scrapy.Spider):
    name = 'bookstoresmoreinfo'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # 书籍列表的解析函数
    def parse(self, response):
        # 爬取书籍详细页URL
        le = LinkExtractor(restrict_css='article.product_pod h3')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, self.parse_book)
        # 爬取书籍列表页的URL
        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        if links:
            next_page = links[0].url
            yield scrapy.Request(next_page, self.parse)

    # 书籍页面的解析函数
    def parse_book(self, response):
        item = ScrapydMoreInfoItem()
        infos = response.css('div.product_main')
        name = infos.xpath('./h1/text()').extract_first()
        price = infos.css('p.price_color::text').extract_first()
        review_rate = infos.css('p.star-rating::attr("class")').re_first('star-rating ([A-Za-z]+)')

        colums = response.css('table.table.table-striped')
        review_number = colums.xpath('(.//tr)[last()]/td/text()').extract_first()
        upc = colums.xpath('(.//tr)[1]/td/text()').extract_first()
        stock = colums.xpath('(.//tr)[last() - 1]/td/text()').re_first('\((\d+) available\)')

        item['name'] = name
        item['price'] = price
        item['review_rating'] = review_rate
        item['review_num'] = review_number
        item['upc'] = upc
        item['stock'] = stock
        yield item
