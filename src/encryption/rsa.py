import os
from outils.prime import generate_prime, mod_inverse, is_prime

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

    return (e, n), (d, n)