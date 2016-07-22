# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#Answer Table

#Author Table
#create table zh_author (id int auto_increment,
#			aid int,
#			name varchar(64),
#			gender varchar(8) default 'F',
#			bio varchar(64),
#			location varchar(32),
#			employment varchar(64),
#			position varchar(64),
#			education varchar(64),
#			content text,
#			upvote int default 0,
#			thanks int default 0,
#			asks rint default 0,
#			answers rint default 0,
#			posts rint default 0,
#			collections rint default 0,
#			logs int default 0,
#			followees  int default 0,
#			followers  int default 0,
#			visits  int default 0,
#			photo varchar(64),
#			primary key(id)
#			);


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TopicItem(scrapy.Item):
    typ = scrapy.Field()
    tid = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    parent = scrapy.Field()

class QuestionItem(scrapy.Item):
    typ = scrapy.Field()
    qid = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    topics = scrapy.Field()
    follow_number = scrapy.Field()

class AnswerItem(scrapy.Item):
    typ = scrapy.Field()
    aid = scrapy.Field()
    qid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_name = scrapy.Field()
    upvote = scrapy.Field()
    issue = scrapy.Field()
    content = scrapy.Field()

class AuthorItem(scrapy.Item):
    typ = scrapy.Field()
    aid = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    bio = scrapy.Field()
    location = scrapy.Field()
    employment = scrapy.Field()
    position = scrapy.Field()
    education = scrapy.Field()
    content = scrapy.Field()
    upvote = scrapy.Field()
    thanks = scrapy.Field()
    asks = scrapy.Field()
    answers = scrapy.Field()
    posts = scrapy.Field()
    collections = scrapy.Field()
    logs = scrapy.Field()
    followees = scrapy.Field()
    followers = scrapy.Field()
    visits = scrapy.Field()
    photo = scrapy.Field()
