#!/usr/bin/env python
import networkx as nx
import math
import csv
import random as rand
import sys
import time
import community
import matplotlib.pyplot as plt

print (time.strftime("%I:%M:%S"))

#this method just reads the graph structure from the file
def buildG(G, file_, delimiter_):
    global Nodospajek
    Nodospajek = []
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("/home/kazem/Data/UCI/karate.txt"), delimiter=" ")
    reader = csv.reader(open(file_), delimiter=delimiter_)
    Arcos = 0
    cont = 0
    for line in reader:
        if Arcos == 0 and  line[0] != "*Arcs" and line[0] != "*vertices":
            Nodospajek.append(line)
        if Arcos == 1:
           if len(line) >  2:
              if float(line[2]) != 0.0:
                #line format: u,v,w
                G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))
           else:
                #line format: u,v
                G.add_edge(int(line[0]),int(line[1]),weight=1.0)
        if line[0] == "*Arcs" : Arcos = 1
            

def comunidad(G):
   Grupo = []
   #first compute the best partition

   partition = community.best_partition(G)
   values =  [partition.get(node) for node in G.nodes()]
   nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=60, with_labels=False)

   #drawing
   size = float(len(set(partition.values())))
   for i in range(int(size)): Grupo.append("")
   pos = nx.spring_layout(G)
   count = 0.
   comp = 0
   
   pr = nx.pagerank(G, alpha=0.9)
   lista = []
       
   for i in pr:
       lista.append(pr[i])
   
   
   for com in set(partition.values()):
       comp += 1
       count = count + 1.
       list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
       if comp/size > 0 and comp/size <= 0.05: colr = "white"
       if comp/size > 0.05 and comp/size <= 0.1:colr = "black", 
       if comp/size > 0.1 and comp/size <= 0.15:colr = "red"
       if comp/size > 0.15 and comp/size <= 0.2:colr = "blue"
       if comp/size > 0.2 and comp/size <= 0.25:colr = "orange"
       if comp/size > 0.25 and comp/size <= 0.3:colr = "green"
       if comp/size > 0.3 and comp/size <= 0.35:colr = "gray"
       if comp/size > 0.35 and comp/size <= 0.4:colr = "brown"
       if comp/size > 0.4 and comp/size <= 0.45:colr = "yellow"
       if comp/size > 0.45 and comp/size <= 0.5: colr = "cyan"
       if comp/size > 0.5 and comp/size <= 0.55: colr = "pink"
       if comp/size > 0.55 and comp/size <= 0.6: colr = "purple"
       if comp/size > 0.6 and comp/size <= 0.65:colr = "violet"
       if comp/size > 0.65 and comp/size <= 0.7:colr = "gold"
       if comp/size > 0.7 and comp/size <= 0.75:colr = "indigo"
       if comp/size > 0.75 and comp/size <= 0.8: colr = "lime"
       if comp/size > 0.8 and comp/size <= 0.85: colr = "silver"
       if comp/size > 0.85 and comp/size <= 0.9: colr = "tan"
       if comp/size > 0.9 and comp/size <= 0.95: colr = "fuchsia"
       if comp/size > 0.95 and comp/size <= 1: colr = "olive"
       nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 60, node_color = colr, with_labels=True)
       print ("Grupo:", comp, "tamano:", len(list_nodes) ,"nodos:", list_nodes)
       Grupo[comp-1] = list_nodes
       
       listamax = []
       
       for i in pr:
            lista.append(pr[i])
             
       #print("nodo mayor valor: ", max(lista))
       
       for i in range(len(list_nodes)):
		   listamax.append(lista[list_nodes[i]-1])
           #if (lista[i] == max(lista)):
           #    print("nodo;   ", i+1)

       for i in range(len(list_nodes)):
		   if lista[list_nodes[i]-1] == max(listamax):
			   print("nodo maximo ", list_nodes[i])
			   
       print("nodo mayor valor: ", max(listamax))
 
   print("numero de componentes", comp)
   mod = community.modularity(partition,G)
   print("modularidad:", mod)
   #print(Nodospajek)
   nx.draw_networkx_edges(G,pos, alpha=0.5)
   plt.show()
   pajek_group(G,Grupo)

def pajek_group(G, Grupos):
    print("comienza reduccion de grafo")

    #elimino nodos con grado cero.

    #nuevo experimento, miraremos si es igual al arrojado por nuestro algoritmo.

    B = nx.blockmodel(G,Grupos)

    #Re nombro los nodos para eliminar el nodo cero y que todo corresponda a los grupos encontrados en la funcion anterior.
    mapping = {} #variable que guardara el nuevo valor de nodos.
    cont = 0
    for i in B.nodes(): #creo diccionario que guarda el nuevo valor de nodos.
        mapping[cont] = cont + 1
        cont += 1

    A=nx.relabel_nodes(B,mapping) #asigno grafo con el nuevo valor de nodos.

   
    NodosBorrar = []
    cont_group = 1
    cont = 1
    for i in A.nodes():
        if A.degree(cont_group) != 0: 
           cont += 1
        if A.degree(cont_group) == 0: 
           NodosBorrar.append(cont_group)
        cont_group += 1
    

    for i in NodosBorrar: A.remove_node(i)
    Nodes = A.number_of_nodes()
    
    print "*vertices ", A.number_of_nodes()
    cont = 1
    for i in A.nodes():
		print cont,'"Grupo', i, '"'
		cont += 1 
    print "*Arcs"
    for i in A.edges(): print i[0], i[1], int(A[i[0]][i[1]]['weight'])
 
    pos = nx.spring_layout(A)
    labels={}
    cont = 1
    for i in A.nodes():
        colr = float(cont)/Nodes
        nx.draw_networkx_nodes(A, pos, [i] , node_size = 250, node_color = str(colr), with_labels=True)
        labels[i] = i
        cont += 1

    nx.draw_networkx_labels(A,pos,labels,font_size=5)        
    nx.draw_networkx_edges(A,pos, alpha=0.5)
    plt.show()
 
def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input graph>\n" % (argv[0],))
        return 1
    graph_fn = argv[1]
    G = nx.Graph()  #let's create the graph first
    buildG(G, graph_fn, ' ')
    
    Nodos = G.nodes()

    
    n = G.number_of_nodes()    #|V|
    A = nx.adj_matrix(G)    #adjacenct matrix

    m_ = 0.0    #the weighted version for number of edges
    for i in range(0,n):
        for j in range(0,n):
            m_ += A[i,j]
    m_ = m_/2.0
    #print ("m: %f" % m_)
        
    comunidad(G)
    
    print (time.strftime("%I:%M:%S"))

        

    #run Newman alg
    #runGirvanNewman(G, Orig_deg, m_)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
