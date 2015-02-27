from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

class PageItem(Item):
    depth = Field()
    title = Field()
    format = Field()

class DesalinationSpider(CrawlSpider):
    name = 'desalination'
    start_urls = [
        "http://en.wikipedia.org/wiki/Desalination"
    ]
    rules = (Rule (SgmlLinkExtractor()))

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select()
        item = scrapy.Item()
        item['id'] = response.xpath()