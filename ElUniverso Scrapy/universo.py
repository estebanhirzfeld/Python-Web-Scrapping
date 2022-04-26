from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class ElUniverso(Item):
    title = Field()
    description = Field()
    id = Field()

class UniversoSpider(Spider):
    name = 'universo'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes/']

    def parse(self, response):
        news_container = Selector(response)

        news = news_container.xpath('//div[@class="content-feed | space-y-2 "]//ul[@class="feed | divide-y relative  "]//li[@class="relative"]')
        id = 0
        for new in news:
            item = ItemLoader(ElUniverso(), new)

            item.add_xpath('title', './/div//div//h2//a//text()')
            item.add_xpath('description', './/div//div//p//text()')

            item.add_value('id',id)
            id += 1

            yield item.load_item()
