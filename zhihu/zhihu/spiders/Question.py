# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zhihu.items import QuestionItem, AnswerItem,AuthorItem,TopicItem

#create table zh_answer (id int auto_increment, aid int, qid int, title varchar(128), author varchar(32), upvote varchar(16), issue varchar(32), content text, primary key(id));


class QuestionSpider(CrawlSpider):
	name = 'question'
	allowed_domains = ['zhihu.com']
	start_urls = [
		'https://www.zhihu.com/explore',
#		'https://www.zhihu.com/question/41351785',
#		'https://www.zhihu.com/topic/19553622',
	]

	rules = (
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/explore$'), follow=True),
#		Rule(LinkExtractor(allow=r'/topic/[^/]+'), callback='parse_topic', follow=True),
		Rule(LinkExtractor(allow=r'/topic/\d+$'), callback='parse_topic'),
		Rule(LinkExtractor(allow=r'/topic/\d+/hot$'), callback='parse_topic'),
		Rule(LinkExtractor(allow=r'/question/\d+$'), callback='parse_question', follow=True),
		Rule(LinkExtractor(allow=r'/question/\d+/answer/\d+'), callback='parse_answer'),
		Rule(LinkExtractor(allow=r'/people/[^/]+', allow_domains=['zhihu.com']), callback='parse_people',follow=True),
	)

	def parse_topic(self, response):
		print "sssssssssssssssssssssssssssssssssssssssssssssssssssss"
		t = TopicItem()
		t['typ'] = u'topic'
		t['title'] = response.xpath('//h1[@class="zm-editable-content"]/text()').extract()
		t['description'] = response.xpath('//div[@class="zm-editable-content"]/text()').extract()
		t['parent'] = self.format_topic_parents(response.xpath('//div[@id="zh-topic-side-parents-list"]/div/div/a/@href').extract())
		t['tid'] = self.get_topic_id(response.url)
    
		yield t

	def format_topic_parents(self, parents):
		pids = [e.split('/')[-1] for e in parents]
		return ','.join(pids)

	def get_topic_id(self, url):
		if url[-3:] == 'hot':
			tid = response.url.split('/')[-2]
		else:
			tid = response.url.split('/')[-1]
                return tid  


	def parse_question(self, response):
		q = QuestionItem()
		q['typ'] = u'question'
		q['qid'] = response.url.split('/')[-1]
		q['title'] = response.xpath('//span[@class="zm-editable-content"]/text()').extract()[0].strip()
		q['description'] = self.get_question_description(response)
		q['topics'] = self.get_question_topics(response)
		q['follow_number'] = self.get_question_follow_number(response)
		yield q

	def parse_answer(self, response):
		a = AnswerItem()
		a['typ'] = u'answer'
		a['aid'] = self.get_answer_id(response)
		a['qid'] = self.get_question_id(response)
		a['title'] = self.get_answer_title(response)
		a['author'] = self.get_answer_author(response)
		a['author_name'] = self.get_answer_author_name(response)
		a['upvote'] = self.get_answer_upvote(response)
		a['issue'] = self.get_answer_issue(response)
		a['content'] = self.get_answer_content(response)
		a['html_content'] = self.get_answer_content(response)
		
		yield a

	def get_question_description(self, response):
		arr = response.xpath('//div[@class="zm-editable-content"]/text()').extract()
		return arr[0].strip() if len(arr)>0 else ''

	def get_question_topics(self, response):
		return ','.join(response.xpath('//a[@class="zm-item-tag"]/@data-token').extract())

	def get_question_follow_number(self, response):
		arr = response.xpath('//div[@id="zh-question-side-header-wrap"]/text()').extract()
		if len(arr) == 0:
			return 0
		else:
			str = arr[-1]
			if len(str)<9:
				return 0
			else:
				return string.atoi(str[2:-9])

	def get_answer_id(self,response):
		return response.url.split('/')[-1]

	def get_question_id(self, response):
		return response.url.split('/')[-3]

	def get_answer_title(self, response):
		pass

	def get_answer_author(self, response):
		#return response.xpath("//a[@class='author-link']/text()").extract()[0] 
		return response.xpath("//a[@class='author-link']/@href").extract()[0].split('/')[-1]

	def get_answer_author_name(self, response):
		return response.xpath("//a[@class='author-link']/text()").extract()[0] 

	def get_answer_upvote(self, response):
		str = response.xpath("//span[@class='count']/text()").extract()[0]
		return self.get_number(str)
		#return response.xpath("//span[@class='count']/text()").extract()[0]

	def get_answer_issue(self, response):
		#return u'context'
		return response.xpath("//a[@class='answer-date-link meta-item']/text()").extract()[0][4:]

	def get_answer_content(self, response):
		return ''.join(response.xpath("//div[@class='zm-editable-content clearfix']/text()").extract())
		#return u'content'

	def get_answer_html_content(self, response):
		return response.xpath("//div[@class='zm-editable-content clearfix']").extract()[0]

	###################################################################
	# people methods
	###################################################################
	def parse_people(self, response):
		a = AuthorItem()
		a['typ'] = u'author'
		a['aid'] = self.get_author_id(response)
		a['name'] = self.get_author_name(response)
		a['gender'] = self.get_author_gender(response)
		a['bio'] = self.get_author_bio(response)
		a['location'] = self.get_author_location(response)
		a['employment'] = self.get_author_employment(response)
		a['position'] = self.get_author_position(response)
		a['education'] = self.get_author_education(response)
		a['content'] = self.get_author_content(response)
		a['upvote'] = self.get_author_upvote(response)
		a['thanks'] = self.get_author_thanks(response)
		a['asks'] = self.get_author_asks(response)
		a['answers'] = self.get_author_answers(response)
		a['posts'] = self.get_author_posts(response)
		a['collections'] = self.get_author_collections(response)
		a['logs'] = self.get_author_logs(response)
		a['followees'] = self.get_author_followees(response)
		a['followers'] = self.get_author_followers(response)
		a['visits'] = self.get_author_visits(response)
		a['photo'] = self.get_author_photo(response)

		yield a

	def get_author_id(self, response):
		return response.url.split('/')[-1]

	def get_author_name(self, response):
		arr = response.xpath('//span[@class="name"]/text()').extract()
		return arr[0] if any(arr) else u''

	def get_author_bio(self, response):
		arr = response.xpath('//span[@class="bio"]/text()').extract()
		return arr[0] if any(arr) else u''

	def get_author_location(self, response):
		arr = response.xpath('//span[@class="location item"]/@title').extract()
		return arr[0] if any(arr) else u''

	def get_author_gender(self, response):
		arr = response.xpath('//span[@class="item gender"]/i/@class').extract()
		if any(arr) == False:
			return u''
		
		gender = arr[0].split('-')[-1]
		return 'F' if gender == u'female' else 'M'

	def get_author_employment(self, response):
		arr = response.xpath('//span[@class="employment item"]/@title').extract()
		return arr[0] if any(arr) else u''

	def get_author_position(self, response):
		arr = response.xpath('//span[@class="position item"]/@title').extract()
		return arr[0] if any(arr) else u''

	def get_author_education(self, response):
		arr = response.xpath('//span[@class="education item"]/@title').extract()
		return arr[0] if any(arr) else u''

	def get_author_content(self, response):
		arr = response.xpath('//span[@class="content"]/text()').extract()
		return arr[0].strip() if any(arr) else u''

	def get_author_upvote(self, response):
		str = response.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()[0]
		return self.get_number(str)

	def get_author_thanks(self, response):
		str = response.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()[0]
		return self.get_number(str)

	def get_author_asks(self, response):
		str = response.xpath('//div[@class="profile-navbar clearfix"]/a[contains(@href,"/asks")]/span/text()').extract()[0]
		return self.get_number(str)

	def get_author_answers(self, response):
		str = response.xpath('//div[@class="profile-navbar clearfix"]/a[contains(@href,"/answers")]/span/text()').extract()[0]
		return self.get_number(str)

	def get_author_posts(self, response):
		str = response.xpath('//div[@class="profile-navbar clearfix"]/a[contains(@href,"/posts")]/span/text()').extract()[0]
		return self.get_number(str)

	def get_author_collections(self, response):
		str = response.xpath('//div[@class="profile-navbar clearfix"]/a[contains(@href,"/collections")]/span/text()').extract()[0]
		return self.get_number(str)

	def get_author_logs(self, response):
		str = response.xpath('//div[@class="profile-navbar clearfix"]/a[contains(@href,"/logs")]/span/text()').extract()[0]
		return self.get_number(str)

	def get_author_followees(self, response):
		str = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[contains(@href,"/followees")]/strong/text()').extract()[0]
		return self.get_number(str)

	def get_author_followers(self, response):
		str = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[contains(@href,"/followers")]/strong/text()').extract()[0]
		return self.get_number(str)

	def get_author_visits(self, response):
		str = response.xpath('//div[@class="zm-side-section-inner"]/span/strong/text()').extract()[0]
		return self.get_number(str)

	def get_author_photo(self, response):
		return response.xpath('//div[@class="zm-profile-header-main"]/div/img/@srcset').extract()[0].split(' ')[0]

	def get_number(self, str):
		if str[-1] == 'K':
			return string.atoi(str[:-1]) * 1000
		elif str[-1] == 'M':
			return string.atoi(str[:-1]) * 1000 * 1000
		else:
			return string.atoi(str)

