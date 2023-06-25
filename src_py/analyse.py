from fractions import Fraction
import time
import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
import graph_parser
from operation_graph import average_set, complexify, correction_probability_law, delete_self_loop, fuse_node, fuse_sink, max_set, min_set, remove_sink, sink_max_set, sink_min_set, verify_probability_law, vertex_to_sink
from ssg import Ssg





def print_label(G):
    nb_max = 0
    nb_min = 0
    nb_sink_0 = 0
    nb_sink_1 = 0
    nb_average = 0
    for node in G.nodes():
        if G.nodes[node]["label"] == "max":
            nb_max += 1
        elif G.nodes[node]["label"] == "min":
            nb_min += 1
        elif G.nodes[node]["label"] == "sink" and G.nodes[node]["value"] == 0:
            nb_sink_0 += 1
        elif G.nodes[node]["label"] == "sink" and G.nodes[node]["value"] == 1:
            nb_sink_1 += 1
        elif G.nodes[node]["label"] == "average":
            nb_average += 1
        
    print("Le graphe possède " + str(nb_max) + " sommets max, " + str(nb_min) + " sommets min, " + str(nb_average) + " sommets average " + str(nb_sink_0) + " sommets sink min et " + str(nb_sink_1) + " sommets sink max")

def print_info(G):
    for node in G.nodes():
        print("Le sommet " + str(node) + " a pour label " + str(G.nodes[node]["label"]) + " et pour valeur " + str(G.nodes[node]["value"]))


#Execution du programme
temp = time.time()
diG = graph_parser.liste_to_graph_oriented("./list.txt")
#On affiche les sommets de diG et leurs labels
#for node in diG.nodes():
#    for neighbor in diG.neighbors(node):
#        print("On a l'arête ", node, "->", neighbor, "de poids ", diG[node][neighbor]["weight"])

#On affiche le nombre de sommets avec un label max, min et average
#print_label(diG)

#Fusion des sommets average

graph_parser.identify_node(diG)





newdiG = diG.copy()
vertex_to_sink(newdiG)
remove_sink(newdiG)
newdiG = fuse_sink(newdiG)
newdiG = fuse_node(newdiG)
delete_self_loop(newdiG)
#print("nombre de sommet total = ", len(newdiG.nodes()))
#On affiche le nombre de composantes fortement connexes
#print("Le graphe possède ", nx.number_strongly_connected_components(newdiG), " composantes fortement connexes")


correction_probability_law(newdiG)
if not(verify_probability_law(newdiG)):
#    print("nombre de sommet total = ", len(newdiG.nodes()))
    exit()


G = newdiG.to_undirected()

graph_parser.undirected_graph_to_file_gr(G)

graph_parser.directed_graph_to_file_gr(newdiG)
#print("le graphe est acyclique : ", nx.is_directed_acyclic_graph(newdiG))

#On compte le nombre de sommet pour chaque label du graphe dig
max_dig = 0
min_dig = 0
average_dig = 0
sink_dig = 0
for node in diG.nodes():
    if diG.nodes[node]["label"] == "max":
        max_dig += 1
    elif diG.nodes[node]["label"] == "min":
        min_dig += 1
    elif diG.nodes[node]["label"] == "average":
        average_dig += 1
    elif diG.nodes[node]["label"] == "sink":
        sink_dig += 1


max_newdig = 0
min_newdig = 0
average_newdig = 0
sink_newdig = 0
sink_min_newdig = 0
sink_max_newdig = 0
for node in newdiG.nodes():
    if newdiG.nodes[node]["label"] == "max":
        max_newdig += 1
    elif newdiG.nodes[node]["label"] == "min":
        min_newdig += 1
    elif newdiG.nodes[node]["label"] == "average":
        average_newdig += 1
    elif newdiG.nodes[node]["label"] == "sink":
        sink_newdig += 1
        if newdiG.nodes[node]["value"] == 0:
            sink_min_newdig += 1
        elif newdiG.nodes[node]["value"] == 1:
            sink_max_newdig += 1
        



