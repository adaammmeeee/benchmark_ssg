from ast import Set
import networkx as nx
import matplotlib.pyplot as plt
import random as rand
import numpy as np
import statistics
import os
from fractions import Fraction
import time
import math
from operation_graph import average_set, max_set, min_set, sink_max_set, sink_min_set, trouve_deg_sortant_max, trouve_feuille, trouve_racine
nombre_iter = 0

def create_liste_frac(denominateur_max):
    list_all_frac = []
    for i in range(1,denominateur_max+1):
        for j in range(1,i):
            list_all_frac.append((j,i))
    list_all_frac.append((1,1))
    list_all_frac.append((0,1))
    return list_all_frac

def tri_fusion_fraction(liste):
        if len(liste) <= 1:
            return liste
        milieu = len(liste) // 2
        liste_gauche = tri_fusion_fraction(liste[:milieu])
        liste_droite = tri_fusion_fraction(liste[milieu:])
        return fusion_fraction(liste_gauche, liste_droite)

def fusion_fraction(liste_gauche, liste_droite):
        liste = []
        i_gauche = 0
        i_droite = 0
        while i_gauche < len(liste_gauche) and i_droite < len(liste_droite):
            if liste_gauche[i_gauche][0]*liste_droite[i_droite][1] < liste_droite[i_droite][0]*liste_gauche[i_gauche][1]:
                liste.append(liste_gauche[i_gauche])
                i_gauche += 1
            else:
                liste.append(liste_droite[i_droite])
                i_droite += 1
        liste.extend(liste_gauche[i_gauche:])
        liste.extend(liste_droite[i_droite:])
        return liste



def read_liste_frac():
    with open("liste_frac.txt", "r") as f:
        liste_frac = []
        for line in f:
            liste_frac.append(tuple(map(int,line.split("/"))))
    return liste_frac





def recherche_dicotomique(val_approx, liste_frac):
    cpt=0
    borne_inf = 0
    borne_sup = len(liste_frac)-1
    borne_mid = len(liste_frac)//2
    closest = liste_frac[borne_mid]
    flag = True
    while (flag):
        cpt+=1

        #On a trouvé la valeur
        if val_approx[0]*liste_frac[borne_mid][1] == liste_frac[borne_mid][0]*val_approx[1]:
            closest = liste_frac[borne_mid]
            flag = False
        
        #Si la valeur est trop grande
        elif val_approx[0]*liste_frac[borne_mid][1] > liste_frac[borne_mid][0]*val_approx[1]:
            #On se déplace vers la droite
            if abs(closest[0]*val_approx[1]-closest[1]*val_approx[0]) > abs(liste_frac[borne_mid][0]*val_approx[1]-liste_frac[borne_mid][1]*val_approx[0]):
                closest = liste_frac[borne_mid]
            borne_inf = borne_mid
            borne_mid = (borne_inf+borne_sup)//2
            if borne_inf == borne_mid:
                flag = False
        #Si la valeur est trop petite
        elif val_approx[0]*liste_frac[borne_mid][1] < liste_frac[borne_mid][0]*val_approx[1]:
            #On se déplace vers la gauche
            if abs(closest[0]*val_approx[1]-closest[1]*val_approx[0]) > abs(liste_frac[borne_mid][0]*val_approx[1]-liste_frac[borne_mid][1]*val_approx[0]):
                closest = liste_frac[borne_mid]
            borne_sup = borne_mid
            borne_mid = (borne_inf+borne_sup)//2
            if borne_sup == borne_mid:
                flag = False
            
        
    #print("Nombre d'itérations : ",cpt)
    return Fraction(closest[0],closest[1])

liste_frac_10000 = read_liste_frac()






