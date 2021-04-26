import time, os
from tkinter import Tk, filedialog
from gramaticas import gramaticas
from graphviz import Digraph
from automatasDePila import AutomataPila
import webbrowser as wb

lista_de_gramaticas = [] #Todas las gramáticas leídas
gramaticas_libres_de_contexto = [] #Sólo las gramáticas libres de contexto
automatas_pila = [] #Contendrá todos los autómatas generados en la opción 3
contador_imagenes = 0
contadorReporteRecorrido = 0

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
            cargar_archivo()
            os.system('cls')

        elif int(opcion) == 2:
            print()
            os.system('cls')
            Mostrar_inf()
            os.system('cls')

        elif int(opcion) == 3:
            print()
            os.system('cls')
            generar_automata_pila()

        elif int(opcion) == 4:
            print()
            os.system('cls')
            reporte_recorrido()

        elif int(opcion) == 5:
            print()
            os.system('cls')
            reporte_tabla()

        elif int(opcion) == 6:
            print()
            #print('Usted eligió la opción seis(Salir)')
            os.system('cls')
            exit()

#Fin métodos visuales -------------------------------------------------------------------


#Métodos funcionales ////////////////////////////////////////////////////////////////////

def cargar_archivo():
    global lista_de_gramaticas
    global gramaticas_libres_de_contexto

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

    for gramatica in lista_de_gramaticas:
        if gramatica.tipo != 'Regular':
            gramaticas_libres_de_contexto.append(gramatica)

def Mostrar_inf():
    global lista_de_gramaticas
    global gramaticas_libres_de_contexto
    
    print('\n<!-- --> Lista de gramáticas existentes: <!-- -->\n')
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
    time.sleep(5)

def generar_automata_pila():
    global gramaticas_libres_de_contexto, contador_imagenes, automatas_pila
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
    os.system('cls')

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

    #Grafo
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

    html = open('Automata pila.html','w')
    html.writelines(cadena_html)
    html.close()

    wb.open_new(r'Automata pila.html')

    nuevo = AutomataPila('AP_'+gram.nombre)
    nuevo.id = nombregrafo+'.png'
    nuevo.no_terminales = gram.no_terminales
    nuevo.terminales = gram.terminales
    nuevo.producciones = gram.producciones
    nuevo.terminal_inicial = gram.terminal_inicial

    automatas_pila.append(nuevo)

    #gram.idImagen = nombregrafo+'.png'
    #gram.nombre = 'AP_'+gram.nombre

