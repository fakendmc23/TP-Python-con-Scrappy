from mercado.mercado.filtrador_de_productos import FiltradorDeProductos
from mercado.mercado.filtrador_de_productos import TipoDeFiltro
from mercado.mercado.spiders.spider_mercado import *
from usuario.entrada_usuario import EntradaUsuario
import pytest
import os
from pathlib import Path

filtrador = FiltradorDeProductos("./cfg/configuracion.json")


def test_distancia_palabra_exacta():
    assert filtrador.distancia_levenshtein(
        "Heladera blanca", "Heladera blanca") == 0


def test_distancia_algunas_palabras():
    assert filtrador.distancia_levenshtein(
        "Heladera blanca", "Heladera Whilpool") == 7


def test_distancia_todas_las_palabras():
    assert filtrador.distancia_levenshtein(
        "Heladera blanca", "Heladera blanca Whilpool") == 9


def test_ordenar_palabras_exactas():

    filtrador.lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "32500"
    }
    ]
    resultado = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "32500"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_EXACTA
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_palabras_exactas_esperando_un_error_de_tipos():

    filtrador.lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": ""
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": ""
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": ""
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": ""
    }
    ]

    filtrador.busqueda_usuario = "Heladera Ciclica Sigma 2F1200B 239lt"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_EXACTA

    with pytest.raises(TypeError):
        filtrador.ordenar_productos()


def test_ordenar_todas_las_palabras():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Vostok KD420F Blanco 420 Lts.",
        "precio": "48999"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Philco PHCT320B Blanco 314 Lts.",
        "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30BD Blanco 358 Lts.",
        "precio": "99799"
    },
    ]
    resultado = [{
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Vostok KD420F Blanco 420 Lts.",
            "precio": "48999"
    },
        {
        "nombre": "Heladera con Freezer Philco PHCT320B Blanco 314 Lts.",
            "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30BD Blanco 358 Lts.",
            "precio": "99799"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_todas_las_palabras_esperando_un_error_de_tipos():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Vostok KD420F Blanco 420 Lts.",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Philco PHCT320B Blanco 314 Lts.",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30BD Blanco 358 Lts.",
        "precio": ""},
    ]

    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    with pytest.raises(TypeError):
        filtrador.ordenar_productos()


def test_ordenar_algunas_palabras_esperando_un_error_de_tipos():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Vostok KD420F Blanco 420 Lts.",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Philco PHCT320B Blanco 314 Lts.",
        "precio": ""},
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30BD Blanco 358 Lts.",
        "precio": ""},
    ]

    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    with pytest.raises(TypeError):
        filtrador.ordenar_productos()


