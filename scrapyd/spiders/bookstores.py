#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy

from scrapy.selector import Selector
from scrapyd.items import ScrapydItem
from scrapy.linkextractors import LinkExtractor

class BookSpider(scrapy.Spider):
    name = "bookstores"

    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):

        item = ScrapydItem()

        for book in response.css('article.product_pod'):

            title = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()

            # yield {
            #     'name': title,
            #     'price': price
            # }
            item['name'] = title
            item['price'] = price
            yield item

        # next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        #
        # if next_url:
        #     page_url = response.urljoin(next_url)
        #     yield scrapy.Request(page_url, self.parse)

        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print("next_url", next_url)
            yield scrapy.Request(next_url, callback=self.parse)