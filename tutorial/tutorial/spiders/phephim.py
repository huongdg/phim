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
    # url = scrapy.Field()
    # imdb = scrapy.Field()

    pass



class QuotesSpider(scrapy.Spider):
    name = "phephim"

    def start_requests(self):
        # urls = [
        #
        #     # 'https://phephimm.net/film/filter?order=update&type=0&page={}'
        #     # 'https://phephimm.net/film/filter?order=update&type=1&page={}',
        #     'https://phephimm.net/danh-sach/phim-chieu-rap?page=1',
        #     'https://phephimm.net/danh-sach/phim-chieu-rap?page=2',
        #     'https://phephimm.net/danh-sach/phim-chieu-rap?page=3',
        #     'https://phephimm.net/danh-sach/phim-chieu-rap?page=4',
        #     'https://phephimm.net/danh-sach/phim-chieu-rap?page=5'
        # ]

        urls = ["https://phephimm.net/film/filter?order=update&type=1&page={}".format(i + 1) for i in range(150)] \
               + ["https://phephimm.net/film/filter?order=update&type=0&page={}".format(i + 1) for i in range(60)] \
               + ["https://phephimm.net/danh-sach/phim-chieu-rap?page={}".format(i + 1) for i in range(6)]


        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_list)


    def get_list_page(self, response):
        for i in range(150):
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
        try :
            name_en = response.xpath('//h2[@class="film-title-en"]//text()').extract_first().lower()
        except:
            name_en = ""

        loaiphim = response.xpath('//div[@class="box-body pre-scrollable"]/ul[1]/li[1]/a//text()').extract()
        loaiphim = [re.sub(r'(\s\s+)|(\n)|(, )', '', i) for i in loaiphim]
        loaiphim = [i for i in loaiphim if i != '']
        infos = response.xpath('//div[@class="box-body pre-scrollable"]/ul[2]//text()').extract()
        infos = [re.sub(r'(\s\s+)|(\n)|(, )', '', i) for i in infos]
        infos = [i for i in infos if i != '']
        #
        id_year = infos.index("Năm phát hành:")
        year = "" if infos[id_year+1] in ["Thời lượng mỗi tập:", "Đang cập nhật", "Đang Cập Nhật", "N/A"] else infos[id_year+1]
        id_quocgia = infos.index("Quốc gia:")
        quocgia = "" if infos[id_quocgia + 1] in ["Năm phát hành:", "Đang cập nhật", "Đang Cập Nhật", "N/A"] else infos[id_quocgia + 1]
        id_daodien = infos.index("Đạo diễn:")
        daodien = "" if infos[id_daodien + 1] in ["Diễn viên:", "Đang cập nhật", "Đang Cập Nhật", "N/A"] else infos[id_daodien + 1]
        id_dienvien = infos.index("Diễn viên:")
        ls_dv = ",".join(infos[id_dienvien + 1:id_quocgia])
        dienvien = "" if ls_dv in [ "Đang cập nhật", "Đang Cập Nhật", "N/A"] else ls_dv

        item['loaiphim'] = ""
        item['name_vi'] = name_vi
        item['name_en'] = name_en
        item['nam_phathanh'] = year
        item['dienvien'] = dienvien
        item['daodien'] = daodien
        item['quocgia'] = quocgia
        item['theloai'] = ",".join(loaiphim)
        yield item