#print("nb_max = ", max_newdig, "nb_min = ", min_newdig, "nb_average = ", average_newdig,  "nb_sink = ", sink_newdig)
#print("nb_max = ", max_dig, "nb_min = ", min_dig, "nb_average = ", average_dig,  "nb_sink = ", sink_dig)


if (False):
    print_label(diG)
    print_label(newdiG)

    #On affiche les pourcentages en evitant les divisions par 0
    if max_dig != 0:
        print("Le graphe a perdu ", int((max_dig - max_newdig) / max_dig * 100), "% de sommets max")
    if min_dig != 0:
        print("Le graphe a perdu ", int((min_dig - min_newdig) / min_dig * 100), "% de sommets min")
    if average_dig != 0:
        print("Le graphe a perdu ", int((average_dig - average_newdig) / average_dig * 100), "% de sommets average")
    if sink_dig != 0:
        print("Le graphe a perdu ", int((sink_dig - sink_newdig) / sink_dig * 100), "% de sommets sink")


    print("nombre de sommets avant modification : ", nb_sommet_original)
    print("nombre de sommets après modification : ", newdiG.number_of_nodes())

    print("Par rapport au graphe original on a perdu ", nb_sommet_original - newdiG.number_of_nodes(), " sommets, soit ", int((nb_sommet_original - newdiG.number_of_nodes()) / nb_sommet_original * 100), "% des sommets")
    temp2 = time.time()
    if(nx.is_directed_acyclic_graph(newdiG)):
        print("Le graphe est acyclique")
    else:
        print("Le graphe n'est pas acyclique")
    #On affiche la treewidth du graphe

    print("Le programme a mis " + str(temp2 - temp) + " secondes à s'exécuter")

    a = [len(c) for c in sorted(nx.strongly_connected_components(newdiG), key=len, reverse=True)]
    print(a)





newdiG = nx.convert_node_labels_to_integers(newdiG, first_label=1, ordering='default', label_attribute=None)
#G = newdiG.to_undirected()
#print("Nombre de composantes fortement connexes : ", nx.number_strongly_connected_components(newdiG))

#graph_parser.directed_graph_to_file_gr(diG)
#graph_parser.undirected_graph_to_file_gr(G)

new_diG_copy = newdiG.copy()




my_ssg = Ssg(new_diG_copy,max_set(new_diG_copy),average_set(new_diG_copy),min_set(new_diG_copy),sink_max_set(new_diG_copy),sink_min_set(new_diG_copy))
temp_reso = time.time()
my_ssg.calcul_composantes_connexes()
temp_reso2 = time.time()
#my_ssg.value_print()
# on affiche le temps en ecriture scientifique
temps_execution = temp_reso2 - temp_reso
print("La résolution par composante connexe a mis " + str("%e"%temps_execution) + " secondes à s'exécuter")

my_ssg1 = Ssg(newdiG,max_set(newdiG),average_set(newdiG),min_set(newdiG),sink_max_set(newdiG),sink_min_set(newdiG))
temp_reso = time.time()
my_ssg1.valeur_iteration(my_ssg1.G)
temp_reso2 = time.time()
temps_execution = temp_reso2 - temp_reso
print("La résolution par itération de valeur a mis " + str(format(temp_reso2 - temp_reso, "e")) + " secondes à s'exécuter")




if (False):
    pos = nx.spring_layout(my_ssg1.G)

    nx.draw(my_ssg1.G, pos)
    node_labels = nx.get_node_attributes(my_ssg1.G,'value')
    #On crée un tuple : (node, value)
    my_dict = {}
    for node in node_labels:
        my_dict[node] = (node, node_labels[node])

    nx.draw_networkx_labels(my_ssg1.G, pos, labels = my_dict)

    plt.show()





if (False):
    pos = nx.spring_layout(newdiG)

    nx.draw(newdiG, pos)
    node_labels = nx.get_node_attributes(newdiG,'value')
    #On crée un tuple : (node, value)
    my_dict = {}
    for node in node_labels:
        my_dict[node] = (node, node_labels[node])

    nx.draw_networkx_labels(newdiG, pos, labels = my_dict)

    plt.show()


#On print dig

