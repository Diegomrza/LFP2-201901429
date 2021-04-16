class gramaticas:
    def __init__(self, nombre):
        self.nombre = nombre
        self.terminales = []
        self.no_terminales = []
        self.producciones = []
        self.terminal_inicial = None
        
    def insertar_terminales(self, cadena_terminales):
        listaAux = cadena_terminales.split(',')
        self.terminales = listaAux

    def insertar_no_terminales(self, cadena_no_terminales):
        listaAux = cadena_no_terminales.split(',')
        self.no_terminales = listaAux
        
    def insertar_producciones(self, produccion):
        self.producciones.append(produccion)
