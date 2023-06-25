from math import log
import random
import networkx as nx
import time
from fractions import Fraction

"""
Fusionne les sommets qui ont les mêmes successeurs
"""
def fuse_node(G):
    dict = {}
    set_of_keys = set()
    cpt = 0
    for node in list(G.nodes()):
        if G.nodes[node]["label"] != "sink":
            tuple_all = ()
            for successor in G.successors(node):
                tuple = (G[node][successor]["weight"], successor)
                tuple_all += tuple
            if tuple_all not in set_of_keys:
                dict[tuple_all] = []
                set_of_keys.add(tuple_all)
            dict[tuple_all].append(node)
            if len(dict[tuple_all]) > 1:
                nx.contracted_nodes(G, dict[tuple_all][0], dict[tuple_all][1], copy=False)
                dict[tuple_all].pop(1)
                cpt += 1

    #print("Nombre de sommets fusionés : ", cpt)
    return G

"""
Fusionne les puits de mêmes valeurs
"""
def fuse_sink(G):
    dico = {}
    set_of_keys = set()
    cpt = 0
    for node in list(G.nodes()):
        time1 = time.time()
        if G.nodes[node]["label"] == "sink":
            value = G.nodes[node]["value"]
            if value not in set_of_keys:
                dico[value] = []
                set_of_keys.add(value)
            dico[value].append(node)
            if len(dico[value]) > 1:
                #On fusionne les sommets
                node_a = dico[value][0]
                node_b = dico[value][1]
                pred_common = set(G.predecessors(node_a)).intersection(set(G.predecessors(node_b)))
                weight = dict()

                for pred in pred_common:
                    weight[pred] = G[pred][node_a]["weight"] + G[pred][node_b]["weight"]
                nx.contracted_nodes(G, node_a, node_b, copy=False)
                for pred in pred_common:
                    G[pred][node_a]["weight"] = weight[pred]
                    
                cpt += 1
                dico[value].pop(1)

    #print("Nombre de puits fusionnés : ", cpt)
    return G

"""
Transforme les sommets non sinks ayant une value (0 ou 1) en sommets sinks et supprime ses successeurs
"""
def vertex_to_sink(G):
    for node in G.nodes():
        if G.nodes[node]["label"] != "sink" and (G.nodes[node]["value"] == 0 or G.nodes[node]["value"] == 1):
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
        if (len(list(G.predecessors(node))) == 0 and G.nodes[node]["label"] == "sink") or (node in list(G.successors(node)) and G.nodes[node]["label"] == "sink"):
            to_delete.append(node)
    #print("On supprime les sommets sinks suivants : ", to_delete)
    G.remove_nodes_from(to_delete)
    return 0

def max_set(G):
    max = set()
    for node in G.nodes():
        if G.nodes[node]["label"] == "max":
            max.add(node)
    return max

def min_set(G):
    min = set()
    for node in G.nodes():
        if G.nodes[node]["label"] == "min":
            min.add(node)
    return min

def sink_min_set(G):
    sink_min = set()
    for node in G.nodes():
        if G.nodes[node]["label"] == "sink" and G.nodes[node]["value"] == 0:
            sink_min.add(node)
    return sink_min

def sink_max_set(G):
    sink_max = set()
    for node in G.nodes():
        if G.nodes[node]["label"] == "sink" and G.nodes[node]["value"] == 1:
            sink_max.add(node)
    return sink_max

def average_set(G):
    average = set()
    for node in G.nodes():
        if G.nodes[node]["label"] == "average":
            average.add(node)
    return average

def trouve_racine(G):
    liste_racine = []
    for node in G.nodes():
        predecessors = list(G.predecessors(node))
        if len(predecessors) == 0:
            liste_racine.append(node)
    return liste_racine

def trouve_feuille(G):
    liste_feuille = []
    for node in G.nodes():
        successors = list(G.successors(node))
        if len(successors) == 0:
            liste_feuille.append(node)
    return liste_feuille

def trouve_deg_sortant_max(G):
    deg_sort_max = 0
    for node in G.nodes():
        deg_sort_max = max(deg_sort_max, len(list(G.successors(node))))
    return deg_sort_max


def delete_self_loop(G):
    for node in G.nodes():
        if node in list(G.successors(node)):
            G.remove_edge(node, node)
    return 0


def correction_probability_law(G):
    cpt = 0
    for node in G:
        if G.nodes[node]["label"] == "average":
            sum = 0
            for successor in G.successors(node):
                sum += G[node][successor]["weight"]
            if sum != 1 or sum == 1:
                #Puisque PRISM n'est pas foutu d'avoir une loi de probabilité correcte, on corrige nous-même
                for successor in G.successors(node):
                    G[node][successor]["weight"] = Fraction(1, len(list(G.successors(node))))
    
    return 1

def verify_probability_law(G):
    for node in G:
        if G.nodes[node]["label"] == "average":
            sum = 0
            for successor in G.successors(node):
                sum += G[node][successor]["weight"]
            if sum != 1:
                print("Erreur : loi de probabilité non respectée")
                return 0
    return 1
            

def complexify(G):
    if nx.is_directed_acyclic_graph(G):
        #On connecte des sommets MAX ou MIN vers d'autre sommet représentant 10% du graphe entre eux
        #On tire au hasard les sommets à connecter
        to_add = []
        for node in G.nodes():
            if G.nodes[node]["label"] == "max" or G.nodes[node]["label"] == "min":
                #On a une chance sur 2 de connecter ce sommet
                if random.randint(0, 1) == 1:
                    to_add.append(node)
                
        for node in to_add:
            #On tire au hasard le nombre de sommets à connecter
            nb_to_add = random.randint(1, int(len(G.nodes())*0.1))
            #On tire au hasard les sommets à connecter
            to_connect = random.sample(list(G.nodes()), nb_to_add)
            for node_to_connect in to_connect:
                if node != node_to_connect:
                    G.add_edge(node, node_to_connect, weight=Fraction(1,1))

