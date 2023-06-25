from decimal import Decimal
from fractions import Fraction
import time
import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt

#On transforme la liste d'adjacence du fichier liste.txt en un graphe networkx
def liste_to_graph_oriented(file):
    G = nx.DiGraph()
    with open(file) as f:        
        #On compte le nombre de ligne
        index_sommet = sum(1 for line in f) + 1
        global nb_sommet_original
        nb_sommet_original = index_sommet -1
        f.seek(0, 0)

        for line in f:
            line = line.split(sep=" ")
            i = 1
            nb_choice = line.count("-1.0")
            while i < len(line)-1:
                    if line[i] == str(-1.0):
                        #Alors on a un nouveau choix, on vérifie si c'est un choix unique ou si il y'a des prob et dans ce cas là on crée un sommet average
                        if line[i+1] == str(1.0):
                            #On a un choix de prob 1 donc on peut directement connecter les sommets
                            G.add_edge(int(line[0])+1, int(line[i+2][:-2]) +1, weight=1)
                            #print("On a crée l'arête ", int(line[0])+1, int(line[i+2][:-2]) +1)
                            i += 3
                        else:
                            #On a un choix de proba différente de 1 donc on crée un sommet average que l'on connecte au sommet de début de ligne
                            G.add_node(index_sommet)
                            nx.set_node_attributes(G, {index_sommet: {"label": "average"}})
                            G.add_edge(int(line[0]) + 1, index_sommet, weight=1)
                            #print("On a crée l'arête ", int(line[0])+1, index_sommet)
                            i+=1

                            #On connecte le sommet average aux sommets suivants
                            while i< len(line)-1 and line[i] != str(-1.0):
                                G.add_edge(index_sommet, int(line[i+1][:-2]) + 1, weight= Fraction(round(float(line[i]), 6)).limit_denominator(10))
                                #print("On a crée l'arête ", index_sommet,"->", int(line[i+1][:-2]) + 1, "de poids ", Fraction(round(float(line[i]), 6)).limit_denominator(100000))
                                i+=2
                            #La valeur du sommet average est la moyenne des valeurs des sommets successeurs

                            index_sommet += 1


    return G

"""
Parcours le fichier info.txt généré depuis le dossier prism games et ajoute les labels et les valeurs aux sommets du graphe G
"""
def identify_node(G):
    f = open("./info.txt", "r")
    first_line = f.readline()
    dict1 = {}    
    dict2 = {}
    dict3 = {}
    for line in f:
        line = line.split(sep=" ")
        dict_label = {}
        dict_value = {}
        dict_original_value = {}
        dict_label["label"] = str(line[1])
        dict_value["value"] = Fraction(int(line[2]))
        dict_original_value["original_value"] = str(line[0])
        dict1[int(line[0])+1] = dict_label
        dict2[int(line[0])+1] = dict_value
        dict3[int(line[0])+1] = dict_original_value

    nx.set_node_attributes(G, dict1)
    nx.set_node_attributes(G, dict2)
    nx.set_node_attributes(G, dict3)
    # Maintenant on va parcourir le graphe et pour chaque sommet de label average on va calculer sa valeur
    for node in G.nodes():
        if G.nodes[node]["label"] == "average":
            value = Fraction(0)
            G.nodes[node]["original_value"] = "-1"
            for successor in G.successors(node):
                #break si le successeur est sink
                if G.nodes[successor]["value"] == -1:
                    value = -1
                    break
                value += G[node][successor]["weight"] * Fraction(float(G.nodes[successor]["value"]))
            nx.set_node_attributes(G, {node: {"value": value}})





"""
On transforme un graphe de networkX en un fichier mygraph.gr
"""
def undirected_graph_to_file_gr(G):
    #On crée un index pour chaque sommet
    nx.set_node_attributes(G, 0, "index")
    index = 1
    for node in G.nodes():
        G.nodes[node]["index"] = index
        index += 1
    
    


    f = open("undirected_graph.gr", "a")
    f.truncate(0) #On vide le fichier
    f.write("p tdp " + str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
        f.write(str(G.nodes[edge[0]]["index"]) + " " + str(G.nodes[edge[1]]["index"]) + "\n")


    f.close()
    return 0

def directed_graph_to_file_gr(G):
    #On crée un index pour chaque sommet
    nx.set_node_attributes(G, 0, "index")
    index = 1
    for node in G.nodes():
        G.nodes[node]["index"] = index
        index += 1

    f = open("directed_graph.gr", "a")
    f.truncate(0) #On vide le fichier
    f.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "0\n")

    for node in sorted(G.nodes(), key=lambda node: G.nodes[node]["index"]):
        for successor in G.successors(node):
            f.write(str(G.nodes[successor]["index"]) + " ")
        f.write("\n")
    f.close()
    return 0