class AutomataPila:

    def __init__(self, nombre):
        self.id = None
        self.nombre = nombre
        self.terminales = {}    #simbolos terminales
        self.no_terminales = {} #simbolos no terminales
        self.producciones = []  #producciones de la gramática
        self.terminal_inicial = None #terminal inicial