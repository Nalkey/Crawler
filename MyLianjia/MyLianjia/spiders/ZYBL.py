# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Rule, CrawlSpider
from scrapy.http import Request
from ..items import MylianjiaItem


class ZyblSpider(Spider):
    name = 'ZYBL'
    allowed_domains = ['bj.lianjia.com']

    base_url = "https://bj.lianjia.com/ershoufang/"
    community_id = "rs西罗园/"
    start_urls = [ base_url + community_id ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.get_links)
    #house = LinkExtractor(allow = ("pg\d+"))
    #rules = [
    #    Rule(LinkExtractor(restrict_xpaths="/html/body/div[@class='content ']/div[@id='leftContent']/div[@class='contentBottom clear']/div[@class='page-box fr']/div[@class='page-box house-lst-page-box']/a/@href"), callback='parse', follow=True),
    #]

    def get_links(self, response):
        # 浏览器上XPATH工具的结果和代码xpath工具出现结果不一致
        # 在Terminal执行scrapy shell "https://bj.lianjia.com/ershoufang/rs西罗园/"来进行调试
        # response.xpath("xxx").xpath("xxx")有返回时有data显示，没返回时返回[]
        total_page = eval(response.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
            .extract_first())['totalPage']
        print("ttt {}".format(total_page))
        for page in range(1, total_page+1):
            url = self.base_url + "pg" + str(page) + self.community_id
            yield Request(url, callback=self.parse)

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
                item['price'] = "None"
            # 单价
            item['unitPrice'] = each.xpath(
                "./div[@class='info clear']/div[@class='followInfo']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()"
            ).extract_first()
            # 标签
            try:
                # TODO: 没找到string-join这些子函数用法
                #item['tags'] = each.xpath(
                #    "string-join((./div[@class='info clear']/div[@class='followInfo']/div[@class='tag']//text()), '-')"
                #).extract()
                item['tags'] = '-'.join(each.xpath(
                    "./div[@class='info clear']/div[@class='followInfo']/div[@class='tag']//text()"
                ).extract())
            except:
                item['tags'] = "None"
            # 链接
            item['link'] = each.xpath("./a/@href").extract_first()

            yield item
