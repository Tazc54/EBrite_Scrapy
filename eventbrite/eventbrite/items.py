# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventbriteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    event_name = scrapy.Field()
    event_start_date = scrapy.Field()
    event_start_time = scrapy.Field()
    event_end_date = scrapy.Field()
    event_end_time = scrapy.Field()
    event_category = scrapy.Field()
    event_format = scrapy.Field()
    event_organizer = scrapy.Field()
    event_location = scrapy.Field()
    event_url = scrapy.Field()
    event_image = scrapy.Field()
    event_location_type = scrapy.Field()
    image_urls = scrapy.Field()
