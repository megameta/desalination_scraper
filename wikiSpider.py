from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field

class PageItem(Item):
    session_id = Field()
    depth = Field()
    current_url = Field()
    referring_url = Field()
    title = Field()
    format = Field()

class DesalinationSpider(CrawlSpider):
    name = 'desalination'
    start_urls = ["http://en.wikipedia.org/wiki/Desalination"]
    rules = ( Rule (SgmlLinkExtractor(allow=("", ),),
                    callback="parse_items", follow= True),
    )

    def __init__(self, session_id=-1, *args, **kwargs):
        super(DesalinationSpider, self).__init__(*args, **kwargs)
        self.session_id = session_id

    def parse_items(self, response):
        sel = Selector(response)
        items = []
        item = PageItem()
        item['session_id'] = self.session_id
        item['depth'] = response.meta['depth']
        item['current_url'] = response.url
        referring_url = response.request.headers.get('Referer', None)
        item['referring_url'] = referring_url
        item['title'] = sel.xpath('').extract()
        items.append(item)
        return items