# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import requests
import os
import hashlib

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = 'man_kz2'
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class Image_Download:
    def __init__(self,filter_path):
        self.filter_path = filter_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
           filter_path=crawler.settings.get("FILTER_PATH")
        )

    def process_item(self,item,spider):
        os.chdir("E:\\ManKeZhan2")
        b_dir_name = item["title"]
        s_dir_name = item["qi_kan"]
        try:
            os.mkdir(b_dir_name)
            os.chdir("E:\\ManKeZhan2\\%s"%b_dir_name)
        except:
            os.chdir("E:\\ManKeZhan2\\%s"%b_dir_name)
        try:
            os.mkdir(s_dir_name)
            os.chdir("E:\\ManKeZhan2\\%s\\%s" %(b_dir_name,s_dir_name))
        except:
            os.chdir("E:\\ManKeZhan2\\%s\\%s" %(b_dir_name, s_dir_name))
        for url in item["image_urls"]:
            sha1 = hashlib.sha1()
            sha1.update(url.encode())
            a = sha1.hexdigest()
            with open(self.filter_path, 'r') as f:
                if a in f.read():
                    break
                else:
                    headers = {
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                    }
                    try:
                        response = requests.get(url,headers,timeout=5)
                    except:
                        response = requests.get(url, headers, timeout=5)
                    with open(self.filter_path,'a') as f:
                        f.write(a)
                    html = response.content
                    try:
                        file_name = "".join((url.split('/')[-1].split('-')[0],'.jpg'))
                        with open(file_name,'wb') as f:
                            print("正在下载：",url)
                            f.write(html)
                    except:
                        print("发生错误，下载终止！")
                        break
        return item