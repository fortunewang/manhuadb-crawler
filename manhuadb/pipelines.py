# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline

class ManhuadbFilesPipeline(FilesPipeline):

    def process_item(self, item, spider):
        self.base_file_path = os.path.join(item['title'], item['page'])
        return super().process_item(item, spider)

    def file_path(self, request, response=None, info=None):
        base, ext = os.path.splitext(urlparse(request.url).path)
        return self.base_file_path + ext
