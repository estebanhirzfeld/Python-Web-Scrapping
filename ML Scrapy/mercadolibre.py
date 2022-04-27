from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess # importar esto para ejecutarlo en codigo

class Articulo(Item):
    title= Field()
    price= Field()
    description= Field()
    url = Field()


class MercadoLibreSpider(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    allowed_domains = ['listado.mercadolibre.com.ar','celulares.mercadolibre.com.ar','mercadolibre.com.ar', 'articulo.mercadolibre.com.ar']
    start_urls = ['https://celulares.mercadolibre.com.ar', ]

    download_delay = 1

    rules = (

        # Pagitation
        Rule(
            LinkExtractor(
                allow=r'&page=',
            ), follow=True
        ),

        # Item Detail
        Rule(
            LinkExtractor(
                allow=r'type=product'
            ), follow=True, callback='parse_item'
        ),

    )

    def parse_item(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('title', '//h1[@class="ui-pdp-title"]//text()')
        item.add_xpath('price', '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]//span[@class="andes-visually-hidden"]/text()')
        item.add_xpath('description', '//p[@class="ui-pdp-description__content"]/text()')
        item.add_value('url', response.url)

        yield item.load_item()
