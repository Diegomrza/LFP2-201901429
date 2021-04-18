import time, os
from tkinter import Tk, filedialog
from gramaticas import gramaticas

lista_de_gramaticas = []

#Métodos visuales -----------------------------------------------------------------------

def pantalla_principal():
    x = 5   
    print('\n\n\t--*-- Gramatizador libre --*--\n\tCreador: Diego Abraham Robles Meza\n\tCarnet: 201901429')
    while x > 0:
        print('\t>>',x,'<<')
        time.sleep(1)
        x-=1
    os.system('cls')

def menú_principal():
    print('\nBienvenido!\n')
    x = True
    while x:
        print('1. Cargar Archivo')
        print('2. Mostrar inf. general de la gramática')
        print('3. Generar autómata de pila equivalente')
        print('4. Reporte de recorrido')
        print('5. Reporte en tabla')
        print('6. Salir')

        opcion = input('\nSeleccione una opción:\n>>')

        if int(opcion) == 1:
            print()
            print('Usted eligió la opción uno')
            cargar_archivo()
        elif int(opcion) == 2:
            print()
            print('Usted eligió la opción dos')
            Mostrar_inf()
        elif int(opcion) == 3:
            print()
            print('Usted eligió la opción tres')
        elif int(opcion) == 4:
            print()
            print('Usted eligió la opción cuatro')
        elif int(opcion) == 5:
            print()
            print('Usted eligió la opción cinco')
        elif int(opcion) == 6:
            print()
            print('Usted eligió la opción seis(Salir)')
            exit()

#Fin métodos visuales -------------------------------------------------------------------


#Métodos funcionales ////////////////////////////////////////////////////////////////////

def cargar_archivo():
    global lista_de_gramaticas

    root = Tk()
    ruta = filedialog.askopenfilename(title="Seleccione un archivo", 
    filetypes = (("glc files","*.glc"),("all files","*.*")))

    abrir_archivo = open(ruta)
    
    lista = abrir_archivo.readlines()
    #contador = len(lista)

    gramaticaAux = []
    for x in lista:
        if x != '*\n' and x!= '*':
            gramaticaAux.append(x.rstrip('\n'))
        else:
            spl = gramaticaAux[1].split(';')
            gram = gramaticas(gramaticaAux[0])

            gram.insertar_no_terminales(spl[0])
            gram.insertar_terminales(spl[1])
            gram.terminal_inicial = spl[2]

            for y in range(2,len(gramaticaAux)):
                gram.insertar_producciones(gramaticaAux[y])

            lista_de_gramaticas.append(gram)
            gramaticaAux.clear()

    abrir_archivo.close()
    root.destroy()

def Mostrar_inf():
    global lista_de_gramaticas
    for x in lista_de_gramaticas:
        print('**********************')
        print('Nombre: ', x.nombre)
        print('No Terminales: ', x.no_terminales)
        print('Terminales: ', x.terminales)
        print('Terminal inicial: ', x.terminal_inicial)
        print('Tipo: ', x.tipo)
        for x in x.producciones:
            print(x)        
        
        print('**********************')

def generar_automata_pila():
    pass

def reporte_recorrido():
    pass

def reporte_tabla():
    pass

#Fin métodos funcionales ///////////////////////////////////////////////////////////////


#Ejecución métodos
#pantalla_principal()
menú_principal()