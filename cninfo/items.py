# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 巨潮资讯网--上市农业企业基本信息
class AgriBasicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    full_name = scrapy.Field()  # 公司名称
    en_name = scrapy.Field()  # 英文名称
    cn_name = scrapy.Field()  # 中文名称
    abbr = scrapy.Field()  # 公司简称
    nation = scrapy.Field()  # 国别
    address = scrapy.Field()  # 注册地址
    established_time = scrapy.Field()  # 成立时间
    stock_time = scrapy.Field()  # 上市时间
    stock_code = scrapy.Field()  # 股票代码
    shareholders = scrapy.Field()  # 主要股东
    industry = scrapy.Field()  # 行业(经营类别)
    managers = scrapy.Field()  # 主要管理人员
    parent_company = scrapy.Field()  # 母公司
    subsidiaries = scrapy.Field()  # 子公司
    offical_website = scrapy.Field()  # 官网
    phone = scrapy.Field()  # 公司电话
    fax = scrapy.Field()  # 公司传真
    Twitter = scrapy.Field()  # Twitter


class AgriManaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    abbr = scrapy.Field()  # 公司简称
    managers = scrapy.Field()  # 主要管理人员

