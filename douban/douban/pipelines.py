# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class TopMoviePipeline(object):
    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'MySQLdb',
            host = '127.0.0.1',
            db = 'spider',
            user = 'root',
            passwd = 'qwer1234',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

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
#        tx.execute(sql, (item['name'][0:],item['director'][0:],item['actors'][0:],item['year'][0:],item['abstract'][0:]))
#        tx.execute(sql, (item['name'][0:],item['director'][0:],item['actors'][0:],item['abstract'][0:]))
#        tx.execute(sql, (item['name'][0:], item['director'][0:], item['actors'][0:],item['year'][0:] ))
#        tx.execute(sql, (item['name'][0:], item['director'][0:], item['abstract'][0:]))
        tx.execute(sql, (item['name'][0:], item['director'][0:], item['actors'][0:]))
#        tx.execute(sql, (item['name'][0:]))


class MoviePipeline(object):
    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName = 'MySQLdb',
            host = '127.0.0.1',
            db = 'spider',
            user = 'root',
            passwd = 'qwer1234',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

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
#        sql = 'insert into db_movie(name, director,actors) values(%s,%s,%s)'
        sql = 'insert into db_movie(name, director,editor,actors, type, country, language, issue, year, abstract, rating, rating_people) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#        sql = 'insert into db_movie_top250(name values(%s)'
#        print item['name']
#        print item['director']
#        print item['actors']
#        print item['year']
#        print item['abstract']
#        tx.execute(sql, (item['name'][0:],item['director'][0:],item['actors'][0:],item['year'][0:],item['abstract'][0:]))
#        tx.execute(sql, (item['name'][0:],item['director'][0:],item['actors'][0:],item['abstract'][0:]))
#        tx.execute(sql, (item['name'][0:], item['director'][0:], item['actors'][0:],item['year'][0:] ))
#        tx.execute(sql, (item['name'][0:], item['director'][0:], item['abstract'][0:]))
        tx.execute(sql, (item['name'][0:], item['director'][0:], item['editor'][0:],item['actors'][0:], item['mtype'][0:], item['country'][0:], item['language'][0:], item['issue'][0:], item['year'][0:],item['abstract'][0:], item['rating'][0:], item['rating_people'][0:]))
#        tx.execute(sql, (item['name'][0:]))

