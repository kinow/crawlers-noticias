import scrapy
import datetime
from scrapy.http.request import Request

from crawlers.items import MancheteItem

class EureporterSpider(scrapy.Spider):
    name = "eureporter"
    allowed_domains = ["globo.com"]
    start_urls = [
        'http://oglobo.globo.com/eu-reporter/ex-prestador-de-servico-usa-carro-da-prefeitura-irregularmente-obstrui-garagem-no-meier-15455470'
    ]

    def parse(self, response):
        url = response.url

        begin = datetime.datetime(2014, 12, 01)
        end = datetime.datetime(2015, 2, 28)

        link = response.url
        title = response.css('.head-materia').xpath('h1/text()')[0].extract()
        date = response.xpath('//time/@datetime')[0].extract()

        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        date = date.replace(hour=00, minute=00, second=00)

        if begin <= date and date <= end:
            manchete = MancheteItem()
            manchete['url'] = link.strip().encode('utf8')
            manchete['title'] = title.strip().\
                replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
            manchete['date'] = date
            yield manchete

        if date > begin:
            new_url = response.css('.mais-antiga > a').xpath('@href')[0].extract().strip()
            yield Request(new_url, meta={},callback=self.parse)





