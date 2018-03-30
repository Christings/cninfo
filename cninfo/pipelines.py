# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from .items import AgriBasicItem
from .items import AgriManaItem


class CninfoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = self.client[settings['MONGO_DB']]
        self.cninfo_base = self.db['cninfo_base']
        self.cninfo_mana = self.db['cninfo_mana']
        self.cninfo_share = self.db['cninfo_share']

    def process_item(self, item, spider):
        if isinstance(item, AgriBasicItem):
            try:
                if item['full_name']:
                    item = dict(item)
                    self.cninfo_base.insert(item)
                    print("insert baseinfo success ！")
                    return item

            except Exception as e:
                spider.logger.exception("insert failed")
        elif isinstance(item,AgriManaItem):
            if item['managers']:
                item = dict(item)
                self.cninfo_mana.insert(item)
                print("insert managers success ！")
                return item
