# myproject/spiders/example_spider.py
import json
from base64 import b64decode
import scrapy
from scrapy import Request, Spider
import re

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['https://zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app/navigation']
    BASE_HOST = 'https://zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app/'


    def parse(self, response):
        # Extract the URLs from the page
        urls = response.xpath('//a//@href').getall()  # Use .getall() to get all URLs as a list of strings
        for url in urls:
            more_info_link = self.BASE_HOST.rstrip("/") + url  # Combine base URL with the relative link
            yield response.follow(more_info_link, callback=self.get_more_info, meta={"url": more_info_link})

    def get_more_info(self, response):
        decoded_response = response.body.decode('utf-8')
        product = None
        if re.search(r"www.ebay.com", decoded_response):
            print("parsing ebay")
            product = self.parse_ebay(response)
        elif re.search(r"amazon.com", decoded_response):
            print("parsing amazon")
            product = self.parse_amazon(response)
        elif re.search(r"bestbuy.com", decoded_response):
            print("parsing best")
            product = self.parse_bestbuy(response)
        elif re.search(r"homedepot.com", decoded_response):
            print("parsing home_depot")
            product = self.parse_home_depot(response)
        elif re.search(r"wayfair.com", decoded_response):
            print("parsing wayfair")
            product = self.parse_wayfair(response)
        
        if not product:
            print(response.meta["url"])
        else:
            yield product
    
    def parse_ebay(self, response):
        print("parsing ebay")
        # ebay
        name = response.xpath('//h1[@class="x-item-title__mainTitle"]//span//text()').get()
        # print(name)
        brand = response.xpath('//dl[contains(@class, "ux-labels-values--brand")]//dd//div//div//span//text()').get()
        # print(brand)
        sku = response.xpath('//div[@class="ux-layout-section ux-layout-section--itemId ux-layout-section--ALIGN-RIGHT"]//div//div//div/span[2]//text()').get()
        # print(sku)
        price = response.xpath('//div[@class="x-price-primary"]//span//text()').get()
        # print(price)
        rating = response.xpath('//span[@class="ux-summary__start--rating"]//text()').get()
        # print(rating)
        reviews = response.xpath('//span[@class="ux-summary__count"]//text()').get()
        reviews = re.sub(r"[^\d]", "", reviews)
        # print(reviews)
        return {
            'url': response.meta["url"],
            'name': name,
            'brand': brand,
            'sku': sku,
            'price': price,
            'rating': rating,
            'reviews': reviews
        }

    def parse_amazon(self, response):
        name = response.xpath('//h1[@id="title"]//span//text()').get().strip()
        # print(name)
        brand = response.xpath('//tr[contains(@class, "po-brand")]//td[2]//span//text()').get().strip()
        # print(brand)
        sku = response.xpath('//div[@id="imgTagWrapperId"]//img//@src').get().strip()
        sku = re.sub(r".*images/I/(.*?)\..*", r"\1", sku)
        # print(sku)
        price = response.xpath('//div[@class="a-section a-spacing-none aok-align-center aok-relative"]//span//text()').get().strip()
        # print(price)
        rating = response.xpath('//span[@data-hook="rating-out-of-text"]//text()').get().strip()
        rating = re.sub(r"\s out.*", "", rating)
        # print(rating)
        reviews = response.xpath('//span[@data-hook="total-review-count"]//text()').get().strip()
        reviews = re.sub(r"[^\d]", "", reviews)
        # print(reviews)
        return {
            'url': response.meta["url"],
            'name': name,
            'brand': brand,
            'sku': sku,
            'price': price,
            'rating': rating,
            'reviews': reviews
        }
        
    def parse_bestbuy(self, response):
        name = response.xpath('//h1[@class="heading-4 leading-6 font-500 "]//text()').get().strip()
        # print(name)
        brand = None
        sku = response.xpath('//div[contains(@class, "sku product-data")]//span[2]//text()').get().strip()
        # print(sku)
        price = response.xpath('//div[contains(@class, "priceView-customer-price")]//span//text()').get().strip()
        # print(price)
        user_rating = response.xpath('//div[contains(@class, "c-ratings-reviews")]//p//text()').get().strip()
        rating = re.sub(r".*?([\d\.]+) out .*", r"\1", user_rating)
        # print(rating)
        reviews = re.sub(r".*([\d]+) reviews", r"\1", user_rating)
        # print(reviews)
        return {
            'url': response.meta["url"],
            'name': name,
            'brand': brand,
            'sku': sku,
            'price': price,
            'rating': rating,
            'reviews': reviews
        }
    
    def parse_home_depot(self, response):
        name = response.xpath('//div[@class="product-details__badge-title--wrapper--vtpd5"]//span//h1//text()').get().strip()
        # print(name)
        brand = response.xpath('//h2[@class="sui-font-regular sui-text-base sui-tracking-normal sui-normal-case sui-line-clamp-unset sui-font-normal sui-text-primary"]//text()').get().strip()
        # print(brand)
        sku = response.xpath('//div[@class="sui-flex sui-text-xs sui-flex-wrap"]//div[3]//h2//span//text()').get().strip()
        # print(sku)
        script = response.xpath('//script[@id="thd-helmet__script--productStructureData"]//text()').get()
        price = None
        if script:
            data = json.loads(script)
            price = data.get('offers', {}).get('price', 'N/A')
        # print(price)
        rating = response.xpath('//span[@class="ugc-c-review-average font-weight-medium order-1"]//text()').get().strip()
        # print(rating)
        reviews = response.xpath('//span[@class="c-reviews order-2"]//text()').get().strip()
        reviews = re.sub(r"[^\d]", "", reviews)
        # print(reviews)
        return {
            'url': response.meta["url"],
            'name': name,
            'brand': brand,
            'sku': sku,
            'price': price,
            'rating': rating,
            'reviews': reviews
        }
        
    def parse_wayfair(self, response):
        name = response.xpath('//h1[@data-hb-id="Heading"]//text()').get().strip()
        print(name)
        brand = response.xpath('//span[@data-rtl-id="listingManufacturerByLineText"]//text()').get().strip()
        print(brand)
        sku = response.xpath('//ol[@class="sfhse63 sfhse61"]//li[5]//span//text()').get().strip()
        print(sku)
        price = response.xpath('//span[@data-test-id="PriceDisplay"]//text()').get()
        print(price)
        rating = response.xpath('//p[@data-rtl-id="reviewsHeaderReviewsAverage"]//text()').get().strip()
        print(rating)
        reviews = response.xpath('//span[@data-rtl-id="reviewsHeaderReviewsLink"]//text()').get().strip()
        reviews = re.sub(r"[^\d]", "", reviews)
        print(reviews)
        return {
            'url': response.meta["url"],
            'name': name,
            'brand': brand,
            'sku': sku,
            'price': price,
            'rating': rating,
            'reviews': reviews
        }
        
