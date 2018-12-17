# -*- coding: utf-8 -*-
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, CrawlSpider
from ..items import MylianjiaItem


class ZyblSpider(CrawlSpider):
    name = 'ZYBL'
    allowed_domains = ['lianjia.com']

    url = "http://bj.lianjia.com/ershoufang/"
    community_id = "rs正阳小区北里/"
    start_urls = [url + community_id]

    house = LinkExtractor(tags='a', attrs='href')
    rules = [
        Rule(house, callback='parse', follow=False),
    ]

    def parse(self, response):
        for each in response.xpath("//li[@class='clear LOGCLICKDATA']"):
            item = MylianjiaItem()
            # 房子代号
            item['house_code'] = each.xpath("./a/@data-housecode").extract_first()
            # 小区名
            item['community'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/a/text()"
            ).extract_first()
            # 房型
            item['type'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()[1]"
            ).extract_first()
            # 大小
            item['size'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()[2]"
            ).extract_first()
            # 朝向
            item['orientation'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()[3]"
            ).extract_first()
            # 装修情况
            item['decoration'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()[4]"
            ).extract_first()
            # 有无电梯
            item['elevator'] = each.xpath(
                "./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()[5]"
            ).extract_first()
            # 楼层
            item['floor'] = each.xpath(
                "./div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/text()[1]"
            ).extract_first()
            item['age'] = each.xpath(
                "./div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/text()[2]"
            ).extract_first()
            # 地区
            item['district'] = each.xpath(
                "./div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/a/text()"
            ).extract_first()
            # 总价
            try:
                item['price'] = ''.join(each.xpath(
                    "./div[@class='info clear']/div[@class='followInfo']/div[@class='priceInfo']/div[@class='totalPrice']//text()"
                ).extract())
            except:
                item['tags'] = "None"
            # 单价
            item['unitPrice'] = each.xpath(
                "./div[@class='info clear']/div[@class='followInfo']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()"
            ).extract_first()
            # 标签
            try:
                item['tags'] = each.xpath(
                    "string-join((./div[@class='info clear']/div[@class='followInfo']/div[@class='tag']//text()), '-')"
                ).extract()
                #item['tags'] = '-'.join(each.xpath(
                #    "./div[@class='info clear']/div[@class='followInfo']/div[@class='tag']//text()"
                #).extract())
            except:
                item['tags'] = "None"
            # 链接
            item['link'] = each.xpath("./a/@href").extract_first()

            yield item
