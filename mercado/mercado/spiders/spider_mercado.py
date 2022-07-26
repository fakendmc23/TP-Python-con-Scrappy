import os
from pathlib import Path
import json
from datetime import datetime
import scrapy
import unidecode
from ..items import ItemProducto
from ..items import ItemEspecificaciones
from scrapy.http.request import Request


class Parser:

    def parse_producto(self, response, selector_nombre, selector_precio, selector_categoria, selector_imagen):
        try:
            nombre = response.css(selector_nombre+"::text").get()
            precio = response.css(selector_precio+"::text").get()
            categoria = response.css(selector_categoria+"::text").get()
            if "aloisetecno" in response.url:
                imagen = response.css(selector_imagen+"::attr(href)").get()
            else:
                imagen = response.css(selector_imagen).xpath("@src").get()
            url = response.url
            fecha = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

            objeto = ItemProducto()

            objeto['nombre'] = unidecode.unidecode(nombre.strip('\n'+' '+'\t'+'\r'+'"')).replace('"', "").replace('*', "")
            if "musimundo" in response.url:
                objeto['precio'] = unidecode.unidecode(precio.strip('$'+'\n'+' '+'\t'+'\r').replace(".", ""))[:-3]
            else:
                objeto['precio'] = unidecode.unidecode(precio.strip('$'+'\n'+' '+'\t'+'\r').replace(".", ""))
            objeto['categoria'] = unidecode.unidecode(categoria.strip('\n'+' '+'\t'+'\r'))
            objeto['image_urls'] = [response.urljoin(imagen)]
            objeto['url'] = url
            objeto['fecha'] = fecha
            objeto['es_item_especificaciones'] = False
            yield objeto

        except AttributeError:
            print("Se produjo un error al leer un dato del producto")

    def parse_especificaciones(self, response, dic_selectores):

        try:
            selector_titulos = dic_selectores["selector_titulos"]
            selector_valores = dic_selectores["selector_valores"]

            titulos = response.css(selector_nombre+"::text").getall()
            valores = response.css(selector_valor+"::text").getall()

            especificaciones = {c: v for c, v in zip(titulos, valores)}
            objeto = ItemEspecificaciones()
            objeto['especificaciones'] = especificaciones
            objeto['es_item_especificaciones'] = True

            yield objeto

        except AttributeError:
            print("Se produjo un error al leer un dato del producto")

    def avanzar_pagina(self, url):

        numero_pagina = []
        for x in range(len(url)-1, -1, -1):
            if url[x] == "=":
                break
            numero_pagina.insert(0, url[x])
        numero_siguiente = int("".join(numero_pagina))+1

        return url[:-len(numero_pagina)]+str(numero_siguiente), str(numero_siguiente)


