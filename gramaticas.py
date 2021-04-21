class gramaticas:
    def __init__(self, nombre):
        self.nombre = nombre    #nombre de la gramática
        self.terminales = {}    #simbolos terminales
        self.no_terminales = {} #simbolos no terminales
        self.producciones = []  #producciones de la gramática
        self.terminal_inicial = None #terminal inicial
        self.tipo = 'Regular'        #tipo de gramática
        #self.idImagen = None
        
    def insertar_terminales(self, cadena_terminales):
        listaAux = cadena_terminales.split(',')

        for x in listaAux:
            self.terminales[x] = 'terminal'

    def insertar_no_terminales(self, cadena_no_terminales):
        listaAux = cadena_no_terminales.split(',')

        for x in listaAux:
            self.no_terminales[x] = 'no terminal'
  
    def insertar_producciones(self, produccion):
        separar = produccion.split('->')
        derecha = separar[1].split(' ')
        #print(separar[0], derecha)
        produccionDict = []

        contadorTerminales = 0
        contadorNoTerminales = 0

        for x in derecha:
            diccionario = {}
            if x in self.terminales:
                diccionario[x] = 'terminal'
                produccionDict.append(diccionario)
                contadorTerminales += 1
            elif x in self.no_terminales:
                diccionario[x] = 'no terminal'
                produccionDict.append(diccionario)
                contadorNoTerminales += 1

        if contadorTerminales >= 2:
            self.tipo = 'GLC'
        elif contadorNoTerminales >= 2:
            self.tipo = 'GLC'
        
        aux = [separar[0], produccionDict]
        self.producciones.append(aux)