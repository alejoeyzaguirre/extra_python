#PREGUNTA 1: LLAVES

import time
import string

def numero_espadas(mapa):
    # Cada elemento en las listas corresponde a el número de espadas no usadas o bestias no matadas
    # del tipo "letra".EXPLICAR EN CUADRO DE TEXTO.

    espadas_sobrantes = [0 for _ in range(26)]
    bestias_no_matadas = [0 for _ in range(26)]

    for i in range(0, len(mapa), 2):

        espada = mapa[i]
        bestia = mapa[i + 1]

        if espada.upper() != bestia:

            espadas_sobrantes[ord(espada) - 97] += 1

            if espadas_sobrantes[ord(bestia) - 65] > 0:
                espadas_sobrantes[ord(bestia) - 65] = espadas_sobrantes[ord(bestia) - 65] - 1

            else:
                bestias_no_matadas[ord(bestia) - 65] += 1

    return sum(bestias_no_matadas)


#PREGUNTA 2.A:

#NECESARIO INSTALAR LA SIGUIENTE LIBRERÍA...
#!pip3 install astar==0.92

#from astar import AStar
#import math


#class Astar_Caballo(AStar):
#    """
#    La clase Astar_Caballo hereda de la clase AStar. Astar_Caballo recibe como input solamente el mapa.
#
#    """
#
#    def __init__(self, mapa_caballo):
#        super().__init__()
#        self.mapa_caballo = mapa_caballo
#        self.ancho = len(mapa_caballo[0])
#        self.alto = len(mapa_caballo)

#    def neighbors(self, node):
#        """
#        node es tupla (f, c) que representa un elemento de la matriz.
#        Evalúo quienes son los vecinos del nodo, teniendo mucho ojo en no entregar "vecinos out of range"
#        especialmente en los bordes de la matriz.
#        """
#        f_0, c_0 = node
#        validos = []
#        for delta_f in range(-1, 2):
#            for delta_c in range(-1, 2):
#                f_1 = f_0 + delta_f
#                c_1 = c_0 + delta_c
#                if f_1 >= 0 and f_1 < self.alto and c_1 >= 0 and c_1 < self.ancho and (f_1, c_1) != node:
#                    validos.append((f_1, c_1))
#        return validos

#    def distance_between(self, n1, n2):
#        """
#        Calculo la distancia entre cada nodo, en este ejercicio en particular la "distancia" estaba
#        determinada por la diferencia de alturas entre cada nodo, o mejor dicho cada punto de la matriz.
#        """
#        f1, c1 = n1
#        f2, c2 = n2
#        if self.mapa_caballo[f2][c2] > self.mapa_caballo[f1][c1]:
#            costo = self.mapa_caballo[f2][c2] - self.mapa_caballo[f1][c1] + 1
#        else:
#            costo = 1
#        return costo

#    def heuristic_cost_estimate(self, n1, n2):
#        """
#        La heurística (que diferencia A* de Djiskstra) que se utiliza es la Distancia Euclidiana entre
#        dos tuplas (n1 y n2). Se normaliza por raíz de dos para poder asegurarnos que la heurística entre
#        dos nodos es siempre menor o igual a el costo de trasladarse entre dos nodos.
#        """
#        (f1, c1) = n1
#        (f2, c2) = n2
        # Retorno la distancia euclidiana entre ambos nodos, y normalizo las diagonales dividiendo por raíz de 2.
#        return (math.hypot(f2 - f1, c2 - c1) / math.sqrt(2))

#    def is_goal_reached(self, current, goal):
#        """
#        Esta función evalúa si el nodo actual es el nodo de destino (goal), si es así entonces A*
#        finaliza su trabajo.
#        """
#        if current == goal:
#            return True


#def ruta_de_jaime(origen, destino, mapa):
#    """
#    Encuentro primero el camino que recorre nuestro caballo según A*. En cada nodo inspecciona el costo
#    agregado (heurística más costo energía caballo) de moverse hacia cada vecino. Avanza hacia el nodo
#    con el menor costo.
#    Luego se calcula la energía consumida por el caballo al recorrer este camino.
#    """
#    camino = list(Astar_Caballo(mapa).astar(origen, destino))
#    energia = 0
#    for i in range(len(camino) - 1):
#        f0, c0 = camino[i]
#        f1, c1 = camino[i + 1]
#        if mapa[f1][c1] > mapa[f0][c0]:
#            energia += mapa[f1][c1] - mapa[f0][c0] + 1
#        else:
#            energia += 1
#    return (camino, energia)


#PREGUNTA 2.B: LÖBEL FINDER

class Nodo:

    def __init__(self, padre, letra, frecuencia):
        self.letra = letra
        self.padre = padre
        self.frecuencia = frecuencia
        self.freq_pal = 0
        self.hijos = {}

    def __repr__(self):
        def recorrer_arbol(raiz, profundidad=0):
            for hijo in raiz.hijos.values():
                self.ret += "{}Arista: {} --> freq: {} ---> freq_pal= {} \n".format("\t"*profundidad, hijo.letra, hijo.frecuencia, hijo.freq_pal, self.letra)
                recorrer_arbol(hijo, profundidad+1)

        self.ret = 'HIJOS:\n'
        recorrer_arbol(self)
        return self.ret


