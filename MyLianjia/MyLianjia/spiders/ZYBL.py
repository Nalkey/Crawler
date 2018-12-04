# -*- coding: utf-8 -*-
import scrapy
from MyLianjia.MyLianjia.items import MylianjiaItem


class ZyblSpider(scrapy.Spider):
    name = 'ZYBL'
    allowed_domains = ['lianjia.com']

    url = "http://bj.lianjia.com/ershoufang/"
    community_id = "rs正阳小区北里/"
    start_urls = [ url + community_id ]

    def parse(self, response):
        for each in response.xpath("//li[@class='clear LOGCLICKDATA']"):
            item = MylianjiaItem()
            # 小区名
            item['community'] = each.xpath("//div[@class='houseInfo']/a/text()").extract_first()
            # 房型
            try:
                item['type'] = each.xpath("//div[@class='houseInfo']/text()").extract()[0].strip()
            except:
                item['type'] = "None"
            # 大小
            try:
                item['size'] = each.xpath("//div[@class='houseInfo']/text()").extract()[1].strip()
            except:
                item['size'] = "None"
            # 朝向
            try:
                item['orientation'] = each.xpath("//div[@class='houseInfo']/text()").extract()[2].strip()
            except:
                item['orientation'] = "None"
            # 装修情况
            try:
                item['decoration'] = each.xpath("//div[@class='houseInfo']/text()").extract()[3].strip()
            except:
                item['decoration'] = "None"
            # 有无电梯
            try:
                item['elevator'] = each.xpath("//div[@class='houseInfo']/text()").extract()[4].strip()
            except:
                item['elevator'] = "None"
            # 楼层
            try:
                item['floor'] = each.xpath("//div[@class='positionInfo']/text()").extract()[0].strip()
            except:
                item['floor'] = "None"
            # 楼龄
            try:
                item['age'] = each.xpath("//div[@class='positionInfo']/text()").extract()[1].strip()
            except:
                item['age'] = "None"
            # 地区
            try:
                item['district'] = each.xpath("//div[@class='positionInfo']/text()").extract()[2].strip()
            except:
                item['district'] = "None"
            # 总价
            item['price'] = each.xpath("//div[@class='totalPrice']/span/text()").extract_first()
            # 单价
            item['unitPrice'] = each.xpath("//div[@class='unitPrice']/span/text()").extract_first()
            # 标签"(//div[@class='tag'])[1]/*/text()"
            tags = scrapy.Field()
            # 链接
            item['link'] = each.xpath("//div[@class='houseInfo']/a/@href").extract_first()