def reporte_recorrido():
    global automatas_pila
    gramaticaAux = None
    contadorAutomatas = 0
    for g in automatas_pila:
        print('\t',contadorAutomatas,'. '+ g.nombre)
        contadorAutomatas += 1
    elegirAutomataDePila = int(input('Seleccione una gramática:\n>>'))
    os.system('cls')

    for x in automatas_pila:
        if x.nombre == automatas_pila[elegirAutomataDePila].nombre:
            gramaticaAux = x
            
    cadena = input('Ingrese una cadena para analizar: ')
    #print('Su cadena es esta: ', cadena)
    
    tamaño_cadena = len(cadena)
    i = 0
    pila=[]
    estado='i'
    #no_terminal_inicial = gramaticaAux.terminal_inicial

    alfabetoPila = gramaticaAux.no_terminales

    for x in gramaticaAux.terminales:
        alfabetoPila[x] = 'terminal'

    alfabetoPila['#'] = 'terminal'


    produccionsPila = {}
    for y in gramaticaAux.producciones:
        cadenita = ''
        for z in y[1]:
            for u in z:
                cadenita += u+','
        produccionsPila[cadenita.rstrip(',')] = y[0]

    

    print(alfabetoPila)
    print(produccionsPila)

    Rhmtl = '''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recorrido</title>
        </head>
            <body>'''

    while i <= tamaño_cadena:
        if estado == 'i':
            pila.insert(0,'#')
            estado = 'p'
            #print('Pila: ',pila)
            nombre = estado_i(gramaticaAux) ##
            Rhmtl += '''<div>'''
            Rhmtl += '<img src="'+nombre+'" alt="">'
            Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
            Rhmtl += '<td>'+ ''.join(pila) +'</td>'
            Rhmtl +='''</tr>
                <tr>
                <td>Entrada</td>'''
            Rhmtl += '<td></td>'
            Rhmtl += '''
                </tr>
                </table>
                </div>'''

        elif estado == 'p':
            no_terminal_inicial0 = gramaticaAux.terminal_inicial
            pila.insert(0,no_terminal_inicial0)
            estado = 'q'
            #print('Pila: ',pila)
            nombre = estado_p(gramaticaAux) ##
            Rhmtl += '''<div>'''
            Rhmtl += '<img src="'+nombre+'" alt="">'
            Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
            Rhmtl += '<td>'+ ''.join(pila) +'</td>'
            Rhmtl +='''</tr>
                <tr>
                <td>Entrada</td>'''
            Rhmtl += '<td></td>'
            Rhmtl += '''
                </tr>
                </table>
                </div>'''

        elif estado == 'q':
            inicio_pila = pila[0]
            if i < tamaño_cadena:
                caracterActual = cadena[i]
            if alfabetoPila[inicio_pila] == 'no terminal':
                for x in produccionsPila:
                    derecha = x.split(',')
                    if (produccionsPila[x] == inicio_pila) and (len(derecha) != 1):
                        if cadena[i] == derecha[0]:
                            pila.remove(inicio_pila)           
                            for cad in reversed(derecha):
                                if cad != '':
                                    pila.insert(0,cad)
                            nombre = estado_q(gramaticaAux) ##
                            Rhmtl += '''<div>'''
                            Rhmtl += '<img src="'+nombre+'" alt="">'
                            Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
                            Rhmtl += '<td>'+ ''.join(pila) +'</td>'
                            Rhmtl +='''</tr>
                            <tr>
                            <td>Entrada</td>'''
                            Rhmtl += '<td>'+caracterActual+'</td>'
                            Rhmtl += '''
                            </tr>
                            </table>
                            </div>'''
                            break
                        elif produccionsPila == inicio_pila:
                            pila.remove(inicio_pila)
                            for cad in reversed(derecha):
                                if cad != '$' and cad != '':
                                    print('x')
                                    pila.insert(0,cad)
                            nombre = estado_q(gramaticaAux) ##
                            Rhmtl += '''<div>'''
                            Rhmtl += '<img src="'+nombre+'" alt="">'
                            Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
                            Rhmtl += '<td>'+ ''.join(pila) +'</td>'
                            Rhmtl +='''</tr>
                            <tr>
                            <td>Entrada</td>'''
                            Rhmtl += '<td>'+caracterActual+'</td>'
                            Rhmtl += '''
                            </tr>
                            </table>
                            </div>'''
                            #print('Pila: ',pila)
                            break

                    elif produccionsPila[x] == inicio_pila and len(derecha) == 1:
                        pila.remove(inicio_pila)
                        if x != '$':
                            pila.insert(0,x)  
                        #print('Pila: ',pila)
                        nombre = estado_q(gramaticaAux) ##
                        Rhmtl += '''<div>'''
                        Rhmtl += '<img src="'+nombre+'" alt="">'
                        Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
                        Rhmtl += '<td>'+ ''.join(pila) +'</td>'
                        Rhmtl +='''</tr>
                        <tr>
                        <td>Entrada</td>'''
                        Rhmtl += '<td>'+caracterActual+'</td>'
                        Rhmtl += '''
                        </tr>
                        </table>
                        </div>'''
                        break
                
            elif alfabetoPila[inicio_pila] == 'terminal' and inicio_pila != '#':

                if caracterActual == inicio_pila:
                    pila.pop(0)
                    i+=1
                    #print('Pila: ',pila)
                    nombre = estado_q(gramaticaAux) ##
                    Rhmtl += '''<div>'''
                    Rhmtl += '<img src="'+nombre+'" alt="">'
                    Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
                    Rhmtl += '<td>'+ ''.join(pila) +'</td>'
                    Rhmtl +='''</tr>
                            <tr>
                            <td>Entrada</td>'''
                    Rhmtl += '<td></td>'
                    Rhmtl += '''
                            </tr>
                            </table>
                            </div>'''
                else:
                    print('Error, cadena no aceptada')
                    Rhmtl += '''<div>'''
                    Rhmtl += '<img src="'+nombre+'" alt="">'
                    Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
                    Rhmtl += '<td>'+ ''.join(pila) +'</td>'
                    Rhmtl +='''</tr>
                            <tr>
                            <td>Entrada</td>'''
                    Rhmtl += '<td></td>'
                    Rhmtl += '''
                            </tr>
                            </table>
                            <p>Cadena Rechazada</p>
                            </div>'''
                    break

            elif caracterActual==cadena[tamaño_cadena-1] and inicio_pila == '#':
                pila.pop(0)
                estado='f'
                #print('Pila: ',pila)
            elif caracterActual==cadena[tamaño_cadena-1] and inicio_pila == '#' and i != tamaño_cadena:
                Rhmtl += '<div><p>Cadena rechazada</p></div>'
                print('Cadena Rechazada')
                break
        elif estado == 'f':
            #print('Pila: ',pila)
            print('Cadena Aceptada')
            nombre = estado_f(gramaticaAux) ##
            Rhmtl += '''<div>'''
            Rhmtl += '<img src="'+nombre+'" alt="">'
            Rhmtl += '''<table border='1'><tr><td>Pila</td>'''
            Rhmtl += '<td>'+ ''.join(pila) +'</td>'
            Rhmtl +='''</tr>
                            <tr>
                            <td>Entrada</td>'''
            Rhmtl += '<td></td>'
            Rhmtl += '''
                            </tr>
                            </table>
                            <p>Cadena Aceptada</p>
                            </div>'''
            break
    
    if estado != 'f':
        Rhmtl += '<div><p>Cadena Rechazada</p></div>'

    print(pila)
    archivoHtml = open('reporteRecorrido.html', 'w')

    
    Rhmtl+='</body></html>'

    archivoHtml.write(Rhmtl)

    archivoHtml.close()

    wb.open_new(r'reporteRecorrido.html')
            
