import scrapy
from pyquery import PyQuery as pq
import datetime
import re
from scrapy.http.request import Request

from crawlers.items import MancheteItem

RE = re.compile('.*page=(\d+)')

class R7Spider(scrapy.Spider):
	name = "r7"
	allowed_domains = ["r7.com"]
	start_urls = [
		'http://noticias.r7.com/jornal-da-record/noticias?page=123'
	]

	def parse(self, response):
		url = response.url

		page = 1
		m = RE.match(url)
		if m:
			page = int(m.group(1))

		date_holders = response.css('#article').css('.nwl-wrapper')

		begin = datetime.datetime(2014, 12, 01)
		end = datetime.datetime(2015, 2, 28)

		oldest_news_seen = datetime.datetime.now()

		for date_holder in date_holders:
			date1 = date_holder.xpath('h6/text()')[0].extract()
			date = datetime.datetime.strptime(date1, '%d/%m/%Y')

			if date < oldest_news_seen:
				oldest_news_seen = date

			if begin <= date and date <= end:
				noticias = date_holder.xpath('ul/li')

				for noticia in noticias:
					link = noticia.css('span.nwl-info')[0].xpath('p[1]/a[1]/@href')[0].extract().strip()
					title = noticia.css('span.nwl-info')[0].xpath('p[1]/a[1]/@title')[0].extract().strip()
					manchete = MancheteItem()
					manchete['url'] = link.strip().encode('utf8')
					manchete['title'] = title.strip().\
						replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
					manchete['date'] = date
					yield manchete

			if oldest_news_seen > begin:
				new_url = 'http://noticias.r7.com/jornal-da-record/noticias?page=' + str(page + 1)
				yield Request(new_url, meta={},callback=self.parse)



