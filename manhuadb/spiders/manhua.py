# -*- coding: utf-8 -*-
import scrapy

class ManhuaSpider(scrapy.Spider):
    name = 'manhua'
    allowed_domains = ['manhuadb.com']

    def start_requests(self):
        if getattr(self, 'id') is None:
            raise ValueError('id is not specified')
        return [
            scrapy.Request(
                f'https://www.manhuadb.com/manhua/{self.id}',
                callback=self.parse_title_page
            )
        ]

    def parse_title_page(self, response):
        self.title = response.css('h1.comic-title').css('::text').get()
        for link in response.css('ol.links-of-books > li > a'):
            yield response.follow(
                link,
                callback=self.parse_chapter_page,
                meta={'title': link.attrib['title']},
            )

    def parse_chapter_page(self, response):
        title = response.meta['title']
        page_count = response.css('div.d-none.vg-r-data').attrib['data-total']
        page_template = f'{{:>0{len(page_count)}}}'
        page_count = int(page_count)
        response.meta['page'] = page_template.format(1)
        yield from self.parse_page(response)
        for i in range(1, page_count):
            page = i + 1
            url = response.url.replace('.html', f'_p{page}.html')
            yield scrapy.Request(
                url,
                callback=self.parse_page,
                meta={'title': title, 'page': page_template.format(page)},
            )

    def parse_page(self, response):
        img = response.css('img.img-fluid.show-pic').attrib['src']
        yield {
            'title': response.meta['title'],
            'page': response.meta['page'],
            # used by: scrapy.pipelines.files.FilesPipeline
            'file_urls': [img],
        }
