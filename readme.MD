>本文首发于我的博客：[gongyanli.com](http://gongyanli.com/PhantomJS-Selenium-Scrapy%E6%8A%93%E5%8F%96%E5%B7%A8%E6%BD%AE%E8%B5%84%E8%AE%AF%E7%BD%91%E4%BC%81%E4%B8%9A%E4%BF%A1%E6%81%AF/)  
>代码传送门：[https://github.com/Gladysgong/cninfo](https://github.com/Gladysgong/cninfo)  
>简书: [https://www.jianshu.com/p/b5ef0e7e2b87](https://www.jianshu.com/p/b5ef0e7e2b87)  
>CSDN: [https://mp.csdn.net/mdeditor/79759833](https://mp.csdn.net/mdeditor/79759833)

        首先说说我的目标把，就是抓取巨潮资讯网上一些上市农业企业的基本信息，主要是对页面的公司概况、高
	管人员、十大股东这几个板块的信息进行抓取，如图。要抓取的上市农业企业的名单已经准备好了，但是同时要
	拿到的这些农业企业的url地址。本来考虑的是做一个整站提取url，但是再想一想，这个网站包含了太多上市
	公司的信息，即使拿到了，也需要慢慢找。加上我们要抓取的农业企业不多，所以分析页面结果后，手动整理
	他们的url，算是本爬虫的一个缺陷。
![](http://p2lakvkq0.bkt.clouddn.com/cninfo.jpg)

		巨潮资讯地址：http://www.cninfo.com.cn/information/companyinfo_n.html?brief?szmb000998
		上面这个就是公司概况的url地址，而高管人员只需要把brief换成management,十大股东只需要把brief
	换成shareholders，而后面的后缀szmb000998这个是手动整理的，这个szmb没看出什么意思，后面的数字是
	当前公司的股票代码。
		经过分析，发现网页是动态加载的，里面的内容都是通过js来控制iframe进行展现的，通过scrapy中
	response.body获取网页的返回结果中，没有完美所需要的内容，所以我们需要用selenium。
## 一、PhantomJS--[PhantomJS安装验证](http://gongyanli.com/Python3%E7%88%AC%E8%99%AB-PhantomJS%E5%AE%89%E8%A3%85/)
	PhantomJS是一个基于webkit内核的没有界面的浏览器，所以它和chrome、Firefox这些没有什么差别，只是
	没有界面而已啦，所以并无高深之处。关于它的安装及验证非常简单，大家可以参考我的另一篇文章，标题处去
	点击链接把。
	
## 二、Selenium--[Selenium的使用](https://cuiqingcai.com/5630.html)
	Selinium是一个自动化的测试工具，用它可以驱动浏览器执行特定的操作，比如点击按钮，切换到ifame中等操
	作，同时能够获取到浏览器渲染后的源码。所以它对于那些用JavaScript渲染的网页来讲，Selenium是再合适
	不过了。
	崔庆才的博客中有一篇详细讲解了Selenium的用法，可以参考。
## 三、通过Scrapy来使用Selenium
![](http://p2lakvkq0.bkt.clouddn.com/cninfo1.jpg)
### 1.中间件
	首先看一下我的工作目录把，没有什么特点，scrapy典型的工作目录，唯一不一样的是middlewares文件夹，里
	面存放的是我自定义的中间件。通过自定义的中间件去把scrapy原本的中间件覆盖，从而用我们自己实现的功能
	去替换scrapy原有的功能。
	我的中间件代码如下：打开PhantomJS浏览器，请求url地址，睡眠，接着切换iframe，因为我要获取的公司概
	况信息就在id='i_nr'的这个ifame中，再睡觉，等待浏览器渲染出这个ifame中的内容，然后再body中保存此
	网页的源码，最后利用HtmlResponse把body传送离开。

----------

    `from selenium import webdriver
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
`

### 2.数据解析--cninfo.py
		之后，我们就可以回到cninfo.py文件中对内容进行解析了。重写__init__，使用webdriver打开
	PhantomJS浏览器。重写start_requests方法，拼接url，同时可以自定义返回函数parse。
	

----------
    `# --*-- coding:utf-8 -*-
	import scrapy
	from scrapy import Request
	from scrapy.spiders import Spider
	from selenium import webdriver
	from ..items import AgriBasicItem
	
	# 巨潮资讯网--上市农业企业基本信息
	class CninfoSpider(Spider):
	    name = 'CninfoSpider'
	
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
	
	`
### 3.数据持久化--pipelines.py

	把抓取下来的数据存进mongo数据库，实现数据的持久化。setting中数据库配置如下：
	MONGO_HOST = '127.0.0.1' # 主机ip
	MONGO_PORT = 27017    # 端口号
	MONGO_DB = 'agriEn'     # 数据库名称

----------
	`import pymongo
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
	                return item`

### 4.配置文件--setting.py
	ROBOTSTXT_OBEY = False

	DOWNLOADER_MIDDLEWARES = {
	# 键是中间件类的路径，值是中间的顺序
    'cninfo.middlewares.middleware.JavaScriptMiddleware': 543,
	# 禁止内置的中间件
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None }

	# 记得开启pipelines的调用
	ITEM_PIPELINES = {
	'cninfo.pipelines.CninfoPipeline': 300,}

## 四、缺陷
	在这个爬虫中，其实出现了蛮多问题的，有些解决了，有些没有，记录一下，加深印象，还有感觉代码好垃圾。
### 1.缺陷1
	上市农业企业的名字，以及名字的url链接手动整理的，因为只有40来个企业，所以才会用这个方法。
	本来是想通过Scarpy的CrawlSpider抓取，抓取时通过Rule来控制所需要的农业企业，但是发现实在没有什么规律
	，只会把巨潮资讯上所有上市企业的url都获取下来，所以最后手动整理的这40多个农业企业，希望日后能找到更简
	便的办法。
### 2.缺陷2
	对于网页中的高管人员信息抓取中，本来是想思考放在一个爬虫中获取到的，但是仔细分析后发现，公司概况和高管
	人员分别对应着不同的url，然后不同的url下再对应中动态加载iframe。url对比如下：
	http://www.cninfo.com.cn/information/companyinfo_n.html?brief?szmb000998
	http://www.cninfo.com.cn/information/companyinfo_n.html?management?szmb000998
	这样子的话，就涉及到我需要在Selenuim中点击按钮，然后再渲染id='i_nr'的iframe，而且不同页面中iframe
	名字都叫i_nr。我试过这个办法，但是拿回的源码并不是高管人员页面的源码，依然是公司概况页面的源码，也许
	是我方法用的不对，有待仔细研究。
	所以我又在cninfo_mana.py中又写了一个爬虫，从而单独来获取高管人员页面的信息。
### 3.缺陷3
	对于十大股东页面，按理说我应该在写一个py文件来单独获取它的页面信息，这样子就ok了，实际上我也是这么做
	的。但是爬虫运行是，却发现我拿不到股东的信息，因为我发现当请求http://www.cninfo.com.cn/
	information/companyinfo_n.html?shareholders?szmb000998时，首先切换到id='i_nr'的iframe中，但
	是随后股东的详细信息又在一个id='i_nr'的ifrma中，相当于这里有两个iframe，我在中间件试了试两个这样子
	切换iframe，但是很遗憾我没拿到我想要的东西，源代码还是停留在第一层iframe中，所以最后我放弃了，没有
	拿十大股东的信息，这个问题智能留着我以后解决了。
### 4.缺陷4
	self.broswer = webdriver.PhantomJS(
            executable_path=r'E:\Program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	这个代码在中间件和爬虫代码中都有，说明两次打开了浏览器，致使性能降低。