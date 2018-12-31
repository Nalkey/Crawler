# -*- coding: utf-8 -*-

from scrapy import cmdline


name = 'ZYBL'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
