import scrapy


class ProxycheckerSpider(scrapy.Spider):
    name = 'proxychecker'
    start_urls = ['https://www.cual-es-mi-ip.net/']

    def parse(self, response, **kwargs):
        ip = response.css('.big-text').css('::text').get()
        print(ip)