def recherche_arbre_stern_brocot(val_approx, borne):
    current_node = (1,2)
    bound_left = (0,1)
    bound_right = (1,1)
    closest = current_node
    flag = True
    #On parcourt l'arbre de Stern-Brocot
    cpt = 0
    while (current_node[1] <= borne and flag):
        cpt+=1
        #On vérifie l'égalité
        if current_node[0]*val_approx[1] == val_approx[0]*current_node[1]:
            closest = current_node
            flag = False
        #Si le noeud de l'arbre est trop petit
        elif val_approx[0]*current_node[1] > current_node[0]*val_approx[1]:
            #On se déplace vers le fils droit
            bound_left = current_node                    
            current_node = (current_node[0] + bound_right[0], current_node[1] + bound_right[1])


        #Si le noeud de l'arbre est trop grand
        elif val_approx[0]*current_node[1] < current_node[0]*val_approx[1]:
            #On se déplace vers le fils gauche
            bound_right = current_node
            current_node = (current_node[0] + bound_left[0], current_node[1] + bound_left[1])
        
        else:
            print(val_approx)
            print(current_node)

        #On met à jour closest
        current_meme_denominateur = (current_node[0]*val_approx[1]*closest[1], current_node[1]*val_approx[1]*closest[1])
        closest_meme_denominateur = (closest[0]*val_approx[1]*current_node[1], closest[1]*val_approx[1]*current_node[1])
        val_approx_meme_denominateur = (val_approx[0]*current_node[1]*closest[1], val_approx[1]*current_node[1]*closest[1])

        if abs(current_meme_denominateur[0] - val_approx_meme_denominateur[0]) < abs(closest_meme_denominateur[0] - val_approx_meme_denominateur[0]):
            closest = current_node


    if abs(Fraction(1,1)-Fraction(val_approx[0],val_approx[1])) < abs(Fraction(closest[0],closest[1])-Fraction(val_approx[0],val_approx[1])):
        return (1,1)
    if abs(Fraction(0,1)-Fraction(val_approx[0],val_approx[1])) < abs(Fraction(closest[0],closest[1])-Fraction(val_approx[0],val_approx[1])):
        return (0,1)
    #print("cpt : ",cpt)
    return closest







