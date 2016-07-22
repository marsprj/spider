# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#create table db_movie (id int auto_increment, 
#	name varchar(128),
#	 editor varchar(128), 
#	 director varchar(128), 
#	 actors varchar(256), 
#	 year varchar(32), 
#	 abstract varchar(4096), 
#	 type varchar(128), 
#	 country varchar(32), 
#	 language varchar(32),
#	 issue varchar(128), 
#	 rating varchar(16), 
#	 rating_people varchar(16), 
#	 primary key(id));

class MovieItem(scrapy.Item):
    tag = scrapy.Field()
    name = scrapy.Field()
    editor = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    mtype = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    issue = scrapy.Field()
    rating = scrapy.Field()
    rating_people = scrapy.Field()
    year = scrapy.Field()
    abstract = scrapy.Field()
