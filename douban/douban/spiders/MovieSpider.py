# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor
from douban.items import MovieItem,ImageItem,ActorItem
import string

class MovieSpider(CrawlSpider):
	name = 'movie'
	allow_domains = [
		'douban.com',
	]

	start_urls = [
		'https://movie.douban.com/tag/',
		'https://movie.douban.com/subject/1297011/',
		'https://movie.douban.com/tag/%E7%83%82%E7%89%87',
		'https://movie.douban.com/subject/26599625/',
		'https://movie.douban.com/tag/%E7%BA%AA%E5%BD%95%E7%89%87',
		'https://movie.douban.com/subject/10741871/',
		'https://movie.douban.com/celebrity/1049485/',
		'https://movie.douban.com/subject/26599625/all_photos',
		'https://movie.douban.com/subject/26599625/photos?type=S',

		'https://movie.douban.com/subject/1292052/',
		'https://movie.douban.com/tag/2015',
		'https://movie.douban.com/subject/5327268/',
		'https://movie.douban.com/subject/25954475/',
		'https://movie.douban.com/subject/26581464/',
		'https://movie.douban.com/subject/26307755/',
		'https://movie.douban.com/subject/26310143/',
		'https://movie.douban.com/subject/26591654/',
		'https://movie.douban.com/subject/1292275/',
		'https://movie.douban.com/subject/3602084/',
		'https://movie.douban.com/subject/25947154/',
		# 'https://movie.douban.com/tag/%E6%83%8A%E6%82%9A',
		# 'https://movie.douban.com/subject/3011051/',
		# 'https://movie.douban.com/subject/3011051/photos?type=S',
		# 'https://movie.douban.com/celebrity/1054442/',
		# 'https://movie.douban.com/celebrity/1054442/photos/',
		# 'https://movie.douban.com/subject/1307332/',
		# 'https://movie.douban.com/subject/1307332/photos?type=S',
	]

	rules = [
		Rule(LinkExtractor(allow=('/tag/$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+/?$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+\?start=\d+&type=T$')), follow=True),
		Rule(LinkExtractor(allow=('/subject/\d+/\?from=subject-page$')), follow=True, callback='parse_movie'),
		Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/$')), callback='parse_movie'),

		Rule(LinkExtractor(allow=('/subject/\d+/all_photos$')), follow=True),
		Rule(LinkExtractor(allow=('/subject/\d+/photos$')), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=('/subject/\d+/photos\?type=S$')), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=('/subject/\d+/photos\?type=S&start=\d+&sortby=vote&size=a&subtype=a$')), follow=True, callback='parse_image'),

		# Rule(LinkExtractor(allow=('/celebrity/\d+/?$')), follow=True, callback='parse_actor'),
		# Rule(LinkExtractor(allow=('/celebrity/\d+/\?from=showing$')), follow=True, callback='parse_actor'),
		# Rule(LinkExtractor(allow=('/celebrity/\d+/photos/$')), follow=True, callback='parse_photo'),
		# Rule(LinkExtractor(allow=('/celebrity/\d+/photos\?type=C&start=\d+&sortby=vote&size=a&subtype=a$')), follow=True, callback='parse_photo'),

		# Rule(LinkExtractor(allow=('/celebrity/\d+/\movies\?sortby=time&format=pic&')), follow=True),
		# Rule(LinkExtractor(allow=('/celebrity/\d+/\movies\?start=\d+&format=pic&sortby=time&')), follow=True),
	]
	
	def parse_movie(self, response):
		x = Selector(response)
		
		item = MovieItem()
		item['typ'] = 'movie'
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
		if response.url[-1] == 'e':
			#response.url = https://movie.douban.com/subject/26582012/?from=subject-page
			return response.url.split('/')[-2]
		else:
			#response.url = https://movie.douban.com/subject/26582012/
			if response.url[-1] == '/':
				return response.url.split('/')[-2]
			else:
				return response.url.split('/')[-1]

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
		arr = response.xpath(u'//span[contains(text(),"语言")]/parent::*').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"语言")]/parent::*').extract()[0]
			language_pos = parent_text.find(u'语言')
			if language_pos == -1:
				return u''
			right_text = parent_text[language_pos:]
			brace_pos = right_text.find('>')
			br_pos = right_text.find('<br>')
			languages  = right_text[brace_pos+1:br_pos].strip()
			return ','.join([s.strip() for s in languages.split('/')])
		else:
			return u''

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

	def parse_image(self, response):
		mid = response.url.split('/')[4]
		urls = response.xpath("//div[@class='cover']/a/img/@src").extract()
		for url in urls:
			i = ImageItem()
			i['typ'] = 'image'
			i['mid'] = mid
			i['url'] = url.replace('thumb','photo')
			yield i

	def parse_photo(self, response):
		mid = response.url.split('/')[4]
		urls = response.xpath("//div[@class='cover']/a/img/@src").extract()
		for url in urls:
			i = ImageItem()
			i['typ'] = 'photo'
			i['mid'] = mid
			i['url'] = url.replace('thumb','photo')
			yield i

	############################################
	# Actor
	############################################
	def parse_actor(self, response):
		item = ActorItem()
		item['typ'] = 'actor'
		item['aid'] = self.get_aid(response)
		item['name'] = self.get_actor_name(response)
		item['gender'] = self.get_gender(response)
		item['constellation'] = self.get_constellation(response)
		item['birthday'] = self.get_birthday(response)
		item['birthplace'] = self.get_birthplace(response)
		item['profession'] = self.get_profession(response)
		item['imdb'] = self.get_imdb(response)
		item['family'] = self.get_family(response)
		item['fname'] = self.get_fname(response)
		item['cname'] = self.get_cname(response)

		yield item

	def get_aid(self, response):
		if response.url[-1] == 'g':
			#response.url = https://movie.douban.com/celebrity/1049485/?from=showing
			return response.url.split('/')[-2]
		else:
			#response.url = https://movie.douban.com/celebrity/1049485/
			if response.url[-1] == '/':
				return response.url.split('/')[-2]
			else:
				return response.url.split('/')[-1]

	def get_actor_name(self, response):
		return response.xpath('//div[@id="content"]/h1/text()').extract()[0]

	def get_gender(self, response):
		arr = response.xpath(u'//span[contains(text(),"性别")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"性别")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u'F'
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			gender = right_text[n_pos+1:brace_pos].strip()
			return u'F' if gender == u'女' else u'M'
		else:
			return u'F'

	def get_constellation(self, response):
		arr = response.xpath(u'//span[contains(text(),"星座")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"星座")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			return right_text[n_pos+1:brace_pos].strip()
		else:
			return u''

	def get_birthday(self, response):
		arr = response.xpath(u'//span[contains(text(),"出生日期")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"出生日期")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			return right_text[n_pos+1:brace_pos].strip()
		else:
			return u''

	def get_birthplace(self, response):
		arr = response.xpath(u'//span[contains(text(),"出生地")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"出生地")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			return right_text[n_pos+1:brace_pos].strip()
		else:
			return u''

	def get_profession(self, response):
		arr = response.xpath(u'//span[contains(text(),"职业")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"职业")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			text = right_text[n_pos+1:brace_pos].strip()
			return text.replace(' / ' , ',')
		else:
			return u''

	def get_imdb(self, response):
		arr = response.xpath(u'//span[contains(text(),"imdb编号")]/following-sibling::a').extract()
		if any(arr):
			imdb_link = response.xpath(u'//span[contains(text(),"imdb编号")]/following-sibling::a/@href').extract()
			imdb = response.xpath(u'//span[contains(text(),"imdb编号")]/following-sibling::a/text()').extract()
			return imdb
		else:
			return u''
        
	def get_family(self, response):
		arr = response.xpath(u'//span[contains(text(),"家庭成员")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"家庭成员")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			return right_text[n_pos+1:brace_pos].strip()
		else:
			return u''

	def get_fname(self, response):
		arr = response.xpath(u'//span[contains(text(),"更多外文名")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"更多外文名")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			text = right_text[n_pos+1:brace_pos].strip()
			return text.replace(' / ' , ',')
		else:
			return u''

	def get_cname(self, response):
		arr = response.xpath(u'//span[contains(text(),"更多中文名")]/text()').extract()
		if any(arr):
			parent_text = response.xpath(u'//span[contains(text(),"更多中文名")]/parent::*').extract()[0]
			comma_pos = parent_text.find(u": ")
			if comma_pos == -1:
				return u''
			right_text = parent_text[comma_pos+1:]
			n_pos = right_text.find('\n')
			brace_pos = right_text.find('<')
			text = right_text[n_pos+1:brace_pos].strip()
			return text.replace(' / ' , ',')
		else:
			return u''
