# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import pymysql
from scrapy.utils.project import get_project_settings


class MylianjiaJSONPipeline(object):
    def __init__(self):
        self.filename = open("ZYBL.json", "wb+")

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(text.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.filename.close()


class MylianjiaMySQLPipeline(object):
    # 创建数据库表Lianjia
    create_sql = "CREATE TABLE IF NOT EXISTS `lianjia` (" \
                 "`record_id` VARCHAR(50) NOT NULL," \
                 "`house_code` VARCHAR(50) NOT NULL," \
                 "`date` VARCHAR(8) NOT NULL," \
                 "`community` VARCHAR(16) DEFAULT NULL," \
                 "`type` VARCHAR(16) DEFAULT NULL," \
                 "`size` VARCHAR(16) DEFAULT NULL," \
                 "`orientation` VARCHAR(8) DEFAULT NULL," \
                 "`decoration` VARCHAR(8) DEFAULT NULL," \
                 "`elevator` VARCHAR(8) DEFAULT NULL," \
                 "`floor` VARCHAR(16) DEFAULT NULL," \
                 "`age` VARCHAR(16) DEFAULT NULL," \
                 "`district` VARCHAR(16) DEFAULT NULL," \
                 "`price` VARCHAR(32) DEFAULT NULL," \
                 "`unitPrice` VARCHAR(32) DEFAULT NULL," \
                 "`tags` VARCHAR(64) DEFAULT NULL," \
                 "`link` VARCHAR(1024) DEFAULT NULL," \
                 "PRIMARY KEY (`record_id`)" \
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    # 新增字段record_id和date：（这两个在JSON中不存在）
    # 在数据库中用id作为primary key，所以要反映趋势就要house code + date作为唯一标识
    insert_sql = "INSERT INTO lianjia (" \
                 "record_id,house_code,date,community,type,size,orientation,decoration,elevator," \
                 "floor,age,district,price,unitPrice,tags,link)" \
                 " VALUES('{record_id}','{house_code}','{date}','{community}','{type}','{size}'," \
                 "'{orientation}','{decoration}','{elevator}','{floor}','{age}','{district}'," \
                 "'{price}','{unitPrice}','{tags}','{link}')"

    def __init__(self):
        self.settings = get_project_settings()
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True
        )
        # 数据库游标用于操作数据库
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 获取抓取的日期
            date = time.strftime("%Y%m%d", time.localtime())
            record_id = item['house_code'] + date
            sql_cmd = self.insert_sql.format(
                record_id=record_id, house_code=item['house_code'], date=date,
                community=item['community'], type=item['type'], size=item['size'],
                orientation=item['orientation'], decoration=item['decoration'],
                elevator=item['elevator'], floor=item['floor'], age=item['age'],
                distric=item['district'], price=item['price'], unitPrice=item['unitPrice'],
                tags=item['tags'], link=item['link']
            )
            # 数据写入数据库
            self.cursor.execute(sql_cmd)
            # 提交信息
            self.connect.commit()
        except Exception as e:
            print("Database ERROR: ", e)
            self.connect.rollback()

        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.connect.close()
