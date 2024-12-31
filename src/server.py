import os

SERVER_DIR = "./server"
USERS_DIR = os.path.join(SERVER_DIR, "Users")
REPERTOIRE_DIR = os.path.join(SERVER_DIR, "Repertoire")
LOG_FILE = os.path.join(SERVER_DIR, "journalisation.log")

def initialize_server():
    """Initialise les répertoires côté serveur."""
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(REPERTOIRE_DIR, exist_ok=True)
    open(LOG_FILE, "a").close()

def log_action(action):
    """Journalise une action côté serveur."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{get_current_time()}] {action}\n")

def get_current_time():
    """Retourne l'heure actuelle formatée."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_user_exists(username):
    """Vérifie si un utilisateur existe déjà."""
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    return os.path.exists(user_file)

def handle_user_enrollment(username, public_key, cert, salt):
    """
    Gère l'enrôlement d'un utilisateur :
    - Stocke la clé publique.
    - Crée un répertoire pour les fichiers de l'utilisateur.
    - Journalise l'action.

    Args:
        username (str): Nom d'utilisateur.
        public_key (tuple): Clé publique de l'utilisateur (e, n).
        cert (str): Certificat généré pour l'utilisateur.
        salt (bytes): Sel utilisé pour dériver la clé privée.
    """
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    with open(user_file, "w") as file:
        file.write(f"{public_key[0]}\n{public_key[1]}\n{cert}\n{salt.hex()}")

    user_dir = os.path.join(REPERTOIRE_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    log_action(f"Utilisateur {username} enrôlé avec succès.")

def handle_file_upload(username, file_name, encrypted_data):
    """
    Permet à un utilisateur de déposer un fichier dans son répertoire côté serveur.

    Args:
        username (str): Nom d'utilisateur.
        file_name (str): Nom du fichier.
        encrypted_data (bytes): Données chiffrées à stocker.
    """
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    if not os.path.exists(user_dir):
        raise FileNotFoundError(f"Le répertoire de l'utilisateur {username} est introuvable.")

    file_path = os.path.join(user_dir, file_name)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

    log_action(f"Fichier '{file_name}' déposé par l'utilisateur {username}.")

def handle_file_download(username, file_name):
    """
    Permet à un utilisateur de consulter un fichier stocké sur le serveur.

    Args:
        username (str): Nom d'utilisateur.
        file_name (str): Nom du fichier à consulter.

    Returns:
        bytes: Données chiffrées du fichier.
    """
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    file_path = os.path.join(user_dir, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier '{file_name}' pour l'utilisateur {username} est introuvable.")

    with open(file_path, "rb") as file:
        data = file.read()

    log_action(f"Fichier '{file_name}' consulté par l'utilisateur {username}.")
    return data

def list_user_files(username):
    """
    Liste les fichiers disponibles dans le répertoire utilisateur côté serveur.

    Args:
        username (str): Nom d'utilisateur.

    Returns:
        list: Liste des noms de fichiers dans le répertoire utilisateur.
    """
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    if not os.path.exists(user_dir):
        raise FileNotFoundError(f"Le répertoire de l'utilisateur {username} est introuvable.")

    files = os.listdir(user_dir)
    log_action(f"L'utilisateur {username} a consulté la liste des fichiers.")
    return files


