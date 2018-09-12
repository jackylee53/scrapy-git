# -*- coding: utf-8 -*-
import scrapy

class TestcssSpider(scrapy.Spider):
    name = 'testcss'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')
        for v in mingyan:
            content = v.css('.text::text').extract_first()
            author = v.css('.author::text').extract_first()
            tags = v.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            fileName = '/Users/jacky/project/scrapyd/scrapyd/spiders/' + '%s-语录.txt' % author
            with open(fileName, "a+") as f:
                print('tt')
                f.write(content)
                f.write('\n')
                f.write('标签：' + tags)
                f.write('\n-------\n')
                f.close()

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


