from outils.prime import generate_prime

def generate_rsa_keypair(bits=1024):
    """Génère un couple de clés publique et privée RSA."""
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choisir e, petit et premier avec phi
    e = 65537
    d = pow(e, -1, phi)  # Calcul de d, l'inverse modulaire de e
    return (e, n), (d, n)
