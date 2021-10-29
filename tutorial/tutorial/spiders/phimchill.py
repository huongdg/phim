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
    name = "phimchill"

    def start_requests(self):
        urls = [

            "https://phimchill.tv/genre/phim-hanh-dong/page-",
            "https://phimchill.tv/genre/phim-tinh-cam/page-",
            "https://phimchill.tv/genre/phim-hai-huoc/page-",
            "https://phimchill.tv/genre/phim-co-trang/page-",
            "https://phimchill.tv/genre/phim-tam-ly/page-",
            "https://phimchill.tv/genre/phim-hinh-su/page-",
            "https://phimchill.tv/genre/phim-chien-tranh/page-",
            "https://phimchill.tv/genre/game-show/page-",
            "https://phimchill.tv/genre/phim-the-thao/page-",
            "https://phimchill.tv/genre/phim-chieu-rap/page-",
            "https://phimchill.tv/genre/phim-sap-chieu/page-",
            "https://phimchill.tv/genre/phim-vo-thuat/page-",
            "https://phimchill.tv/genre/phim-hoat-hinh/page-",
            "https://phimchill.tv/genre/phim-vien-tuong/page-",
            "https://phimchill.tv/genre/phim-phieu-luu/page-",
            "https://phimchill.tv/genre/phim-khoa-hoc/page-",
            "https://phimchill.tv/genre/phim-ma-kinh-di/page-",
            "https://phimchill.tv/genre/phim-am-nhac/page-",
            "https://phimchill.tv/genre/phim-than-thoai/page-",
            "https://phimchill.tv/genre/phim-truyen-hinh/page-",
            "https://phimchill.tv/genre/phim-anime/page-",
            "https://phimchill.tv/genre/phim-thuyet-minh/page-"

        ]

        # urls = ["https://phimchill.tv/country/phim-trung-quoc/page-{}/".format(i + 1) for i in range(1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_list_page)


    def get_list_page(self, response):
        for i in range(100):
            loaiphim = response.xpath('//div[@class="heading"]/h1//text()').extract_first()
            # print(loaiphim)
            # url = response.url.format(i + 1)
            yield scrapy.Request(response.url + str(i+1), self.get_list, meta = {"loaiphim" : loaiphim})


    def get_list(self, response):
        try:
            links = response.xpath('//ul[@class = "list-film horizontal"]/li/a/@href').extract()
            # print(links)
            for link in links:
                yield scrapy.Request(link, self.get_data, meta = response.meta)
                # break
        except:
            pass


    def get_data(self, response):
        item = PhimItem()
        divs = response.xpath('//div[@class="film-info"]')
        name_vi = divs.xpath('.//div[@class="image"]/div[@class="text"]/h1//text()').extract_first().lower()

        name_en = " ".join(response.xpath('.//div[@class="image"]/div[@class="text"]/h2//text()').extract_first().lower().split()[:-1])

        # print(name_vi , "-", name_en)


        loaiphim = response.meta["loaiphim"]
        # print(loaiphim)
        infos = response.xpath('//ul[@class="entry-meta block-film"]//text()').extract()
        infos = [re.sub(r'(\s\s+)|(\n)|(, )', '', i) for i in infos]
        infos = [i for i in infos if i != '']

        id_year = infos.index('Năm Phát Hành: ') + 2
        year = "" if infos[id_year] in ['Quốc gia: '] else infos[id_year]
        id_quocgia = infos.index('Quốc gia: ') + 2
        quocgia = "" if infos[id_quocgia] in [ 'Thể loại: '] else infos[id_quocgia]
        id_daodien = infos.index( 'Đạo diễn: ') + 3
        daodien = "" if infos[id_daodien ] in ['Diễn viên: '] else infos[id_daodien]
        id_dienvien = infos.index('Diễn viên: ') + 2
        id_thoiluong = infos.index('Thời lượng: ')
        ls_dv = ",".join(infos[id_dienvien:id_thoiluong])
        dienvien = "" if ls_dv in [ 'Thời lượng: '] else ls_dv
        id_theloai = infos.index('Thể loại: ') + 2
        ls_theloai = ",".join(infos[id_theloai:id_daodien -3 ])
        theloai = "" if ls_theloai in ['Đạo diễn: '] else ls_theloai

        item['loaiphim'] = loaiphim
        item['name_vi'] = name_vi
        item['name_en'] = name_en
        item['nam_phathanh'] = year
        item['dienvien'] = dienvien
        item['daodien'] = daodien
        item['quocgia'] = quocgia
        item['theloai'] = theloai
        yield item