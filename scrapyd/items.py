# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field
from scrapy.exceptions import DropItem

class ScrapydItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    price = Field()

# 爬取图书详细信息存入excel的item
class ScrapydMoreInfoItem(scrapy.Item):
    # 书名
    name = Field()
    # 价格
    price = Field()
    # 评级等级
    review_rating = Field()
    # 评价数量
    review_num = Field()
    # 产品编码
    upc = Field()
    # 产品库存
    stock = Field()

# 下载matplotlib.org中py文件的item
class ExampleItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

# 下载matplotlib.org中py文件的item
class SplashQuotesItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()

# 百度贴吧的item
class BaiduTieBa(scrapy.Item):
    keyword = scrapy.Field()
    tzname = scrapy.Field()
    tzurl = scrapy.Field()
    author = scrapy.Field()
    userid = scrapy.Field()
    subcontent = scrapy.Field()
    subauthor = scrapy.Field()
    subuserid = scrapy.Field()

# 糗事百科的item
class QiuShiBaiKe(scrapy.Item):
    column_name = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    imgurl = scrapy.Field()
    vote_number = scrapy.Field()