import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

from crawler.gov.gov.items import PdfItem


class GovDuSpider(scrapy.Spider):
    name = 'govdu'
    start_urls = ['http://dziennikustaw.gov.pl/DU/rok/2020']
    allowed_domains = ['gov.pl']

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._link_extractor = LxmlLinkExtractor(allow_domains=['gov.pl'])

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_page_list)

    def parse_page_list(self, response):
        for link in self._link_extractor.extract_links(response):
            if '/DU/rok/2020/' in link.url:
                yield response.follow(link, callback=self.parse_filtered_list)

    def parse_filtered_list(self, response):
        for item in response.xpath('//tr[contains(td[3]/a/@href, "pdf")]'):
            # TODO: consider using "title" in filename
            title = item.xpath('td[2]/text()').get().strip()
            href = item.xpath('td[3]/a/@href').get()
            url = response.urljoin(href)
            date = item.xpath('td[4]/text()').get().strip()
            yield PdfItem(file_urls=[url], date=date)


class GovMpSpider(scrapy.Spider):
    name = 'govmp'
    start_urls = ['http://www.monitorpolski.gov.pl/MP/rok/2020']
    allowed_domains = ['gov.pl']

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._link_extractor = LxmlLinkExtractor(allow_domains=['gov.pl'])

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_page_list)

    def parse_page_list(self, response):
        for link in self._link_extractor.extract_links(response):
            if '/MP/rok/2020/' in link.url:
                yield response.follow(link, callback=self.parse_filtered_list)

    def parse_filtered_list(self, response):
        for item in response.xpath('//tr[contains(td[3]/a/@href, "pdf")]'):
            # TODO: consider using "title" in filename
            title = item.xpath('td[2]/text()').get().strip()
            href = item.xpath('td[3]/a/@href').get()
            url = response.urljoin(href)
            date = item.xpath('td[4]/text()').get().strip()
            yield PdfItem(file_urls=[url], date=date)


class GovCrawler(scrapy.spiders.CrawlSpider):
    name = 'gov'
    start_urls = ['http://gov.pl/']
    allowed_domains = ['gov.pl']
    rules = [
        Rule(LinkExtractor(deny=[r'http(s)?://(www\.)?sejm.gov.pl/Sejm8.nsf/transmisje_arch*'])),
        Rule(LinkExtractor(deny=[r'http(s)?://(www\.)?dziennikustaw.gov.pl/DU/(19|200|201)*'])),
        Rule(LinkExtractor(deny=[r'http(s)?://(www\.)?dziennikustaw.gov.pl/MP/(19|200|201)*']))
    ]

    def parse_start_url(self, response: Response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response: Response):
        if 'content-type' in response.headers and b'application/pdf' in response.headers['content-type']:
            yield PdfItem(file_urls=[response.url])
