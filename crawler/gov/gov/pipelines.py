import os

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

from crawler.gov.gov.items import PdfItem
from pdfparser.tasks import process_pdf_link


class RenamePdfFilesPipeline(FilesPipeline):
    def item_completed(self, results, item: PdfItem, info):
        success, data = results[0]
        if success:
            old_path = os.path.join('pdfs', data['path'])
            if os.path.exists(old_path):
                new_path = item.save_path()
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                os.rename(old_path, new_path)
            return item
        else:
            raise DropItem(f"Error while downloading item: {data}")


class DropDuplicatesPipeline:
    def process_item(self, item: PdfItem, spider):
        # TODO: Instead of checking on local FS, we should check if pdf with given url is in database
        if os.path.exists(item.save_path()):
            raise DropItem(f"Item {item['file_urls'][0]} is already saved under path: {(item.save_path())}")
        else:
            return item


class CreateProcessPdfTaskPipeline:
    def process_item(self, item: PdfItem, spider):
        for url in item['file_urls']:
            process_pdf_link.delay(url)
