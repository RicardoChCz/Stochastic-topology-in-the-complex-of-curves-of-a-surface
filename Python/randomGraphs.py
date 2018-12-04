# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 11:40:57 2017

@author: Ricardo Esteban Chávez Cáliz
"""

import numpy as np

import networkx as nx
import matplotlib.pyplot as plt
from time import clock
from numpy import log
from numpy.random import rand
from numpy.random import randint

def Bernoulli(p):
    """
    Función que simula una v.a distribución Bernoulli con parámetro p
    Input: float
    Output: int (éxito ó fracaso)
    """
    M = rand(1)
    if p > 1 or p<0:
        raise ValueError("El parametro no es apropiado")
    if M < p:
        M=1
    else:
        M=0        
    return M

def erdosRenyi(n,p):
    """
    Devuelve una gráfica aleatoría del modelo Erdos Renyi con parámetros n y p
    Input: int n, float p en [0,1]
    Output: Objeto G de networkX
    """
    #Crea gráfica vacía
    G=nx.Graph()    
    #Añade n nodos
    G.add_nodes_from(list(range(0, n)))
    #Añade aristas según e reultado de v.a. ~ Bernoulli(p)
    for i in range(0,n):
        for j in range(i+1,n):
            if Bernoulli(p)==1:
                G.add_edge(i,j)                            
    return G

def conexidad(n,p,M):
    """
    Estima la probabilidad de obtener una gráfica aleatoria conexa en G(n,p)
    Input: int n, float p entre 0 y 1, int M - número de repeticiones
    Output: float (probabilidad estimada)
    """
    r=0.0
    for i in range(0,M):
        G=erdosRenyi(n,p)
        if nx.is_connected(G)==True:
            r=r+1
    return r/M

def generate(G):
    """
    Simula una caminata aleatoría simple en G, y obtiene un árbol usando el
    algoritmo generate.
    Input: Gráfica G (objeto en python de networkX)
    Output: Árbol T (objeto en python de networkX)
    """
    V=G.nodes()
    n=len(V)
    #punto inicial
    u = randint(n)
    Visitados = [u]
    T=nx.empty_graph(n)
    
    while len(Visitados) < n:    
        #Obtener v vecino aleatorio de u
        N=G.neighbors(u)
        N = list(N)
        k=len(N)
        v = N[randint(k)]        
        #Revisa si ya lo visitó
        if (v in Visitados)==False:
            Visitados.append(v)
            T.add_edge(u,v)
        #Actualiza el punto donde estás
        u=v
    
    return T
    
def graficaGrafos():
    """
    Grafica un conjunto de gráficas aleatorias Erdos-Renyi variando p, con n=10
    Input: ninguno
    Output: genera un archivo.png
    """
    r=3
    c=3
    k=1.0
    f, axarr = plt.subplots(r, c,figsize=(6, 6.3), dpi=80)
    for i in range(0,3):
        for j in range(0,3):
            G = erdosRenyi(10,(k/10))
            nx.draw_shell(G,node_size=50, node_color='#003366',ax=axarr[i, j])
            axarr[i, j].set_title('p = ' + str(int(k)) + "/10")
            k=k+1
    plt.savefig('Figures/ER-10.png')
    f.subplots_adjust(hspace=0.4)
    plt.show()

def graficaArboles(n):
    """
    Grafica un conjunto de árboles aleatorios con generate
    Input: int (n)
    Output: genera un archivo.png
    """
    r=4
    c=4
    f, axarr = plt.subplots(r, c,figsize=(6, 6), dpi=80)
    for i in range(0,4):
        for j in range(0,4):
            G = generate(nx.complete_graph(n))
            nx.draw_random(G,node_size=30, node_color='#006600',ax=axarr[i, j])
    plt.savefig('Figures/Arboles'+str(n)+'.png')
    plt.show()

        
if __name__ == "__main__":
    """
    Muestra de gráficas obtenidas con erdosRenyi
    """
    print ("Muestra de gráficas obtenidas con erdosRenyi")
    graficaGrafos()
    
    """
    Muestra de árboles obtenidos con algoritmo generate.
    """
    
    print ("Muestra de árboles obtenidos con algoritmo generate.")
    graficaArboles(8)
    
    """    
    Pruebas de tiempo para algoritmos
    """
    
    print ("Haciendo pruebas de tiempo para algoritmo erdosRenyi. Esto puede tardar un tiempo")
    R=1000
    T = np.arange(1, R+5, 5)    
    y1= np.zeros(len(T))
    j=0
    for t in T:
        tiempo_inicial = clock()
        erdosRenyi(t,0.5)
        y1[j] = clock() - tiempo_inicial
        j=j+1    
    fig, axarr = plt.subplots(1, 2, figsize=(6,3),dpi=80)
    axarr[0].plot(T, y1, linestyle='-', color='#003366', label="erdosRenyi")
    axarr[1].plot(T, log(y1), linestyle='-', color='#003366', label="erdosRenyi")
    axarr[0].set_title('Escala normal')    
    axarr[1].set_title('Escala logaritmica')
    axarr[0].set_ylabel('Tiempo')
    axarr[0].set_xlabel('Tamano de la grafica')
    axarr[1].set_xlabel('Tamano de la grafica')
    plt.savefig("Figures/Times-ER.png")
    plt.show()
    print ("Haciendo pruebas de tiempo para algoritmo generate. Esto puede tardar un tiempo")
    R=1000
    T = np.arange(1, R+5, 5)    
    y1= np.zeros(len(T))
    j=0
    for t in T:
        tiempo_inicial = clock()
        generate(nx.complete_graph(t))
        y1[j] = clock() - tiempo_inicial 
        j=j+1
    fig, axarr = plt.subplots(1, 2, figsize=(6,3),dpi=80)
    axarr[0].plot(T, y1, linestyle='-', color='#006600', label="Generate")
    axarr[1].plot(T, log(y1), linestyle='-', color='#006600', label="Generate")
    axarr[0].set_title('Escala normal')    
    axarr[1].set_title('Escala logaritmica')
    axarr[0].set_ylabel('Tiempo')
    axarr[0].set_xlabel('Tamano de la grafica')
    axarr[1].set_xlabel('Tamano de la grafica')
    plt.savefig("Figures/Time-generate.png")
    plt.show()