# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapyd.items import ExampleItem

class DownloadpyfileSpider(scrapy.Spider):
    name = 'downloadpyfile'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):

        le = LinkExtractor(restrict_css='li.toctree-l2', deny='/index.html$')
        links = le.extract_links(response)
        for link in links:
            detail_page_url = link.url
            yield scrapy.Request(detail_page_url, callback=self.detail_page)

    def detail_page(self, response):

        href = response.css('div.section a.reference::attr("href")').extract_first()
        download_url = response.urljoin(href)
        example = ExampleItem()
        example['file_urls'] = [download_url]
        return example