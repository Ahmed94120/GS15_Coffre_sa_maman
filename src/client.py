from server import *
from encryption.cobra import cobra_encode, cobra_decode
import os

CLIENT_DIR = "./client"

def initialize_client(username, public_key, private_key):
    """
    Initialise le répertoire client et génère les clés publique et privée.

    Args:
        username (str): Nom d'utilisateur.
        password (str): Mot de passe pour dériver la clé privée.
    """
    client_user_dir = os.path.join(CLIENT_DIR, username)
    os.makedirs(client_user_dir, exist_ok=True)


    # Sauvegarder les clés dans le répertoire client
    private_key_file = os.path.join(client_user_dir, f"private_key.txt")
    with open(private_key_file, "w") as file:
        file.write(f"{private_key[0]},\n{private_key[1]}")
    
    public_key_file = os.path.join(client_user_dir, f"public_key.txt")
    with open(public_key_file, "w") as file:
        file.write(f"{public_key[0]},\n{public_key[1]}")

    print(f"Répertoire client initialisé pour {username}. Clés générées et sauvegardées.")


def load_private_key(username): 
    """
    Loads the private key from the user's directory.
    """
    filepath = os.path.join(CLIENT_DIR, username, "private_key.txt") 
    try:
        with open(filepath, "r") as f:
            n, d = map(int, f.read().strip().split(","))  # Read n and d as integers
        return (n, d)
    except FileNotFoundError:
        print(f"Error: Private key file not found in {filepath}.")
        return None
    except ValueError:
        print("Error: Invalid private key format.")
        return None

def upload_file(username, shared_key, file_path):
    """
    Gère l'upload d'un fichier en le chiffrant avec COBRA puis RSA.

    Args:
        username (str): Nom d'utilisateur.
        shared_key (str): Clé partagée générée par Diffie-Hellman.
        file_path (str): Chemin du fichier à uploader.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")

    # Lire le contenu du fichier
    with open(file_path, "rb") as file:
        data = file.read()

    # Chiffrement avec COBRA (clé partagée)
    cobra_encrypted_data = cobra_encode(data.decode(), shared_key)

    # Charger la clé publique de l'utilisateur
    public_key = load_public_key(username)

    # Chiffrement avec RSA
    rsa_encrypted_data = pow(int.from_bytes(cobra_encrypted_data.encode(), "big"), public_key[0], public_key[1])

    # Déposer le fichier côté serveur
    encrypted_file_name = os.path.basename(file_path) + ".enc"
    handle_file_upload(username, encrypted_file_name, rsa_encrypted_data.to_bytes((rsa_encrypted_data.bit_length() + 7) // 8, "big"))
    print(f"Fichier '{file_path}' chiffré et uploadé avec succès.")

def download_file(username, shared_key, file_name):
    """
    Gère le téléchargement d'un fichier en le déchiffrant avec RSA puis COBRA.

    Args:
        username (str): Nom d'utilisateur.
        shared_key (str): Clé partagée générée par Diffie-Hellman.
        file_name (str): Nom du fichier à télécharger.
    """
    # Télécharger le fichier chiffré depuis le serveur
    encrypted_data = handle_file_download(username, file_name)

    # Charger la clé privée de l'utilisateur
    private_key = load_private_key(username)

    # Déchiffrement avec RSA
    rsa_decrypted_data = pow(int.from_bytes(encrypted_data, "big"), private_key[0], private_key[1])

    # Déchiffrement avec COBRA (clé partagée)
    cobra_decrypted_data = cobra_decode(rsa_decrypted_data.to_bytes((rsa_decrypted_data.bit_length() + 7) // 8, "big").decode(), shared_key)

    # Sauvegarder le fichier dans le répertoire client
    client_user_dir = os.path.join(CLIENT_DIR, username, "Repertoire")
    os.makedirs(client_user_dir, exist_ok=True)
    output_file_path = os.path.join(client_user_dir, file_name.replace(".enc", ""))
    with open(output_file_path, "wb") as file:
        file.write(cobra_decrypted_data.encode())
    print(f"Fichier '{file_name}' téléchargé et déchiffré avec succès.")