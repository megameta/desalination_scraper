# Spider for crawling links relevant to Desalination, starting at the Wikipedia desalination
# and Salt Gland pages, and making this output available in a format that IBM Watson can consume.
#
# These Wikipedia pages contain three types of links: internal, external, and PDF files
# I'm going to start with the internal links, expand to external, then (hopefully) grab and parse PDFs
#
# Effectively parsing PDFs appears to require a pipeline, a more complex way of managing spiders
# I'm not going to mess with pipelines for this initial project, so I'll keep the scope of this spider to Wikipedia
#
# Author: Brian Creeden

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.conf import settings

import os

class DesalinationSpider(CrawlSpider):
    name = 'desalination'
    start_urls = ["http://en.wikipedia.org/wiki/Desalination", "http://en.wikipedia.org/wiki/Salt_gland"]
    allowed_domains = ["en.wikipedia.org"]

    rules = [
        Rule(LinkExtractor(allow='en.wikipedia.org\/wiki'), callback='parse_html')
    ]

    def __init__(self, *args, **kwargs):
        settings.set('DEPTH_LIMIT', 2)
        #settings.set('DOWNLOAD_DELAY', 2)
        settings.set('COOKIES_ENABLED', False)
        super(DesalinationSpider, self).__init__(*args, **kwargs)

    def parse_html(self, response):
        sel = Selector(response)
        filename = sel.xpath('//title/text()').extract()[0]
        file = open(filename + '.html', 'w')
        file.write(response.body)