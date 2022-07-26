# import csv
# import pickle
# from filtrador_de_productos import FiltradorDeProductos
import unidecode
from dominate.tags import *
import dominate
from mercado.mercado.items import ItemProducto
import json
import csv
# with open("result.p", "rb") as f:
#     for item in f:
#         print(pickle.load(item))

# lista = []
# with open("result.p", "rb") as contenedor:
#     try:
#         while contenedor:
#             obj = pickle.load(contenedor)
#             lista.append(obj)
#     except EOFError:
#         pass
#     except:
#         raise
# for p in lista:
#     print(p)

# url = "https://www.fravega.com/l/?keyword=preservativos&page=11"


# def avanzar_pagina(url):
#     numero_pagina = []
#     for x in range(len(url)-1, -1, -1):
#         if url[x] == "=":
#             break
#         numero_pagina.insert(0, url[x])
#     numero_pagina[-1] = str(int(numero_pagina[-1])+1)

#     return url[:-len(numero_pagina)]+"".join(numero_pagina)


# print(avanzar_pagina(url))
# def distance(str1, str2):
#     d = dict()
#     for i in range(len(str1)+1):
#         d[i] = dict()
#         d[i][0] = i
#     for i in range(len(str2)+1):
#         d[0][i] = i
#     for i in range(1, len(str1)+1):
#         for j in range(1, len(str2)+1):
#             d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
#     return d[len(str1)][len(str2)]


# # print(distance("Heladera", "heladera whirpool"))

# # heladera = "Heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox".split(" ")
# # heladera1 = "Heladera Cíclica Con Extra Freezer 394 Lts. Patrick HPK151M00B Blanca".split(" ")
# # heladera2 = "Tv Smart Led 43 Full Hd Samsung UN43J5290".split(" ")
# # heladera3 = "Heladera Ciclica 374 Lts. Gafa HGF387AFB Blanca".split(" ")

# dic = {"Heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox": 1402,
#        "Heladera Cíclica Con Extra Freezer 394 Lts. Patrick HPK151M00B Blanca": 32,
#        "Tv Smart Led 43 Full Hd Samsung UN43J5290": 344,
#        "Heladera Ciclica 374 Lts. Gafa HGF387AFB Blanca": 12312312}


# # dic= {"heladera ciclica 374 Lts. Gafa HGF387AFB Blanca": 12312312,
# #  "heladera ciclica Con Extra Freezer 394 Lts. Patrick HPK151M00B Blanca": 32,
# #  "heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox": 1402}

# dic = {"heladera ciclica": 12312312,
#        "heladera ciclica Con": 32,
#        "heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox": 1402}

# # lista_productos = [{"heladera ciclica": 12312312}, {"heladera ciclica Con": 32}, {"heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox": 1402}]
# lista_productos = [{"nombre": "heladera ciclica", "precio": 12312312},
#                    {"nombre": "heladera ciclica No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox1231231231231", "precio": 32},
#                    {"nombre": "heladera ciclic No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox", "precio": 1402},
#                    {"nombre": "heladera ciclica", "precio": 1402},
#                    {"nombre": "heladera ciclica", "precio": 1406},
#                    {"nombre": "heladera ciclica", "precio": 1408},
#                    {"nombre": "heladera ciclica", "precio": 1402},
#                    {"nombre": "heladera ciclica", "precio": 1401}, ]


# lista = sorted(lista_productos, key=ordenar_por_algunas_frases)


# f = FiltradorDeProductos([""], "", "")
# x = f.filtrar_productos_por_algunas_palabras
# x()
# with open("configuracion.json", "w") as archivo:
#     json.dump({
#         "paginas": ["musimundo", "fravega", "ribeiro"],
#         "ruta_archivo": "C:/Users/Pedro/Desktop/Nueva carpeta (3)/Tp/salida.csv",
#         "limite_paginas": [1, 3, 2, 4]
#     }, archivo)

# from ....cfg
# cfg/configuracion.json
# from pathlib import Path
# import os
# with open(Path(os.getcwd()+"/cfg/configuracion.json"), "r") as archivo:
# print(json.load(archivo))

# titulos = ["nombre", "categoria", "precio", "url", "fecha"]

# dic = {"nombre": "pedro",
#        "categoria": "bueno",
#        "precio": "200",
#        "url": "www",
#        "fecha": "2020"}


# producto = ItemProducto()

# producto["nombre"] = "pedro"
# producto["categoria"] = "bueno"
# producto["precio"] = "200"
# producto["url"] = "www"
# producto["fecha"] = "2020"


# lista = [producto, producto]

# print(producto.__dict__["_values"])

# with open("hola.json", "w", newline="", encoding="utf-8") as archivo:
#     lista_final = []
#     for item in lista:
#         lista_final.append(json.dumps(item.__dict__["_values"]))
#     json.dump(lista_final, archivo)

