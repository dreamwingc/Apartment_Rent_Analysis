import scrapy
import re
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = []
        for i in range(0, 2500, 120):
            url = 'https://sfbay.craigslist.org/search/sby/apa?s=' + str(i)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('p.result-info'):
            link = quote.css('a::attr(href)').extract_first()
            subLink = link.split("/")
            usePart = subLink[-1].split(".")


            floor = quote.css('span.housing::text').extract_first()
            if floor:
                subFloor1 = floor.replace('\n', '')
                subFloor = subFloor1.replace(' ', '')

                if '-' in subFloor:
                    bed_sqr = subFloor.split('-')
                    bedrooms = bed_sqr[0]
                    sqrfeet = bed_sqr[1]
                else:
                    bedrooms = 0
                    sqrfeet = subFloor

            title = quote.css('a.result-title::text').extract_first()

            price = quote.css('span.result-price::text').extract_first()
            price = price.replace('$', '')

            location = quote.css('span.result-hood::text').extract_first()

            if location:
                location = location.replace('(', '')
                location = location.replace(')', '')

            # later may include
            # related_link = "https://sfbay.craigslist.org/sby/apa/" + usePart[0] + ".html"
            # yield scrapy.Request(url=related_link, callback=self.subparse)

            yield {
                'title': title,
                'price': price,
                'floor_plan': subFloor,
                'bedrooms': bedrooms,
                'square_feet': sqrfeet,
                'location': location,
                'related_link': "https://sfbay.craigslist.org/sby/apa/" + usePart[0] + ".html"
            }

    # later may include
    # def subparse(self, response):
    #     latitude = response.css('div').xpath('@data-latitude').extract()
    #     longitude = response.css('div').xpath('@data-longitude').extract()
    #
    #     yield {
    #         'latitude': latitude,
    #         'longitude': longitude
    #     }

