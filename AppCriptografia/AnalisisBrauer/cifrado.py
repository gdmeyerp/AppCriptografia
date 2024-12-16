import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph


def ejecutarAnalisis(mensaje, longitud):

    #Organizar entradas para el analisis
    mensaje_min = mensaje.lower().replace(' ', '')
    mensaje_min = np.array(list(mensaje_min))
    letras = np.array(list(set(mensaje_min)))
    longitud = int(longitud)
    try:
        if len(mensaje_min)%longitud != 0:
            raise ValueError('La longitud de las palabras no divide a la longitud del mensaje. Revise e intente de nuevo')
        mensaje_partido = np.array_split(mensaje_min, len(mensaje_min)/longitud)
    except Exception as e:
        ValueError('No se puede hacer el analisis de Brauer')

    # Secuencia de Sucesores
    sucesiones = getSucesiones(mensaje_partido, letras)

    # Carcaj de Brauer
    grafo, isGrafoConnected, numberOfSelfEdges, img_bytes = getGrafo(mensaje_partido, sucesiones, letras)

    # Calculo de Val(alpha)(val(alpha)u(alpha)-1)
    valu = getValU(sucesiones)

    # Calculo de las dimensiones
    if isGrafoConnected:
        dimension_val = dimension(mensaje_partido, valu)
    else: 
        dimension_val = 0
    dimension_centro_val = dimension_centro(mensaje_partido, numberOfSelfEdges)

    return sucesiones, dimension_val, dimension_centro_val, img_bytes


def getSucesiones(mensaje_partido, letras):
    sucesiones = []
    for letra in letras:
        sucesion = []
        for i in range(len(mensaje_partido)):
            if letra in mensaje_partido[i]:
                veces = np.count_nonzero(mensaje_partido[i] == letra)
                for j in range(veces):
                    sucesion.append(f'W{i+1}')
        sucesiones.append(sucesion)
    return sucesiones


def getGrafo(mensaje_partido, sucesiones, letras):
    G = nx.MultiDiGraph()
    numberOfSelfEdges = 0
    for i in range(len(mensaje_partido)):
        G.add_node(f'W{i+1}')
    for sucesion in sucesiones:
        for i in range(len(sucesion)):
            if i == len(sucesion) - 1:
                G.add_edge(sucesion[i], sucesion[0])
                if sucesion[i] == sucesion[0]:
                    numberOfSelfEdges = numberOfSelfEdges + 1
            else:
                G.add_edge(sucesion[i], sucesion[i+1])
                if sucesion[i] == sucesion[i+1]:
                    numberOfSelfEdges = numberOfSelfEdges + 1
    G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
    G.graph['graph'] = {'scale': '3'}
    A = to_agraph(G)
    A.layout('dot')
    img_bytes = A.draw(format="png")
    #A.draw('AppCriptografia/static/images/grafo.png')
    G_undirec = G.to_undirected()
    return G, nx.is_connected(G_undirec), numberOfSelfEdges, img_bytes


def getValU(sucesiones):
    result = 0
    for sucesion in sucesiones:
        val = len(sucesion)
        if val == 1:
            u = 2
        else:
            u = 1
        result = result + val*(val*u -1)
    return result


def dimension(mensaje_partido, valu):
    dimension = 2*len(mensaje_partido) + valu
    return dimension


def dimension_centro(mensaje_partido, numberOfSelfEdges):
    dimension_centro = 1 + len(mensaje_partido) + numberOfSelfEdges
    return dimension_centro


# ejecutarAnalisis('rmepattunboiuearnaarsiyl', '4')