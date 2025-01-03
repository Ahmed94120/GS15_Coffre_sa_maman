import os
from outils.prime import generate_prime, mod_inverse, is_prime
import libnum

def sponge_hash(password, iterations=100):
    """Implements a hash function based on a sponge construction with multiple phases of absorption and squeezing."""
    state = 0
    for _ in range(iterations):
        for char in password:
            state = (state * 31 + ord(char)) % (2**64)
        password = str(state) + password[::-1]  # Absorption phase
    return state

def key_derivation(password, phi):
    """Derives the private key component 'd' using a sponge function and phi."""
    d = sponge_hash(password) % phi
    if d < 2:
        d += 2

    # Ensures 'd' is prime and coprime with phi
    while True:
        if is_prime(d) and phi % d != 0:
            break
        d += 1
    return d

def rsa_key_derivaded(password):
    """Generates RSA keys using a password."""
    # Step 1: Generate two large primes
    p = generate_prime(2048 // 2)  # Use 2048-bit keys for increased block size
    q = generate_prime(2048 // 2)

    # Step 2: Compute n and phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Step 3: Derive d using the password and compute e
    d = key_derivation(password, phi)
    e = mod_inverse(d, phi)

    if e is None:
        raise ValueError("Failed to calculate modular inverse. 'd' and 'phi' might not be co-prime.")

    return (e, n), (d, n)


def rsa_encrypt(data, public_key):
    """Encrypt binary data using RSA."""
    e, n = public_key
    block_size = (n.bit_length() // 8) - 11  # Allow room for padding or metadata
    encrypted_data = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        block_int = libnum.s2n(block)  # Convert to integer
        encrypted_block = pow(block_int, e, n)  # RSA encryption
        encrypted_block_bytes = libnum.n2s(encrypted_block)  # Convert back to bytes

        # Add the block size as a 2-byte prefix for each encrypted block
        block_size_bytes = len(encrypted_block_bytes).to_bytes(2, 'big')
        encrypted_data += block_size_bytes + encrypted_block_bytes

    return bytes(encrypted_data)

def rsa_decrypt(data, private_key):
    """Decrypt RSA-encrypted data."""
    d, n = private_key
    offset = 0
    decrypted_data = bytearray()

    while offset < len(data):
        # Read the size of the encrypted block
        block_size = int.from_bytes(data[offset:offset + 2], 'big')
        offset += 2

        # Extract and decrypt the block
        encrypted_block = data[offset:offset + block_size]
        offset += block_size
        block_int = libnum.s2n(encrypted_block)  # Convert back to integer
        decrypted_block_int = pow(block_int, d, n)  # RSA decryption
        decrypted_block = libnum.n2s(decrypted_block_int)  # Convert to bytes

        # Append the decrypted block to the output
        decrypted_data += decrypted_block

    return bytes(decrypted_data)