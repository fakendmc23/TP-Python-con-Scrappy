from scrapy.crawler import CrawlerProcess

from mercado.mercado.spiders.spider_mercado import SpiderMusimundo
from mercado.mercado.spiders.spider_mercado import SpiderGarbarino
from mercado.mercado.spiders.spider_mercado import SpiderAloise
from mercado.mercado.spiders.spider_mercado import SpiderRibeiro

from mercado.mercado.spiders.spider_mercado import SpiderNoblex
from mercado.mercado.spiders.spider_mercado import SpiderAtma
from mercado.mercado.spiders.spider_mercado import SpiderPhilco


class EntradaUsuario:

    def __init__(self):
        self.paginas_disponibles_para_buscar = []
        self.paginas_a_buscar = []
        self.producto_a_buscar = ""
        self.busqueda = ""
        self.dic_url_paginas_disponibles = {}
        self.buscar_especificaciones = ""
        self.busqueda_especificaciones = ""

    def construir_url(self, producto_a_buscar, separador):

        return separador.join(list(map(lambda x: x.lower(), producto_a_buscar.replace('"', " ").split())))

    def recibir_datos(self, diccionario):

        self.paginas_disponibles_para_buscar = diccionario["paginas_disponibles"]
        self.paginas_a_buscar = diccionario["paginas_a_buscar"]
        self.producto_a_buscar = diccionario["busqueda_usuario"]
        self.dic_url_paginas_disponibles = diccionario["url_paginas_disponibles"]
        self.buscar_especificaciones = diccionario["busqueda_especificaciones"]
        self.busqueda = self.construir_url(self.producto_a_buscar, "+")
        self.busqueda_especificaciones = self.construir_url(self.producto_a_buscar, "-")

    def comenzar_busqueda(self):

        process = CrawlerProcess(
            {'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
             'ITEM_PIPELINES': {'mercado.mercado.pipelines.ProductoPipeline': 300},
             'IMAGES_STORE': 'imagenes_scrapy'})

        dic_spiders = {'aloise': SpiderAloise,
                       'ribeiro': SpiderRibeiro,
                       'musimundo': SpiderMusimundo,
                       'garbarino': SpiderGarbarino,
                       'noblex': SpiderNoblex,
                       'atma': SpiderAtma,
                       'philco': SpiderPhilco}

        if self.buscar_especificaciones:
            process.crawl(dic_spiders["noblex"], start_urls=[self.dic_url_paginas_disponibles["noblex"].replace("frase_a_buscar", self.busqueda_especificaciones)])
            process.crawl(dic_spiders["atma"], start_urls=[self.dic_url_paginas_disponibles["atma"].replace("frase_a_buscar", self.busqueda_especificaciones)])
            process.crawl(dic_spiders["philco"], start_urls=[self.dic_url_paginas_disponibles["philco"].replace("frase_a_buscar", self.busqueda_especificaciones)])

        for pagina in self.paginas_a_buscar:
            if pagina in self.paginas_disponibles_para_buscar:
                spider = dic_spiders[pagina]
                url = self.dic_url_paginas_disponibles[pagina].replace("frase_a_buscar", self.busqueda)
                process.crawl(spider, start_urls=[url])

        process.start()
