import os
from outils.prime import generate_prime, mod_inverse, is_prime

def simple_hash_long(data, output_size=1024):
    """Generates an extended hash by iterating hashing."""
    hash_value = 0
    result = ""
    for i in range(output_size // 32):  # Generate enough blocks for the desired size
        for char in data:
            hash_value = (hash_value * 31 + ord(char) + i) % (2**32)
        result += format(hash_value, "08x")  # 8-character hex representation
    return int(result[:output_size // 4], 16)

def key_derivation(mdp, phi):
    """Derives the private key component 'd' using the password and phi."""
    d = simple_hash_long(mdp, output_size=1024) % phi
    if d < 2:
        d += 2

    # Ensure 'd' is co-prime with phi and is prime
    while True:
        if is_prime(d) and phi % d != 0:
            break
        d += 1
    return d

def rsa_key_derivaded(mdp):
    """Generates RSA keys using a password."""
    # Step 1: Generate two large primes
    p = generate_prime(512)
    q = generate_prime(512)

    # Step 2: Compute n and phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Step 3: Derive d and compute e
    e = 65537  # Standard public exponent
    try:
        d = mod_inverse(e, phi)
    except ValueError:
        raise ValueError("Failed to calculate modular inverse. 'e' and 'phi' might not be co-prime.")

    return (n, e), (n, d)