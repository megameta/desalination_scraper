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
from scrapy.item import Item, Field

from nltk import clean_html

from docx import Document

class PageItem(Item):
    depth = Field()
    current_url = Field()
    format = Field()
    title = Field()
    body = Field()

class DesalinationSpider(CrawlSpider):
    name = 'desalination'
    start_urls = ["http://en.wikipedia.org/wiki/Desalination"]

    # pass responses to either parse_html or parse_pdf depending on whether URLs end in .html and .pdf

    rules = [
        Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_html'),
        Rule(SgmlLinkExtractor(allow=('\.pdf', )), callback='parse_pdf')
    ]

    def __init__(self, *args, **kwargs):
        super(DesalinationSpider, self).__init__(*args, **kwargs)

    def parse_html(self, response):
        sel = Selector(response)
        items = []
        item = PageItem()
        item['depth'] = response.meta['depth']
        item['current_url'] = response.url
        item['title'] = sel.xpath('//head/title/text()').extract()
        item['body'] = clean_html(sel.xpath('//body'))
        items.append(item)
        return items

    def parse_pdf(self, response):
        sel = Selector(response)