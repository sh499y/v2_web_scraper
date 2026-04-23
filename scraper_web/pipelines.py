# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.core.downloader.handlers import http
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse

class NazwaProjektuPipeline:
    def process_item(self, item, spider):
        return item

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        page_url = item.get('page', '')

        domain = urlparse(page_url).netloc

        folder_name = domain.replace('.', '_').replace(':', '_')

        image_name = request.url.split('/')[-1]

        return f'{folder_name}/{image_name}'