def test_ordenar_todas_las_palabras_y_distintas_distancias():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Vostok KD420FFSA Blanco 420 Lts.",
        "precio": "4899"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M0 Blanco",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Philco Blanco 314 Lts",
        "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30ASDASBD Blanco 358 Lts.",
        "precio": "997"
    },
    ]
    resultado = [{
        "nombre": "Heladera con Freezer Philco Blanco 314 Lts",
        "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M0 Blanco",
            "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Vostok KD420FFSA Blanco 420 Lts.",
            "precio": "4899"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30ASDASBD Blanco 358 Lts.",
            "precio": "997"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanco"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_algunas_palabras_distintas_distancias():
    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Vostok KD420FFSA Blanco 420 Lts.",
        "precio": "4899"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M0 Blanco",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Philco Blanco 314 Lts",
        "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30ASDASBD Blanco 358 Lts.",
        "precio": "997"
    },
    ]
    resultado = [{
        "nombre": "Heladera con Freezer Philco Blanco 314 Lts",
        "precio": "63839"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M0 Blanco",
            "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Vostok KD420FFSA Blanco 420 Lts.",
            "precio": "4899"
    },
        {
        "nombre": "Heladera con Freezer Siam HSI-NT30ASDASBD Blanco 358 Lts.",
            "precio": "997"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_algunas_palabras():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Philco PHCT320B Blanca",
        "precio": "55999"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
            "precio": "47999"
    },
        {
        "nombre": "Purificador de Agua DVIGI Para Heladera",
            "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca 318 L",
            "precio": "47999"
    }
    ]
    resultado = [{
        "nombre": "Heladera con Freezer Philco PHCT320B Blanca",
        "precio": "55999"
    },
        {
        "nombre": "Purificador de Agua DVIGI Para Heladera",
            "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Patrick HPK141M00B Blanco",
            "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca 318 L",
            "precio": "47999"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_todas_las_palabras_y_misma_distancia():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Philco PHCT320B Blanca",
        "precio": "55999"
    },
        {
        "nombre": "Heladera con Freezer Philco HPK141M0 Blanca",
            "precio": "47999"
    },
        {
        "nombre": "Purifica de Agua DVIGI Para Heladera Blanca",
            "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca",
            "precio": "47300"
    }
    ]
    resultado = [{
        "nombre": "Purifica de Agua DVIGI Para Heladera Blanca",
        "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca",
        "precio": "47300"
    },
        {

        "nombre": "Heladera con Freezer Philco HPK141M0 Blanca",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Philco PHCT320B Blanca",
        "precio": "55999"
    }
    ]
    filtrador.busqueda_usuario = "Heladera blanca"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_ordenar_algunas_las_palabras_y_misma_distancia():

    filtrador.lista_productos = [{
        "nombre": "Heladera con Freezer Philco PHCT320BG Blanca",
        "precio": "55999"
    },
        {
        "nombre": "Heladera con Freezer Philco HPK141M0F Blanca",
            "precio": "47999"
    },
        {
        "nombre": "Purifica de Agua DVIGIF Para Heladera Blanca",
            "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca",
            "precio": "47300"
    }
    ]
    resultado = [{
        "nombre": "Purifica de Agua DVIGIF Para Heladera Blanca",
        "precio": "1999"
    },
        {
        "nombre": "Heladera con Freezer Nueva Neba A-320 Blanca",
        "precio": "47300"
    },
        {

        "nombre": "Heladera con Freezer Philco HPK141M0F Blanca",
        "precio": "47999"
    },
        {
        "nombre": "Heladera con Freezer Philco PHCT320BG Blanca",
        "precio": "55999"
    }
    ]
    filtrador.busqueda_usuario = "Heladera"
    filtrador.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    filtrador.ordenar_productos()

    assert filtrador.lista_productos == resultado


def test_normalizar_producto():
    assert filtrador.normalizar_palabra(
        "Heladera con Freezer Nueva Neba A-320 Blanca 318 L") == ["heladera", "con", "freezer", "nueva", "neba", "a-320", "blanca", "318", "l"]


def test_eliminar_stopwords_producto():

    assert filtrador.eliminar_stopwords(
        "Heladera con Freezer Nueva Neba A-320 Blanca 318 L") == ["heladera", "freezer", "nueva", "neba", "a-320", "blanca", "318", "l"]


def test_filtrar_productos_con_palabras_exactas():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 29lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    }
    ]
    filtrador2.busqueda_usuario = "Heladera Ciclica Sigma 2F1200B 239lt"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_EXACTA
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_palabras_exactas_y_no_desechar_ninguno():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "32500"
    }
    ]
    filtrador2.busqueda_usuario = "Heladera Ciclica Sigma 2F1200B 239lt"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_EXACTA
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_algunas_palabras():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    }
    ]
    filtrador2.busqueda_usuario = "Heladera"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_algunas_palabras_y_no_desechar_ninguno():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]
    filtrador2.busqueda_usuario = "Heladera Sigma"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_todas_las_palabras():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },

    ]
    filtrador2.busqueda_usuario = "Heladera Sigma"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_todas_las_palabras_y_no_desechar_ninguno():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma Heladera 2F120B 239lt",
            "precio": "32500"
    }
    ]
    lista_productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma Heladera 2F120B 239lt",
            "precio": "32500"
    }
    ]
    filtrador2.busqueda_usuario = "Heladera Sigma"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert lista_productos == filtrador2.lista_productos


