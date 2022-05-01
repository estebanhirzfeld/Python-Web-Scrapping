from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from tables import Description


class UrbaniaItem(Item):
    title = Field()
    description = Field()


class UrbaniaCrawler(CrawlSpider):
    name = 'urbania'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 24
    }

    start_urls = ['https://urbania.pe/buscar/venta-de-casas', 'https://urbania.pe/buscar/venta-de-casas?page=2', 'https://urbania.pe/buscar/venta-de-casas?page=3', 'https://urbania.pe/buscar/venta-de-casas?page=4', 'https://urbania.pe/buscar/venta-de-casas?page=5', 'https://urbania.pe/buscar/venta-de-casas?page=6', 'https://urbania.pe/buscar/venta-de-casas?page=7', 'https://urbania.pe/buscar/venta-de-casas?page=8', 'https://urbania.pe/buscar/venta-de-casas?page=9']

    allowed_domains = ['urbania.pe']

    download_delay = 5

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/inmueble/',
            ), follow=True, callback='parse_item'
        ),
    )


def parse_item(self, response):
    sel = Selector(response)
    item = ItemLoader(UrbaniaItem(), sel)

    # title = response.selector.xpath      ('//h1[@class="title"]/text()').get()
    # description = response.selector.xpath('//div[@id="longDescription"]/div/text()').get()

    item.add_xpath('title, ','//h1[@class="title"]/text()')
    item.add_xpath('description, ','//div[@id="longDescription"]/div/text()')

    yield item.load_item()

