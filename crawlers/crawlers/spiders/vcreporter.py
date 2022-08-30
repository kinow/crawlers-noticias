import scrapy
import json
import datetime
import re
from scrapy.http.request import Request
from pyquery import PyQuery as pq

from crawlers.items import MancheteItem

RE = re.compile('.*p=(\d+)')

class VcreporterSpider(scrapy.Spider):
    name = "vcreporter"
    allowed_domains = ["terra.com.br"]
    start_urls = [
        'http://vcreporter.terra.com.br/?html=2&ch=cc5f473cbc22b310VgnVCM20000099cceb0aRCRD&p=1&psz=60&cb=timeline_cb&sz=500&lomas=br.noticias.vcreporter&dflt=0&context=country=br,lang=pt,locale=pt-BR,channel=vcre,idItemMenu=vcre,countryLive=br,device=web,channelID=cc5f473cbc22b310VgnVCM20000099cceb0aRCRD,deliverFormat=json,tableSequence=11,tableSequenceContent=8,channelPath=Brasil.vc-reporter,tmgKey=br.news_vcreporter.home'
    ]

    def parse(self, response):
        url = response.url

        page = 1
        m = RE.match(url)
        if m:
            page = int(m.group(1))

        body = response.body_as_unicode()

        begin = datetime.datetime(2014, 12, 1)
        end = datetime.datetime(2015, 2, 28)

        oldest_news_seen = datetime.datetime.now()

        if url.index('timeline_cb') > 0:
            index1 = body.index('{"status": 200')
            if index1 > 0:
                temp = '"page": %s}' % str(page)
                index2 = body.index(temp , index1+1)

                if index2 > 0:
                    text = body[index1:index2+len(temp)]

                    j = json.loads(text)

                    cards = j['cards']
                    for card in cards:
                        items = card['items']
                        for item in items:
                            link = item['url']
                            if link == 'http://vcreporter.terra.com.br/':
                                # skip self marketing
                                pass
                            title = item['title']
                            if title is None or title == '':
                                # skip empty titles
                                pass
                            date = item['publishedDate']

                            if date.count(' ') > 1:
                                date = date[0:date.rfind(' ')]
                            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
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
                                pagina_atual = j['page']
                                pagina = pagina_atual + 1
                                new_url = 'http://vcreporter.terra.com.br/?html=2&ch=cc5f473cbc22b310VgnVCM20000099cceb0aRCRD&p=%s&psz=60&cb=timeline_cb&sz=240&lomas=br.noticias.vcreporter&dflt=0&context=country=br,lang=pt,locale=pt-BR,channel=vcre,idItemMenu=vcre,countryLive=br,device=web,channelID=cc5f473cbc22b310VgnVCM20000099cceb0aRCRD,deliverFormat=json,tableSequence=11,tableSequenceContent=8,channelPath=Brasil.vc-reporter,tmgKey=br.news_vcreporter.home' % str(pagina)
                                yield Request(new_url, meta={},callback=self.parse)
