# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Job name
    jobName = scrapy.Field()
    # Job link
    jobLink = scrapy.Field()
    # Job category
    jobCategory = scrapy.Field()
    # Job number
    jobNum = scrapy.Field()
    # Job city
    jobCity = scrapy.Field()
    # Publish date
    publishDate = scrapy.Field()
