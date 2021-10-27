import scrapy
import re

class MotPhimItem(scrapy.Item):
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



class QuotesSpider(scrapy.Spider):
    name = "phephim"

    def start_requests(self):
        urls = [

            'https://phephimm.net/film/filter?order=update&type=0&page={}'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_list_page)


    def get_list_page(self, response):
        for i in range(1):
            # url = response.url.format(i + 1)
            yield scrapy.Request(response.url + str(i+1), self.get_list)


    def get_list(self, response):
        try:
            divs = response.xpath('//a[@class="film-cover"]/@href').extract()
            print(divs)
            # for link in divs:
            #     yield scrapy.Request("https://motphimtv.com" + link, self.get_data, meta=response.meta)

        except:
            pass


    def get_data(self, response):
        item = MotPhimItem()
        divs = response.xpath('//div[@class="info"]')
        name_vi = divs.xpath('.//div[@class="text"]/h1/span//text()').extract_first().lower()
        # name_en = divs.xpath('.//div[@class="text"]/h2/span//text()').extract_first().lower()

        name_en = " ".join(divs.xpath('.//div[@class="text"]/h2/span//text()').extract_first().lower().split(" ")[:-1])

        # year = divs.xpath('.//div[@class="name2 fr"]/span[@class="year"]//text()').extract_first()[1:-1].lower()
        infos = divs.xpath('.//div[@class="dinfo"]//text()').extract()
        infos = [re.sub(r'(\s\s+)|(\n)|(, )', '', i) for i in infos]
        infos = [i for i in infos if i != '']

        id_year = infos.index("Năm sản xuất:")
        year = infos[id_year+1]
        try:
            id_daodien = infos.index("Đạo diễn:")
            daodien = infos[id_daodien + 1]
        except:
            daodien = ""
        id_quocgia = infos.index("Quốc gia:")
        quocgia = infos[id_quocgia + 1]
        id_theloai = infos.index("Thể loại:")
        try:
            id_dienvien = infos.index("Diễn viên:")
            theloai = ",".join(infos[id_theloai + 1:id_dienvien])
            dienvien = ",".join(infos[id_dienvien + 1:])
        except:
            dienvien  = ""
            theloai = ",".join(infos[id_theloai + 1:])


        item['loaiphim'] = response.meta['loaiphim']
        item['name_vi'] = name_vi
        item['name_en'] = name_en

        item['nam_phathanh'] = year
        item['dienvien'] = dienvien
        item['daodien'] = daodien
        item['quocgia'] = quocgia
        item['theloai'] = theloai
        yield item