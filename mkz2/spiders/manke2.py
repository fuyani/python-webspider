# -*- coding: utf-8 -*-
import scrapy
import urllib

class Manke2Spider(scrapy.Spider):
    name = 'manke2'
    allowed_domains = ['mkzhan.com']
    start_urls = ['https://www.mkzhan.com/category/?is_free=1']

    def parse(self, response):
        div_list = response.xpath("//div[@class='cate-comic-list clearfix']/div")
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./p[1]/a/text()").extract_first()
            item["detail_url"] = div.xpath("./a/@href").extract_first()
            if item["detail_url"] is not None:
                item["detail_url"] = urllib.parse.urljoin(response.url,item["detail_url"])
                yield scrapy.Request(
                    item["detail_url"],
                    callback=self.next_parse,
                    meta={"item":item}
                )

    def next_parse(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='chapter__list-box clearfix hide']/li")
        for li in li_list:
            item["qk_url"] = li.xpath("./a/@data-hreflink").extract_first()
            if item["qk_url"] is not None:
                item["qk_url"] = urllib.parse.urljoin(response.url,item["qk_url"])
                yield scrapy.Request(
                    item["qk_url"],
                    callback=self.detail_parse,
                    meta={"item":item}
                )

    def detail_parse(self,response):
        item = response.meta["item"]
        item["qi_kan"] = response.xpath("//a[@class='last-crumb']/text()").extract_first()
        imgs = []
        div_list = response.xpath("//div[@class='rd-article-wr clearfix']/div")
        for div in div_list:
            img = div.xpath("./img/@data-src").extract_first()
            if img is not None:
                imgs.append(img)
        item["image_urls"] = imgs
        yield item

