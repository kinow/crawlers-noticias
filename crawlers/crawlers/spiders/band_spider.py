import scrapy
import datetime
import re
from scrapy.http.request import Request

from crawlers.items import MancheteItem

RE = re.compile('.*p=(\d+)')
MDC_RE = re.compile('.*(\d{4}\/\d{2}\/\d{2}).*')

class BandSpider(scrapy.Spider):
	name = "band"
	allowed_domains = ["band.uol.com.br"]
	start_urls = [
		'http://noticias.band.uol.com.br/jornaldaband/?p=17'
	]

	def parse(self, response):
		url = response.url

		page = 1
		m = RE.match(url)
		if m:
			page = int(m.group(1))

		noticias_holder = response.css('#box_lista_dia')

		begin = datetime.datetime(2014, 12, 01)
		end = datetime.datetime(2015, 2, 28)

		oldest_news_seen = datetime.datetime.now()

		###
		# Materia de Capa
		materia_de_capa = response.css('.titDestaque')
		if (len(materia_de_capa) > 0):
			materia_de_capa = materia_de_capa[0]
			materia_de_capa_link = materia_de_capa.xpath('a/@href').extract()[0]
			materia_de_capa_title = materia_de_capa.xpath('a/text()').extract()[0]
			m = MDC_RE.match(materia_de_capa_link)
			if m:
				materia_de_capa_date = m.group(1)
				materia_de_capa_date = datetime.datetime.strptime(materia_de_capa_date, '%Y/%m/%d')
				if begin <= materia_de_capa_date and materia_de_capa_date <= end:
					manchete = MancheteItem()
					manchete['url'] = materia_de_capa_link.strip().encode('utf8')
					manchete['title'] = materia_de_capa_title.strip().\
						replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
					manchete['date'] = materia_de_capa_date
					yield manchete

		###

		for noticia_holder in noticias_holder:
			date = noticia_holder.css('.titulo_box').xpath('h3/@title').extract()[0].strip().split(' ')[-1]
			date = datetime.datetime.strptime(date, '%d/%m/%Y')
		
			if date < oldest_news_seen:
				oldest_news_seen = date

			noticias = noticia_holder.css('ul > li')
			for noticia in noticias:
				link = noticia.xpath('p/*/a/@href').extract()[0]
				title = noticia.xpath('p/*/a/text()').extract()[0]

				if begin <= date and date <= end:
					manchete = MancheteItem()
					manchete['url'] = link.strip().encode('utf8')
					manchete['title'] = title.strip().\
						replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
					manchete['date'] = date
					yield manchete

			if oldest_news_seen > begin:
				new_url = 'http://noticias.band.uol.com.br/jornaldaband/?p=' + str(page + 1)
				yield Request(new_url, meta={},callback=self.parse)