# {c: v for c, v in datos["dic_selectores"]["garbarino"].items() if c in claves_dic_selectores}

# claves_dic_selectores = ["selector_nombre", "selector_precio", "selector_categoria"]
# claves_dic_proximas_paginas = ["selector_ultima_pagina", "selector_proximos_links"]
# with open("cfg/cfg_programa.json", "r", newline="", encoding="utf-8") as archivo:

#     datos = json.load(archivo)
#     print({c: v for c, v in datos["dic_selectores"]["garbarino"].items() if c in claves_dic_selectores})
#     print({c: datos["dic_selectores"]["garbarino"][c] for c in claves_dic_selectores})
#     print({c: v for c, v in datos["dic_selectores"]["garbarino"].items() if c in claves_dic_proximas_paginas})
#     print({clave: datos["dic_selectores"]["garbarino"][clave] for clave in claves_dic_proximas_paginas})

# print(type(x["dic_selectores"]["garbarino"]))
# print(type(json.load(*archivo)[0]))

# print(os.path.abspath(os.curdir))
# os.chdir("..")
# p = Path(os.getcwd()+"/cfg")
# print(os.listdir(p))
# # os.chdir(p.parent)
# print(p)
# print(os.path.abspath(os.curdir))


# class pedro:
#     items = []
#     spiders_cerradas = 0

#     def cargar_item(self):
#         self.items.append(1)
#         self.spiders_cerradas += 1


# p = pedro()
# p.cargar_item()
# print(p.items)
# print(p.spiders_cerradas)

# # p = None

# x = pedro()
# x.cargar_item()
# print(x.items)
# print(x.spiders_cerradas)
# lista2 = sorted(lista_productos, key=ordenar_todas_las_frases, reverse=False)


# lista2 = sorted(lista_productos, key=lambda valor: (distance("heladera ciclica", valor), -int(float(valor[1][0].strip()))))


# print(lista2)


# dic_casos = {c: v for c, v in sorted(diccionario.items(), , reverse=True)}
# dic_casos = {c: v for c, v in sorted(diccionario.items(), key=lambda valor: any([True for palabra in valor[0].split(" ") if "heladera" in palabra.lower().strip()]), reverse=True)}

# encabezado = ("Titulo", "Precio", "Url", "Categoria", "Fecha y hora")


# def escribir_archivo_longitud_variable(nombre_archivo, encabezados, datos):
#     with open(nombre_archivo, "w", newline="") as archivo:
#         writer = csv.DictWriter(archivo, fieldnames=encabezados, delimiter=",", dialect="excel")
#         writer.writeheader()
#         for clave, valor in datos.items():
#             writer.writerow({encabezados[0]: clave, encabezados[1]: valor[0],
#                              encabezados[2]: valor[1], encabezados[3]: valor[2], encabezados[4]: valor[3]})


# escribir_archivo_longitud_variable("heladera.csv", encabezado, dic_casos)

# print(dic_casos)

# lista = [heladera, heladera1, heladera2, heladera3]

# for x in lista:
#     if "Heladera" in x:
#         print(x)

# heladera = "Heladera No Frost Touch Led 405 Lts. Peabody PE-TM40D Inox"


# table_headers = ["Nombre", "Categoria", "Precio", "Url", "Fecha"]

# producto = ItemProducto()

# producto["nombre"] = "pedro"
# producto["categoria"] = "bueno"
# producto["precio"] = "200"
# producto["url"] = "www"
# producto["fecha"] = "2020"


# lista = [producto, producto]

# for _ in range(len(producto.__dict__["_values"].keys())):
#     print(1)


# def create_page():


# doc = dominate.document(title="Example Table")

# with doc.head:
#     link(rel="stylesheet", href="style.css")

# with doc:
#     with div(cls="container"):
#         h1("Hello, World!")
#         with table(id="main", cls="table table-striped"):
#             caption(h3("A table to show data"))
#             with thead():
#                 with tr():
#                     for table_head in table_headers:
#                         th(table_head)
#             with tbody():
#                 for producto in lista:
#                     with tr():
#                         for valor in producto.__dict__["_values"].values():
#                             td(valor)

# with open("index.html", "w") as file:
#     file.write(doc.render())

# create_page()


# def normalizar_palabra(palabra_a_normalizar):
#     return [unidecode.unidecode(palabra.lower()) for palabra in palabra_a_normalizar.split()]


def distancia_levenshtein(str1, str2):
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


print(distancia_levenshtein("heladera blanca",
                            "Heladera con Freezer Philco PHCT320B Blanca"))
print(distancia_levenshtein("heladera blanca",
                            "Heladera con Freezer Philco HPK141M0 Blanca"))
print(distancia_levenshtein("heladera blanca",
                            "Purifica de Agua DVIGI Para Heladera Blanca"))
print(distancia_levenshtein("heladera blanca",
                            "Heladera con Freezer Nueva Neba A-320 Blanca"))

