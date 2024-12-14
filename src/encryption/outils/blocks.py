def pad_key_to_size(key, size):
    """
    Pads the key to ensure it is {size} bits in binary.
    """
    # Convert key to binary
    key_binary = ''.join(format(ord(char), '08b') for char in key)
    
    # Pad with "0" to ensure it's KEY_BIT_SIZE bits
    if len(key_binary) < size:
        key_binary = key_binary.ljust(size, '0')
    return key_binary[:size]  # Truncate if it's longer than KEY_BIT_SIZE bits
