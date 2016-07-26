# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor
from douban.items import MovieItem
import string

class MovieSpider(CrawlSpider):
	name = 'movie'
	allow_domains = [
		'douban.com',
	]

	start_urls = [
		'https://movie.douban.com/tag/',
	]

	rules = [
		Rule(LinkExtractor(allow=('/tag/$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+/?$')), follow=True),
		Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/$')), callback='parse_movie'),
	]
	
	def parse_movie(self, response):
		x = Selector(response)
		
		item = MovieItem()
		#item['subject_id'] = response.url.split("/")[-1]
		#item['url'] = response.url
		item['mid'] = self.get_mid(response)
		item['name'] = self.get_name(response)
		item['director'] = self.get_director(response)
		item['writer'] = self.get_writer(response)
		item['actors'] = self.get_actors(response)
		item['mtype'] = self.get_mtype(response)
		item['runtime'] = self.get_runtime(response)
		#item['country'] = ''.join(x.xpath('//*[@id="info"]/text()[3]').extract()).strip()
		item['country'] = self.get_country(response)
		item['language'] = self.get_language(response)
		item['issue'] = self.get_issue(response)
		item['year'] = self.get_year(response)
		#item['abstract'] = ''.join(x.xpath('//*[@id="link-report"]/span[1]/text()').extract()).strip()
		item['abstract'] = self.get_abstract(response)
		item['rating'] = self.get_rating(response)
		item['rating_people'] = self.get_rating_people(response)

		yield item

	def get_mid(self, response):
		if response.url[-1] == '/':
			return response.url.split('/')[-1]
		else:
			return response.url.split('/')[-2]

	def get_name(self, response):
		return response.xpath('//div[@id="content"]/h1/span/text()').extract()[0]
	
	def get_director(self, response):
		arr =  response.xpath(u'//span[contains(text(),"导演")]/following-sibling::span/a/text()').extract()
		return arr[0] if any(arr) else u''

	def get_writer(self, response):
		arr = response.xpath(u'//span[contains(text(),"编剧")]/following-sibling::span/a/text()').extract()
		return ','.join(arr)

	def get_actors(self, response):
		arr = response.xpath(u'//span[contains(text(),"主演")]/following-sibling::span/a/text()').extract()
		return ','.join(arr)

	def get_mtype(self, response):
		arr = response.xpath(u'//span[@property="v:genre"]/text()').extract()
		return ','.join(arr)

	def get_year(self, response):
		return ''.join(response.xpath('//*[@id="content"]/h1/span[2]/text()').extract()).strip()[1:-1]
		
	def get_country(self, response):
		arr = response.xpath(u'//span[contains(text(),"制片国家")]/text()').extract()
		if any(arr):
			tag_name = arr[0]
			parent_text = response.xpath(u'//span[contains(text(),"制片国家")]/parent::*').extract()[0]
			tag_pos = parent_text.find(tag_name)
			if tag_pos == -1:
				return u''
			right_text = parent_text[tag_pos:]
			brace_pos = right_text.find('>')
			br_pos = right_text.find('<br>')
			countries = right_text[brace_pos+1:br_pos].strip()
			return ','.join([s.strip() for s in countries.split('/')])
		else:
			return u''

	def get_language(self, response):
		parent_text = response.xpath(u'//span[contains(text(),"语言")]/parent::*').extract()[0]
		language_pos = parent_text.find(u'语言')
		if language_pos == -1:
			return u''
		right_text = parent_text[language_pos:]
		brace_pos = right_text.find('>')
		br_pos = right_text.find('<br>')
		languages  = right_text[brace_pos+1:br_pos].strip()
		return ','.join([s.strip() for s in languages.split('/')])

	def get_issue(self, response):
		arr = response.xpath(u'//span[contains(text(),"上映日期")]/following-sibling::span[@property="v:initialReleaseDate"]/@content').extract()
		return ",".join(arr)

	def get_abstract(self, response):
		return ''.join((response.xpath(u'//div[@id="link-report"]/span/text()').extract())).strip()

	def get_rating(self, response):
		arr = response.xpath(u'//strong[@class="ll rating_num"]/text()').extract()
		return string.atof(arr[0]) if any(arr) else 0.0

	def get_rating_people(self, response):
		arr = response.xpath(u'//span[@property="v:votes"]/text()').extract()
		return string.atoi(arr[0]) if any(arr) else 0

	def get_runtime(self, response):
		arr = response.xpath(u'//span[@property="v:runtime"]/@content').extract()
		return string.atoi(arr[0]) if any(arr) else 0
