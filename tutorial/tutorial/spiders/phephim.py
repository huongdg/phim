import scrapy
import re

class PhimItem(scrapy.Item):
    # define the fields for your item here like:
    name_vi = scrapy.Field()
    name_en = scrapy.Field()
    loaiphim = scrapy.Field()
    daodien = scrapy.Field()
    dienvien = scrapy.Field()
    quocgia = scrapy.Field()
    theloai = scrapy.Field()
    nam_phathanh = scrapy.Field()
    url = scrapy.Field()
    # imdb = scrapy.Field()

    pass



class QuotesSpider(scrapy.Spider):
    name = "phephim"

    def start_requests(self):
        urls = [

            'https://phephimm.net/film/filter?order=update&type=0&page={}'
            # 'https://phephimm.net/film/filter?order=update&type=1&page={}'
            # 'https://phephimm.net/danh-sach/phim-chieu-rap?page={}'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_list_page)


    def get_list_page(self, response):
        for i in range(5,10):
            # url = response.url.format(i + 1)
            yield scrapy.Request(response.url + str(i+1), self.get_list)


    def get_list(self, response):
        try:
            links = response.xpath('//a[@class="film-cover"]/@href').extract()
            # print(len(links))
            for link in links:
                yield scrapy.Request(link, self.get_data, meta={"url": response.url })
        except:
            pass


    def get_data(self, response):
        item = PhimItem()
        # divs = response.xpath('//div[@class="info"]')
        name_vi = response.xpath('//h1[@class="film-title"]/a//text()').extract_first().lower()
        name_en = response.xpath('//h2[@class="film-title-en"]//text()').extract_first().lower()

        loaiphim = response.xpath('//div[@class="box-body pre-scrollable"]/ul[1]/li[1]/a//text()').extract_first()
        infos = response.xpath('//div[@class="box-body pre-scrollable"]/ul[2]//text()').extract()
        infos = [re.sub(r'(\s\s+)|(\n)|(, )', '', i) for i in infos]
        infos = [i for i in infos if i != '']
        #
        id_year = infos.index("Năm phát hành:")
        year = infos[id_year+1]
        id_quocgia = infos.index("Quốc gia:")
        quocgia = infos[id_quocgia + 1]
        id_daodien = infos.index("Đạo diễn:")
        daodien = infos[id_daodien + 1]
        id_dienvien = infos.index("Diễn viên:")
        dienvien = "" if infos[id_dienvien + 1] in ["Diễn viên:", "Đang cập nhật"] else infos[id_dienvien + 1]

        item['loaiphim'] = loaiphim
        item['name_vi'] = name_vi
        item['name_en'] = name_en
        item['url'] = response.meta['url']
        item['nam_phathanh'] = year
        item['dienvien'] = dienvien
        item['daodien'] = daodien
        item['quocgia'] = quocgia
        item['theloai'] = ""
        yield item