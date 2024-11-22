import numpy as np
from outils.blocks import *

# Xor entre un bloc et une clé
def add_round_key(block_msg, block_key):
    return np.bitwise_xor(block_msg, block_key)


# Fonction principale pour chiffrer un message avec une clé
def encrypt_message_with_key(message, key, block_size=16):
    # Convertir le message et la clé en tableau de bytes
    message = pad_message(message, block_size)
    message_bytes = text_to_byte_array(message)
    key_bytes = text_to_byte_array(key)

    # Assurer que la clé est de 128 bits (16 octets)
    if len(key_bytes) < block_size:
        key_bytes = np.pad(key_bytes, (0, block_size - len(key_bytes)), 'wrap')
    elif len(key_bytes) > block_size:
        key_bytes = key_bytes[:block_size]

    # Découper le message en blocs
    blocks = split_into_blocks(message_bytes, block_size)

    # Appliquer XOR bloc par bloc
    encrypted_blocks = [add_round_key(block, key_bytes) for block in blocks]

    # Retourner le message chiffré
    return np.concatenate(encrypted_blocks)




# Fonction pour déchiffrer un message avec une clé
def decrypt_message_with_key(encrypted_bytes, key, block_size=16):
    # Convertir la clé en tableau de bytes
    key_bytes = text_to_byte_array(key)

    # Assurer que la clé est de 128 bits (16 octets)
    if len(key_bytes) < block_size:
        key_bytes = np.pad(key_bytes, (0, block_size - len(key_bytes)), 'wrap')
    elif len(key_bytes) > block_size:
        key_bytes = key_bytes[:block_size]

    # Découper les données chiffrées en blocs
    blocks = split_into_blocks(encrypted_bytes, block_size)

    # Appliquer XOR bloc par bloc pour déchiffrer
    decrypted_blocks = [add_round_key(block, key_bytes) for block in blocks]

    # Convertir les blocs en texte et retirer le padding
    decrypted_message = byte_array_to_text(np.concatenate(decrypted_blocks))
    return unpad_message(decrypted_message)
