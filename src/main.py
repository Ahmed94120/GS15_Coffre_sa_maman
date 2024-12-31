from key_management.user_enrollment import enroll_user

from encryption.diffiehellman import *

from encryption.cobra import *

if __name__ == "__main__":
    #username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
    #enroll_user(username)
    
    # Diffie-Hellman
    # Serveur
    p, g = parametres_globaux()
    private_key_server = private_key(p)
    public_key_server = mod_exp(g, private_key_server, p)

    # Client
    private_key_client = private_key(p)
    public_key_client = mod_exp(g, private_key_client, p)

    # Serveur
    shared_key_server = str(diffiehellman(public_key_client, private_key_server, p))

    # Client
    shared_key_client = str(diffiehellman(public_key_server, private_key_client, p))

    assert shared_key_client == shared_key_server, "Les clés partagées ne correspondent pas !"
    print(f"Clé partagée : {shared_key_client}")


    # Exemple d'utilisation COBRA
    message = "Hello, World! This is a test message."
    key = "Monmdp1234"
    print(f"Message original: {message}")
    print(f"Clé original: {key}\n")

    encoded = cobra_encode(message, shared_key_client)
    print(f"Message encodé: {encoded}\n")

    decoded = cobra_decode(encoded, shared_key_server)
    print(f"Message décodé: {decoded}")