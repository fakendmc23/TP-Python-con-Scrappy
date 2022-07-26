from nltk.corpus import stopwords
import csv
import json
import os
from pathlib import Path
import unidecode
from dominate.tags import *
import dominate
from enum import Enum
from datetime import datetime


class TipoDeFiltro(Enum):

    FRASE_EXACTA = 0
    FRASE_ALGUNAS_PALABRAS = 1
    FRASE_TODAS_LAS_PALABRAS = 2


class FiltradorDeProductos():

    def __init__(self, ruta_archivo_configuracion):
        self.busqueda_usuario = ""
        self.filtro_busqueda = -1
        self.formatos_salida = []
        self.ruta_archivo_salida = ""
        self.paginas_a_buscar = []
        self.busqueda_especificaciones = False
        self.leer_archivo_configuracion(ruta_archivo_configuracion)
        self.lista_productos = []
        self.nombre_archivo_salida = self.ruta_archivo_salida+"/" + \
            self.busqueda_usuario.replace(" ", "_").replace(
                '"', " ")+"_"+datetime.now().strftime("%d-%m-%Y")
        self.nombre_archivo_salida_especificaciones = self.ruta_archivo_salida+"/" + "ESPECIFICACIONES_" + \
            self.busqueda_usuario.replace(" ", "_").replace(
                '"', " ")+"_"+datetime.now().strftime("%d-%m-%Y")
        self.lista_items_especificaciones = []

    def escribir_archivo_especificaciones(self):

        lista_productos = [producto for producto in self.lista_productos if self.distancia_levenshtein(
            producto["nombre"], self.busqueda_usuario) < 30]
        path = Path(os.getcwd()+'/imagenes_scrapy')
        archivos = [f for f in os.listdir(
            path) if os.path.isfile(os.path.join(path, f))]
        precios = [producto["precio"] for producto in lista_productos]

        try:
            doc = dominate.document(title="Especificaciones")
            with doc.head:
                link(rel="stylesheet", href="style.css")

            with doc:
                for item in lista_productos:
                    with div(cls="container"):
                        with div():
                            h2("Nombre: "+item["nombre"])
                        with div():
                            with table(id="main", cls="table table-striped"):
                                caption(h3("Especificaciones"))
                                with thead():
                                    with tr():
                                        for table_head in ["Especificacion", "Valor"]:
                                            th(table_head)
                                with tbody():
                                    for titulo, valor in self.lista_items_especificaciones[0].__dict__["_values"]["especificaciones"].items():
                                        with tr():
                                            td(titulo)
                                            td(valor)

                    with div():
                        archivo = ""
                        for imagen in archivos:
                            if item["nombre"] in imagen:
                                archivo = imagen
                                break
                        img(src="./imagenes_scrapy/"+archivo, width=300)
                    with div():
                        h2("Precio: $"+item["precio"])
                    hr()
                    hr()

            with open(self.nombre_archivo_salida_especificaciones+".html", "w") as file:
                file.write(doc.render())

        except FileNotFoundError:
            print("No se pudo escribir el archivo json, no se proporciono la ruta")

    def leer_archivo_configuracion(self, ruta):

        try:
            with open(ruta, "r") as archivo:
                datos = json.load(archivo)
                self.filtro_busqueda = TipoDeFiltro(datos["filtro_busqueda"])
                self.ruta_archivo_salida = datos["ruta_archivo"]
                self.busqueda_usuario = datos["busqueda_usuario"]
                self.formatos_salida = datos["formatos_salida"]
                self.paginas_a_buscar = datos["paginas_a_buscar"]
                self.busqueda_especificaciones = datos["busqueda_especificaciones"]
        except FileNotFoundError:
            raise FileNotFoundError

    def eliminar_stopwords(self, palabra_a_eliminar_stopwords):
        return [palabra for palabra in self.normalizar_palabra(palabra_a_eliminar_stopwords) if palabra not in frozenset(stopwords.words('spanish'))]

    def normalizar_palabra(self, palabra_a_normalizar):
        return [unidecode.unidecode(palabra.lower()) for palabra in palabra_a_normalizar.split()]

    def distancia_levenshtein(self, str1, str2):

        d = dict()
        for i in range(len(str1)+1):
            d[i] = dict()
            d[i][0] = i
        for i in range(len(str2)+1):
            d[0][i] = i
        for i in range(1, len(str1)+1):
            for j in range(1, len(str2)+1):
                d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1]
                              [j-1]+(not str1[i-1] == str2[j-1]))
        return d[len(str1)][len(str2)]

    # frase exacta
    def ordenar_por_frase_exacta(self, diccionario):

        try:
            return int(float(diccionario['precio']))
        except (ValueError, TypeError) as e:
            print(e)

    # todas las frases
    def ordenar_todas_las_frases(self, diccionario):

        try:
            return (self.distancia_levenshtein(self.busqueda_usuario, diccionario['nombre']), int(float(diccionario['precio'])))
        except (ValueError, TypeError) as e:
            print(e)

    # algunas frases
    def ordenar_por_algunas_frases(self, diccionario):

        input_usuario = self.normalizar_palabra(self.busqueda_usuario)
        nombre_producto = diccionario['nombre'].split()
        try:
            return (sum([1 for palabra in input_usuario if palabra in nombre_producto]), self.distancia_levenshtein(self.busqueda_usuario, diccionario['nombre']), int(float(diccionario['precio'])))
        except (ValueError, TypeError) as e:
            print(e)

    def filtrar_producto(self, item):

        item_agregado = False

        if self.filtro_busqueda == TipoDeFiltro.FRASE_EXACTA:
            if self.normalizar_palabra(self.busqueda_usuario) == self.normalizar_palabra(item['nombre']):
                self.lista_productos.append(item)
                item_agregado = True

        elif self.filtro_busqueda == TipoDeFiltro.FRASE_ALGUNAS_PALABRAS:
            if any(palabra in self.normalizar_palabra(self.busqueda_usuario) for palabra in self.eliminar_stopwords(item['nombre'])):
                self.lista_productos.append(item)
                item_agregado = True

        elif self.filtro_busqueda == TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS:
            if all(palabra in self.eliminar_stopwords(item['nombre']) for palabra in self.normalizar_palabra(self.busqueda_usuario)):
                self.lista_productos.append(item)
                item_agregado = True

        return item_agregado, self.busqueda_especificaciones

    def ordenar_productos(self):

        if self.filtro_busqueda == TipoDeFiltro.FRASE_EXACTA:
            self.lista_productos.sort(key=self.ordenar_por_frase_exacta)
        elif self.filtro_busqueda == TipoDeFiltro.FRASE_ALGUNAS_PALABRAS:
            self.lista_productos.sort(key=self.ordenar_por_algunas_frases)
        elif self.filtro_busqueda == TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS:
            self.lista_productos.sort(key=self.ordenar_todas_las_frases)

    def escribir_archivos_salida(self):

        dic_formatos_archivos = {"csv": self.escribir_csv,
                                 "json": self.escribir_json,
                                 "html": self.escribir_html}

        for producto in self.lista_productos:
            del (producto.__dict__['_values']['es_item_especificaciones'])

        if self.busqueda_especificaciones:
            if len(self.lista_items_especificaciones) >= 1:
                self.escribir_archivo_especificaciones()
            else:
                print("No se encontraron productos con esa especificacion")

        for formato in self.formatos_salida:
            dic_formatos_archivos[formato]()

    def escribir_csv(self):

        try:
            with open(self.nombre_archivo_salida+".csv", 'w', newline='', encoding="utf-8") as csvfile:
                titulos = ['nombre', 'categoria',
                           'precio', 'url', 'fecha', 'image_urls']
                writer = csv.DictWriter(csvfile, fieldnames=titulos)
                writer.writeheader()
                for producto in self.lista_productos:
                    writer.writerow(producto.__dict__['_values'])
        except FileNotFoundError:
            print("No se pudo escribir el archivo csv, no se proporciono la ruta")

    def escribir_json(self):

        try:
            with open(self.nombre_archivo_salida+".json", 'w', newline='', encoding="utf-8") as jsonfile:
                json.dump({
                    "productos": [producto.__dict__['_values'] for producto in self.lista_productos],
                    "tipo_de_busqueda": self.filtro_busqueda.value
                }, jsonfile)
        except FileNotFoundError:
            print("No se pudo escribir el archivo json, no se proporciono la ruta")

    def escribir_html(self):

        try:
            import os  # no funciona si no se importa dentro
            archivos = [f for f in os.listdir(
                "./imagenes_scrapy") if os.path.isfile(os.path.join("./imagenes_scrapy", f))]
            doc = dominate.document(title="Tabla de productos")
            with doc.head:
                link(rel="stylesheet", href="style.css")
                link(rel="stylesheet",
                     href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap")

            with doc:
                with div(cls="container"):
                    with table(id="main", cls="table table-striped"):
                        caption(h3("Productos Encontrados"))
                        with thead():
                            with tr():
                                for table_head in ["Nombre", "Precio", "Categoria", "Url Imagen", "Url Producto", "Fecha"]:
                                    th(table_head)
                        with tbody():
                            for producto in self.lista_productos:
                                with tr():
                                    for valor in producto.__dict__['_values'].values():
                                        td(valor)

            with open(self.nombre_archivo_salida+".html", "w") as file:
                file.write(doc.render())

        except FileNotFoundError:
            print("No se pudo escribir el archivo html, no se proporciono la ruta")