class Ssg:
    def __init__(self, G, max_set, average_set, min_set, sink_max, sink_min):
        self.G = G
        self.max_set = max_set
        self.average_set = average_set
        self.min_set = min_set
        self.sink_max = sink_max
        self.sink_min = sink_min
        self.n = len(G.nodes)
        self.values = []
        self.set = {i for i in self.G.nodes if i not in self.sink_max and i not in self.sink_min}
        


    def value_print(self):
        vec = []
        for i in self.G.nodes:
            vec.append(Fraction(self.G.nodes[i]["value"]))
        print(vec)


    def one_step(self, node):
        if node in self.max_set:
            self.G.nodes[node]["value"]= max([self.G.nodes[j]["value"]
                                for j in list(self.G.successors(node))])
            
        elif node in self.min_set:
            self.G.nodes[node]["value"]= min([self.G.nodes[j]["value"]
                                for j in list(self.G.successors(node))])
        elif node in self.average_set:
            val = Fraction(0,1)


            for succ in list(self.G.successors(node)):
                val += self.G.nodes[succ]["value"]*self.G.edges[node,succ]["weight"]
            self.G.nodes[node]["value"] = val
    

    def valeur_iteration(self, node_set):
        if node_set == set():
            return 0

            

        old_values = {}
        save_values = {}
        for i in node_set:
            old_values[i] = 0
            save_values[i] = 0

        cpt = 0
        flag = False
        begin = time.time()
        while (not flag):
            #print("On a fait ", cpt, " itérations")
            
            cpt += 1
            current = time.time()
            if current - begin > 1200:
                print("timeout")
                return 0
            flag = True
            perfect = True
            for i in node_set:
                    old_values[i] = self.G.nodes[i]["value"]
            for i in node_set:
                self.one_step(i)

            if (cpt % 50 == 0):
                #On sauvegarde les anciennes valeurs
                for i in node_set:
                    save_values[i] = self.G.nodes[i]["value"]
               
                
                vec_test = {}
                self.resout_exact(node_set)
                for i in node_set:
                    vec_test[i] = self.G.nodes[i]["value"]



                for i in node_set:    
                    self.one_step(i)
                    if vec_test[i] != self.G.nodes[i]["value"]:
                        perfect = False
                        #print("AIE DOMMAGE, mais", vec_test[i], "est différent de", self.G.nodes[i]["value"], "le noeud est de type", self.G.nodes[i]["label"])
                        break
                
                if not perfect:
                    for i in node_set:
                        self.G.nodes[i]["value"] = save_values[i]
                else:
                    #print("On a trouvé un vecteur valeur parfait grace brobro !")
                    break



            #On compare les valeurs de nos deux graph et si on a aucun switch on arrête
            for i in node_set:
                if self.G.nodes[i]["value"] != old_values[i]:
                    #print("Dommage, mais", self.G.nodes[i]["value"], "est différent de", old_values[i], "le noeud est de type", self.G.nodes[i]["label"])
                    flag = False
                    break


            
            
            #print("On a trouvé une valeur parfaite !")
        #print(self.value_print())

    



    def dichotomie_naive(self, node_set, bound):
            borne_inf = 0
            borne_sup = 1
            borne_milieu = Fraction((borne_inf + borne_sup),2)
            #On assigne un noeud de départ aléatoire
            node = rand.choice(list(self.G.nodes))

            #Lorsque l'on a traité tous les noeuds on appel la fonction valeur_iteration sur les noeuds restants
            if node_set == set():
                print("On a traité tous les noeuds")
                print(self.value_print())
                newset = self.set.difference(node_set)
                self.valeur_iteration(newset)
                time.sleep(5)
                return 0
            
            while (node not in node_set):
                node = rand.choice(list(self.G.nodes))



            while (borne_sup - borne_inf > bound):
                #self.value_print()

                borne_milieu = Fraction((borne_inf + borne_sup),2)
                # On transforme le sommet traité 
                self.G.nodes[node]['value'] = borne_milieu

                # On résout le jeu à l'aide d'un oracle
                self.dichotomie_naive(node_set - {node}, bound)


                # Maintenant on regarde la valeur après un ONESTEP
                val = 0
                if node in self.max_set:
                    val = max([self.G.nodes[j]['value']
                            for j in list(self.G.successors(node))])
                if node in self.min_set:
                    val = min([self.G.nodes[j]['value']
                            for j in list(self.G.successors(node))])
                if node in self.average_set:
                    for succ in list(self.G.successors(node)):
                        val += self.G.nodes[succ]['value']*self.G.edges[node,succ]['weight']
                        print("je multiplie par ", self.G.edges[node,succ]['weight'])

                # On regarde si la borne sup ou inf doit être modifiée
                if val > borne_milieu:
                    borne_inf = borne_milieu
                else:
                    borne_sup = borne_milieu

            # On transforme le sommet traité (aléatoire)
            self.G.nodes[node]['value'] = (borne_sup+borne_inf)/2
            return 


    def resout_exact(self, node_set):
        vec_lcm = []
        if node_set == set():
            return 0
        vec_q = []
        nb_average = 0
        time1 = time.time()
        for i in node_set:
            if i in self.average_set:
                nb_average += 1
                for succ in list(self.G.successors(i)):
                    vec_q.append(self.G.edges[i,succ]["weight"])
                    if succ not in node_set:
                        vec_lcm.append(self.G.edges[i,succ]["weight"].denominator)
        time2 = time.time()
    
        q = 1
        for i in vec_q:
            q = max(i.denominator, q)
        lcm = math.lcm(*vec_lcm)
        borne = (lcm*q)**(nb_average)
        if borne > 10**4:
            borne = 10**4
        
        #print("La borne est ", borne)
        for node in node_set:
            if node not in self.sink_max and node not in self.sink_min:
                closest = recherche_dicotomique( (self.G.nodes[node]['value'].numerator, self.G.nodes[node]['value'].denominator), liste_frac_10000)

                #On met à jour notre valeur
                self.G.nodes[node]['value'] = closest
        timeX = time.time()
            
        return 0
    
    def liste_connexe_component(self):
        list_component = []
        for c in sorted(nx.strongly_connected_components(self.G), key=len, reverse=True):
            list_component.append(c)
        graphe_com_con = nx.DiGraph()
        for i in range(len(list_component) ):
            graphe_com_con.add_node(i, id = i, value = [0 for i in range(0, len(list_component[i]))], liste_sommets = list_component[i])


        for i in range(len(list_component)):
            for node in list_component[i]:
                test = False
                for pred in self.G.predecessors(node):
                    if pred not in list_component[i]:
                        test = True
                        for j in range(len(list_component)):
                            if pred in list_component[j]:
                                graphe_com_con.add_edge(j, i)

        return graphe_com_con
            
    #On part des feuilles et on remonte jusqu'à la racine pour obtenir la valeur du jeu
    def calcul_composantes_connexes(self):
        if nx.is_directed_acyclic_graph(self.G):
            print("Le graphe est acyclique")
            
            return self.resol_acyclique()
        else :
            print("Le graphe n'est pas acyclique")
        time1 = time.time()
        graphe_com_con = self.liste_connexe_component()
        time2 = time.time()
        print("fin de la construction du graphe com con en ", time2 - time1)
        liste_racine = trouve_racine(graphe_com_con)
        print("fin de la recherche des racines")
        done = [False for i in range(len(graphe_com_con.nodes))]
        for racine in liste_racine:
            self.calcul_composantes_connexes_rec(racine, graphe_com_con,done)
        return 0
    

    """
    """

    def calcul_composantes_connexes_rec(self,node, graphe_com_con, done):
        done[node] = True
        for succ in graphe_com_con.successors(node):
            if not done[succ]:
                self.calcul_composantes_connexes_rec(succ, graphe_com_con, done)
        self.valeur_iteration(graphe_com_con.nodes[node]["liste_sommets"])
        
    def resol_acyclique(self):
        liste_racine = trouve_racine(self.G)
        done = [False for i in range(len(self.G.nodes)+1)]
        for racine in liste_racine:
            self.resol_acyclique_rec(racine,done)
        return 0
    
    def resol_acyclique_rec(self,node, done):
        done[node] = True
        for succ in self.G.successors(node):
            if not done[succ]:
                self.resol_acyclique_rec(succ, done)
        self.valeur_iteration({node})