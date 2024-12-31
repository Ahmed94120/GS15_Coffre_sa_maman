import random
import os
from math import gcd
from outils.prime import is_prime

CLIENT_DIR = "./client"

def generate_rsa_keypair_from_derived_key(derived_key, bits=1024):
    """
    Génère une paire de clés RSA à partir d'une clé dérivée.
    
    Args:
        derived_key (bytes): La clé dérivée.
        bits (int): Taille des clés RSA.
    
    Returns:
        tuple: Clé publique (e, n) et clé privée (d, n).
    """

    # Convertir la clé dérivée en un entier
    random.seed(int.from_bytes(derived_key, byteorder="big"))

    # Générer deux nombres premiers
    def generate_prime(bits):
        while True:
            num = random.getrandbits(bits)
            if is_prime(num):
                return num

    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Trouver e tel que gcd(e, phi) = 1
    e = 65537
    while gcd(e, phi) != 1:
        e += 2

    # Calculer d, l'inverse modulaire de e mod phi
    d = pow(e, -1, phi)
    return (e, n), (d, n)


def custom_kdf(password, salt, iterations=100000, key_length=32):
    """
    Implémentation simple d'une fonction de dérivation de clé sans librairies externes.
    
    Args:
        password (str): Le mot de passe en entrée.
        salt (bytes): Un sel aléatoire (16 octets par exemple).
        iterations (int): Nombre d'itérations pour augmenter la sécurité.
        key_length (int): Taille de la clé dérivée en octets.
    
    Returns:
        bytes: La clé dérivée.
    """
    # Convertir le mot de passe et le sel en entiers
    password_int = sum([ord(c) for c in password])
    salt_int = sum([b for b in salt])

    # Initialiser la clé dérivée
    derived_key = password_int ^ salt_int  # XOR initial pour mélanger le mot de passe et le sel

    # Effectuer les itérations
    for _ in range(iterations):
        derived_key = (derived_key * 31 + salt_int) % (2 ** 256)  # Mélange simple avec modulo

    # Convertir la clé dérivée en bytes
    derived_key_bytes = derived_key.to_bytes(key_length, 'big')
    return derived_key_bytes[:key_length]


def generate_salt(length=16):
    """Génère un sel aléatoire."""
    return os.urandom(length)


def load_public_key(username):
    """Charge la clé publique d'un utilisateur."""
    public_key_path = os.path.join(CLIENT_DIR, username, "public_key.txt")
    if not os.path.exists(public_key_path):
        raise FileNotFoundError(f"La clé publique de l'utilisateur {username} est introuvable.")
    with open(public_key_path, "r") as file:
        e = int(file.readline().strip())
        n = int(file.readline().strip())
    return (e, n)


def load_private_key(username):
    """Charge la clé privée d'un utilisateur."""
    private_key_path = os.path.join(CLIENT_DIR, username, "private_key.txt")
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"La clé privée de l'utilisateur {username} est introuvable.")
    with open(private_key_path, "r") as file:
        d = int(file.readline().strip())
        n = int(file.readline().strip())
    return (d, n)


def save_keypair(username, public_key, private_key):
    """Sauvegarde les clés publique et privée dans le répertoire de l'utilisateur."""
    user_dir = os.path.join(CLIENT_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    # Sauvegarder la clé publique
    public_key_path = os.path.join(user_dir, "public_key.txt")
    with open(public_key_path, "w") as file:
        file.write(f"{public_key[0]}\n{public_key[1]}")

    # Sauvegarder la clé privée
    private_key_path = os.path.join(user_dir, "private_key.txt")
    with open(private_key_path, "w") as file:
        file.write(f"{private_key[0]}\n{private_key[1]}")
    print(f"Clés sauvegardées pour l'utilisateur {username}.")

def load_public_key(username):
    """Charge la clé publique d'un utilisateur."""
    public_key_path = os.path.join(CLIENT_DIR, username, "public_key.txt")
    if not os.path.exists(public_key_path):
        raise FileNotFoundError(f"La clé publique de l'utilisateur {username} est introuvable.")
    with open(public_key_path, "r") as file:
        e = int(file.readline().strip())
        n = int(file.readline().strip())
    return (e, n)

def load_private_key(username):
    """Charge la clé privée d'un utilisateur."""
    private_key_path = os.path.join(CLIENT_DIR, username, "private_key.txt")
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"La clé privée de l'utilisateur {username} est introuvable.")
    with open(private_key_path, "r") as file:
        d = int(file.readline().strip())
        n = int(file.readline().strip())
    return (d, n)
