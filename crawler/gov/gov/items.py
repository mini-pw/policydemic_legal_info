import os

import scrapy


class PdfItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    date = scrapy.Field(serializer=str)

    def save_path(self):
        return os.path.join('files', self['date'], self['file_urls'][0].split('/')[-1])
