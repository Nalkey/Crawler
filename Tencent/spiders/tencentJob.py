# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentjobSpider(scrapy.Spider):
    # 爬虫名
    name = 'tencentJob'
    # 爬虫作用范围
    allowed_domains = ['tencent.com']

    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    # 起始URL
    start_urls = [url + str(offset)]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            # 初始化对象
            item = TencentItem()
            # 如果使用extract()[0]会因为如果text为空，而产生数组越界，故改用extract_first()
            # 职位名赋值
            item['jobName'] = each.xpath("./td[1]/a/text()").extract_first()
            # 职位类别赋值
            item['jobCatogary'] = each.xpath("./td[2]/text()").extract_first()
            # 招聘人数赋值
            item['jobNum'] = each.xpath("./td[3]/text()").extract_first()
            # 工作地点赋值
            item['jobCity'] = each.xpath("./td[4]/text()").extract_first()
            # 发布时间
            item['jobPublishDate'] = each.xpath("./td[5]/text()").extract_first()
            # 职位链接
            item['jobLink'] = each.xpath("./td[1]/a/@href").extract_first()

            yield item

        if self.offset < 300:
            self.offset += 10

        # 每次处理完一页后，发送下一页请求
        # self.offset自增10，生成新的url，并调用回调函数self.parse处理response
        yield scrapy.Request(self.url + str(self.offset), callback = self.parse)
