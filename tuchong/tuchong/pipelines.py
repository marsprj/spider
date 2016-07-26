# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import string
import os
import os.path
import urllib

class TuchongPipeline(object):
    def process_item(self, item, spider):
        return item

class TuPipeline(object):

    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'photo')
        if os.path.exists(self.base_dir) != True:
            os.mkdir(self.base_dir)

    def open_spider(self, spider):
        # self.dbpool = adbapi.ConnectionPool(
        #     dbapiName = 'psycopg2',
        #     host = '192.168.111.160',
        #     database = 'spider',
        #     user = 'postgres',
        #     password = 'qwer1234',
        # )
        pass

    def close_spider(self, spider):
        pass


    def process_item(self, item, spider):
        self.process_photo(item)
        return item

    def process_photo(self, item):
        photo_url  = item['url']
        print photo_url
        if len(photo_url)>0:
        	photo_name = self.get_photo_name(item['url'])
        	photo_id   = photo_name[:-4]

        	self.save_image(photo_url, photo_name)

    def get_photo_name(self, photo_url):
        return photo_url.split('/')[-1]

    def save_image(self, url, name):
        fpath = os.path.join(self.base_dir, name)
        urllib.urlretrieve(url, fpath)
