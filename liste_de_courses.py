# Auteur : ngbamedistingue@yahoo.com

import sys

###############################################################
#                   VARIABLES GLOBALES                        #
###############################################################

liste_de_courses = []     # Liste de courses
option = ""               # choix de l'utilisateur
ajouter = "1"             # choix 1: ajouter un élément
supprimer = "2"           # choix 2: supprimer un élément
afficher = "3"            # choix 3: afficher les éléments
vider = "4"               # choix 4: vider la liste
quitter = "5"             # choix 5: quitter le programme

###############################################################
#                    MENU PRINCIPAL                           #
###############################################################


def mon_application():

    print(f"""
    Choisissez parmi les 5 options suivantes :\n
    {ajouter}: Ajouter un élément à la liste
    {supprimer}: Retirer un élément de la liste
    {afficher}: Afficher la liste
    {vider}: Vider la liste
    {quitter}: Quitter
    """)
    option = input("Votre choix : ")

    if option == ajouter:
        ajout()
    elif option == supprimer:
        suppression()
    elif option == afficher:
        affichage()
    elif option == vider:
        nettoyer()
    elif option == quitter:
        fermeture()
    else:
        print(
            "Veillez saisir une option valide 'ex: un chiffre [1, 5]' svp!\n")
        mon_application()


###############################################################
#                        AJOUT                                #
###############################################################


def ajout():
    global liste_de_courses
    ajoute_element = input(
        "Entrez le nom d'un élément à ajouter à la liste de courses : ")
    liste_de_courses.append(ajoute_element.capitalize())
    print(f"L'élément {ajoute_element} a bien été ajouté à la liste.")
    print("_________________________________________________________")
    mon_application()

###############################################################
#                      SUPPRESSION                            #
###############################################################


def suppression():

    if liste_de_courses == []:
        print("Désolé vous n'avez aucun élément dans votre liste.")
    else:
        supprime_element = input(
            "Entrez le nom d'un élément à rétirer de la liste de courses : ")
        if supprime_element in liste_de_courses:
            liste_de_courses.remove(supprime_element)
            print(
                f"L'élément {supprime_element} a bien été rétiré de la liste.")
        else:
            print(f"L'élément {supprime_element} n'est pas dans la liste.")
    print("_________________________________________________________")
    mon_application()

###############################################################
#                      AFFICHAGE                              #
###############################################################


def affichage():

    if liste_de_courses == []:
        print("Votre liste ne contient aucun élément.")
    else:
        print("Voici le contenu de votre liste :")
        for ordre, element in enumerate(liste_de_courses):
            print(f"{ordre+1}. {element}")
    print("_________________________________________________________")
    mon_application()

###############################################################
#                     NETTOYAGE                               #
###############################################################


def nettoyer():

    global liste_de_courses
    liste_de_courses = []
    print("La liste a été vidée de son contenu.")
    print("_________________________________________________________")
    mon_application()


###############################################################
#                    FERMETURE                                #
###############################################################

def fermeture():
    print("\nÀ bientôt !")
    sys.exit()

###############################################################
#             OUVERTURE DE MON APPLICATION                    #
###############################################################


while True:
    mon_application()
