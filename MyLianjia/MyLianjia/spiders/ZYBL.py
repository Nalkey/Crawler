# -*- coding: utf-8 -*-
import scrapy


class ZyblSpider(scrapy.Spider):
    name = 'ZYBL'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://lianjia.com/']

    def parse(self, response):
        pass
