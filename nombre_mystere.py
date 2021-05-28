# Auteur : ngbamedistingue@yahoo.com
# Python version 3.7
# !/usr/bin/env python3
# encoding=utf8
"""
Projet : Nombre mystère
"""
import sys
import random

###############################################################
#                   VARIABLES GLOBALES                        #
###############################################################

nombre_mystere = random.randint(0, 100) # un nombre aléatoire [0,100]
titre = "* Le Jeu Du Nombre Mystère *\n **************************"    # titre du jeu
essais = 5                                      # nombre d'essais
tentative = 1                                   # nombre d'essais pour gagner
nombre_choisi = 0                               # nombre choisi

###############################################################
#                    MENU PRINCIPAL                           #
###############################################################

print(titre)
def mon_application():
    global nombre_choisi
    if essais != 0:
        print(f"Il vous reste {essais}\U0001FA78 essais")
        nombre_choisi = input("Devinez le nombre : ")
        if nombre_choisi.isdigit() and int(nombre_choisi) in range(0, 101):
            test_le_resultat(nombre_choisi)
        else:
            print(
                "Veillez saisir un nombre valide 'ex: un chiffre [0, 100]' svp!\n")
    else:
        print(f"\U0001F622 Dommage ! Le Nombre Mystère était {nombre_mystere}")
        fermeture()

###############################################################
#                    TEST LE RESULTAT                         #
###############################################################

def test_le_resultat(nombre_choisi):
    global essais, tentative
    if int(nombre_choisi) == nombre_mystere:
        print(f"\n\U0001F44F Bravo ! Le Nombre Mystère était bien {nombre_mystere}\U0001F31F")
        print(
            f"Félicittions! vous avez truvé Le Nombre Mystère en {tentative} essai")
        fermeture()
    elif nombre_mystere > int(nombre_choisi):
        print(f"\nLe Nombre Mystère est plus grand que {nombre_choisi}")
        essais -= 1
        tentative += 1
    else:
        print(f"\nLe Nombre Mystère est plus petit que {nombre_choisi}")
        essais -= 1
        tentative += 1

###############################################################
#                    FERMETURE                                #
###############################################################

def fermeture():
    print("Fin du jeu.\U0001F44B")
    sys.exit()

###############################################################
#             OUVERTURE DE MON APPLICATION                    #
###############################################################

while True:
    mon_application()
