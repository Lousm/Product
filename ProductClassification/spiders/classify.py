# -*- coding: utf-8 -*-
import scrapy
from ProductClassification.items import ProductclassificationItem
# from scrapy_redis.spiders import RedisSpider
from scrapy_redis_bloomfilter.spiders import RedisSpider


class ClassifySpider(RedisSpider):
    name = 'classify'
    redis_key = 'ClassifySpider:start_urls'
    # allowed_domains = ['stats.gov.cn']
    # start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjypflml/index.html']

    def parse(self, response):

        classif_lis = response.xpath('//ul[@class="center_list_contlist"]/li')
        print(classif_lis)
        for classif in classif_lis:
            item = ProductclassificationItem()
            oneclassname = classif.xpath('.//font[@class="cont_tit03"]/text()').extract_first()
            url = classif.xpath('./a/@href').extract_first()
            if oneclassname is not None:
                item['oneclassname'] = oneclassname
                new_href = response.urljoin(url)

                yield scrapy.Request(url=new_href, meta={'meat1': item}, callback=self.classif2)

        n_url = response.xpath('//a[@id="pagenav_tail"]/@href').extract_first()
        next_url = response.urljoin(n_url)
        yield scrapy.Request(url=next_url, callback=self.parse)

    def classif2(self, response):
        meat2 = response.meta['meat1']
        cli2_lis = response.xpath('//tr[@class="citytr"]/td[2]/a')
        for cli in cli2_lis:
            item = ProductclassificationItem()
            city2 = cli.xpath('./text()').extract_first()
            city2_href = cli.xpath('./@href').extract_first()
            item['oneclassname'] = meat2['oneclassname']
            item['twoclassname'] = city2
            if city2_href is not None:
                new_href = response.urljoin(city2_href)
                yield scrapy.Request(url=new_href, meta={'meat2': item}, callback=self.classif3)

    def classif3(self, response):
        meat3 = response.meta['meat2']
        cli3_lis = response.xpath('//tr[@class="countytr"]/td[2]/a')
        for cli in cli3_lis:
            item = ProductclassificationItem()
            city3 = cli.xpath('./text()').extract_first()
            city3_href = cli.xpath('./@href').extract_first()
            item['oneclassname'] = meat3['oneclassname']
            item['twoclassname'] = meat3['oneclassname']
            item['threeclassname'] = city3
            if city3_href is not None:
                new_href = response.urljoin(city3_href)
                yield scrapy.Request(url=new_href, meta={'meat3': item}, callback=self.classif4)

    def classif4(self, response):
        meat4 = response.meta['meat3']
        cli4_lis = response.xpath('//tr[@class="towntr"]/td[2]/a')
        for cli in cli4_lis:
            item = ProductclassificationItem()
            city4 = cli.xpath('./text()').extract_first()
            city4_href = cli.xpath('./@href').extract_first()
            item['oneclassname'] = meat4['oneclassname']
            item['twoclassname'] = meat4['oneclassname']
            item['threeclassname'] = meat4['threeclassname']
            item['fourclassname'] = city4
            if city4_href is not None:
                new_href = response.urljoin(city4_href)
                yield scrapy.Request(url=new_href, meta={'meat4': item}, callback=self.classif5)

    def classif5(self, response):
        meat5 = response.meta['meat4']
        cli5_list = response.xpath('//tr[@class="villagetr"]/td[2]/text()').extract()
        for cli in cli5_list:
            item = ProductclassificationItem()
            item['oneclassname'] = meat5['oneclassname']
            item['twoclassname'] = meat5['oneclassname']
            item['threeclassname'] = meat5['threeclassname']
            item['fourclassname'] = meat5['fourclassname']
            item['fiveclassname'] = cli
            yield item
