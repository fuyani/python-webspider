# -*- coding: utf-8 -*-

# Define your item["refer_urls"] pipelines here
#
# Don't forget to add your pipeline to the item["refer_urls"]_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item["refer_urls"]-pipeline.html

import pymongo
import requests
import os
from scrapy.exceptions import DropItem

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # @classmethod 只在类中运行，不在实例中运行
    @classmethod
    def from_crawler(cls,crawler):
        #获取在setting中设置的连接地址和数据库的名称
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        #使用insert方法进行数据的插入
        name = "Qi_Zhi"
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

class images_download():
    def process_item(self,item,spider):
        #更改目录进行指定目录的存储
        os.chdir("E:\\meitulu")
        #每个套图用一个文件夹来存放，文件夹名字用套图模特的名字和套路刊号来命名
        dir_name = "".join((item["img_model"],item["detail_url"].split('/')[-1].split('.')[0]))
        #尝试创建文件夹并更改目录，如果文件夹存在则移动到命名的文件夹
        try:
            os.mkdir(dir_name)
            os.chdir(dir_name)
        except:
            os.chdir("E:\\meitulu\\%s"%dir_name)
        #进行refererurl的判断
        for url in item["image_urls"]:
            try:
                if int(url.split('/')[-1].split('.')[0])<5:
                    u = item["refer_urls"][0]
                if 5<= int(url.split('/')[-1].split('.')[0])<9:
                    u = item["refer_urls"][1]
                if 9<= int(url.split('/')[-1].split('.')[0])<13:
                    u = item["refer_urls"][2]
                if 13<=int(url.split('/')[-1].split('.')[0])<17:
                    u = item["refer_urls"][3]
                if 17<=int(url.split('/')[-1].split('.')[0])<21:
                    u = item["refer_urls"][4]
                if 21<=int(url.split('/')[-1].split('.')[0])<25:
                    u = item["refer_urls"][5]
                if 25<=int(url.split('/')[-1].split('.')[0])<29:
                    u = item["refer_urls"][6]
                if 29<=int(url.split('/')[-1].split('.')[0])<33:
                    u = item["refer_urls"][7]
                if 33<=int(url.split('/')[-1].split('.')[0])<37:
                    u = item["refer_urls"][8]
                if 37<=int(url.split('/')[-1].split('.')[0])<41:
                    u = item["refer_urls"][9]
                if 41<=int(url.split('/')[-1].split('.')[0])<45:
                    u = item["refer_urls"][10]
                if 45<=int(url.split('/')[-1].split('.')[0])<49:
                    u = item["refer_urls"][11]
                if 49<=int(url.split('/')[-1].split('.')[0])<53:
                    u = item["refer_urls"][12]
                if 53<=int(url.split('/')[-1].split('.')[0])<57:
                    u = item["refer_urls"][13]
                if 57<=int(url.split('/')[-1].split('.')[0])<61:
                    u = item["refer_urls"][14]
                if 61<=int(url.split('/')[-1].split('.')[0])<65:
                    u = item["refer_urls"][15]
                if 65<=int(url.split('/')[-1].split('.')[0])<69:
                    u = item["refer_urls"][16]
                if 69<=int(url.split('/')[-1].split('.')[0])<73:
                    u = item["refer_urls"][17]
                if 73<=int(url.split('/')[-1].split('.')[0])<77:
                    u = item["refer_urls"][18]
                if 77<=int(url.split('/')[-1].split('.')[0])<81:
                    u = item["refer_urls"][19]
                if 81<=int(url.split('/')[-1].split('.')[0])<85:
                    u = item["refer_urls"][20]
                if 85<=int(url.split('/')[-1].split('.')[0])<89:
                    u = item["refer_urls"][21]
                if 89<=int(url.split('/')[-1].split('.')[0])<93:
                    u = item["refer_urls"][22]
                if 93<=int(url.split('/')[-1].split('.')[0])<97:
                    u = item["refer_urls"][23]
                if 97<=int(url.split('/')[-1].split('.')[0])<101:
                    u = item["refer_urls"][24]
                if 101<=int(url.split('/')[-1].split('.')[0])<105:
                    u = item["refer_urls"][25]
                if 105<=int(url.split('/')[-1].split('.')[0])<109:
                    u = item["refer_urls"][26]
                if 109<=int(url.split('/')[-1].split('.')[0])<118:
                    u = item["refer_urls"][27]
                if 118<=int(url.split('/')[-1].split('.')[0])<122:
                    u = item["refer_urls"][28]
                else:
                    u = item["refer_urls"][29]
            except:
                pass
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
                "Request": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": u
            }

            try:
                response = requests.get(url,headers=headers,timeout=5)
            except:
                response = requests.get(url, headers=headers, timeout=5)
            html = response.content
            if "permission" in str(html):
                pass
            else:
                try:
                    file_name = url.split('/')[-1]
                    with open(file_name,'wb') as f:
                        print('正在下载：',url)
                        f.write(html)
                except:
                    print("发生错误，终止")
                    break

        os.getcwd()
        return item


