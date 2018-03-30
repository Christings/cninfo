# --*-- coding:utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from selenium import webdriver
from ..items import AgriBasicItem
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException


# broswer = webdriver.PhantomJS(executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# broswer.get("http://www.cninfo.com.cn/information/companyinfo_n.html?brief?szmb000998")
# broswer.switch_to.frame('i_nr')
# try:
#     logo = broswer.find_element_by_xpath('//div[@class="clear"]/table/tbody/tr[1]/td[2]')
# except NoSuchElementException:
#     print("no")
# # broswer.switch_to.parent_frame()
# # logo = broswer.find_element_by_class_name('zx_right_title')
# print(logo)
# print(logo.text)


# print(broswer.page_source)
# print(broswer.current_url)



# 巨潮资讯网--上市农业企业基本信息
class CninfoSpider(Spider):
    name = 'CninfoSpider'

    #
    # allow_domains = ['cninfo.com.cn']
    # start_urls = ['http://www.cninfo.com.cn/information/companyinfo_n.html?brief?szmb000998']

    def __init__(self):
        self.broswer = webdriver.PhantomJS(
            executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        self.broswer.set_page_load_timeout(30)


    def closed(self, spider):
        print('spider closed!')
        self.broswer.close()

    def start_requests(self):
        myurls = ['szmb000998', 'szsme002041', 'szsme002772', 'szcn300087', 'szcn300189', 'szcn300511',
                       'shmb600108',
                       'shmb600313', 'shmb600354', 'shmb600359',
                       'shmb600371', 'shmb600506', 'shmb600598', 'shmb601118', 'szmb000592', 'szsme002200',
                       'szsme002679',
                       'shmb600265', 'szmb000735', 'szsme002234',
                       'szsme002299', 'szsme002321', 'szsme002458', 'szsme002477', 'szsme002505', 'szsme002714',
                       'szsme002746', 'szcn300106', 'szcn300313', 'szcn300498',
                       'shmb600965', 'shmb600975', 'szmb000798', 'szsme002086', 'szsme002696', 'szmb200992',
                       'szcn300094',
                       'shmb600097', 'shmb600257', 'shmb600467', 'szmb000711', 'szmb000713']
        start_urls = [
            ('http://www.cninfo.com.cn/information/companyinfo_n.html?brief?' + each) for each in myurls]

        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = AgriBasicItem()

        # base = response.xpath('//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/')
        # for each in base:
        #     # full_name = each.xpath('//tr[1]/td[2]/text()').extract()  # 公司名称
        # en_name = each.xpath('//tr[2]/td[2]/text()').extract()  # 英文名称
        # cn_name = full_name  # 中文名称
        # nation = 'china'  # 国别
        # address = each.xpath('//tr[3]/td[2]/text()').extract()  # 注册地址
        # established_time = None  # 成立时间
        # stock_time = each.xpath('//tr[13]/td[2]/text()').extract()  # 上市时间
        # # shareholders = scrapy.Field()  # 主要股东
        # industry = each.xpath('//tr[8]/td[2]/text()').extract()  # 行业(经营类别)
        # # managers = scrapy.Field()  # 主要管理人员
        # parent_company = None  # 母公司
        # subsidiaries = None  # 子公司
        # offical_website = each.xpath('//tr[12]/td[2]/text()').extract()  # 官网
        # phone = each.xpath('//tr[10]/td[2]/text()').extract()  # 公司电话
        # fax = each.xpath('//tr[11]/td[2]/text()').extract()  # 公司传真
        # Twitter = None  # Twitter

        item['full_name'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]  # 公司名称
        item['en_name'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[2]/td[2]/text()').extract()[0]  # 英文名称
        item['cn_name'] = item['full_name']  # 中文名称
        item['nation'] = 'china'  # 国别
        item['address'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[3]/td[2]/text()').extract()[0]  # 注册地址
        item['established_time'] = None  # 成立时间
        item['stock_time'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[13]/td[2]/text()').extract()[0]  # 上市时间
        # shareholders = scrapy.Field()  # 主要股东
        item['industry'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[8]/td[2]/text()').extract()[
            0]  # 行业(经营类别)
        # managers = scrapy.Field()  # 主要管理人员
        item['parent_company'] = None  # 母公司
        item['subsidiaries'] = None  # 子公司
        item['offical_website'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[12]/td[2]/text()').extract()[0]  # 官网
        item['phone'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[10]/td[2]/text()').extract()[0]  # 公司电话
        item['fax'] = response.xpath(
            '//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr[11]/td[2]/text()').extract()[0]  # 公司传真
        item['Twitter'] = None  # Twitter

        item['stock_code'] = response.xpath('//div[@class="zx_info"]/form/table/tbody/tr/td[1]/text()').extract()[
            0]  # 股票代码
        item['abbr'] = response.xpath('//div[@class="zx_info"]/form/table/tbody/tr/td[1]/text()').extract()[1]  # 公司简称


        yield item

