# -*- coding: utf-8 -*-

# Scrapy settings for scrapyd project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapyd'

SPIDER_MODULES = ['scrapyd.spiders']
NEWSPIDER_MODULE = 'scrapyd.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyd (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# 用来支持cache_args（可选）
SPIDER_MIDDLEWARES = {
   # 'scrapyd.middlewares.ScrapydSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapyd.middlewares.UserAgentMiddleware': 401,
    'scrapyd.middlewares.ScrapydDownloaderMiddleware': 543,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 123,
    # 'scrapyd.middlewares.IPPOOLS': 125,

    # Splash代理相关配置
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,


}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.files.FilesPipeline': 1,
    # 'scrapyd.pipelines.PyFilePipeline': 1,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    # 'scrapyd.pipelines.PriceConverterPipeline': 300,
    'scrapyd.pipelines.JsonWithEncodingPipeline': 300,

    # MongoDB配置项
    'scrapyd.pipelines.MongoDBPipeline': 400,

    # SQLite DB配置项
    # 'scrapyd.pipelines.SQLitePipeline': 400,

    # MySQL DB配置项
    # 'scrapyd.pipelines.MySQLPipeline': 400,

    # MySQLAsync配置项
    # 'scrapyd.pipelines.MySQLAsyncPipeline': 400,

    # Redis配置项
    'scrapyd.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

IPPOOL = [
    {"ipaddr": "101.236.22.141:8866"},
    {"ipaddr": "101.236.60.48:8866"},
    {"ipaddr": "180.118.243.207:808"},
    {"ipaddr": "222.84.21.162:8118"},
    {"ipaddr": "123.207.30.131:80"},
    {"ipaddr": "61.135.217.7:80"},
    {"ipaddr": "122.114.31.177:808"},
]

MONGO_DB_URI = 'mongodb://192.168.1.105:27017/'
MONGO_DB_NAME = 'liushuo_scrapy_data'

# # excel格式导出文件
# FEED_EXPORTERS = {
#     'excel': 'scrapyd.excel_exporters.ExcelItemExporter'
# }
# # 设置excel列的的数据
# FEED_EXPORT_FIELDS = ['upc', 'name', 'price', 'stock', 'review_rate', 'review_number']


# 下载文件的保存路径
FILES_STORE = 'examples_src'

# 下载图片的保存路径
IMAGES_STORE = 'download_images'

# 伪装成常规浏览器      
# 用BrowserCookiesMiddleware替代CookiesMiddleware启用前后,关闭后者      
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
#     'scrapyd.middlewares.BrowserCookiesMiddleWare': 701,
# }

"""设置Splash运行js相关参数"""
# # Splash服务器地址
# SPLASH_URL = 'http://localhost:8050'
#
# # 设置去重过滤器
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# SQLIte DB配置项
SQLITE_DB_NAME = 'scrapy.db'

# MySQL DB配置项
myhost = '192.168.12.31'
myport = 3306
myuser = 'pes'
mypasswd = 'pes123&*()'
mydb = 'pes'