#!/usr/bin/python

from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request,Response,FormRequest
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor

class ZhihuSpider(CrawlSpider):
	
	name = 'zhihu'
	allowed_domains = ["zhihu.com"]
	start_urls = [
		"http://www.zhihu.com"
#		"https://www.zhihu.com/explore"
#		"https://www.zhihu.com/topic"
	]

	rules = [
#		Rule(LinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
#		Rule(LinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
		Rule(LinkExtractor(allow = ('://www.zhihu.com/topic', )), callback = 'parse_page'),
#		Rule(LinkExtractor(allow = ('://www.zhihu.com/explore', )), callback = 'parse_page'),
	]

	headers = {
#		'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#		'Accept-Encoding:gzip, deflate, sdch, br',
#		'Accept-Language:zh-CN,zh;q=0.8',
#		'Referer:https://www.zhihu.com/',
#		'User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
	}

	

	def start_requests(self):
		return [
			Request('https://www.zhihu.com/login/email', meta={'cookiejar':1}, callback=self.post_login)
		]

	def post_login(self, response):
		print 'Preparing login'
		xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]

		return [
			FormRequest.from_response(
				response.replace(url="https://www.zhihu.com/login/email"),
#				url = 'https://www.zhihu.com/login/email',
				meta = {'cookiejar': response.meta['cookiejar']},
				headers = self.headers,
				formdata = {
					'_xsrf' : xsrf,
					'email' : 'marsprj@gmail.com',
					'password' : '0p(O8i&U'
				},
				callback = self.after_login,
				dont_filter = True
			)
		]

	def after_login(self, response):
		for url in self.start_urls:
			yield self.make_requests_from_url(url)

	def parse_page(self,response):
		print "************************************************************"
		print response.url
		print response.body
