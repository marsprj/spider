# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import string
import os
import os.path
import urllib

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item

class TopicPipeline(object):

    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), 'photo')
        if os.path.exists(self.base_dir) != True:
            os.mkdir(self.base_dir)

    def open_spider(self, spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'MySQLdb',
            host = 'localhost',
            db = 'spider',
            user = 'root',
            passwd = 'qwer1234',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if spider.name == 'topic':
            query = self.dbpool.runInteraction(self.topic_insert, item)
        elif spider.name=='question':
            if item['typ'] == u'question':
                query = self.dbpool.runInteraction(self.question_insert, item)
            elif item['typ'] == u'answer':
                query = self.dbpool.runInteraction(self.answer_insert, item)
            elif item['typ'] == u'author':
                self.process_author(item)
        return item

    def topic_insert(self, tx, item):
        sql  = 'insert into zh_topic(tid,title,description,parent) value(%s,%s,%s,%s)'
        tx.execute(sql, (item['tid'], item['title'], item['description'], item['parent']))

    def question_insert(self, tx, item):
        sql  = 'insert into zh_question(qid,title,description,topics,follow_number) value(%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['qid'], item['title'], item['description'], item['topics'], item['follow_number']))

    def answer_insert(self, tx, item):
        sql  = 'insert into zh_answer(aid, qid,author, author_name, upvote, issue, content) value(%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['aid'], item['qid'], item['author'], item['author_name'], item['upvote'], item['issue'], item['content']))

    def process_author(self, item):
        photo_url  = item['photo']
        photo_name = self.get_photo_name(item['photo'])
        photo_id   = photo_name[:-4]
        
#        self.save_image(photo_url,item['gender'].lower() + '_' + photo_name)
        
        query = self.dbpool.runInteraction(self.author_insert, item)

    def author_insert(self, tx, item):
        photo_name = self.get_photo_name(item['photo'])

        sql = 'insert into zh_author (aid, name, gender, bio, location, employment, position, education, content, upvote, thanks, asks, answers, posts, collections, logs, followees, followers, visits, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        tx.execute(sql, (item['aid'], item['name'], item['gender'], item['bio'], item['location'], item['employment'], item['position'], item['education'], item['content'], item['upvote'], item['thanks'], item['asks'], item['answers'], item['posts'], item['collections'], item['logs'], item['followees'], item['followers'], item['visits'], photo_name)) 

    def get_photo_name(self, photo_url):
        return photo_url.split('/')[-1]

    def save_image(self, url, name):
        fpath = os.path.join(self.base_dir, name)
        urllib.urlretrieve(url, fpath)
