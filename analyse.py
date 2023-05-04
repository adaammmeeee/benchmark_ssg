import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt




#On transforme la liste d'adjacence du fichier liste.txt en un graphe networkx
def liste_to_graph_oriented(file):
    print("Je suis dans la fonction liste_to_graph_oriented")
    G = nx.DiGraph()
    with open(file) as f:
        for line in f:
            cpt = 0
            line = line.split(sep=" ")
            G.add_node(line[0])
            i = 1
            nb_choice = line.count("-1.0")
            if nb_choice > 1:
                while i < len(line)-1:
                    if line[i] == str(-1.0):
                        cpt += 1
                        #Alors on a un nouveau choix et on crée un nouveau sommet
                        G.add_edge(line[0], line[0] + "c" + str(cpt)) 
                        print("J'ai ajouté une arête entre ",line[0]," et ",line[0] + 'c' + str(cpt))   
                        i += 1

                    else:
                        G.add_edge(line[0] + 'c' + str(cpt), line[i+1][:-2], weight=line[i])
                        print("J'ai ajouté une arête entre ",line[0] + 'c' + str(cpt)," et ",line[i+1][:-2]," de poids ",line[i])
                        i+=2
            else:
                i = 2
                while i < len(line)-1:
                    G.add_edge(line[0], line[i+1][:-2], weight=line[i])
                    print("J'ai ajouté une arête entre ",line[0]," et ",line[i+1][:-2]," de poids ",line[i])
                    i+=2
    return G


#On calcule treewidth du graphe

def treewidth(G):
    tw = approximation.treewidth_min_degree(G)
    return tw[0]


#On calcule le nombre de cycles dans le graphe

def nb_cycles(G):
    a = nx.recursive_simple_cycles(G.copy())
    return len(nx.recursive_simple_cycles(G.copy()))

#Execution du programme


diG = liste_to_graph_oriented("list.txt")
G = diG.to_undirected()
print("Le graphe contient",diG.number_of_nodes(),"noeuds")
print("Le graphe contient",diG.number_of_edges(),"arcs")
print("Le graphe est connexe :",nx.is_connected(G))

#On affiche les transitions de diG

nx.draw(diG, with_labels=True)
plt.show()