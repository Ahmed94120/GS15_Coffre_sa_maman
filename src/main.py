from encryption.diffiehellman import parametres_globaux, private_key, mod_exp, diffiehellman
from server import *
from client import *
from encryption.rsa import rsa_key_derivaded
from authentification.zkp import ZeroKnowledgeProof

def handle_diffie_hellman():
    """
    Gère l'échange de clés Diffie-Hellman entre le client et le serveur.
    """
    print("\n=== Échange de clé Diffie-Hellman ===")
    p, g = parametres_globaux()
    private_key_server = private_key(p)
    public_key_server = mod_exp(g, private_key_server, p)
    print(f"Clé publique du serveur : {public_key_server}")

    private_key_client = private_key(p)
    public_key_client = mod_exp(g, private_key_client, p)
    print(f"Clé publique du client : {public_key_client}")

    shared_key_server = str(diffiehellman(public_key_client, private_key_server, p))
    shared_key_client = str(diffiehellman(public_key_server, private_key_client, p))

    print()
    assert shared_key_server == shared_key_client, "Erreur : Les clés partagées ne correspondent pas !"
    print(f"Clé partagée générée avec succès : {shared_key_client}")
    return shared_key_client

def handle_file_operations(username, shared_key):
    """
    Permet de gérer les opérations d'upload et de download des fichiers.
    """
    while True:
        print("\n=== Gestion des fichiers ===")
        print("1. Upload d'un fichier")
        print("2. Liste des fichiers disponibles")
        print("3. Télécharger un fichier")
        print("4. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            file_path = input("Entrez le chemin du fichier à uploader : ")
            encrypted_file_name, cobra_encrypted_data = upload_file_client_to_serv(username, shared_key, file_path)
            handle_file_upload_server(username, encrypted_file_name, cobra_encrypted_data, shared_key)

        elif choice == "2":
            files = list_user_files(username)
            print("\nFichiers disponibles dans votre répertoire serveur :")
            for file in files:
                print(f"- {file}")
        elif choice == "3":
            file_name = input("Entrez le nom du fichier à télécharger : ")
            download_file(username, shared_key, file_name)
        elif choice == "4":
            print("Retour au menu principal.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    
        initialize_server()
        print("\nBienvenue dans le système de coffre-fort sécurisé.")
        choice = input("\n===Souhaitez-vous créer un compte (1) ou vous authentifier (2) ? (1/2) : ===")

        if choice == "1":
            # Enrôlement d'un nouvel utilisateur
            username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
            if check_user_exists(username):
                print(f"Erreur : l'utilisateur {username} existe déjà.")
            else:
                password = input("Entrez un mot de passe : ")
                public_key, private_key = rsa_key_derivaded(password)
                # Créer le répertoire client et sauvegarder les clés
                initialize_client(username, public_key, private_key)
                # Enregistrer les informations côté serveur
                handle_user_enrollment(username, public_key)
                print(f"Utilisateur {username} enrôlé avec succès.")

        elif choice == "2":
                 # Authentification d'un utilisateur existant
                username = input("Entrez votre nom d'utilisateur : ")
                if not check_user_exists(username):
                    print(f"Erreur : l'utilisateur {username} n'existe pas. Veuillez créer un compte.")
                else:
                    print(f"Authentification pour l'utilisateur {username} en cours...")
                   

                    connected = ZeroKnowledgeProof(load_public_key(username), load_private_key(username))
                    if connected:
                        print(f"Authentification réussie pour l'utilisateur {username}.")
                        shared_key = handle_diffie_hellman()
                        handle_file_operations(username, shared_key)
                                    
                    else:
                        print("Authentification échouée. Accès refusé.")
                    
   
        
        print("Merci d'avoir utilisé le coffre-fort sécurisé. Programme terminé.")