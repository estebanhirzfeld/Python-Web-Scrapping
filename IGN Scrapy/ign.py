from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
# importar esto para ejecutarlo en codigo
from scrapy.crawler import CrawlerProcess


class Review(Item):
    type = Field()
    title = Field()
    rank = Field()
    url = Field()


class Gallery(Item):
    type = Field()
    gallery_title = Field()
    list_title = Field()
    list_description = Field()
    url = Field()


class Video(Item):
    type = Field()
    title = Field()
    date = Field()
    url = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 30
    }
    start_urls = [
        'https://es.ign.com/se/?type=review&q=anime&order_by=-date']

    allowed_domains = ['es.ign.com']

    download_delay = 1

    rules = (
        # X Axis per Type
        Rule(
            LinkExtractor(
                allow = [r'type=' , r'model=gallery'],
            ), follow = True
        ),
        # X Axis per Page
        Rule(
            LinkExtractor(
                allow = r'&page=\d+',
            ), follow = True
        ),
        # Y Axis per Review
        Rule(
            LinkExtractor(
                allow = r'/review/',
            ), follow = True, callback='parse_review'
        ),
        # Y Axis per Gallery
        Rule(
            LinkExtractor(
                allow = r'/gallery/',
            ), follow = True, callback='parse_gallery'
        ),
        # Y Axis per Video
        Rule(
            LinkExtractor(
                allow = r'/video/',
            ), follow = True, callback='parse_video'
        ),
    )

    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_value('type', 'review')
        item.add_xpath('title', '//h1[@class="strong"]/text()')
        item.add_xpath('rank', '//div[@class="review"]//figure//div[@class="side-wrapper side-wrapper hexagon"]//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')
        item.add_value('url', response.url)

        yield item.load_item()

    def parse_gallery(self, response):
        item = ItemLoader(Gallery(), response)
        item.add_value('type', 'gallery')
        item.add_xpath('gallery_title', '//h1[@id="gallery_title"]/text()')
        item.add_value('url', response.url)

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_value('type', 'video')
        item.add_xpath('title', '//h1[@id="id_title"]/text()')
        item.add_xpath('date', '//span[@class="publish-date"]/text()')
        item.add_value('url', response.url)

        yield item.load_item()
