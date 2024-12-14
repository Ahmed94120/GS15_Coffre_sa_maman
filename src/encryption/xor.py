from encryption.outils.blocks import pad_key_to_size

KEY_BIT_SIZE = 128

def string_to_bits_separated(input_string):
    """
    Converts a string into its binary representation as a list of 8-bit strings.
    """
    return [format(ord(char), '08b') for char in input_string]

def binary_to_list(bits):
    return [bits[i:i + 8] for i in range(0, len(bits), 8)]

def xor_encrypt_decrypt(binary_message, key):
    """
    Encrypts or decrypts a binary message using XOR with a key.
    """
    # Get x-bit binary key
    binary_key = pad_key_to_size(key, KEY_BIT_SIZE)
    
    # Repeat key bits to match the length of the message
    full_key_bits = ''.join(binary_key[i % KEY_BIT_SIZE] for i in range(len(binary_message) * 8))
    #print("Full key :", full_key_bits)
    
    # XOR each bit of the binary message with the corresponding key bit
    encrypted_binary_message = []
    for i, char_bits in enumerate(binary_message):
        encrypted_bits = ''.join(
            str(int(bit) ^ int(full_key_bits[i * 8 + j])) for j, bit in enumerate(char_bits)
        )
        encrypted_binary_message.append(encrypted_bits)
    
    return encrypted_binary_message
