import scrapy
from pyquery import PyQuery as pq
import datetime
import re
from scrapy.http.request import Request

from crawlers.items import MancheteItem

RE = re.compile('.*Pagina=(\d+)')

class SBTSpider(scrapy.Spider):
    name = "sbt"
    allowed_domains = ["sbt.com.br"]
    start_urls = [
        'http://www.sbt.com.br/jornalismo/noticias/noticias_todas.asp?Pagina=512'
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        # http://g1.globo.com/jornal-nacional/noticia/

        url = response.url

        page = 1
        m = RE.match(url)
        if m:
            page = int(m.group(1))

        noticias = response.css('.BoxNoticias')[0].xpath('ul/li')

        begin = datetime.datetime(2014, 12, 01)
        end = datetime.datetime(2015, 2, 28)

        oldest_news_seen = datetime.datetime.now()

        for noticia in noticias:
            link = 'http://www.sbt.com.br' + noticia.xpath('a/@href')[0].extract()
            title = noticia.xpath('a/h4/text()').extract()[0].strip()
            date = noticia.xpath('a/h4/span/text()')[0].extract()

            date = datetime.datetime.strptime(date, '%d/%m/%Y')

            if date < oldest_news_seen:
                oldest_news_seen = date

            if begin <= date and date <= end:
                manchete = MancheteItem()
                manchete['url'] = link.strip().encode('utf8')
                manchete['title'] = title.strip().\
                    replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
                manchete['date'] = date
                yield manchete

            if oldest_news_seen > begin:
                new_url = 'http://www.sbt.com.br/jornalismo/noticias/noticias_todas.asp?Pagina=' + str(page + 1)
                yield Request(new_url, meta={},callback=self.parse)



