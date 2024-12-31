from outils.prime import generate_prime
import random

def mod_exp(base, exponent, modulus):
    """
    Exponentiation modulaire pour éviter les calculs avec de grands nombres.
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:  # Si l'exponent est impair
            result = (result * base) % modulus
        exponent = exponent >> 1  # Division par 2
        base = (base * base) % modulus
    return result

def parametres_globaux():
    p = generate_prime()  # Nombre premier
    g = random.randint(2, p-1)  # Générateur aléatoire

    print(f"Paramètres globaux : p = {p}, g = {g}")

    return p, g

def private_key(p):
    private_key = random.randint(2, p-2)  # Clé privée du client

    return private_key

def diffiehellman(public_key, private_key, p):

    shared_key = mod_exp(public_key, private_key, p)

    return shared_key