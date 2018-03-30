# --*-- coding:utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from selenium import webdriver
from ..items import AgriManaItem

# 巨潮资讯网--上市农业企业基本信息
class CninfoSpider(Spider):
    name = 'CninfoManaSpider'

    def __init__(self):
        self.broswer = webdriver.PhantomJS(
            executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        self.broswer.set_page_load_timeout(30)

    def closed(self, spider):
        print('spider closed!')
        self.broswer.close()

    def start_requests(self):
        myurls = ['szmb000998', 'szsme002041', 'szsme002772', 'szcn300087', 'szcn300189', 'szcn300511', 'shmb600108',
                  'shmb600313', 'shmb600354', 'shmb600359',
                  'shmb600371', 'shmb600506', 'shmb600598', 'shmb601118', 'szmb000592', 'szsme002200', 'szsme002679',
                  'shmb600265', 'szmb000735', 'szsme002234',
                  'szsme002299', 'szsme002321', 'szsme002458', 'szsme002477', 'szsme002505', 'szsme002714',
                  'szsme002746', 'szcn300106', 'szcn300313', 'szcn300498',
                  'shmb600965', 'shmb600975', 'szmb000798', 'szsme002086', 'szsme002696', 'szmb200992', 'szcn300094',
                  'shmb600097', 'shmb600257', 'shmb600467', 'szmb000711', 'szmb000713']

        start_urls = [
            ('http://www.cninfo.com.cn/information/companyinfo_n.html?management?' + each) for each in myurls]

        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = AgriManaItem()

        item['abbr'] = response.xpath('//div[@class="zx_info"]/form/table/tbody/tr/td[1]/text()').extract()[1]  # 公司简称

        managers_list = []
        base = response.xpath('//div[@class="clear2"]/div[@class="zx_left"]/div[2]/table/tbody/tr')
        for each in base:
            temp = each.xpath('td[1]/text()').extract()[0]
            temp = temp.replace('\n', '')
            managers_list.append(temp)
        # print(managers_list)
        manager_str = ''.join(managers_list).replace("姓名", '')
        # print(manager_str)
        item['managers'] = manager_str
        yield item
