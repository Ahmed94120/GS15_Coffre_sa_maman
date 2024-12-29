from key_management.user_enrollment import enroll_user

from encryption.cobra import *

if __name__ == "__main__":
    #username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
    #enroll_user(username)

    # Exemple d'utilisation
    message = "Hello, World! This is a test message."
    key = "Monmdp1234"
    print(f"Message original: {message}")
    print(f"Clé original: {key}\n")

    encoded = cobra_encode(message, key)
    print(f"Message encodé: {encoded}\n")

    decoded = cobra_decode(encoded, key)
    print(f"Message décodé: {decoded}")