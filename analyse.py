import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt




#On transforme la liste d'adjacence du fichier liste.txt en un graphe networkx
def liste_to_graph_oriented(file):
    G = nx.DiGraph()
    with open(file) as f:        
        #On compte le nombre de ligne
        index_sommet = sum(1 for line in f) + 1
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
                                G.add_edge(index_sommet, int(line[i+1][:-2]) + 1, weight=line[i])
                                #print("On a crée l'arête ", index_sommet,"->", int(line[i+1][:-2]) + 1, "de poids ", line[i])
                                i+=2
                            #La valeur du sommet average est la moyenne des valeurs des sommets successeurs

                            index_sommet += 1


    return G

"""
Parcours le fichier info.txt généré depuis le dossier prism games et ajoute les labels et les valeurs aux sommets du graphe G
"""
def identify_node(G):
    f = open("info.txt", "r")
    first_line = f.readline()
    dict1 = {}    
    dict2 = {}
    for line in f:
        line = line.split(sep=" ")
        dict_label = {}
        dict_value = {}
        dict_label["label"] = str(line[1])
        dict_value["value"] = int(line[2])
        dict1[int(line[0])+1] = dict_label
        dict2[int(line[0])+1] = dict_value
    nx.set_node_attributes(G, dict1)
    nx.set_node_attributes(G, dict2)
    # Maintenant on va parcourir le graphe et pour chaque sommet de label average on va calculer sa valeur
    for node in G.nodes():
        if G.nodes[node]["label"] == "average":
            value = 0
            for successor in G.successors(node):
                #break si le successeur est sink
                if G.nodes[successor]["value"] == -1:
                    value = -1
                    break
                value += float(G[node][successor]["weight"]) * float(G.nodes[successor]["value"])
            nx.set_node_attributes(G, {node: {"value": value}})


"""
Fusionne les sommets de label average qui ont les mêmes successeurs
"""
def fuse_average(G):
    dict = {}
    for node in G.nodes():
        if G.nodes[node]["label"] == "average":
            tuple_all = ()
            for successor in G.successors(node):
                tuple = (G[node][successor]["weight"], successor)
                tuple_all += tuple
            dict[tuple_all] = []
            dict[tuple_all].append(node)
    #Maintenant si deux sommets average ont les mêmes successeurs, on les fusionne
    for key in dict:
        if len(dict[key]) > 1:
            #On fusionne les sommets
            for i in range(1, len(dict[key])):
                G = nx.contracted_nodes(G, dict[key][0], dict[key][i])

"""
Transforme les sommets non sinks ayant une value (0 ou 1) en sommets sinks et supprime ses successeurs
"""
def vertex_to_sink(G):
    for node in G.nodes():
        if G.nodes[node]["label"] != "sink" and G.nodes[node]["value"] >= 0:
            G.nodes[node]["label"] = "sink"
            successors = list(G.successors(node))
            while len(successors) > 0:
                G.remove_edge(node, successors[0])
                successors = list(G.successors(node))
    return 0


"""
On supprime les sommets sinks qui n'ont pas de prédécesseurs ou qui ont pour predesseur eux-mêmes
"""
def remove_sink(G):
    to_delete = []
    for node in G.nodes():
        if len(list(G.predecessors(node))) == 0 or node in list(G.predecessors(node)):
            to_delete.append(node)
    print("On supprime les sommets sinks suivants : ", to_delete)
    G.remove_nodes_from(to_delete)
    return 0



"""
On transforme un graphe de networkX en un fichier mygraph.gr
"""
def undirected_graph_to_file_gr(G):
    f = open("undirected_graph.gr", "a")
    f.truncate(0) #On vide le fichier
    f.write("p tdp " + str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
        f.write(str(edge[0]) + " " + str(edge[1]) + "\n")


    f.close()
    return 0

def directed_graph_to_file_gr(G):
    f = open("directed_graph.gr", "a")
    f.truncate(0) #On vide le fichier
    f.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "0\n")
    for node in G.nodes():
        #On parcourt les voisins de node
        for neighbor in G.neighbors(node):
            f.write(str(neighbor) + " ")
        f.write("\n")

    f.close()
    return 0

def print_label(G):
    nb_max = 0
    nb_min = 0
    nb_sink_0 = 0
    nb_sink_1 = 0
    nb_average = 0
    for node in diG.nodes():
        if diG.nodes[node]["label"] == "max":
            nb_max += 1
        elif diG.nodes[node]["label"] == "min":
            nb_min += 1
        elif diG.nodes[node]["label"] == "sink" and diG.nodes[node]["value"] == 0:
            nb_sink_0 += 1
        elif diG.nodes[node]["label"] == "sink" and diG.nodes[node]["value"] == 1:
            nb_sink_1 += 1
        elif diG.nodes[node]["label"] == "average":
            nb_average += 1
        
    print("Le graphe possède " + str(nb_max) + " sommets max, " + str(nb_min) + " sommets min, " + str(nb_average) + " sommets average " + str(nb_sink_0) + " sommets sink min et " + str(nb_sink_1) + " sommets sink max")

def print_info(G):
    for node in G.nodes():
        print("Le sommet " + str(node) + " a pour label " + str(G.nodes[node]["label"]) + " et pour valeur " + str(G.nodes[node]["value"]))


#Execution du programme

diG = liste_to_graph_oriented("list.txt")
#On affiche les sommets de diG et leurs labels
#for node in diG.nodes():
#    for neighbor in diG.neighbors(node):
#        print("On a l'arête ", node, "->", neighbor, "de poids ", diG[node][neighbor]["weight"])

#On affiche le nombre de sommets avec un label max, min et average
#print_label(diG)

#Fusion des sommets average

identify_node(diG)

newdiG = diG.copy()

fuse_average(newdiG)


vertex_to_sink(newdiG)

remove_sink(newdiG)

#print_info(newdiG)

G = diG.to_undirected()

#directed_graph_to_file_gr(diG)
#undirected_graph_to_file_gr(G)

#print_label(newdiG)

#print("Le graphe non orienté possède " + str(G.number_of_nodes()) + " sommets et " + str(G.number_of_edges()) + " arêtes")
#print("Le graphe orienté possède " + str(diG.number_of_nodes()) + " sommets et " + str(diG.number_of_edges()) + " arêtes")


#On affiche dig et newdig sur chaque côté de la figure
pos = nx.spring_layout(G)

nx.draw(newdiG, pos)
node_labels = nx.get_node_attributes(newdiG,'value')
nx.draw_networkx_labels(newdiG, pos, labels = node_labels)
# On affiche les successeurs et predesseurs des sommets 78 86 70 90 80 71




plt.show()