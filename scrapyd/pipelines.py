# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapyd.items import ScrapydItem
from scrapyd.settings import myhost, myport, myuser, mypasswd, mydb

# 重写FilesPipeline
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join

# 重写ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline

class ScrapydPipeline(object):
    def process_item(self, item, spider):
        return item

class PriceConverterPipeline(object):

    # 英镑兑换人民币汇率
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        # 提取item的price字段,去掉前面的"$",转换为float类型,乘以汇率
        price = float(item['price'][1:]) * self.exchange_rate

        # 保留2为小数,赋值回item的price字段
        item['price'] = '¥%.2f' % price
        return item

from scrapy.item import Item
# import pymongo
#
# class MongoDBPipeline(object):
#     # 数据库的URL地址,名字
#     DB_URL = 'mongodb://localhost:27017/'
#     DB_NAME = 'scrapy_data'
#
#     # @classmethod
#     # def from_crawler(cls, crawler):
#     #     cls.DB_URI = crawler.settings.get('MONGO_DB_URI', 'mongodb:localhost:27017/')
#     #     cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')
#     #     return cls()
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.DB_URL)
#         self.db = self.client[self.DB_NAME]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         collection = self.db[spider.name]
#         post = dict(item) if isinstance(item, Item) else item
#         collection.insert_one(post)
#         return item

# 重写FilesPipeline
class PyFilePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))

# 重写FilesPipeline
class ImageFilePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))


"""
写SQLite数据库

创建库并在库中建表：
sqlite3 scrapy.db
建表语句
CREATE TABLE books (
    upc CHAR(16) NOT NULL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    price VARCHAR(16) NOT NULL,
    review_rating VARCHAR(16),
    review_num INT,
    stock INT
    );
"""
import sqlite3
class SQLitePipeline(object):

    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'scrapy_defaut.db')
        print("db_name", db_name)
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (?,?,?,?,?,?)'
        self.db_cur.execute(sql, values)

# 每插入一条就commit一次会影响效率
# self.db_conn.commit()


"""
写MySQL数据库

"""

import pymysql
class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', mydb)
        host = spider.settings.get('MYSQL_HOST', myhost)
        port = spider.settings.get('MYSQL_PORT', myport)
        user = spider.settings.get('MYSQL_USER', myuser)
        passwd = spider.settings.get('MYSQL_PASSWORD', mypasswd)

        self.db_conn = pymysql.connect(host=host, port=port, db=db,user=user,passwd=passwd,charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)

"""
写Twisted操作数据库,支持MySQL、SQLite3
Scrapy框架自身是使用另一个Python框架Twisted编写的程序，Twisted是一个事件驱动型的异步网络框架，
鼓励用户编写异步代码，Twisted中提供了以异步方式多线程访问数据库的模块adbapi，使用该模块可以显著提高程序访问数据库的效率。
下面是使用adbapi中的连接池访问MySQL数据库的简单示例：
"""
from twisted.enterprise import adbapi
class MySQLAsyncPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', mydb)
        host = spider.settings.get('MYSQL_HOST', myhost)
        port = spider.settings.get('MYSQL_PORT', myport)
        user = spider.settings.get('MYSQL_USER', myuser)
        passwd = spider.settings.get('MYSQL_PASSWORD', mypasswd)
        self.dbpool = adbapi.ConnectionPool('pymysql', host=host, db=db,
                                    user=user, passwd=passwd, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)

"""
写MongoDB数据库
查询步骤：mongo scrapy_default登录数据库, db.books.count()查询对应表中的记录书
"""
from pymongo import MongoClient
from scrapy import Item

class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scrapy_default')
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
            self.db.books.insert_one(item)

"""
写Redis数据库
redis-server：启动数据库
redis-cli：连接数据库客户端
keys book*：罗列books相关的key
HGETALL book:1：查询特定key的内容
"""

import redis
from scrapy import Item
class RedisPipeline:
    def open_spider(self, spider):
        db_host = spider.settings.get('REDIS_HOST', 'localhost')
        db_port = spider.settings.get('REDIS_PORT', 6379)
        db_index = spider.settings.get('REDIS_DB_INDEX', 0)
        self.db_conn = redis.StrictRedis(host=db_host, port=db_port, db=db_index)
        self.item_i = 0

    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
            self.item_i += 1
            self.db_conn.hmset('book:%s' % self.item_i, item)

# 写如json文件
import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('baidutieba.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()