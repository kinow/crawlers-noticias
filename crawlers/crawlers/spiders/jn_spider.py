import scrapy
from pyquery import PyQuery as pq
import datetime

from crawlers.items import MancheteItem

class JNSpider(scrapy.Spider):
    name = "jn"
    allowed_domains = ["globo.com"]
    start_urls = [
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/01.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/02.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/03.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/04.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/05.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/06.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/07.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/08.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/09.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/10.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/11.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/12.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/13.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/14.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/15.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/16.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/17.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/18.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/19.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/20.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/21.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/22.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/23.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/24.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/25.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/26.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/27.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/28.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/29.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/30.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2014/12/31.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/01.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/02.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/03.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/04.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/05.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/06.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/07.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/08.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/09.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/10.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/11.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/12.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/13.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/14.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/15.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/16.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/17.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/18.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/19.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/20.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/21.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/22.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/23.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/24.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/25.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/26.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/27.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/28.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/29.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/30.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/01/31.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/01.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/02.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/03.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/04.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/05.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/06.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/07.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/08.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/09.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/10.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/11.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/12.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/13.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/14.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/15.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/16.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/17.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/18.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/19.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/20.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/21.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/22.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/23.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/24.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/25.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/26.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/27.html',
        'http://g1.globo.com/jornal-nacional/edicoes/2015/02/28.html',
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        # http://g1.globo.com/jornal-nacional/noticia/

        url = response.url
        date = url.split('/')
        root_date = ''+date[-3]+'/'+date[-2]
        date = ''+date[-3]+'/'+date[-2]+'/'+date[-1].split('.')[0]
        self.log('Date: ' + date)

        date = datetime.datetime.strptime(date, '%Y/%m/%d')

        links = response.selector.xpath('//a')
        visited = set()
        items = []
        for link in links:
            anchor = link.xpath('@href')
            if len(anchor) == 1:
                if link.xpath('@href').extract()[0].startswith('http://g1.globo.com/jornal-nacional/noticia/' + root_date):
                    doc = pq(response.body_as_unicode())
                    url = link.xpath('@href').extract()[0]
                    if url not in visited and len(link.xpath('h3/text()'))>0:
                        manchete = MancheteItem()
                        manchete['url'] = url.strip().encode('utf8')
                        manchete['title'] = link.xpath('h3/text()').extract()[0].strip().\
                            replace("\r\n", "").replace("\n", "").replace("\t", "").encode('utf8')
                        manchete['date'] = date
                        items.append(manchete)
                        visited.add(url)
        return items


