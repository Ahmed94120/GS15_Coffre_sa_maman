from encryption.xor import * 
from encryption.substitution import *
from encryption.feistel import *
from encryption.linearTransformation import *
from encryption.cobra import *

from outils.hashing import *

if __name__ == "__main__":
    #username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
    #enroll_user(username)

    key = "Monmdp1234"

    # Exemple d'utilisation
    with open("bigprimes.jpg", "rb") as file:
        file_content = file.read()
    print(file_content)

    encoded = cobra_encode(file_content, key)

    with open("output_file", "wb") as file:  # "wb" pour écrire en mode binaire
        file.write(encoded)




    with open("output_file", "rb") as file:  # "wb" pour écrire en mode binaire
        file_content = file.read()

    decoded = cobra_decode(file_content, key)

    with open("image.jpg", "wb") as file:
        file.write(decoded)