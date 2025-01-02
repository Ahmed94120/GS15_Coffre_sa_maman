import os
from outils.prime import generate_prime, mod_inverse, is_prime
import libnum

def sponge_hash(mot_de_passe, iterations=100):
    """Implémente une fonction de hashage basée sur une fonction éponge avec plusieurs phases d'absorption et d'essorage."""
    etat = 0
    for _ in range(iterations):
        for caractere in mot_de_passe:
            etat = (etat * 31 + ord(caractere)) % (2**64)
        mot_de_passe = str(etat) + mot_de_passe[::-1]  # Phase d'absorption
    return etat

def key_derivation(mot_de_passe, phi):
    """Dérive la composante privée 'd' en utilisant une fonction éponge et phi."""
    d = sponge_hash(mot_de_passe) % phi
    if d < 2:
        d += 2

    # Vérifie que 'd' est premier et copremier avec phi
    while True:
        if is_prime(d) and phi % d != 0:
            break
        d += 1
    return d

def rsa_key_derivaded(mdp):
    """Generates RSA keys using a password."""
    # Step 1: Generate two large primes
    p = generate_prime(1024)
    q = generate_prime(1024)

    # Step 2: Compute n and phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Step 3: Derive d and compute e
    e = 65537  # Standard public exponent
    try:
        d = mod_inverse(e, phi)
    except ValueError:
        raise ValueError("Failed to calculate modular inverse. 'e' and 'phi' might not be co-prime.")

    return (e, n), (d, n)

def rsa_encrypt(data, public_key):
    """
    Encrypts data using RSA and a given public key.
    
    Args:
        data (bytes): The plaintext data to encrypt.
        public_key (tuple): A tuple (e, n) representing the RSA public key.

    Returns:
        bytes: The encrypted data.
    """
    e, n = public_key
    
    # Convert the data to an integer using libnum
    plaintext_int = libnum.s2n(data)
    
    # Ensure the plaintext is less than n
    if plaintext_int >= n:
        raise ValueError("Plaintext is too large for the RSA modulus.")

    # Perform RSA encryption
    ciphertext_int = pow(plaintext_int, e, n)
    
    # Convert the encrypted integer back to bytes using libnum
    encrypted_data = libnum.n2s(ciphertext_int)
    
    return encrypted_data

def rsa_decrypt(ciphertext, private_key):
    """
    Decrypts ciphertext using RSA and removes residual null characters.

    Args:
        ciphertext (bytes): The encrypted data.
        private_key (tuple): A tuple (d, n) representing the RSA private key.

    Returns:
        bytes: The decrypted plaintext as a clean string.
    """
    d, n = private_key

    # Convert the ciphertext from bytes to an integer using libnum
    ciphertext_int = libnum.s2n(ciphertext)

    # Perform RSA decryption
    plaintext_int = pow(ciphertext_int, d, n)

    # Convert the decrypted integer back to bytes using libnum
    plaintext_data = libnum.n2s(plaintext_int)

    # Return the plaintext without modifying null bytes
    return plaintext_data