def reporte_tabla():
    global automatas_pila
    gramaticaAux = None
    contadorAutomatas = 0
    for g in automatas_pila:
        print('\t',contadorAutomatas,'. '+ g.nombre)
        contadorAutomatas += 1
    elegirAutomataDePila = int(input('Seleccione una gramática:\n>>'))
    os.system('cls')

    for x in automatas_pila:
        if x.nombre == automatas_pila[elegirAutomataDePila].nombre:
            gramaticaAux = x
            
    cadena = input('Ingrese una cadena para analizar: ')
    
    tamaño_cadena = len(cadena)
    i = 0
    pila=[]
    estado='i'
    alfabetoPila = gramaticaAux.no_terminales

    for x in gramaticaAux.terminales:
        alfabetoPila[x] = 'terminal'

    alfabetoPila['#'] = 'terminal'

    produccionsPila = {}
    for y in gramaticaAux.producciones:
        cadenita = ''
        for z in y[1]:
            for u in z:
                cadenita += u+','
        produccionsPila[cadenita.rstrip(',')] = y[0]

    Thtml = '''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tabla</title>
        </head>
            <body>
            <div>
            <table border='1'>
            <tr>
                <td>Iteración</td>
                <td>Pila</td>
                <td>Entrada</td>
                <td>Transiciones</td>
            </tr>'''

    contadorTransiciones = 0

    while i <= tamaño_cadena:
        if estado == 'i':
            pila.insert(0,'#')
            estado = 'p'

            Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td></td><td>(i, $, $;p,#)</td></tr>'
            contadorTransiciones += 1
            print('Pila: ',pila)

        elif estado == 'p':
            no_terminal_inicial0 = gramaticaAux.terminal_inicial
            pila.insert(0,no_terminal_inicial0)
            estado = 'q'

            Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td></td><td>(p, $, $;q,'+gramaticaAux.terminal_inicial+')</td></tr>'
            contadorTransiciones += 1

            print('Pila: ',pila)
        elif estado == 'q':
            inicio_pila = pila[0]
            if i < tamaño_cadena:
                caracterActual = cadena[i]
            if alfabetoPila[inicio_pila] == 'no terminal':
                for x in produccionsPila:
                    derecha = x.split(',')
                    if (produccionsPila[x] == inicio_pila) and (len(derecha) != 1):
                        if cadena[i] == derecha[0]:
                            pila.remove(inicio_pila)           
                            for cad in reversed(derecha):
                                if cad != '':
                                    pila.insert(0,cad)
                            Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>'+caracterActual+'</td><td>(q, $, $;q,'+''.join(derecha)+')</td></tr>'
                            contadorTransiciones += 1
                            print('Pila: ',pila)
                            break
                        elif produccionsPila == inicio_pila:
                            pila.remove(inicio_pila)
                            for cad in reversed(derecha):
                                if cad != '$' and cad != '':
                                    pila.insert(0,cad)
                            Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>'+caracterActual+'</td>'+'<td>(q, $, $;q,'+''.join(derecha)+')</td></tr>'
                            contadorTransiciones += 1
                            print('Pila: ',pila)
                            break
                    elif produccionsPila[x] == inicio_pila and len(derecha) == 1:
                        pila.remove(inicio_pila)
                        if x != '$':
                            pila.insert(0,x)
                        Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>'+caracterActual+'</td><td>(q, $, $;q,'+x+')</td></tr>'
                        contadorTransiciones += 1
                        print('Pila: ',pila)
                        break
            elif alfabetoPila[inicio_pila] == 'terminal' and inicio_pila != '#':
                if caracterActual == inicio_pila:
                    pila.pop(0)
                    i+=1
                    Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>'+caracterActual+'</td><td>(q,'+caracterActual+','+caracterActual+';q, $)</td></tr>'
                    contadorTransiciones += 1
                    print('Pila: ',pila)
                else:
                    print('Error, cadena no aceptada')
                    break
            elif caracterActual==cadena[tamaño_cadena-1] and inicio_pila == '#' and i == tamaño_cadena:
                pila.pop(0)
                estado='f'
                Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>$</td><td>(q, $,#;f, $)</td></tr>'
                contadorTransiciones += 1
                print('Pila: ',pila)
            elif caracterActual==cadena[tamaño_cadena-1] and inicio_pila == '#' and i != tamaño_cadena:
                print('Cadena rechazada')
                Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td>'+''.join(pila)+'</td><td>'+caracterActual+'</td><td>(q, $,#;f, $)</td></tr>'
                contadorTransiciones += 1
                break
        elif estado == 'f':
            print('Pila: ',pila)
            print('Cadena Aceptada')
            Thtml += '<tr><td>'+str(contadorTransiciones)+'</td><td></td><td>$</td><td>(q, $,#;f, $)</td></tr>'
            contadorTransiciones += 1
            break
    
    archivoHtml = open('TablaRecorrido.html', 'w')
    if estado == 'f':
        Thtml +='</table><p>Cadena Aceptada</p></div></body></html>'
    else:
        Thtml +='</table><p>Cadena Rechazada</p></div></body></html>'
    archivoHtml.write(Thtml)
    archivoHtml.close()

    wb.open_new(r'TablaRecorrido.html')


#Estados

def estado_i(gram):
    global contadorReporteRecorrido
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

    g =Digraph('G', format='png')
    g.attr(label='Imagen original')
    g.attr(rankdir='LR')

    g.node('i', color='yellow')
    g.node('p')
    g.node('q')
    g.node('f', shape='doublecircle')

    g.edge('i','p', label='λ,λ;#', fontcolor='red')
    g.edge('p','q',label='λ,λ;'+gram.terminal_inicial)
    g.edge('q','q',label=labeel)
    g.edge('q','f',label='λ,#;λ')

    nombre = 'rep'+str(contadorReporteRecorrido)
    g.render(nombre)
    contadorReporteRecorrido += 1

    return nombre+'.png'

def estado_p(gram):
    global contadorReporteRecorrido
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

    g =Digraph('G', format='png')
    g.attr(rankdir='LR')

    g.node('i')
    g.node('p',color='yellow')
    g.node('q')
    g.node('f', shape='doublecircle')

    g.edge('i','p', label='λ,λ;#')
    g.edge('p','q', label='λ,λ;'+gram.terminal_inicial, fontcolor='red')
    g.edge('q','q', label=labeel)
    g.edge('q','f', label='λ,#;λ')
    nombre = 'rep'+str(contadorReporteRecorrido)
    g.render(nombre)
    contadorReporteRecorrido += 1
    return nombre+'.png'

def estado_q(gram):
    global contadorReporteRecorrido
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

    g =Digraph('G', format='png')
    g.attr(rankdir='LR')

    g.node('i')
    g.node('p')
    g.node('q', color='yellow')
    g.node('f', shape='doublecircle')

    g.edge('i','p', label='λ,λ;#')
    g.edge('p','q', label='λ,λ;'+gram.terminal_inicial)
    g.edge('q','q', label=labeel, fontcolor='red')
    g.edge('q','f', label='λ,#;λ')
    nombre = 'rep'+str(contadorReporteRecorrido)
    g.render(nombre)
    contadorReporteRecorrido += 1

    return nombre+'.png'

def estado_f(gram):
    global contadorReporteRecorrido
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

    g =Digraph('G', format='png')
    g.attr(rankdir='LR')

    g.node('i')
    g.node('p')
    g.node('q')
    g.node('f', shape='doublecircle',color='yellow')

    g.edge('i','p', label='λ,λ;#')
    g.edge('p','q', label='λ,λ;'+gram.terminal_inicial)
    g.edge('q','q', label=labeel)
    g.edge('q','f',label='λ,#;λ', fontcolor='red')

    nombre = 'rep'+str(contadorReporteRecorrido)
    g.render(nombre)
    contadorReporteRecorrido += 1
    return nombre+'.png'


#Fin métodos funcionales ///////////////////////////////////////////////////////////////

#Ejecución métodos
pantalla_principal()
menú_principal()
