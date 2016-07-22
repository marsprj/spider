# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zhihu.items import PhotoItem

#create table zh_answer (id int auto_increment, aid int, qid int, title varchar(128), author varchar(32), upvote varchar(16), issue varchar(32), content text, primary key(id));


class QuestionSpider(CrawlSpider):
	name = u'photo'
	allowed_domains = ['zhihu.com']
	start_urls = [
		'https://www.zhihu.com/explore',
	]

	rules = (
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/explore$'), follow=True),
#		Rule(LinkExtractor(allow=r'/topic/[^/]+'), callback='parse_topic', follow=True),
		Rule(LinkExtractor(allow=r'/topic/\d+$'), follow=True),
		Rule(LinkExtractor(allow=r'/topic/\d+/hot$'), follow=True),
		Rule(LinkExtractor(allow=r'/question/\d+$'),  follow=True),
		Rule(LinkExtractor(allow=r'/question/\d+/answer/\d+'), follow=True),
		Rule(LinkExtractor(allow=r'/people/[^/]+', allow_domains=['zhihu.com']), callback='parse_people',follow=True),
	)

	###################################################################
	# people methods
	###################################################################
	def parse_people(self, response):
		a = PhotoItem()
		a['typ'] = u'photo'
		a['photo'] = self.get_author_photo(response)
		a['gender'] = self.get_author_gender(response)

		yield a

	def get_author_photo(self, response):
		return response.xpath('//div[@class="zm-profile-header-main"]/div/img/@srcset').extract()[0].split(' ')[0]

	def get_author_gender(self, response):
		arr = response.xpath('//span[@class="item gender"]/i/@class').extract()
		if any(arr) == False:
			return u'' 

		gender = arr[0].split('-')[-1]
		return 'F' if gender == u'female' else 'M' 
