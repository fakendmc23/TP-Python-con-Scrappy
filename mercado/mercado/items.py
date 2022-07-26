# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItemProducto(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    precio = scrapy.Field()
    categoria = scrapy.Field()
    image = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    fecha = scrapy.Field()
    es_item_especificaciones = scrapy.Field()
    # pass


class ItemEspecificaciones(scrapy.Item):
    # define the fields for your item here like:
    especificaciones = scrapy.Field()
    es_item_especificaciones = scrapy.Field()
    # pass
