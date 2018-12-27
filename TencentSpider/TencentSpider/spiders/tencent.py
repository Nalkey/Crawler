# -*- coding: utf-8 -*-
import scrapy
# 导入链接规则匹配类，用来提取符合规则的链接
from scrapy.linkextractors import LinkExtractor
# 导入CrawlSpider类和Rule
from scrapy.spiders import CrawlSpider, Rule
from ..items import TencentspiderItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ["http://hr.tencent.com/position.php?&start=0#a"]

    # Response里链接的提取规则，返回的符合匹配规则的链接的列表
    page_link = LinkExtractor(allow = ("start=\d+"))

    rules = [
        # 获取列表里的链接，依次发送请求，并且继续跟进，调用指定回调函数处理
        Rule(page_link, callback='parseTencent', follow=True),
    ]

    def parseTencent(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentspiderItem()
            item['jobName'] = each.xpath("./td[1]/a/text()").extract_first()
            item['jobLink'] = each.xpath("./td[1]/a/@href").extract_first()
            item['jobCategory'] = each.xpath("./td[2]/text()").extract_first()
            item['jobNum'] = each.xpath("./td[3]/text()").extract_first()
            item['jobCity'] = each.xpath("./td[4]/text()").extract_first()
            item['publishDate'] = each.xpath("./td[5]/text()").extract_first()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
            yield item
