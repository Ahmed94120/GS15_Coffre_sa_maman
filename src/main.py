from key_management.user_enrollment import enroll_user
from encryption.xor import *
from encryption.substitution import *
from encryption.feistel import *
from encryption.outils.hashing import *

if __name__ == "__main__":
    #username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
    #enroll_user(username)

    # Exemple d'utilisation
    message = "Hello, World! This is a test message."
    key = "Monmdp1234"
    print(f"Message original: {message}")
    print(f"Clé original: {key}\n")

    hash = sha256(key.encode())
    print(f"Hash du mdp : {hash}\n")

    K = subkeys(hash)
    print(f"Sous clé du hash: {K}\n\n")

    W = generate_tour_keys(K)
    #print(f"Liste des clés de tour: {W}\n")

    print("############################################################")
    print("#Test")
    print("############################################################\n")

    def tabulate_f():
        # Initialise le tableau des résultats pour f(x)
        Z = [0] * 256  # 256 entrées pour les valeurs 0 à 255
        
        for x in range(256):
            inv1 = pow(x + 1, -1, 257)  # pow(a, -1, m) calcule l'inverse modulaire de a mod m

            Z[x] = inv1
        
        return Z

# Appeler la fonction pour générer le tableau
    Z = tabulate_f()
    print("Z", Z)

    print("############################################################")
    print("# encode the message")
    print("############################################################\n")


   # Convert the message to binary representation
    binary_result_list = string_to_bits_separated(message)
    print(f"Message original: {message}")
    print(f"Representation binaire de '{message}' en liste: {binary_result_list}\n")
    print(f"Length message: {len(message)}")
    print(f"Length of binary message: {len(binary_result_list)}\n")

    # Encrypt the binary message
    encrypted_message = xor_encrypt_decrypt(binary_result_list, key)
    print(f"Message encodé: {''.join(encrypted_message)}\n")

    # Substitute using S-boxes
    # Join encrypted binary into a single string
    encrypted_binary_string = ''.join(encrypted_message)
    substituted_blocks = substitute_with_sboxes(encrypted_binary_string)
    print(f"Message encodé après substitution: {''.join(substituted_blocks)}\n")

    # Feistel
    encrypted_feistel = feistel(substituted_blocks, W)
    print(f"Message encodé après feistel: {encrypted_feistel}\n")


    print("\n############################################################")
    print("Decode the message")
    print("############################################################\n")

    # Decode the feistel encoded message
    decoded = feistel_decode(encrypted_feistel, W)
    print(f"Message decodé après feistel: {''.join(decoded)}\n")

    # Decode the substituted blocks
    decoded_binary_string = decode_substituted_blocks(decoded)
    print(f"Message decodé après subsitution: {''.join(decoded_binary_string)}\n")

    binary_result_list = binary_to_list(decoded_binary_string)
    # Decrypt the xored message
    decrypted_message = xor_encrypt_decrypt(binary_result_list, key)
    print(f"Message decodé: {''.join(decrypted_message)}\n")

    # Convert decrypted binary back to text
    decrypted_text = ''.join(chr(int(bits, 2)) for bits in decrypted_message)
    print(f"Message clair: {decrypted_text}")