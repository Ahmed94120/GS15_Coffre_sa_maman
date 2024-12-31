import random

def generate_prime(bits=2024):
    """Génère un nombre premier de la taille spécifiée."""
    while True:
        prime = random.getrandbits(bits)
        if Miller_Rabin(prime):
            return prime

def Miller_Rabin(n, k=10):
    """Test de primalité de Miller-Rabin."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True