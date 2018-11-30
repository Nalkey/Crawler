# -*- coding: utf-8 -*-

# TODO: https://bj.lianjia.com/chengjiao/c1111027382765/
# TODO: 每个房子的图片
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MylianjiaItem(scrapy.Item):
    # 小区名
    community = scrapy.Field()
    # 房型
    type = scrapy.Field()
    # 大小
    size = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 装修情况
    decoration = scrapy.Field()
    # 有无电梯
    elevator = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 楼龄
    age = scrapy.Field()
    # 地区
    district = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unitPrice = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 链接
    link = scrapy.Field()
