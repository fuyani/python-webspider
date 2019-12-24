# -*- coding: utf-8 -*-
import scrapy
import urllib


class QiZhiSpider(scrapy.Spider):
    name = 'qi_zhi'
    allowed_domains = ['meitulu.com']
    start_urls = ['https://www.meitulu.com/t/qizhi/']
    i = 0

    def parse(self, response):
        li_list = response.xpath("//ul[@class='img']/li")
        for li in li_list:
            item = {}
            item["detail_url"] = li.xpath("./a/@href").extract_first()
            item["img_amount"] = li.xpath("./p[1]/text()").extract_first()
            item["img_model"] = li.xpath("./p[3]/text()").extract_first()
            if item["img_model"] == "模特： ":
                item["img_model"] = li.xpath("./p[3]/a/text()").extract_first()
            if item["detail_url"] is not None:
                yield scrapy.Request(
                    item["detail_url"],
                    callback=self.detail_parse,
                    meta={"item":item}
                )
        #翻页
        if self.i <self.settings.get('MAX_PAGE'):
            urls = response.xpath("//div[@id='pages']/a")
            for url in urls:
                if url.xpath("./text()").extract_first() == "下一页":
                    next_url = url.xpath("./@href").extract_first()
            if next_url is not None:
                next_url = urllib.parse.urljoin(response.url,next_url)
                self.i += 1
                if next_url != response.url:
                    yield scrapy.Request(
                        next_url,
                        callback=self.parse
                    )

    def detail_parse(self,response):
        #翻页之后获取item，同一个套图的图片用一个imgs来进行存储，因为需要referer的url所以需要把每个大页面的url进行存储
        item = response.meta["item"]
        try:
            imgs = response.meta["imgs"]
        except:
            imgs = []
        try:
            r_urls = response.meta["r_urls"]
        except:
            r_urls = []
        images = response.xpath("//div[@class='content']/center/img")
        for img in images:
            a = img.xpath("./@src").extract_first()
            imgs.append(a)
        item["image_urls"] = imgs
        urls = response.xpath("//div[@id='pages']/a")
        for url in urls:
            if url.xpath("./text()").extract_first() == "下一页":
                next_url = url.xpath("./@href").extract_first()
        r_urls.append(response.url)
        item["refer_urls"] = r_urls
        #翻页处理，美图录的下一页在最后一页还是存在的，而且最后一页的下一页url与最后一页的url相同，这里进行了一个判断，如果爬取到了最后一页就把item交给pipeline进行处理
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            if next_url != response.url:
                yield scrapy.Request(
                    next_url,
                    callback=self.detail_parse,
                    meta={"item":item,"imgs":imgs,"r_urls":r_urls}
                )
            else:
                yield item