class Configuraciones:

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.configuracion_garbarino = dict()
        self.configuracion_aloise = dict()
        self.configuracion_musimundo = dict()
        self.configuracion_ribeiro = dict()

        self.configuracion_noblex = dict()
        self.configuracion_atma = dict()
        self.configuracion_philco = dict()

        self.lista_dic_selectores_garbarino = dict()
        self.lista_dic_selectores_aloise = dict()
        self.lista_dic_selectores_musimundo = dict()
        self.lista_dic_selectores_ribeiro = dict()

        self.lista_dic_selectores_noblex = dict()
        self.lista_dic_selectores_atma = dict()
        self.lista_dic_selectores_philco = dict()

        self.leer_archivo_configuracion()

    def leer_archivo_configuracion(self):
        try:
            with open(self.ruta_archivo, "r") as archivo:
                datos = json.load(archivo)
                lista = datos['limite_paginas']
                claves_dic_selectores = ["selector_nombre", "selector_precio", "selector_categoria", "selector_imagen"]
                claves_dic_selectores_especificaciones = ["selector_titulos", "selector_valores"]
                claves_dic_proximas_paginas = ["selector_ultima_pagina", "selector_proximos_links"]
                self.configuracion_garbarino['DEPTH_LIMIT'] = lista[0]
                self.configuracion_garbarino['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_garbarino['IMAGES_STORE'] = "imagenes_scrapy"
                self.configuracion_aloise['DEPTH_LIMIT'] = lista[1]
                self.configuracion_aloise['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_aloise['IMAGES_STORE'] = "imagenes_scrapy"
                self.configuracion_musimundo['DEPTH_LIMIT'] = lista[2]
                self.configuracion_musimundo['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_musimundo['IMAGES_STORE'] = "imagenes_scrapy"
                self.configuracion_ribeiro['DEPTH_LIMIT'] = lista[3]
                self.configuracion_ribeiro['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_ribeiro['IMAGES_STORE'] = "imagenes_scrapy"

                self.configuracion_noblex['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_atma['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}
                self.configuracion_philco['ITEM_PIPELINES'] = {'mercado.mercado.pipelines.ProductoPipeline': 300}

                self.lista_dic_selectores_garbarino = [{c: datos["dic_selectores"]["garbarino"][c] for c in claves_dic_selectores},
                                                       {c: datos["dic_selectores"]["garbarino"][c] for c in claves_dic_proximas_paginas}]
                self.lista_dic_selectores_aloise = [{c: datos["dic_selectores"]["aloise"][c] for c in claves_dic_selectores},
                                                    {c: datos["dic_selectores"]["aloise"][c] for c in claves_dic_proximas_paginas}]
                self.lista_dic_selectores_musimundo = [{c: datos["dic_selectores"]["musimundo"][c] for c in claves_dic_selectores},
                                                       {c: datos["dic_selectores"]["musimundo"][c] for c in claves_dic_proximas_paginas}]
                self.lista_dic_selectores_ribeiro = [{c: datos["dic_selectores"]["ribeiro"][c] for c in claves_dic_selectores},
                                                     {c: datos["dic_selectores"]["ribeiro"][c] for c in claves_dic_proximas_paginas}]

                self.lista_dic_selectores_noblex = {c: datos["dic_selectores"]["noblex"][c] for c in claves_dic_selectores_especificaciones}
                self.lista_dic_selectores_atma = {c: datos["dic_selectores"]["atma"][c] for c in claves_dic_selectores_especificaciones}
                self.lista_dic_selectores_philco = {c: datos["dic_selectores"]["philco"][c] for c in claves_dic_selectores_especificaciones}

        except FileNotFoundError:
            print("No se encontro el archivo de configuracion, se completaran los datos por default")
            self.configuracion_garbarino['DEPTH_LIMIT'] = 1
            self.configuracion_aloise['DEPTH_LIMIT'] = 1
            self.configuracion_musimundo['DEPTH_LIMIT'] = 1
            self.configuracion_ribeiro['DEPTH_LIMIT'] = 1


configuraciones = Configuraciones(Path(os.getcwd()+'/cfg/cfg_programa.json'))


class SpiderNoblex(scrapy.Spider):
    name = 'noblex'
    custom_settings = configuraciones.configuracion_noblex

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_noblex

    def parse(self, response):

        try:
            selector_titulos = self.dic_selectores["selector_titulos"]
            selector_valores = self.dic_selectores["selector_valores"]

            titulos = response.css(selector_titulos+"::text").getall()
            valores = response.css(selector_valores+"::text").getall()

            especificaciones = {c: v for c, v in zip(titulos, valores)}
            objeto = ItemEspecificaciones()
            objeto['especificaciones'] = especificaciones
            objeto['es_item_especificaciones'] = True

            yield objeto

        except AttributeError:
            print("Se produjo un error al leer un dato del producto")


class SpiderAtma(scrapy.Spider):
    name = 'atma'
    custom_settings = configuraciones.configuracion_atma

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_atma

    def parse(self, response):

        try:
            selector_titulos = self.dic_selectores["selector_titulos"]
            selector_valores = self.dic_selectores["selector_valores"]

            titulos = response.css(selector_titulos+"::text").getall()
            valores = response.css(selector_valores+"::text").getall()

            especificaciones = {c: v for c, v in zip(titulos, valores)}
            objeto = ItemEspecificaciones()
            objeto['especificaciones'] = especificaciones
            objeto['es_item_especificaciones'] = True

            yield objeto

        except AttributeError:
            print("Se produjo un error al leer un dato del producto")


class SpiderPhilco(scrapy.Spider):
    name = 'philco'
    custom_settings = configuraciones.configuracion_philco

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_philco

    def parse(self, response):

        try:
            selector_titulos = self.dic_selectores["selector_titulos"]
            selector_valores = self.dic_selectores["selector_valores"]

            titulos = response.css(selector_titulos+"::text").getall()
            valores = response.css(selector_valores+"::text").getall()

            especificaciones = {c: v for c, v in zip(titulos, valores)}
            objeto = ItemEspecificaciones()
            objeto['especificaciones'] = especificaciones
            objeto['es_item_especificaciones'] = True

            yield objeto

        except AttributeError:
            print("Se produjo un error al leer un dato del producto")


class SpiderAloise(scrapy.Spider):

    name = 'aloise'
    custom_settings = configuraciones.configuracion_aloise

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_aloise[0]
        self.dic_ultimas_paginas = configuraciones.lista_dic_selectores_aloise[1]

    def parse(self, response):

        no_es_ultima_pagina = response.css(self.dic_ultimas_paginas["selector_ultima_pagina"]).get()

        lista_links_productos = response.css(self.dic_ultimas_paginas["selector_proximos_links"]).getall()

        if lista_links_productos:
            yield from response.follow_all(lista_links_productos,
                                           self.parser.parse_producto,
                                           cb_kwargs=self.dic_selectores)

        if no_es_ultima_pagina:
            yield scrapy.Request(response.urljoin(no_es_ultima_pagina), callback=self.parse)


class SpiderGarbarino(scrapy.Spider):

    name = 'garbarino'
    custom_settings = configuraciones.configuracion_garbarino

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_garbarino[0]
        self.dic_ultimas_paginas = configuraciones.lista_dic_selectores_garbarino[1]

    def parse(self, response):

        es_ultima_pagina = bool(response.css(self.dic_ultimas_paginas["selector_ultima_pagina"]).getall())

        lista_links_productos = list(map(lambda x: "https://www.garbarino.com"+x, response.xpath(self.dic_ultimas_paginas["selector_proximos_links"]).getall()))

        if lista_links_productos:
            yield from response.follow_all(lista_links_productos,
                                           self.parser.parse_producto,
                                           cb_kwargs=self.dic_selectores)

        if es_ultima_pagina:
            yield scrapy.Request(self.parser.avanzar_pagina(response.url)[0], callback=self.parse)


class SpiderMusimundo(scrapy.Spider):

    name = 'musimundo'
    custom_settings = configuraciones.configuracion_musimundo

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_musimundo[0]
        self.dic_ultimas_paginas = configuraciones.lista_dic_selectores_musimundo[1]

    def parse(self, response):

        proxima_pagina = response.css(self.dic_ultimas_paginas["selector_ultima_pagina"]).getall()
        lista_links_productos_caja = list(map(lambda x: "https://www.musimundo.com"+x, response.css(self.dic_ultimas_paginas["selector_proximos_links"][0]).getall()))
        lista_links_productos_alargado = list(map(lambda x: "https://www.musimundo.com"+x, response.css(self.dic_ultimas_paginas["selector_proximos_links"][1]).getall()))

        if lista_links_productos_caja + lista_links_productos_alargado:
            yield from response.follow_all(lista_links_productos_caja + lista_links_productos_alargado,
                                           self.parser.parse_producto,
                                           cb_kwargs=self.dic_selectores)

        if proxima_pagina:
            yield scrapy.Request("https://www.musimundo.com"+proxima_pagina[0], callback=self.parse)


class SpiderRibeiro(scrapy.Spider):

    name = 'ribeiro'
    custom_settings = configuraciones.configuracion_ribeiro

    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.parser = Parser()
        self.dic_selectores = configuraciones.lista_dic_selectores_ribeiro[0]
        self.dic_ultimas_paginas = configuraciones.lista_dic_selectores_ribeiro[1]

    def parse(self, response):

        lista_links_productos = list(map(lambda x: "https://www.ribeiro.com.ar"+x, response.css(self.dic_ultimas_paginas["selector_proximos_links"]).getall()))

        if lista_links_productos:
            yield from response.follow_all(lista_links_productos,
                                           self.parser.parse_producto,
                                           cb_kwargs=self.dic_selectores)
