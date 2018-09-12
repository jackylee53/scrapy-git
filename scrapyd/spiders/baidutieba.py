# -*- coding: utf-8 -*-
import json
import scrapy
from urllib.parse import quote, urljoin
from scrapyd.items import BaiduTieBa
from scrapy.linkextractors import LinkExtractor

class BaidutiebaSpider(scrapy.Spider):
    name = 'baidutieba'
    allowed_domains = ['tieba.baidu.com']
    keyword = 'python爬虫'
    baseurl = 'https://tieba.baidu.com/'
    urlname = 'https://tieba.baidu.com/f?ie=utf-8&kw={keyword}&fr=search'
    start_urls = [urlname.format(keyword=quote(keyword))]

    def parse(self, response):
        # 提取起始页所有帖子的URL
        links = response.css('ul[id="thread_list"] div[class="threadlist_lz clearfix"]')

        for link in links:
            tzid = link.xpath('./div/a/@href').extract_first()
            tzname = link.xpath('./div/a/@title').extract_first()
            tzurl = urljoin(response.url, tzid)
            author = link.xpath('./div/span[@class="tb_icon_author "]/@title').extract_first()
            userid = link.xpath('./div/span[@class="tb_icon_author "]/@data-field').extract_first()
            userid = json.loads(userid)['user_id']
            yield scrapy.Request(tzurl, callback=self.parse_content, meta={'tzname': tzname, 'author': author,\
                                                                            "userid": userid, 'tzurl': tzurl})
        # 提取并判断是否包含下一页的链接
        next_page_url = response.xpath('//div[@id="frs_list_pager"]/a[contains(@class,"next")]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        tiezi = BaiduTieBa()
        contents = response.css('div[id="j_p_postlist"] div[class="l_post l_post_bright j_l_post clearfix  "]')
        for content in contents:

            data_field = content.xpath('./@data-field').extract_first()
            contentinfo = json.loads(data_field)
            subauthor = contentinfo['author'].get('user_name')
            subuserid = contentinfo['author'].get('user_id')
            subcontent = contentinfo['content'].get('content')

            tiezi['keyword'] = self.keyword
            tiezi['tzurl'] = response.meta['tzurl']
            tiezi['tzname'] = response.meta['tzname']
            tiezi['author'] = response.meta['author']
            tiezi['userid'] = response.meta['userid']
            tiezi['subauthor'] = subauthor
            tiezi['subuserid'] = subuserid
            tiezi['subcontent'] = subcontent
            yield tiezi

        # 提取并判断是否包含下一页的链接
        next_page_url = None
        links = response.css('div[id="thread_theme_5"] a')
        if links:
            for link in links:
                button_url = link.xpath('./@href').extract_first()
                button_text = link.xpath('./text()').extract_first()
                if button_text == "下一页":
                    next_page_url = urljoin(response.url, button_url)
                    break
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse_content, meta=response.meta)
