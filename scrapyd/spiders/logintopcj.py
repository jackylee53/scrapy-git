# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request, FormRequest
from PIL import Image
from io import BytesIO
import pytesseract

class LogintopcjSpider(scrapy.Spider):
    name = 'logintopcj'
    allowed_domains = ['a.topcj.com']
    start_urls = ['http://a.topcj.com/jsoa/login.jsp']

    login_url = 'http://a.topcj.com/jsoa/login.jsp'
    user = '12690'
    pwd = 'xbmuDQGC2'
    image_url = 'http://a.topcj.com/jsoa/CreateImage'

    def parse(self, response):
        pass

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        # 该方法既是登录页面的解析函数，又是下载验证码图片的响应处理函数
        # 如果response.meta['login_response']存在,当前response为验证码图片的响应
        # 否则当前response为登录页面的响应
        login_response = response.meta.get('login_response')
        if not login_response:
            captchaUrl = response.css('label.field.prepend-icon img::attr(src)').extract_first()
            captchaUrl = response.urljoin(captchaUrl)
            yield Request(captchaUrl, callback=self.login, meta={'login_response': response}, dont_filter=True)
        else:
            formdata = {
                'email': self.user,
                'pass': self.pwd,
                'code': self.get_captcha_by_OCR(self.image_url)
            }
            yield FormRequest.from_response(response, callback=self.parse_login, formdata=formdata, dont_filter=True)

    def parse_login(self, response):
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('登录成功:-)')
            return super().start_requests()
        logger.info('登录失败:-(, 重新登录...')
        return self.start_requests()

    def get_captcha_by_OCR(self, data):
        img = Image.open(BytesIO(data))
        captcha = pytesseract.image_to_string(img)
        img.close()
        return captcha