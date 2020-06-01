# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path
import scrapy
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline

class ManhuadbFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        title = request.meta['title']
        page = request.meta['page']
        base, ext = os.path.splitext(urlparse(request.url).path)
        return os.path.join(title, page + ext)

    def get_media_requests(self, item, info):
        meta = {
            'title': item['title'],
            'page': item['page'],
        }
        return [
            scrapy.Request(url, meta=meta)
            for url in item.get(self.files_urls_field, [])
        ]
