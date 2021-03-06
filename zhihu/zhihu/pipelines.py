# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import psycopg2
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

#    def open_spider(self, spider):
#        self.dbpool = adbapi.ConnectionPool(
#            dbapiName = 'psycopg2',
#            host = 'localhost',
#            host = '192.168.111.155',
#            user = 'root',
#            cursorclass = MySQLdb.cursors.DictCursor,
#            charset = 'utf8',
#            use_unicode = False
#        )

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
        if spider.name == 'topic':
            query = self.dbpool.runInteraction(self.topic_insert, item)
        elif spider.name=='question':
            if item['typ'] == u'question':
                query = self.dbpool.runInteraction(self.question_insert, item)
            elif item['typ'] == u'answer':
                query = self.dbpool.runInteraction(self.answer_insert, item)
            elif item['typ'] == u'author':
                self.process_author(item)
            #elif spider.name==u'photo':
            #    self.process_photo(item)
        return item

    def topic_insert(self, tx, item):
        sql  = 'insert into zh_topic(tid,title,description,parent) values(%s,%s,%s,%s)'
        tx.execute(sql, (item['tid'], item['title'], item['description'], item['parent']))

    def question_insert(self, tx, item):
        sql  = 'insert into zh_question(qid,title,description,topics,follow_number) values(%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['qid'], item['title'], item['description'], item['topics'], item['follow_number']))

    def answer_insert(self, tx, item):
        sql  = 'insert into zh_answer(aid, qid,author, author_name, upvote, issue, content, html_content) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['aid'], item['qid'], item['author'], item['author_name'], item['upvote'], item['issue'], item['content'], item['html_content']))

    def process_author(self, item):
        photo_url  = item['photo']
        photo_name = self.get_photo_name(item['photo'])
        photo_id   = photo_name[:-4]

        self.process_photo(item)
        self.dbpool.runInteraction(self.author_insert, item)

    def author_insert(self, tx, item):
        photo_name = self.get_photo_name(item['photo'])

        sql = 'insert into zh_author (aid, name, gender, bio, location, employment, position, education, content, upvote, thanks, asks, answers, posts, collections, logs, followees, followers, visits, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        tx.execute(sql, (item['aid'], item['name'], item['gender'], item['bio'], item['location'], item['employment'], item['position'], item['education'], item['content'], item['upvote'], item['thanks'], item['asks'], item['answers'], item['posts'], item['collections'], item['logs'], item['followees'], item['followers'], item['visits'], photo_name)) 

    def get_photo_name(self, photo_url):
        return photo_url.split('/')[-1]

    def save_image(self, url, name):
        fpath = os.path.join(self.base_dir, name)
        urllib.urlretrieve(url, fpath)

    def process_photo(self, item):
        photo_url  = item['photo']
        photo_name = self.get_photo_name(item['photo'])
        photo_id   = photo_name[:-4]
        photo_path  = item['gender'].lower() + '_' + photo_name

        if os.path.exists(photo_path) == False:
            self.save_image(photo_url,photo_path)

