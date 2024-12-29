from encryption.xor import *
from encryption.substitution import *
from encryption.feistel import *
from encryption.linearTransformation import *

from encryption.outils.hashing import *

def cobra_encode(file, key):
    hash = sha256(key.encode())
    #print(f"Hash du mdp : {hash}\n")

    K = subkeys(hash)
    #print(f"Sous clé du hash: {K}\n\n")

    W = generate_tour_keys(K)
    #print(f"Liste des clés de tour: {W}\n")

    binary_result_list = string_to_bits_separated(file)
    encrypted_message = xor_encrypt_decrypt(binary_result_list, key)
    substituted_blocks = substitute_with_sboxes(''.join(encrypted_message))
    encrypted_feistel = feistel(substituted_blocks, W)
    final_encrypted = encode_linear_transformation(encrypted_feistel)

    return final_encrypted

def cobra_decode(encoded_file, key):
    hash = sha256(key.encode())
    #print(f"Hash du mdp : {hash}\n")

    K = subkeys(hash)
    #print(f"Sous clé du hash: {K}\n\n")

    W = generate_tour_keys(K)
    #print(f"Liste des clés de tour: {W}\n")

    decoded = decode_linear_transformation(encoded_file)
    decoded_feistel = feistel_decode(decoded, W)
    decoded_binary_string = decode_substituted_blocks(decoded_feistel)
    binary_result_list = binary_to_list(decoded_binary_string)
    decrypted_message = xor_encrypt_decrypt(binary_result_list, key)

    return ''.join(chr(int(bits, 2)) for bits in decrypted_message)