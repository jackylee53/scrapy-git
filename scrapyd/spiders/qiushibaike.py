# -*- coding: utf-8 -*-
import scrapy
from scrapyd.items import QiuShiBaiKe
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor

class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com',
                  'https://www.qiushibaike.com/hot',
                  'https://www.qiushibaike.com/imgrank/',
                  'https://www.qiushibaike.com/text/',
                  'https://www.qiushibaike.com/history/',
                  'https://www.qiushibaike.com/pic/',
                  'https://www.qiushibaike.com/textnew/']

    column_names = {
        'hot': '24小时',
        'imgrank': '热图',
        'text': '文字',
        'history': '穿越',
        'pic': '糗图',
        'textnew': '新鲜'
    }

    def start_requests(self):
        requests = []
        for item in self.start_urls:
            column_value = None
            for column_name in self.column_names:
                if column_name in item:
                    column_value = self.column_names[column_name]
            if not column_value:
                column_value = '热门'
            requests.append(scrapy.Request(url=item, headers={'Referer': 'https://www.qiushibaike.com'},\
                                           meta={'column_value': column_value}))
        return requests

    def parse(self, response):
        pattern = '/.+/page/.+'
        le = LinkExtractor(restrict_css='div[id="content-left"] a', allow=pattern)
        links = le.extract_links(response)
        print("links", links)
        for link in links:
            yield scrapy.Request(url=link.url, callback=self.parse_content, meta=response.meta)

    def parse_content(self, response):
        item = QiuShiBaiKe()
        tags = response.xpath('//div[contains(@id, "qiushi_tag")]')
        for tag in tags:
            author = tag.xpath('./div[contains(@class, "author")]/a[2]/h2/text()').extract_first()
            content = tag.xpath('.//div[@class="content"]/span/text()').extract()
            imgurl = tag.xpath('./div[@class="thumb"]/a/img/@src').extract_first()
            vote_number = tag.xpath('.//span[@class="stats-vote"]/i/text()').extract_first()

            if imgurl:
                imgurl = urljoin(response.url, imgurl)

            # 截取含换行符
            if author:
                author = author.strip()
            # 截取含换行符并拼接字段
            rescontent = ''
            if len(content) > 0:
                for i in content:
                    rescontent = rescontent + i.replace('\n', '')

            item['column_name'] = response.meta['column_value']
            item['author'] = author
            item['content'] = rescontent
            item['vote_number'] = vote_number
            item['imgurl'] = imgurl

            yield item

