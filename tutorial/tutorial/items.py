# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TVHayItem(scrapy.Item):
    # define the fields for your item here like:
    name_vi = scrapy.Field()
    name_en = scrapy.Field()
    loaiphim = scrapy.Field()
    daodien = scrapy.Field()
    dienvien = scrapy.Field()
    quocgia = scrapy.Field()
    theloai = scrapy.Field()
    nam_phathanh = scrapy.Field()
    # imdb = scrapy.Field()

    pass

