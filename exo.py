#encoding="utf-8"
import json
chemin = "dossier_test/fichier.json"

# Mode lecture
# with open(chemin, "r", encoding="utf-8") as f:
#     contenu = f.read().splitlines() # splitlines: le contenu du fichier dans une liste
#     print(contenu)

# with open(chemin, "a") as f: # mode 'w' ecrase, mode 'a' ajoute
#     f.write("\nBonjour")

# with open(chemin, "r") as f:
#     # json.dump(list(range(5)), f, ensure_ascii=False,indent=4) # pour écrire 'w'
#     contenue = json.load(f)
#     print(contenue)

with open(chemin, "a") as f:
    donnees = f.write([])
print(donnees)
donnees.append(6)
donnees.append(6)
# with open(chemin, "w") as f:
#     json.dump(donnees, f, indent=4)
print(donnees)

# print(f.seek(1)) # afficher avec le curseur
# print(f.read(10)) # afiicher une partie du fichier