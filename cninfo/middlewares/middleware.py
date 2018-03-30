from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'CninfoSpider':
            print('PhantomJS1 is starting...')
            driver = webdriver.PhantomJS(executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            driver.get(request.url)
            time.sleep(1)
            driver.switch_to.frame('i_nr')
            time.sleep(2)
            body = driver.page_source
            print("访问：", request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8')
        elif spider.name == 'CninfoManaSpider':
            print('PhantomJS2 is starting...')
            driver = webdriver.PhantomJS(executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            driver.get(request.url)
            time.sleep(1)
            driver.switch_to.frame('i_nr')
            time.sleep(2)
            body = driver.page_source
            print("访问：", request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8')
        else:
            return
