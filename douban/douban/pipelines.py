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

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class TopMoviePipeline(object):

    def __init__(self):
        self.photo_dir = os.path.join(os.getcwd(), 'photo')
        if os.path.exists(self.photo_dir) != True:
            os.mkdir(self.photo_dir)

        self.image_dir = os.path.join(os.getcwd(), 'image')
        if os.path.exists(self.image_dir) != True:
            os.mkdir(self.image_dir)

    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'psycopg2',
            host = '192.168.111.160',
            database = 'spider',
            user = 'postgres',
            password = 'qwer1234',
        )
#    def open_spider(self,spider):
#        self.dbpool = adbapi.ConnectionPool(
#            dbapiName = 'MySQLdb',
#            host = '192.168.111.86',
#            db = 'spider',
#            user = 'root',
#            password = 'qwer1234',
#            cursorclass = MySQLdb.cursors.DictCursor,
#            charset = 'utf8',
#            use_unicode = False
#        )

    def close_spider(self,spider):
        pass

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._condition_insert, item)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print item['abstract']
	return item

    def _condition_insert(self, tx, item):
#        sql = 'insert into db_movie_top250(name, director, actors, year, abstract) values(%s,%s,%s,%d,%s)'
#        sql = 'insert into db_movie_top250(name, director, actors, abstract) values(%s,%s,%s,%s)'
#        sql = 'insert into db_movie_top250(name, director,actors,year) values(%s,%s,%s,%s)'
#        sql = 'insert into db_movie_top250(name, director,abstract) values(%s,%s,%s)'
        sql = 'insert into db_movie_top250(name, director,actors) values(%s,%s,%s)'
#        sql = 'insert into db_movie_top250(name values(%s)'
#        print item['name']
#        print item['director']
#        print item['actors']
#        print item['year']
#        print item['abstract']
#        tx.execute(sql, (item['name'],item['director'],item['actors'],item['year'],item['abstract']))
#        tx.execute(sql, (item['name'],item['director'],item['actors'],item['abstract']))
#        tx.execute(sql, (item['name'], item['director'], item['actors'],item['year'] ))
#        tx.execute(sql, (item['name'], item['director'], item['abstract']))
        tx.execute(sql, (item['name'], item['director'], item['actors']))
#        tx.execute(sql, (item['name']))


class MoviePipeline(object):

    def __init__(self):
        self.photo_dir = os.path.join(os.getcwd(), 'photo')
        if os.path.exists(self.photo_dir) != True:
            os.mkdir(self.photo_dir)

        self.image_dir = os.path.join(os.getcwd(), 'image')
        if os.path.exists(self.image_dir) != True:
            os.mkdir(self.image_dir)

    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'psycopg2',
            host = '192.168.111.160',
            database = 'spider',
            user = 'postgres',
            password = 'qwer1234',
        )
#        self.dbpool = adbapi.ConnectionPool(
#            dbapiName = 'MySQLdb',
#            host = 'localhost',
#            db = 'spider',
#            user = 'root',
#            password = 'qwer1234',
#            cursorclass = MySQLdb.cursors.DictCursor,
#            charset = 'utf8',
#            use_unicode = False
#        )

    def close_spider(self,spider):
        pass

    def process_item(self, item, spider):
        typ = item['typ']
        if typ == 'image':
            self.save_image(item['mid'], item['url'])
        elif typ == 'photo':
            self.save_photo(item['mid'], item['url'])
        elif typ == 'actor':
            self.process_actor(item)
        else:
            query = self.dbpool.runInteraction(self._condition_insert, item)
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            print item['abstract']
        return item

    def _condition_insert(self, tx, item):
#        sql = 'insert into db_movie(name, director,writer,actors, type, runtime, country, language, issue, year) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#        tx.execute(sql, (item['name'], item['director'], item['writer'],item['actors'], item['mtype'], item['runtime'], item['country'], item['language'], item['issue'], item['year']))


        sql = 'insert into db_movie_2(mid, name, director,writer,actors, type, runtime, country, language, issue, year, abstract, rating, rating_people) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['mid'],item['name'], item['director'], item['writer'],item['actors'], item['mtype'], item['runtime'], item['country'], item['language'], item['issue'], item['year'],item['abstract'], item['rating'], item['rating_people']))

    def save_image(self, mid, url):
        name = url.split('/')[-1]
        fname = mid + "_" + name
        fpath =os.path.join(self.image_dir, fname) 
        urllib.urlretrieve(url, fpath)

    def save_photo(self, mid, url):
        name = url.split('/')[-1]
        fname = mid + "_" + name
        fpath =os.path.join(self.photo_dir, fname) 
        urllib.urlretrieve(url, fpath)

    def process_actor(self, item):
        self.dbpool.runInteraction(self.actor_insert, item)

    def actor_insert(self, tx, item):
        text = item['name']
        pos = text.find(' ')
        if pos < 0:
            name = text
        else:
            name = text[:pos].strip()
            ename=text[pos+1:].strip()

        sql = 'insert into db_actor(aid, gender, name, ename, constellation, birthday, birthplace, profession, family, fname, cname, imdb) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        tx.execute(sql, (item['aid'] , item['gender'] , name , ename , item['constellation'] , item['birthday'] , item['birthplace'] , item['profession'] , item['family'] , item['fname'] , item['cname'] , item['imdb']))
