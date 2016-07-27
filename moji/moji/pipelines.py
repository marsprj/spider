# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import psycopg2
import string
import os
import os.path
import urllib

class MojiPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagePipeline(object):
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'image')
        if os.path.exists(self.base_dir) != True:
            os.mkdir(self.base_dir)

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'psycopg2',
            host = '192.168.111.160',
            database = 'spider',
            user = 'postgres',
            password = 'qwer1234',
        )
        
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['typ'] == 'info':
            self.process_info(item)
        elif item['typ']=='image':
            self.process_image(item)
        return item

    def process_info(self, item):
    	pid = item['pid']
    	if self.has_image(pid):
    		self.update_info(item)
    	else:
    		self.insert_info(item)

    def process_image(self, item):
    	pid = item['pid']
    	if self.has_image(pid):
    		self.update_image(item)
    	else:
    		self.insert_image(item)

    def has_image(self, item):
    	return False

    def insert_image(self, item):
    	self.dbpool.runInteraction(self._condition_insert_image, item)
    	self.save_image(item['pname'], item['url'])

    def _condition_insert_image(self, tx, item):
    	ptime = item['ptime'].replace('AM','')[:-3]
    	print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    	print ptime
        sql  = 'insert into mj_photo(pid,location,ptime,pname) values(%s,%s,%s,%s)'
        tx.execute(sql, (item['pid'], item['location'], ptime, item['pname']))

    def update_image(self, item):
    	print '====================================='
    	pass

    def insert_info(self, item):
    	self.dbpool.runInteraction(self._condition_insert_info, item)

    def _condition_insert_info(self, tx, item):
        sql  = 'insert into mj_photo(pid,country,province,district) values(%s,%s,%s,%s)'
        tx.execute(sql, (item['pid'], item['country'], item['province'], item['disrict']))

    def update_info(self, item):
    	pass

    def save_image(self, name, url):
    	fpath = os.path.join(self.base_dir, name)
        urllib.urlretrieve(url, fpath)