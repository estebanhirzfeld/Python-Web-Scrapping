from py import process
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import scrapy

repo_lenght = []

class GithubSpider(Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
        response,
        formdata = {
            "login": "username@mail.com",
            "password": "*********",
        }, callback=self.after_login
    )

    def after_login(self, response):
        request = scrapy.Request(
            url='http://github.com/estebanhirzfeld?tab=repositories',
            callback=self.parse_repositories
        )
        yield request

    def parse_repositories(self, response):
        selector = Selector(response)
        repos = selector.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repo in repos:
            repo_lenght.append(repo)

process = CrawlerProcess()
process.crawl(GithubSpider)
process.start()

print(len(repo_lenght))