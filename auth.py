from modules.gestion_produits import *
import csv 
import os
import hashlib
import requests

from modules.gestion_commercant import menu_modif

def verif_mdp(password):
    password_hash = hashlib.md5(password.encode()).hexdigest()  

    try:
        with open('mdp_compromis.csv', mode='r') as file:
            reader = csv.reader(file)
            # next(reader)  
            for row in reader:
                if row[0] == password_hash:
                    return True 
        return False  
    except FileNotFoundError:
        return False  

def verif_api(username):
    # Convertir le mot de passe en hash SHA-1
    sha1_hash = hashlib.sha1(username.encode('utf-8')).hexdigest().upper()
    
    # Séparer le hash en deux parties
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    # Requête API Have I Been Pwned
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    headers = {
        'User-Agent': 'VotreNomDeProduit/1.0'  # Remplacez par un User-Agent valide
    }
    
    try:
        # Envoi de la requête GET
        response = requests.get(url, headers=headers)
        
        # Vérifier si la requête a réussi
        if response.status_code != 200:
            raise RuntimeError(f'Erreur {response.status_code}, veuillez réessayer plus tard.')
        
        # Analyser la réponse de l'API
        hashes = (line.split(':') for line in response.text.splitlines())
        
        # Chercher le suffix dans les hashes
        for h, count in hashes:
            if h == suffix:
                return int(count)  # Retourner le nombre de fois où le mot de passe a été compromis
        
        return 0  # Retourner 0 si le mot de passe n'a pas été compromis

    except requests.exceptions.RequestException as e:
        # Gestion des erreurs liées à la requête (problèmes réseau, etc.)
        print(f"Erreur lors de la requête API : {e}")
        return 0



def inscription():
    id = input("Entrez votre numero d'identifiant: ")
    nom = input("Entrez votre nom: ")
    username = input("Entrez votre nom d'utilisateur: ")

    while True:
        password = input("Entrez votre mot de passe: ")
        
        if verif_mdp(password):
            print("Ce mot de passe est compromis. Veuillez en choisir un autre.")
        else:
            break  
    
    password_hash = hashlib.md5(password.encode()).hexdigest() 

    with open('data_user.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        
        file.seek(0, 2)  
        if file.tell() == 0:
            writer.writerow(["ID", "Nom", "Username", "Password"]) 
        
        writer.writerow([id, nom, username, password_hash])

    print("Inscription réussie!")


def connexion():
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    try:
        with open('data_user.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'entête du fichier CSV
            for row in reader:
                # Vérifier si la ligne contient suffisamment de colonnes
                if len(row) >= 4:  # Assurez-vous qu'il y a 4 colonnes (ID, Nom, Username, Password)
                    stored_username = row[2]
                    stored_password = row[3]
                    
                    # Vérifier si les identifiants correspondent
                    if stored_username == username and stored_password == password:
                        print("Connexion réussie!")

                        # Vérification avec l'API pour le mot de passe
                        compromises = verif_api(password)
                        if compromises > 0:
                            print(f"Alerte : Ce mot de passe a été compromis {compromises} fois dans des violations de données.")
                            
                            # Rediriger vers le menu de modification si le mot de passe est compromis
                            menu_modif(username)
                        else:
                            print("Le mot de passe semble sécurisé.")

                        menu_user(username)  # Appel de la fonction menu_user() si la connexion réussie
                        return
        print("Nom d'utilisateur ou mot de passe incorrect.")
    except FileNotFoundError:
        print("Le fichier 'data_user.csv' est introuvable.")




def connexion_et_supprimer_fichier():
    # Demander le nom d'utilisateur et le mot de passe
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    # Ouvrir le fichier CSV contenant les données des utilisateurs
    try:
        with open('data_user.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Passer l'en-tête
            
            # Vérifier les informations de connexion
            for row in reader:
                nom, stored_username, stored_password = row
                
                if stored_username == username and stored_password == password:
                    print("Connexion réussie!")

                    # Vérifier si le fichier correspondant à l'utilisateur existe
                    user_filename = f"{username}.csv"
                    
                    if os.path.exists(user_filename):
                        try:
                            # Supprimer le fichier de l'utilisateur
                            os.remove(user_filename)
                            print(f"Le fichier {user_filename} a été supprimé avec succès.")
                        except Exception as e:
                            print(f"Une erreur est survenue lors de la suppression du fichier: {e}")
                    else:
                        print(f"Le fichier {user_filename} n'existe pas.")
                    
                    return  # Fin de la fonction, l'utilisateur est authentifié et le fichier supprimé
                    
            print("Nom d'utilisateur ou mot de passe incorrect.")
            
    except FileNotFoundError:
        print("Le fichier 'data_user.csv' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
import sys

def quitter():
    print("Au revoir !")
    sys.exit()  # Cette ligne arrête le programme


from colorama import Fore, Style, init
from modules.auth import *

init(autoreset=True)

def menu_user(username):
    while True:  # Boucle infinie pour revenir au menu après chaque action
        print(Fore.BLUE + """
 ::::::::  :::::::::: :::::::: ::::::::::: ::::::::::: ::::::::  ::::    ::: 
:+:    :+: :+:       :+:    :+:    :+:         :+:    :+:    :+: :+:+:   :+: 
+:+        +:+       +:+           +:+         +:+    +:+    +:+ :+:+:+  +:+ 
:#:        +#++:++#  +#++:++#++    +#+         +#+    +#+    +:+ +#+ +:+ +#+ 
#+#   +#+# +#+              +#+    +#+         +#+    +#+    +#+ +#+  +#+#+# 
#+#    #+# #+#       #+#    #+#    #+#         #+#    #+#    #+# #+#   #+#+# 
 ########  ########## ########     ###     ########### ########  ###    ####
    """)

        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print(Fore.MAGENTA + f"   Menu de {username}   ")  
        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print()

        print(Fore.CYAN + "Que souhaitez-vous faire ?")
        print(Fore.GREEN + "1. Créer")
        print(Fore.YELLOW + "2. Supprimer")
        print(Fore.BLUE + "3. Ajouter un produit")
        print(Fore.RED + "4. Afficher")
        print(Fore.LIGHTGREEN_EX + "5. Rechercher")
        print(Fore.LIGHTYELLOW_EX + "6. Trier")
        print(Fore.LIGHTYELLOW_EX + "7. Quitter")

        print()

        choix = input(Fore.LIGHTCYAN_EX + "Entrez votre choix : ")

        if choix == '1':
            print(Fore.GREEN + Style.BRIGHT + "\nCréation en cours...")  
            create(username)
        elif choix == '2':
            print(Fore.RED + Style.BRIGHT + "\nSuppression en cours...")  
            supprimer(username)
        elif choix == '3':
            print(Fore.BLUE + Style.BRIGHT + "\nAjout de produit en cours...")  
            add_produit(username)
        elif choix == '4':
            print(Fore.RED + Style.BRIGHT + "\nAffichage en cours...") 
            afficher(username)

        elif choix == '5':
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nRecherche en cours...")  
            rechercher_sequ(username)
        elif choix == '6':
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\nTri en cours...")  
            tri_bul(username)
        elif choix == '7':
            quitter()  # Quitter la fonction et le programme
        else:
            print(Fore.RED + Style.BRIGHT + "\nChoix invalide. Veuillez essayer à nouveau.")  # Erreur en rouge