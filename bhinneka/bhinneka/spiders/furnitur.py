import scrapy
from ..items import BhinnekaItem

class FurniturSpider(scrapy.Spider):
    name = "furnitur"
    allowed_domains = ["bhinneka.com"]
    start_urls = ["https://bhinneka.com/jual-furniture/4lYAjEM"]

    def parse(self, response):

        products = response.css("div.o_wsale_product_grid_wrapper")

        for product in products:
            item = BhinnekaItem()

            item['nama_product'] = product.css("h6.o_wsale_products_item_title a::text").get()
            item['harga'] = product.css("span.oe_currency_value::text").get()
            item['cicilan'] = product.css("span.bmd-installment::text").get()

            yield item

        next_page = response.xpath('//*[@id="products_grid"]/div[5]/ul/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            next_page = response.xpath('//*[@id="products_grid"]/div[5]/ul/li[7]/a/@href').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
            else:
                pass
