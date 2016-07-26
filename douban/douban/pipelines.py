# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import psycopg2

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class TopMoviePipeline(object):
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
        query = self.dbpool.runInteraction(self._condition_insert, item)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	print item['abstract']
	return item

    def _condition_insert(self, tx, item):
#        sql = 'insert into db_movie(name, director,writer,actors, type, runtime, country, language, issue, year) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#        tx.execute(sql, (item['name'], item['director'], item['writer'],item['actors'], item['mtype'], item['runtime'], item['country'], item['language'], item['issue'], item['year']))


        sql = 'insert into db_movie(mid, name, director,writer,actors, type, runtime, country, language, issue, year, abstract, rating, rating_people) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, (item['mid'],item['name'], item['director'], item['writer'],item['actors'], item['mtype'], item['runtime'], item['country'], item['language'], item['issue'], item['year'],item['abstract'], item['rating'], item['rating_people']))
