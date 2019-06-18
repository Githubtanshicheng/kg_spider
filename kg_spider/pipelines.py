# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from kg_spider import settings


class KgSpiderPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.HOST_IP,
            user=settings.USER,
            passwd=settings.PASSWD,
            db=settings.DB_NAME,
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = item.get('name')
        para = item.get('para')

        sql = "INSERT INTO kg_table(name, para) VALUES (%s, %s)"
        self.cursor.execute(sql, (name, para))
        self.conn.commit()
        '''
        self.cursor.execute("SELECT name FROM kg_table")
        namelist = self.cursor.fetchall()
        if (name,) not in namelist:
            self.cursor.execute("SELECT MAX(id) FROM name")
            result = self.cursor.fetchall()[0]
            if None in result:
                id = 1
            else:
                id = result[0] + 1
            sql = "INSERT INTO kg_table(id, name, para) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (id, name, para))
            self.cursor.commit()
        else:
            print("#" * 20, "Got a duplict actor!!", name)
        '''
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
