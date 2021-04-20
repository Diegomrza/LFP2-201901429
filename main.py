import time, os
from tkinter import Tk, filedialog
from gramaticas import gramaticas
from graphviz import Digraph

lista_de_gramaticas = [] #Todas las gramáticas leídas
gramaticas_libres_de_contexto = [] #Sólo las gramáticas libres de contexto
contador_imagenes = 0

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
            #print('Usted eligió la opción uno')
            cargar_archivo()
            #os.system('cls')

        elif int(opcion) == 2:
            print()
            #print('Usted eligió la opción dos')
            #os.system('cls')
            Mostrar_inf()

        elif int(opcion) == 3:
            print()
            #print('Usted eligió la opción tres')
            #os.system('cls')
            generar_automata_pila()

        elif int(opcion) == 4:
            print()
            #print('Usted eligió la opción cuatro')
            #os.system('cls')
            reporte_recorrido()

        elif int(opcion) == 5:
            print()
            #print('Usted eligió la opción cinco')
            os.system('cls')

        elif int(opcion) == 6:
            print()
            #print('Usted eligió la opción seis(Salir)')
            os.system('cls')
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
    global gramaticas_libres_de_contexto
    
    for gramaticas in lista_de_gramaticas:
        if gramaticas.tipo != 'Regular':
            gramaticas_libres_de_contexto.append(gramaticas)

    print('\nLista de gramáticas existentes: \n')
    cont = 0
    for gram in gramaticas_libres_de_contexto:
        print('\t',cont,'. ', gram.nombre)
        cont += 1
    seleccion = int(input('\nSeleccione una gramática\n>>'))
    os.system('cls')
    for x in gramaticas_libres_de_contexto:
        if x.nombre == gramaticas_libres_de_contexto[seleccion].nombre: 
            print('\nNombre: ', x.nombre)
            print('No Terminales= {',end='')
            for a in x.no_terminales:
                print(a,',', end='')
            print('}')
            print('Terminales= {',end='')
            for b in x.terminales:
                print(b,',',end='')
            print('}')
            print('No terminal inicial= ', x.terminal_inicial)
            print('Tipo: ', x.tipo)
            print('Producciones: ')
            terminalActual = ''
            for x in x.producciones:
                if terminalActual != x[0]:
                    print(x[0],'-> ', end='')
                    lisita = x[1]        
                    for y in lisita:
                        for z in y:
                            print(z,' ',end='')
                    print()
                else:
                    print('| ', end='')
                    lisita = x[1]        
                    for y in lisita:
                        for z in y:
                            print(z,' ',end='')
                    print()
                terminalActual = x[0]
                print()

def generar_automata_pila():
    global gramaticas_libres_de_contexto, contador_imagenes
    cadena_html = '''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte</title>
        <style>
            #imagen{ width: 720px;margin: 0 auto; }
            #informacion{ margin: 0 auto;width: 720px;height: 300px; }
        </style>
        </head>
            <body>
                <div id="informacion">
                    '''
    #########################################
    gram = None
    indice = 0
    for g in gramaticas_libres_de_contexto:
        print('\t',indice, '. ' ,g.nombre)
        indice += 1

    busqueda = int(input('\tSeleccione una gramática:\n\t>>'))
    for x in gramaticas_libres_de_contexto:
        if x.nombre == gramaticas_libres_de_contexto[busqueda].nombre:
            gram = x
        
    labeel = ''
    for x in gram.producciones:
        cad = ''
        labeel += 'λ,' + x[0] + ';'
        lisita = x[1]        
        for y in lisita:
            for z in y:
                cad += z +' '
        labeel+=cad +'\n'
    labeel +='\n'
    for x in gram.terminales:
        labeel += x+','+x +';'+'λ\n'

    g = Digraph ('G', format='png')
    g.attr(rankdir='LR')
    g.node('f',shape='doublecircle')
    g.edge('i','p', label='λ,λ;#')
    g.edge('p','q',label='λ,λ;'+gram.terminal_inicial)
    g.edge('q','q',label=labeel)
    g.edge('q','f',label='λ,#;λ')
    nombregrafo = 'grafo'+str(contador_imagenes)
    g.render(nombregrafo)
    contador_imagenes += 1
    ############################################
    terminales_hmtl = ''
    for h in gram.terminales:
        terminales_hmtl += ' '+h+','

    no_terminales_html = terminales_hmtl
    for i in gram.no_terminales:
        no_terminales_html += ' '+i + ','
    
    no_terminales_html+=' #'

    cadena_html += '<h1>Nombre: AP_'+gram.nombre+'</h1>'
    cadena_html += '<h2>Terminales ='+'{'+terminales_hmtl.rstrip(',')+' }'+'</h2>'
    cadena_html += '<h2>Alfabeto de pila ='+'{'+no_terminales_html.rstrip(',')+' }'+'</h2>'
    cadena_html += '''
                    <h2>Estados = { i, p, q, f }</h2>
                    <h2>Estado inicial = { i }</h2>
                    <h2>Estado de aceptacion = { f }</h2>
                </div>
                <div id="imagen">'''
    
    cadena_html += '<img src="'+ nombregrafo +'.png'+'">'
    
    cadena_html+='''
                </div>
            </body>
        </html>'''

    hmtl = open('Automata pila.html','w')
    hmtl.writelines(cadena_html)

    gram.idImagen = nombregrafo+'.png'
    gram.nombre = 'AP_'+gram.nombre

def reporte_recorrido():
    for x in gramaticas_libres_de_contexto:
        if x.idImagen != None:
            print(x.nombre)
            print(x.idImagen)
    

def reporte_tabla():
    pass

#Fin métodos funcionales ///////////////////////////////////////////////////////////////


#Ejecución métodos
#pantalla_principal()
menú_principal()