def test_filtrar_productos_con_todas_las_palabras_y_desechar_todos():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Ciclica 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Ciclica  2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "2F120B 239lt",
            "precio": "32500"
    }
    ]

    filtrador2.busqueda_usuario = "Heladera Sigma"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_TODAS_LAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert [] == filtrador2.lista_productos


def test_filtrar_productos_con_algunas_palabras_y_desechar_todos():
    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Ciclica Sigma 2F1200B 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Sigma 2F1200B 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Ciclica Sigma 2F1200B 239lt",
            "precio": "34000"
    },
        {
        "nombre": "Sigma 2F120B 239lt",
            "precio": "32500"
    }
    ]

    filtrador2.busqueda_usuario = "Heladera"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_ALGUNAS_PALABRAS
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert [] == filtrador2.lista_productos


def test_filtrar_productos_con_palabras_exactas_y_desechar_todos():

    filtrador2 = FiltradorDeProductos("./cfg/configuracion.json")

    productos = [{
        "nombre": "Heladera Ciclica Sigma 2F1200 239lt",
        "precio": "31324"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200 239lt",
            "precio": "35000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F1200 29lt",
            "precio": "34000"
    },
        {
        "nombre": "Heladera Ciclica Sigma 2F120 239lt",
            "precio": "32500"
    }
    ]

    filtrador2.busqueda_usuario = "Heladera Ciclica Sigma 2F1200B 239lt"
    filtrador2.filtro_busqueda = TipoDeFiltro.FRASE_EXACTA
    for producto in productos:
        filtrador2.filtrar_producto(producto)

    assert [] == filtrador2.lista_productos


def test_configuraciones_por_default_si_no_le_paso_ruta():
    configuracion = Configuraciones("")

    assert configuracion.configuracion_garbarino['DEPTH_LIMIT'] == 1
    assert configuracion.configuracion_aloise['DEPTH_LIMIT'] == 1
    assert configuracion.configuracion_musimundo['DEPTH_LIMIT'] == 1
    assert configuracion.configuracion_ribeiro['DEPTH_LIMIT'] == 1


