# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

###################################################
#PostgreSQL
###################################################
#create table db_movie(
#    id serial,
#    mid character varying(128),
#    name character varying(128),
#    director character varying(128),
#    writer character varying(128),
#    actors character varying(128),
#    runtime int default 0,
#    year int default 0,
#    abstract text,
#    type character varying(128),
#    country character varying(32),
#    language character varying(32),
#    issue character varying(32),
#    ratint double precision,
#    rating_people int default 0,
#    primary key(id),
#    CONSTRAINT db_movie_name_uk UNIQUE (name)
#    CONSTRAINT db_movie_mid_uk UNIQUE (mid)
#);

###################################################
#MySQL
###################################################
#create table db_movie (id int auto_increment, 
#   name varchar(128),
#    editor varchar(128), 
#    director varchar(128), 
#    actors varchar(256), 
#    year varchar(32), 
#    abstract varchar(4096), 
#    type varchar(128), 
#    country varchar(32), 
#    language varchar(32),
#    issue varchar(128), 
#    rating varchar(16), 
#    rating_people varchar(16), 
#    primary key(id));


import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(scrapy.Item):
    tag = scrapy.Field()
    mid = scrapy.Field()
    name = scrapy.Field()
    writer = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    mtype = scrapy.Field()
    runtime = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    issue = scrapy.Field()
    rating = scrapy.Field()
    rating_people = scrapy.Field()
    year = scrapy.Field()
    abstract = scrapy.Field()
