import os

BASE_PATH = "./users"

def save_public_key(username, public_key):
    """Sauvegarde la clé publique dans le répertoire utilisateur."""
    user_path = os.path.join(BASE_PATH, username)
    os.makedirs(user_path, exist_ok=True)
    with open(os.path.join(user_path, "public_key.txt"), "w") as pub_file:
        pub_file.write(f"{public_key[0]}\n{public_key[1]}")

def save_private_key(username, private_key):
    """Sauvegarde la clé privée dans le répertoire utilisateur."""
    user_path = os.path.join(BASE_PATH, username)
    with open(os.path.join(user_path, "private_key.txt"), "w") as priv_file:
        priv_file.write(f"{private_key[0]}\n{private_key[1]}")