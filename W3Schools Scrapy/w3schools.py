from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request


class W3Schools(Item):
    web_title = Field()
    iframe_title = Field()
    url = Field()


class W3SchoolsCrawler(Spider):
    name = 'w3schools'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'REDIRECT_ENABLED': True
    }
    allowed_domains = ['w3schools.com']

    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    download_delay = 1

    def parse(self, response):
        sel = Selector(response)

        # web_title = sel.xpath('//div[@id="main"]//h1/span/text()').get()
        web_title = sel.xpath('//div[@id="main"]/h1/text()').get() + sel.xpath('//div[@id="main"]//span/text()').get()
        meta_data = {'web_title': web_title, 'url': response.url}

        iframe_url = sel.xpath(
            '//div[@id="main"]//iframe[@width="99%"]/@src').get()
        iframe_url = 'https://www.w3schools.com/html/' + iframe_url


        yield Request(iframe_url, callback=self.parse_iframe, meta=meta_data)

    def parse_iframe(self, response):
        item = ItemLoader(W3Schools(), response)
        item.add_value("web_title", response.meta.get('web_title'))
        item.add_xpath('iframe_title', '//div[@id="main"]//h1/span/text()')
        item.add_value('url', response.meta.get('url'))

        yield item.load_item()
