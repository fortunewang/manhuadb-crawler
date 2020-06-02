# -*- coding: utf-8 -*-
import json
import scrapy

class MangadexSpider(scrapy.Spider):
    name = 'mangadex'
    allowed_domains = ['mangadex.org']
    start_urls = ['http://mangadex.org/']

    def start_requests(self):
        return [
            scrapy.Request(
                f'https://www.mangadex.org/api/?id={self.id}&type=manga',
                callback=self.parse_title
            )
        ]

    def parse_title(self, response):
        result = json.loads(response.body)
        filter_chapter = getattr(self, 'chapter', None)
        for chapter_id, chapter in result['chapter'].items():
            # volume = int(chapter['volume'])
            # title = chapter['title'] 
            chapter = chapter['chapter']
            if filter_chapter is not None and filter_chapter != chapter:
                continue
            yield scrapy.Request(
                f'https://www.mangadex.org/api/?id={chapter_id}&server=null&type=chapter',
                callback=self.parse_chapter_page,
                meta={'title': chapter}
            )

    def parse_chapter_page(self, response):
        result = json.loads(response.body)
        page_count = str(len(result['page_array']))
        page_template = f'{{:>0{len(page_count)}}}'
        for idx, file_name in enumerate(result['page_array']):
            img = result['server'] + result['hash'] + '/' + file_name
            yield {
                'title': response.meta['title'],
                'page': page_template.format(idx + 1),
                # used by: scrapy.pipelines.files.FilesPipeline
                'file_urls': [img],
            }
