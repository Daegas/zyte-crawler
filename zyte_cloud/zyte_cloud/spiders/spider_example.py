# myproject/spiders/example_spider.py
import json
from base64 import b64decode
import scrapy
from scrapy import Request, Spider

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['http://quotes.toscrape.com/']


    # pages
    # start_urls = [
    #     f"http://quotes.toscrape.com/api/quotes?page={n}" for n in range(1, 11)
    # ]


    def parse(self, response):
        # Extract the quotes from the page
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
