from outils.hashing import sha256

def generate_hmac(key, message, block_size=64):
    """
    Manual HMAC implementation using SHA-256.
    key : The key used for HMAC.
    message : The message or file to protect.
    block_size : Block size (default 64 bytes for SHA-256).
    """
    # Convert key and message to bytes if they are not already
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(message, str):
        message = message.encode('utf-8')

    if len(key) > block_size:
        # If the key is larger than the block size, hash it to reduce its size
        key = bytes.fromhex(sha256(key))  # Ensure the result is treated as bytes
    if len(key) < block_size:
        # If the key is smaller than the block size, pad it with zeros
        key += b'\x00' * (block_size - len(key))

    # Create ipad and opad keys
    ipad = bytes((x ^ 0x36) for x in key)
    opad = bytes((x ^ 0x5c) for x in key)

    # Calculate the HMAC
    inner_hash = bytes.fromhex(sha256(ipad + message))  # Ensure bytes conversion
    final_hmac = bytes.fromhex(sha256(opad + inner_hash))  # Ensure bytes conversion

    return final_hmac

def hmac_verify(key, message, expected_hmac, block_size=64):
    """
    Verifies if the calculated HMAC matches the expected HMAC.
    key : The key used for HMAC.
    message : The message or file to verify.
    expected_hmac : The expected HMAC for comparison.
    block_size : Block size (default 64 bytes for SHA-256).
    """
    # Recompute the HMAC for the given message and key
    calculated_hmac = generate_hmac(key, message, block_size)

    # Constant-time comparison to prevent timing attacks
    return constant_time_compare(calculated_hmac, expected_hmac)

def constant_time_compare(val1, val2):
    """
    Compares two values in constant time to prevent timing attacks.
    """
    print(f"val1: {val1}")
    print(f"val2: {val2}")
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= x ^ y
    return result == 0