# Auteur : ngbamedistingue@yahoo.com
# Python version 3.7
# !/usr/bin/env python3
# encoding=utf8
"""
Projet : Jeu De Rôle
"""
import sys
import random

###############################################################
#                   VARIABLES GLOBALES                        #
###############################################################

titre = "* JEU De Rôle *\n *************"    # titre du jeu
mon_pv, ennemi_pv = 50, 50              # PV : point de vie
possion = 3                             # permet de récupérer des PV
pv_aleatoire = 0                        # point de vie aléatoire
mon_attaque = 0                         # dégât de mon attaque
ennemi_attaque = 0                      # dégât de l'attaque de l'ennemi

###############################################################
#                    CONSTANTES                               #
###############################################################

ATTAQUE = "1"                           # code pour attaquer
DEFENSE = "2"                           # code pour gagner des vies


###############################################################
#                    EMOJIS                                   #
###############################################################

e_hache = "\U0001FA93"              # emoji d'une hache
e_possion = "\U0001F9EA"            # emoji de la possion
e_sang = "\U0001FA78"               # emoji de vies restantes
e_passer_tour = "\U0001F501"        # emoji de passage de tour
e_bravo = "\U0001F44F"              # emoji lorsque tu as gagné
e_triste = "\U0001F622"             # emoji lorsque tu as perd

###############################################################
#                    MENU PRINCIPAL                           #
###############################################################

print(titre)


def mon_application():
    global ennemi_pv, mon_pv, possion
    option = input(f"Souhaitez-vous attaquer (1) {e_hache} ou utiliser une potion {e_possion} (2) ? ")
    if option == ATTAQUE:
        mon_attaque = random.randint(5, 10)
        ennemi_attaque = random.randint(5, 15)
        ennemi_pv -= mon_attaque
        mon_pv -= ennemi_attaque
        print(f"Vous avez infligé {mon_attaque} {e_hache} points de dégats à l'ennemi")
        test_la_partie(mon_pv, ennemi_pv)
        print(f"L'ennemi vous a infligé {ennemi_attaque} {e_hache} points de dégats")
        affiche_vie_restant(mon_pv, ennemi_pv)
        print("---------------------------------------------------------------")
        mon_application()
    elif option == DEFENSE:
        if possion != 0:
            pv_aleatoire = random.randint(15, 50)
            ennemi_attaque = random.randint(5, 15)
            mon_pv += pv_aleatoire
            mon_pv -= ennemi_attaque
            possion -= 1
            print(f"Vous récupérez {pv_aleatoire}{e_possion} points de vie ({possion} restantes) $")
            print(f"L'ennemi vous a infligé {ennemi_attaque}{e_hache} points de dégats")
            test_la_partie(mon_pv, ennemi_pv)
            print("---------------------------------------------------------------")
            ennemi_attaque = random.randint(5, 15)
            mon_pv -= ennemi_attaque
            print(f"Vous passez votre tour {e_passer_tour}")
            print(f"L'ennemi vous a infligé {ennemi_attaque}{e_hache} points de dégats")
            test_la_partie(mon_pv, ennemi_pv)
            affiche_vie_restant(mon_pv, ennemi_pv)
        else:
            print("Désolé ! vous n'avez plus de possion")
        print("---------------------------------------------------------------")
        mon_application()
    else:
        mon_application()

###############################################################
#                    TEST LA PARTIE                           #
###############################################################

def test_la_partie(mon_pv, ennemi_pv):
    if ennemi_pv <= 0:
        print(f"{e_bravo} Bravo ! vous avez gagné")
        fermeture()
    elif mon_pv <= 0:
        print(f"{e_triste} Dommage ! vous avez perdu")
        fermeture()


###############################################################
#                    AFFICHE VIE RESTANTE                     #
###############################################################

def affiche_vie_restant(mon_pv, ennemi_pv):
    print(f"Il vous reste {mon_pv}{e_sang} points de vie.")
    print(f"Il reste {ennemi_pv}{e_sang} points de vie à l'ennemi")

###############################################################
#                    FERMETURE                                #
###############################################################


def fermeture():
    print("À bientôt !\U0001F44B\n")
    sys.exit()

###############################################################
#             OUVERTURE DE MON APPLICATION                    #
###############################################################


while True:
    mon_application()