def recursive_create(palabra, frecuencia, nodo):
    nodo.frecuencia = max(frecuencia, nodo.frecuencia)
    if len(palabra) == 0:
        nodo.freq_pal = frecuencia
        return

    letra = palabra[0]
    if not letra in nodo.hijos:
        nodo.hijos[letra] = Nodo(nodo, letra, 0)

    recursive_create(palabra[1:], frecuencia, nodo.hijos[letra])

def seleccion_pro(nodo, prefijo):
    if len(prefijo)!= 0:
        letra_p = prefijo[0]
        hijo = nodo.hijos[letra_p]
        ret = letra_p + seleccion_pro(hijo, prefijo[1:])
        return ret
    else:
        max_freq = 0
        max_hijo = None
        for hijo in nodo.hijos.values():
            if hijo.frecuencia > max_freq:
                max_freq = hijo.frecuencia
                max_hijo = hijo
        if max_hijo is not None and max_hijo.frecuencia > nodo.freq_pal:
            ret = max_hijo.letra + seleccion_pro(max_hijo, "")
            return ret
        return ""

def motor_lobel(prefijos, historico):
    #Primero creo arbol usando mi función recursive create.
    #creo raíz del árbol...
    raiz = Nodo(None, "", 0)
    for tupla in historico:
        frecuencia, palabra = tupla
        recursive_create(palabra, frecuencia, raiz)
    #Con el arbol creado selecciono la búsqueda más frecuente que parten con los prefijos entregados.
    lista = list()
    for prefijo in prefijos:
        try:
            lista.append(seleccion_pro(raiz, prefijo))
        except:
            lista.append(prefijo)
    return lista

from random import sample, randint

#def get_rec_info():
    # esta funcion retorna una lista con tuplas de la frecuencia y la frase asociada y
    # tambien una lista de prefijos asociada, para la cual deberian poder dar una
    # recomendacion en menos de 1.5 segundos (en colab).
    # es importante que el archivo 'info_recomendaciones.txt' este el la misma carpeta que
    # el script. En colab se pueden subir archivos con el navegador en la izquierda.

#    with open('info_recomendaciones.txt', 'r') as file:
#        ret = [(int(line[0]), ' '.join(line[2:])) for line in [l.strip().split() for l in file]]
#    prefijos = sample(list(set(pal[:randint(1,9*len(pal)//10)] for pal in [p[1] for p in ret])), 3000)
#    return ret, prefijos

#historico_2, prefijos_2 = get_rec_info()

#PREGUNTA 3: TRADUCTOR EXTRATERRESTRE

def estructura_pro(estructura):
    estructura = estructura.split(" ")
    return estructura

def movidas_validas(resultado_parcial, estructura, mensaje):
    # resultado parcial con forma [0, indice_termino_0, indice_termino_1, ...]
    # estructura es lista ["a", "b", "b", "c"]
    return list(range(1 + resultado_parcial[-1], 1 + len(mensaje) - len(estructura) + len(resultado_parcial)))


def es_valido(resultado_parcial, estructura, mensaje):
    # Es valido cuando el resultado parcial tiene un largo igual a estructura.
    if len(resultado_parcial) <= len(estructura):
        return True
    elif len(resultado_parcial) == (len(estructura) + 1) and resultado_parcial[-1] == len(mensaje):
        return True

    else:
        return False


class Elemento:

    def __init__(self, letra):
        self.letra = letra
        self.indices = []

    def agregar_indice(self, string):
        for i in range(len(string)):
            if string[i] == self.letra:
                self.indices.append(i)


def elementizar(estructura):
    dicc = dict()
    for elem in estructura:
        cosa = Elemento(elem)
        cosa.agregar_indice(estructura)
        dicc[elem] = cosa.indices
    return dicc

def parcial_lista(resultado_parcial, estructura, mensaje):
    lista = []
    lista.append(mensaje[0:resultado_parcial[1]])
    for i in range(1, len(resultado_parcial)-1):
        lista.append(mensaje[resultado_parcial[i]:resultado_parcial[i+1]])
    return lista

def formato_pedido(estructura, lista_de_slices):
    final = []
    for j in range(len(estructura)):
        if (estructura[j], lista_de_slices[j]) not in final:
            final.append((estructura[j], lista_de_slices[j]))
    return (tuple(final))


def es_estado_solucion(resultado_parcial, estructura, mensaje):
    if len(resultado_parcial) != (len(estructura) + 1) or resultado_parcial[-1] != (len(mensaje)):
        return False

    # Hago una lista que contiene cada slice del string correspondiente a cada letra de la estructura.
    lista = parcial_lista(resultado_parcial, estructura, mensaje)
    elementos = elementizar(estructura)

    # Reviso que los slices del tipo X sean iguales entre sí...
    for elem in elementos.values():
        seteo = set()
        for indiz in elem:
            agrego = lista[indiz]
            seteo.add(agrego)
        if len(seteo) > 1:
            return False

    return True


def resolver(resultado_parcial, estructura, mensaje):
    if not es_valido(resultado_parcial, estructura, mensaje):
        return False

    if es_estado_solucion(resultado_parcial, estructura, mensaje):
        return True

    else:
        for movida in movidas_validas(resultado_parcial, estructura, mensaje):
            resultado_parcial.append(movida)
            nuevo = resultado_parcial

            if resolver(nuevo, estructura, mensaje):
                lista = parcial_lista(resultado_parcial, estructura, mensaje)
                ret = formato_pedido(estructura, lista)
                return ret

            else:
                resultado_parcial.pop()
        return False

def traduccion(mensaje, estructura):
    estructura = estructura_pro(estructura)
    return resolver([0], estructura, mensaje)

