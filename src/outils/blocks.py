import numpy as np

# Convertir une chaîne de caractères en tableau de bytes
def text_to_byte_array(text):
    return np.frombuffer(text.encode('utf-8'), dtype=np.uint8)

# Convertir un tableau de bytes en chaîne de caractères
def byte_array_to_text(byte_array):
    return byte_array.tobytes().decode('utf-8')

# Ajouter du padding pour que le message soit un multiple de 128 bits (16 octets)
def pad_message(message, block_size=16):
    padding_length = block_size - (len(message) % block_size)
    padding = chr(padding_length) * padding_length
    return message + padding

# Supprimer le padding après le déchiffrement
def unpad_message(message):
    padding_length = ord(message[-1])
    return message[:-padding_length]

# Découper le message en blocs de taille fixe
def split_into_blocks(byte_array, block_size=16):
    return [byte_array[i:i + block_size] for i in range(0, len(byte_array), block_size)]
