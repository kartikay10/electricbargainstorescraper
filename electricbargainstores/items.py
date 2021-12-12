# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from time import process_time
import scrapy


class ElectricbargainstoresItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name  = scrapy.Field()
    ProductCode  = scrapy.Field()
    Price  = scrapy.Field()
    TechSpecs  = scrapy.Field()
    ProductPhoto  = scrapy.Field()
    PhotoPath  = scrapy.Field()  
    PDFlink  = scrapy.Field()
    PDFPath  = scrapy.Field()
    Link  = scrapy.Field()
