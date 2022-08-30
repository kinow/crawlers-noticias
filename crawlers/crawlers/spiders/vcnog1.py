import scrapy
import json
import datetime
from scrapy.http.request import Request

from crawlers.items import MancheteItem

class Vcnog1Spider(scrapy.Spider):
    name = "vcnog1"
    allowed_domains = ["globo.com"]
    start_urls = [
        'http://g1.globo.com/dynamo/plantao/vc-no-g1/1.json'
    ]

    def parse(self, response):
        url = response.url
        body = response.body_as_unicode()
        data = json.loads(body)

        begin = datetime.datetime(2014, 12, 1)
        end = datetime.datetime(2015, 2, 28)

        oldest_news_seen = datetime.datetime.now()

        for conteudo in data['conteudos']:
            link = conteudo['permalink']
            title = conteudo['titulo']
            date = conteudo['primeira_publicacao']

            #date = datetime.datetime.strptime(date, '%B %d, %Y %H:%M:%S')
            date = datetime.datetime.strptime(date, '%B %d, %Y %H:%M:%S')
            date = date.replace(hour=00, minute=00, second=00)

            if date < oldest_news_seen:
                oldest_news_seen = date

            if begin <= date and date <= end:
                manchete = MancheteItem()
                manchete['url'] = link.strip().encode('utf8')
                manchete['title'] = title.strip().replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
                manchete['date'] = date
                yield manchete

            if oldest_news_seen > begin:
                pagina_atual = data['paginaAtual']
                pagina = pagina_atual + 1
                new_url = 'http://g1.globo.com/dynamo/plantao/vc-no-g1/%s.json' % str(pagina)
                yield Request(new_url, meta={},callback=self.parse)
