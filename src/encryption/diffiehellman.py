from outils.prime import generate_prime
import random

def mod_exp(base, exponent, modulus):
    """
    Performs modular exponentiation to handle calculations with large numbers efficiently.
    This computes (base^exponent) % modulus using an optimized method.
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        # If the current exponent bit is 1, multiply the base with the result
        if exponent % 2 == 1:
            result = (result * base) % modulus
        # Right shift the exponent (equivalent to integer division by 2)
        exponent = exponent >> 1
        # Square the base and apply modulus
        base = (base * base) % modulus
    return result

def parametres_globaux():
    """
    Generates global parameters for the Diffie-Hellman key exchange:
    - A large prime number (p)
    - A random generator (g) within the range [2, p-1]
    """
    p = generate_prime(512)  # Generate a 512-bit prime number
    g = random.randint(2, p-1)  # Random generator
    print(f"Global parameters: p = {p}, g = {g}")
    return p, g

def private_key(p):
    """
    Generates a private key for Diffie-Hellman.
    The private key is a random integer within the range [2, p-2].
    """
    return random.randint(2, p-2)

def diffiehellman(public_key, private_key, p):
    """
    Computes the shared key using Diffie-Hellman:
    - public_key: The public key of the other party
    - private_key: The private key of the current party
    - p: The prime modulus
    Returns the shared key as an integer.
    """
    return mod_exp(public_key, private_key, p)