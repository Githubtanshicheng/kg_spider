from kg_spider.items import KgSpiderItem

import scrapy
import re
import requests

class KgSpider(scrapy.Spider):
    name = 'kg'
    allowed_dommains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/%E7%A9%BA%E4%B8%AD%E4%BA%A4%E9%80%9A%E7%AE%A1%E5%88%B6?fromtitle=%E7%A9%BA%E7%AE%A1&fromid=10877913']

    def myparse(self, response):
        item = KgSpiderItem()
        name = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()
        print('===========================')

        item['name'] = name
        para = response.xpath('//div[@class="lemma-summary"]/div/descendant::text()').extract()  # 获取所有div下的文本
        parastr = ''
        for i in para:
            parastr = parastr + i

        parastr = parastr.split('\n')                           #去除所有带[1]的字段
        item['para'] = parastr[0]

        yield item

        print('===========================')


    def parse(self, response):
        item = KgSpiderItem()
        name = response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()
        print('===========================')

        item['name'] = name
        para = response.xpath('//div[@class="lemma-summary"]/div/descendant::text()').extract()         #获取所有div下的文本
        parastr = ''
        for i in para:
            parastr = parastr + i
        item['para'] = parastr

        yield item

        print('===========================')


        # 航行与空中交通管理
        box = 'https://baike.baidu.com/guanxi/jsondata?action=getViewLemmaData&args=%5B0%2C8%2C%7B%22fentryTableId%22%3A35046%2C%22lemmaId%22%3A95039%2C%22subLemmaId%22%3A95039%7D%2Cfalse%5D'
        
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        context = s.get(box).text
        new_con = eval(context)['html']
        s4 = re.findall('http:(.*)"', new_con)
        for x in s4:
            x = x.replace("\\", "")
            url = re.findall('//(.*).htm', x)
            url = "https://" + ''.join(url)  # list转str
            print('url:', url)
            yield scrapy.Request(url, callback=self.myparse)







