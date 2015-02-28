# Spider for crawling links relevant to Desalination, starting at the Wikipedia desalination page, and making
#   this output available in a format that IBM Watson can consume
#
# The Wikipedia desalination page contains three types of links: internal, external, and PDF files
# I'm going to start with the internal links, expand to extern, then (hopefully) grab and parse PDFs
#
# Effectively parsing PDFs appears to require a pipeline, a more complex way of managing spiders
# I'm not going to mess with pipelines for this initial project, so I'll keep the scope of this spider to Wikipedia
#
# Author: Brian Creeden

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.conf import settings

class DesalinationSpider(CrawlSpider):
    name = 'desalination'
    start_urls = ["http://en.wikipedia.org/wiki/Desalination"]
    allowed_domains = ['en.wikipedia.com']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//body')), follow=True, callback='parse_html')
    )

    def __init__(self, *args, **kwargs):
        settings.overrides['DEPTH_LIMIT'] = 1
        super(DesalinationSpider, self).__init__(*args, **kwargs)

    def parse_html(self, response):
        sel = Selector(response)
        with open(sel.xpath("//h1[@id='firstHeading']").extract(), 'w') as f:
            f.write(response.body)