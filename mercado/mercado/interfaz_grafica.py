from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
import json
import os
from pathlib import Path
from usuario.entrada_usuario import EntradaUsuario


class InterfazGrafica:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Bienvenido al buscador")
        self.ventana.resizable(False, False)

        self.paginas_a_buscar = [IntVar() for x in range(4)]
        self.tipo_archivo = [IntVar() for x in range(3)]
        self.filtro_busqueda = IntVar()
        self.directorio_texto = StringVar()
        self.directorio_texto.set(
            '      	    Directorio:  \n(donde se guardaran los archivos)')

        self.entrada_usuario = EntradaUsuario()
        self.busqueda_especificaciones = IntVar()

    def buscar(self):
        hay_paginas_elegidas = any([x.get() for x in self.paginas_a_buscar])
        hay_formato_salida_elegido = any([x.get() for x in self.tipo_archivo])
        hay_busqueda = bool(self.entrada_busqueda.get().strip())
        hay_directorio_seleccionado = self.directorio_texto.get() != '      	    Directorio:  \n(donde se guardaran los archivos)'

        if not hay_paginas_elegidas or not hay_formato_salida_elegido or not hay_busqueda or not hay_directorio_seleccionado:
            messagebox.showinfo('Atencion!', 'Complete los campos faltantes')

        else:
            dic_paginas_a_buscar = ['aloise',
                                    'musimundo', 'garbarino', 'ribeiro']
            dic_fortmatos_salida = ['json', 'csv', 'html']

            dic_datos_a_devolver = dict()

            try:
                with open(Path(os.getcwd()+'/cfg/configuracion.json'), 'r') as archivo:
                    diccionario = json.load(archivo)
                    dic_datos_a_devolver.update(diccionario)

                with open(Path(os.getcwd()+'/cfg/cfg_programa.json'), 'r') as archivo:
                    dic_datos_a_devolver.update(json.load(archivo))

                with open(Path(os.getcwd()+'/cfg/configuracion.json'), 'w') as archivo:
                    lista_paginas_a_buscar = [x.get()
                                              for x in self.paginas_a_buscar]
                    lista_formatos_salida = [x.get()
                                             for x in self.tipo_archivo]
                    diccionario['paginas_a_buscar'] = [dic_paginas_a_buscar[x]
                                                       for x in range(4) if lista_paginas_a_buscar[x] == 1]
                    diccionario['ruta_archivo'] = self.directorio_texto.get()[12:]
                    diccionario['filtro_busqueda'] = self.filtro_busqueda.get()
                    diccionario['busqueda_usuario'] = self.entrada_busqueda.get()
                    diccionario['formatos_salida'] = [dic_fortmatos_salida[x]
                                                      for x in range(3) if lista_formatos_salida[x] == 1]
                    diccionario['busqueda_especificaciones'] = True if self.busqueda_especificaciones.get() == 1 else False
                    json.dump(diccionario, archivo)
                dic_datos_a_devolver.update(diccionario)
                self.entrada_usuario.recibir_datos(dic_datos_a_devolver)
                self.entrada_usuario.comenzar_busqueda()

            except FileNotFoundError:
                pass
                # raise ExcepcionEntradaError("La ruta ingresada es incorrecta")

    def cambiar_directorio(self):
        self.directorio_texto.set("Directorio: "+filedialog.askdirectory())

    def crear_interfaz(self):

        titulo = Label(self.ventana, text="Buscador")
        titulo.config(font=("Verdana", 18))

        self.entrada_busqueda = Entry(self.ventana, width=60)

        self.filtro_busqueda_exacta = Radiobutton(
            self.ventana, text='Frase exacta', value=0, var=self.filtro_busqueda)
        self.filtro_busqueda_algunas = Radiobutton(
            self.ventana, text='Algunas palabras', value=1, var=self.filtro_busqueda)
        self.filtro_busqueda_todas = Radiobutton(
            self.ventana, text='Todas las palabras', value=2, var=self.filtro_busqueda)

        aloise = Checkbutton(self.ventana, text='Aloise',
                             var=self.paginas_a_buscar[0])
        musimundo = Checkbutton(
            self.ventana, text='Musimundo', var=self.paginas_a_buscar[1])
        garbarino = Checkbutton(
            self.ventana, text='Garbarino', var=self.paginas_a_buscar[2])
        ribeiro = Checkbutton(self.ventana, text='Ribeiro',
                              var=self.paginas_a_buscar[3])

        directorio = Label(self.ventana)
        directorio.config(textvariable=self.directorio_texto)

        boton_directorio = Button(
            self.ventana, text="Buscar directorio", command=self.cambiar_directorio)

        self.tipo_archivo_json = Checkbutton(
            self.ventana, text='JSON', var=self.tipo_archivo[0])
        self.tipo_archivo_csv = Checkbutton(
            self.ventana, text='CSV', var=self.tipo_archivo[1])
        self.tipo_archivo_html = Checkbutton(
            self.ventana, text='HTML', var=self.tipo_archivo[2])

        boton_busqueda = Button(
            self.ventana, text="Buscar", command=self.buscar)

        especificaciones = Checkbutton(
            self.ventana, text='Buscar producto con especificaciones', var=self.busqueda_especificaciones)

        titulo.grid(column=0, row=0, columnspan=4, pady=7)
        self.entrada_busqueda.grid(
            column=0, row=1, columnspan=4, pady=7, padx=5)

        self.filtro_busqueda_exacta.grid(column=0, row=2, pady=7)
        self.filtro_busqueda_algunas.grid(
            column=1, row=2, pady=7, columnspan=2)
        self.filtro_busqueda_todas.grid(column=3, row=2, pady=7)

        aloise.grid(column=0, row=3, pady=7)
        musimundo.grid(column=1, row=3, pady=7)
        garbarino.grid(column=2, row=3, pady=7)
        ribeiro.grid(column=3, row=3, pady=7)

        directorio.grid(column=0, row=4, columnspan=4, pady=7)
        boton_directorio.grid(column=1, row=5, columnspan=2, pady=7)

        self.tipo_archivo_json.grid(column=0, row=6, pady=7)
        self.tipo_archivo_csv.grid(column=1, row=6, columnspan=2, pady=7)
        self.tipo_archivo_html.grid(column=3, row=6, pady=7)

        especificaciones.grid(column=0, row=7, columnspan=2, pady=7)

        boton_busqueda.grid(column=1, row=8, columnspan=2, pady=7)

        self.ventana.mainloop()