def test_configuraciones_pasandole_ruta_del_archivo():

    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))
    assert configuraciones.configuracion_garbarino['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert configuraciones.configuracion_garbarino['IMAGES_STORE'] == "imagenes_scrapy"
    assert configuraciones.configuracion_aloise['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert configuraciones.configuracion_aloise['IMAGES_STORE'] == "imagenes_scrapy"
    assert configuraciones.configuracion_musimundo['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert configuraciones.configuracion_musimundo['IMAGES_STORE'] == "imagenes_scrapy"
    assert configuraciones.configuracion_ribeiro['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert configuraciones.configuracion_ribeiro['IMAGES_STORE'] == "imagenes_scrapy"


def test_configuraciones_selectores_aloise():

    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    resultado_datos = [{
        "selector_nombre": "#product-name",
        "selector_precio": "#price_display",
        "selector_categoria": ".breadcrumb-crumb:nth-child(5)",
        "selector_imagen": ".js-desktop-zoom.cloud-zoom"},
        {"selector_ultima_pagina": ".pagination-arrow-link.m-left-half::attr(href)",
         "selector_proximos_links": ".item-image-container div a::attr(href)"}
    ]

    assert configuraciones.lista_dic_selectores_aloise == resultado_datos


def test_configuraciones_selectores_ribeiro():

    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    resultado_datos = [{"selector_nombre": ".name-prod",
                        "selector_precio": ".precio1pagoFormat",
                        "selector_categoria": "#atg_store_breadcrumbs_mod .font-weight-bold",
                        "selector_imagen": "#zoom_03f"},
                       {"selector_ultima_pagina": "",
                        "selector_proximos_links": "li.col-6 > a::attr(href)"}
                       ]

    assert configuraciones.lista_dic_selectores_ribeiro == resultado_datos


def test_configuraciones_selectores_garbarino():

    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    resultado_datos = [{
        "selector_nombre": "h1",
        "selector_precio": "#final-price",
        "selector_categoria": ".gb-breadcrumb li:nth-child(3) a",
        "selector_imagen": ".gb-main-detail-gallery-grid-img-full img"},
        {"selector_ultima_pagina": "li.pagination__page:nth-child(3) > a:nth-child(1)",
         "selector_proximos_links": "/html/body/div[4]/div[2]/div[2]/div/div/div/div/div/a/@href"}
    ]

    assert configuraciones.lista_dic_selectores_garbarino == resultado_datos


def test_configuraciones_selectores_musimundo():

    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    resultado_datos = [{
        "selector_nombre": ".mus-pro-name",
        "selector_precio": ".mus-pro-price-number span",
        "selector_categoria": "#breadcrumb li:nth-child(3) a",
        "selector_imagen": "#productMainImage"},
        {"selector_ultima_pagina": ".next a::attr(href)",
         "selector_proximos_links": [
             ".productGridItem::attr(href)",
             ".productListItemPromotion::attr(href)"
         ]}
    ]
    assert configuraciones.lista_dic_selectores_musimundo == resultado_datos


def test_al_crear_spider_garbarino_tiene_asignado_sus_selectores():

    spider = SpiderGarbarino("")
    assert spider.dic_selectores["selector_nombre"] == "h1"
    assert spider.dic_selectores["selector_precio"] == "#final-price"
    assert spider.dic_selectores[
        "selector_categoria"] == ".gb-breadcrumb li:nth-child(3) a"
    assert spider.dic_selectores["selector_imagen"] == ".gb-main-detail-gallery-grid-img-full img"
    assert spider.dic_ultimas_paginas[
        "selector_ultima_pagina"] == "li.pagination__page:nth-child(3) > a:nth-child(1)"
    assert spider.dic_ultimas_paginas["selector_proximos_links"] == "/html/body/div[4]/div[2]/div[2]/div/div/div/div/div/a/@href"


def test_al_crear_spider_musimundo_tiene_asignado_sus_selectores():

    spider = SpiderMusimundo("")

    assert spider.dic_selectores["selector_nombre"] == ".mus-pro-name"
    assert spider.dic_selectores["selector_precio"] == ".mus-pro-price-number span"
    assert spider.dic_selectores[
        "selector_categoria"] == "#breadcrumb li:nth-child(3) a"
    assert spider.dic_selectores["selector_imagen"] == "#productMainImage"
    assert spider.dic_ultimas_paginas[
        "selector_ultima_pagina"] == ".next a::attr(href)"
    assert spider.dic_ultimas_paginas["selector_proximos_links"] == [
        ".productGridItem::attr(href)",
        ".productListItemPromotion::attr(href)"]


def test_al_crear_spider_ribeiro_tiene_asignado_sus_selectores():

    spider = SpiderRibeiro("")

    assert spider.dic_selectores["selector_nombre"] == ".name-prod"
    assert spider.dic_selectores["selector_precio"] == ".precio1pagoFormat"
    assert spider.dic_selectores[
        "selector_categoria"] == "#atg_store_breadcrumbs_mod .font-weight-bold"
    assert spider.dic_selectores["selector_imagen"] == "#zoom_03f"
    assert spider.dic_ultimas_paginas[
        "selector_ultima_pagina"] == ""
    assert spider.dic_ultimas_paginas[
        "selector_proximos_links"] == "li.col-6 > a::attr(href)"


def test_al_crear_spider_aloise_tiene_asignado_sus_selectores():

    spider = SpiderAloise("")

    assert spider.dic_selectores["selector_nombre"] == "#product-name"
    assert spider.dic_selectores["selector_precio"] == "#price_display"
    assert spider.dic_selectores[
        "selector_categoria"] == ".breadcrumb-crumb:nth-child(5)"
    assert spider.dic_selectores["selector_imagen"] == ".js-desktop-zoom.cloud-zoom"
    assert spider.dic_ultimas_paginas[
        "selector_ultima_pagina"] == ".pagination-arrow-link.m-left-half::attr(href)"
    assert spider.dic_ultimas_paginas[
        "selector_proximos_links"] == ".item-image-container div a::attr(href)"


def test_al_crear_spider_aloise_tiene_asignado_su_configuracion_correctamente():

    spider = SpiderAloise("")
    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    assert spider.custom_settings['DEPTH_LIMIT'] == 1
    assert spider.custom_settings['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert spider.custom_settings['IMAGES_STORE'] == "imagenes_scrapy"


def test_al_crear_spider_musimundo_tiene_asignado_su_configuracion_correctamente():

    spider = SpiderMusimundo("")
    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    assert spider.custom_settings['DEPTH_LIMIT'] == 1
    assert spider.custom_settings['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert spider.custom_settings['IMAGES_STORE'] == "imagenes_scrapy"


def test_al_crear_spider_ribeiro_tiene_asignado_su_configuracion_correctamente():

    spider = SpiderRibeiro("")
    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    assert spider.custom_settings['DEPTH_LIMIT'] == 1
    assert spider.custom_settings['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert spider.custom_settings['IMAGES_STORE'] == "imagenes_scrapy"


def test_al_crear_spider_garbarino_tiene_asignado_su_configuracion_correctamente():

    spider = SpiderGarbarino("")
    configuraciones = Configuraciones(
        Path(os.getcwd()+'/cfg/cfg_programa.json'))

    assert spider.custom_settings['DEPTH_LIMIT'] == 1
    assert spider.custom_settings['ITEM_PIPELINES'] == {
        'mercado.mercado.pipelines.ProductoPipeline': 300}
    assert spider.custom_settings['IMAGES_STORE'] == "imagenes_scrapy"


def test_construir_url_buscando_heladera_blanca():

    entrada = EntradaUsuario()

    assert entrada.construir_url("heladera blanca", "+") == "heladera+blanca"


def test_recibir_datos_en_entrada_usuario():

    entrada = EntradaUsuario()

    diccionario = {

        "url_paginas_disponibles": {
            "aloise": "https://www.aloisetecno.com/search/page/1/?q=frase_a_buscar",
            "ribeiro": "https://www.ribeiro.com.ar/browse/?No=0&Ntt=frase_a_buscar&Nrpp=1000",
            "musimundo": "https://www.musimundo.com/search?q=frase_a_buscara&page=0",
            "garbarino": "https://www.garbarino.com/q/frase_a_buscar/srch?q=frase_a_buscar&page=1"
        },
        "paginas_disponibles": [
            "aloise",
            "musimundo",
            "garbarino",
            "ribeiro"
        ],
        "paginas_a_buscar": ["aloise", "ribeiro"],
        "busqueda_especificaciones": True,
        "busqueda_usuario": "Heladera blanca Sigma"
    }

    entrada.recibir_datos(diccionario)

    assert entrada.paginas_disponibles_para_buscar == [
        "aloise",
        "musimundo",
        "garbarino",
        "ribeiro"
    ]
    assert entrada.paginas_a_buscar == ["aloise", "ribeiro"]
    assert entrada.busqueda == "heladera+blanca+sigma"
    assert entrada.dic_url_paginas_disponibles == {
        "aloise": "https://www.aloisetecno.com/search/page/1/?q=frase_a_buscar",
        "ribeiro": "https://www.ribeiro.com.ar/browse/?No=0&Ntt=frase_a_buscar&Nrpp=1000",
        "musimundo": "https://www.musimundo.com/search?q=frase_a_buscara&page=0",
        "garbarino": "https://www.garbarino.com/q/frase_a_buscar/srch?q=frase_a_buscar&page=1"
    }
    assert entrada.buscar_especificaciones == True