# def ordenar_todas_las_frases(diccionario):
#     # return distancia_levenshtein("heladera blanca", diccionario['nombre']), -int(float(diccionario['precio']))
#     print(distancia_levenshtein("heladera blanca", diccionario['nombre']), int(float(diccionario['precio'])))
#     return distancia_levenshtein("heladera blanca", diccionario['nombre']), int(float(diccionario['precio']))


# def ordenar_por_algunas_frases(diccionario):
#     input_usuario = normalizar_palabra("heladera blanca")
#     nombre_producto = diccionario['nombre'].split()

#     return (sum([1 for palabra in input_usuario if palabra in nombre_producto]), distancia_levenshtein("heladera blanca", diccionario['nombre']), int(float(diccionario['precio'])))


# lista = [{'categoria': 'Heladeras',
#           'fecha': '10-11-2020-19-41-43',
#           'nombre': 'Heladera Ciclica Gafa HGF357AFB Blanca 286Lts',
#           'precio': '40999',
#           'url': 'https://www.fravega.com/p/heladera-ciclica-gafa-hgf357afb-blanca-286lts-161088'},
#          {'categoria': 'Con Freezer',
#           'fecha': '10-11-2020-19-41-43',
#           'nombre': 'Heladera Ciclica 374 Lts. Gafa HGF387AFB Blanca',
#           'precio': '53869',
#           'url': 'https://www.ribeiro.com.ar/producto/heladera-ciclica-374-lts-gafa-hgf387afb-blanca/_/A-016021158000-016021158000_s/;jsessionid=uiGte+JrtBQWCOQs6EnJQKrH.ATGWEBBOT_01'},
#          {'categoria': 'Con Freezer',
#           'fecha': '10-11-2020-19-41-43',
#           'nombre': 'Heladera Ciclica 360 Lts. Philco PHCT360B/01 Blanca',
#           'precio': '66689',
#           'url': 'https://www.ribeiro.com.ar/producto/heladera-ciclica-360-lts-philco-phct360b-01-blanca/_/A-016021160000-016021160000_s/;jsessionid=uiGte+JrtBQWCOQs6EnJQKrH.ATGWEBBOT_01'},
#          {'categoria': 'Con Freezer',
#           'fecha': '10-11-2020-19-41-43',
#           'nombre': 'Heladera Ciclica Con Extra Freezer 394 Lts. Patrick HPK151M00B '
#           'Blanca',
#           'precio': '57759',
#           'url': 'https://www.ribeiro.com.ar/producto/heladera-ciclica-con-extra-freezer-394-lts-patrick-hpk151m00b-blanca/_/A-016021162000-016021162000_s/;jsessionid=uiGte+JrtBQWCOQs6EnJQKrH.ATGWEBBOT_01'},
#          {'categoria': 'Heladeras',
#           'fecha': '10-11-2020-19-41-44',
#           'nombre': 'Heladera con freezer Gafa HGF377AFB 326 Lt  Blanca',
#           'precio': '44699',
#           'url': 'https://www.fravega.com/p/heladera-con-freezer-gafa-hgf377afb-326-lt-blanca-50003305'},
#          {'categoria': 'Heladeras',
#           'fecha': '10-11-2020-19-41-44',
#           'nombre': 'Heladera Ciclica Gafa HGF387AFB Blanca 375Lts',
#           'precio': '52999',
#           'url': 'https://www.fravega.com/p/heladera-ciclica-gafa-hgf387afb-blanca-375lts-160979'},
#          {'categoria': 'Heladeras y Freezers',
#           'fecha': '10-11-2020-19-41-49',
#           'nombre': 'Heladera con Freezer Coventry 2F1600Ba Blanca 330 L',
#           'precio': '44999',
#           'url': 'https://www.garbarino.com/producto/heladera-con-freezer-coventry-2f1600ba-blanca-330-l/49ce45dcb0'},
#          {'categoria': 'Heladeras y Freezers',
#           'fecha': '10-11-2020-19-41-49',
#           'nombre': 'Heladera No Frost Patrick HPK350M00B    Blanca 271 Lts.',
#           'precio': '67999',
#           'url': 'https://www.garbarino.com/producto/heladera-no-frost-patrick-hpk350m00b-blanca-271-lts./ad5d3327b2'},
#          {'categoria': 'Heladeras y Freezers',
#           'fecha': '10-11-2020-19-41-50',
#           'nombre': 'Heladera con Freezer Philco PHCT320B Blanca',
#           'precio': '50499',
#           'url': 'https://www.garbarino.com/producto/heladera-con-freezer-philco-phct320b-blanca/0b9a3a9311'}]

# lista.sort(key=ordenar_por_algunas_frases)
# for x in lista:
#     # print(x, distancia_levenshtein("heladera blanca", x['nombre']), int(float(x['precio'])), end="\n\n")
#     print(x, end="\n\n")
