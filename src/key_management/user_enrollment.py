from key_management.key_generation import generate_rsa_keypair
from storage.key_storage import save_public_key, save_private_key

def enroll_user(username):
    """Enrôle un nouvel utilisateur en générant et stockant ses clés RSA."""
    # Générer les clés publique et privée RSA
    public_key, private_key = generate_rsa_keypair()

    # Sauvegarder les clés
    save_public_key(username, public_key)
    save_private_key(username, private_key)

    print(f"Utilisateur '{username}' enrôlé avec succès. Les clés sont stockées dans './users/{username}'")