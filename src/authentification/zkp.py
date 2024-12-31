import random
import os
from server import USERS_DIR


def compute_certificate(public_key, private_key):
    e, n = public_key
    d, _ = private_key
    cert = random.randint(1, n - 1)
    computed_cert = pow(cert, d, n)
    print(f"Certificat généré lors de l'enrôlement : {computed_cert}")
    return computed_cert

def store_user_certificate(username, public_key, cert):
    """
    Stocke la clé publique et le certificat pour un utilisateur.
    """
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    e, n = public_key
    with open(user_file, "w") as file:
        file.write(f"{e}\n{n}\n{cert}")

def load_user_certificate(username):
    """
    Charge la clé publique et le certificat d'un utilisateur.
    """
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    if not os.path.exists(user_file):
        raise FileNotFoundError(f"Certificat pour l'utilisateur {username} introuvable.")
    
    with open(user_file, "r") as file:
        try:
            lines = file.readlines()
            e = int(lines[0].strip())
            n = int(lines[1].strip())
            cert = int(lines[2].strip())
        except (ValueError, IndexError):
            raise ValueError(f"Format incorrect dans le fichier utilisateur {username}.")
    return (e, n), cert



def guillou_quisquater_generate_proof(public_key, private_key, cert):
    e, n = public_key
    d, _ = private_key

    # Étape 1 : Génération de m
    m = random.randint(1, n - 1) % n
    M = pow(m, e, n)

    # Étape 2 : Génération du challenge
    r = random.randint(1, e - 1)
    cert_r = pow(cert, r, n)

    # Étape 3 : Calcul de la preuve
    proof = (m * cert_r) % n

    print(f"M calculé : {M}, m utilisé : {m}")
    print(f"Proof calculé : {proof}, Cert^r mod n : {cert_r}")

    return M, proof, r

def guillou_quisquater_verify_proof(public_key, cert, M, proof, r):
    e, n = public_key

    # Étape 1 : Calcul de Left
    left = pow(proof, e, n)

    # Étape 2 : Calcul de Right
    right_M = M % n
    right_cert = pow(cert, r, n)
    right = (right_M * right_cert) % n

    # Affichage pour validation
    print(f"Verification Guillou-Quisquater :")
    print(f"  Left (Proof^e mod n): {left}")
    print(f"  Right_M (M mod n): {right_M}")
    print(f"  Right_Cert (Cert^r mod n): {right_cert}")
    print(f"  Right (M * Cert^r mod n): {right}")

    return left == right

def load_salt(username):
    """
    Charge le sel associé à un utilisateur.

    Args:
        username (str): Nom de l'utilisateur.

    Returns:
        bytes: Le sel associé.
    """
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    if not os.path.exists(user_file):
        raise FileNotFoundError(f"Le fichier utilisateur pour {username} est introuvable.")

    with open(user_file, "r") as file:
        lines = file.readlines()
        if len(lines) < 4:
            raise ValueError(f"Le fichier utilisateur pour {username} est corrompu.")
        return bytes.fromhex(lines[3].strip())