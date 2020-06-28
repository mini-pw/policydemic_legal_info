import scrapy
import json

BASE_URL = 'https://covid19policywatch.org/'
SITE_NAME = 'COVID-19 Policy Watch'

class PolicyWatchSpider(scrapy.Spider):
    name = 'policywatch'
    start_urls = [
        BASE_URL,
    ]

    def parse(self, response):
        country_dropdown_list = response.xpath('//ul[@id="jump-menu-countries"]')
        anchors = country_dropdown_list.xpath('//li/a')
        yield from response.follow_all(anchors, callback=self.parse_country_subpage)

    def parse_country_subpage(self, response):
        movement_of_people_section = response.xpath('//*[@class="topic" and text()="Movement of people"]/parent::*/following-sibling::div[1]')
        details_links = movement_of_people_section.xpath('//div[contains(@class, "views-row")]//a/@href').getall()
        for link in details_links:
            yield scrapy.http.Request(url=f'{BASE_URL}colorbox{link}', method='POST', callback=self.parse_statement)
    
    def parse_statement(self, response):
        json_response = json.loads(response.text)
        data = next(elem for elem in json_response if 'method' in elem and elem['method'] == 'html')['data']
        selector = scrapy.selector.Selector(text=data)
        country_name = selector.css('div.field-name-field-country div.field-name-title::text').get()
        date_announced = selector.xpath('//div[contains(@class, "field-name-field-date-announced")]/*[@content]/@content').get()
        date_unified = None  
        if date_announced is not None:
            date_unified =  date_announced[:10]
        paragraphs = selector.xpath('//div[contains(@class, "field-name-field-policy-details")]/p/text()').getall() 
        textFormatted = "\n".join(paragraphs)
        entry = {
            'country': country_name,
            'info-date': date_unified,
            'original_text': textFormatted,
            'organization': SITE_NAME
        }
        yield entry