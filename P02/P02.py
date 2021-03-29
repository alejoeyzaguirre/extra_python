import P02_Lib as P02

archivo_red = 'red_ejemplo.txt'
red = P02.leer_red(archivo_red)

red_big_archivo = "red_grande.txt"
red_grande = P02.leer_red(red_big_archivo)

def con_bluetooth(red):
    lista_nodos = red[0]
    bolsa = set()
    for nodo in lista_nodos:
        if nodo[1] == 1:
            bolsa.add(nodo[0])
    return bolsa


from collections import defaultdict as df

# De la materia de clases.

class Nodo:
    def __init__(self, letra, bluetooth):
        self.letra = letra
        if bluetooth == 1:
            self.bluetooth = 1
        else:
            self.bluetooth = 0
        self.conexiones = []

    def add_vertex(self, letra):
        self.conexiones.append(letra)

    def __repr__(self):
        l = "Node: {} / Bluetooth: {}".format(self.letra, self.bluetooth)
        if len(self.conexiones) > 0:
            l += "-> (" + ",".join([c.__repr__() for c in self.conexiones]) + ") \n"
        return l


def nodicemos(tupla):
    nodo = Nodo(tupla[0], tupla[1])
    return nodo


# Creo un diccionario de los nodos, llave es self.letra

def recopilacion_nodos(red):
    df1 = df(lambda: "No está este nodo")
    for tupla in red[0]:
        df1[tupla[0]] = nodicemos(tupla)
    return df1


def agregado_de_conexiones(df1, red):
    for padre, hijo in red[1]:
        df1[padre].add_vertex(hijo)
    return df1


df1 = recopilacion_nodos(red)
df1 = agregado_de_conexiones(df1, red)


# backtracking...

def es_estado_solucion(actual, final):
    # Significa que avanzando por el grafo conectamos con el nodo 2.
    if actual.letra == final.letra:
        return True


def es_estado_valido(punto, final, camino):
    lista = camino[:-1]
    if len(camino) != 0:
        if punto not in lista and punto.bluetooth == 0 or punto == final:
            return True
        else:
            return False
    else:
        return True


def conexion(actual, final, df1, camino):
    if not es_estado_valido(actual, final, camino):
        return False

    if es_estado_solucion(actual, final):
        return True
    else:
        for hijo in actual.conexiones:
            actualizado = df1[hijo]
            camino.append(actualizado)
            if conexion(actualizado, final, df1, camino):
                return True

            else:
                camino.pop()

        return False


def conexion_inicio(actual, final, df1):
    camino = []
    ret = conexion(actual, final, df1, camino)

    return ret


# Probando para que me puede servir la librería itertools...


import itertools as it

set_blutu = con_bluetooth(red)


# Recibe un default_dict y el set_blutu que corresponde a todos los nodos que tienen bluetooth.
def itere(nodos_con_bluetooth, dicc):
    aristas = []
    seteo = set()
    for n1, n2 in it.permutations(nodos_con_bluetooth, 2):
        nodo_1 = dicc[n1]
        nodo_2 = dicc[n2]
        if conexion_inicio(nodo_1, nodo_2, dicc):
            l1, l2 = nodo_1.letra, nodo_2.letra
            aristas.append((l1, l2))
            seteo.add(l1)
            seteo.add(l2)

    puntos = []

    for elem in seteo:
        puntos.append((dicc[elem].letra, dicc[elem].bluetooth))

    lista_final = []

    lista_final.append(puntos)
    lista_final.append(aristas)

    return lista_final


def red_simplificada(red):
    df1 = recopilacion_nodos(red)
    df1 = agregado_de_conexiones(df1, red)
    set_blutu = con_bluetooth(red)
    return itere(set_blutu, df1)

red_simplificada(red)

red2 = [[('A', 1), ('B', 0), ('C', 0), ('D', 1)], [('A', 'C'), ('C', 'D'), ('B', 'D'), ('B', 'A')]]

red_simplificada(red2)

red_simplificada(red_grande)

