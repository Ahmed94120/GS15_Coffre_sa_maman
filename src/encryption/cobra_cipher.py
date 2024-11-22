import numpy as np

# Xor entre un bloc et une clé
def add_round_key(block, key):
    return np.bitwise_xor(block, key)

# Substitution des octets d'un bloc avec une S-Box
def substitution(block, s_box):
    return [s_box[b] for b in block]


# Convertir le texte en blocs de taille fixe (16 octets)
def text_to_blocks(text, block_size=16):
    # Ajouter des caractères de remplissage pour que la longueur soit un multiple du bloc
    padding_length = block_size - (len(text) % block_size)
    text += chr(padding_length) * padding_length  # Ajout du padding PKCS7
    return [np.frombuffer(text[i:i+block_size].encode('utf-8'), dtype=np.uint8)
            for i in range(0, len(text), block_size)]

# Convertir la clé en un bloc de 16 octets
def key_to_block(key, block_size=16):
    key = key.ljust(block_size, '\0')  # Remplir la clé si nécessaire
    return np.frombuffer(key.encode('utf-8'), dtype=np.uint8)