from mercado.mercado.filtrador_de_productos import FiltradorDeProductos
import os
from pathlib import Path
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem


class ProductoPipeline(ImagesPipeline):

    contador_spiders_cerradas = []
    filtrador = FiltradorDeProductos(Path(os.getcwd()+'/cfg/configuracion.json'))

    def file_path(self, request, response=None, info=None, *, item=None):
        return item["nombre"].replace("/", "-").replace('"', "")+".jpeg"

    def get_media_requests(self, item, info):

        if item["es_item_especificaciones"]:
            ProductoPipeline.filtrador.lista_items_especificaciones.append(item)
        else:
            producto_agregado, descargar_imagen = ProductoPipeline.filtrador.filtrar_producto(item)
            if producto_agregado and descargar_imagen:
                for image_url in item['image_urls']:
                    yield scrapy.Request(image_url)

    def close_spider(self, spider):
        spiders_especificaciones = 3 if ProductoPipeline.filtrador.busqueda_especificaciones else 0
        self.contador_spiders_cerradas.append(1)
        if len(self.contador_spiders_cerradas) == len(ProductoPipeline.filtrador.paginas_a_buscar)+spiders_especificaciones:
            self.ordenar_items_y_escribir_archivos()

    def ordenar_items_y_escribir_archivos(self):
        ProductoPipeline.filtrador.ordenar_productos()
        ProductoPipeline.filtrador.escribir_archivos_salida()
