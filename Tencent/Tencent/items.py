# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名
    jobName = scrapy.Field()
    # 职位类别
    jobCatogary = scrapy.Field()
    # 招聘人数
    jobNum = scrapy.Field()
    # 工作地点
    jobCity = scrapy.Field()
    # 发布时间
    jobPublishDate = scrapy.Field()
    # 职位链接
    jobLink = scrapy.Field()
