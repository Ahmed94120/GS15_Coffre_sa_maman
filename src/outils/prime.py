import random

def generate_prime(bits):
    """
    Generates a prime number of the specified bit size.

    Parameters:
    - bits (int): The desired bit size of the prime number.

    Returns:
    - int: A prime number with the specified bit size.
    """
    while True:
        prime = random.getrandbits(bits)  # Generate a random number with the specified bit size
        if is_prime(prime):  # Check if the number is prime
            return prime  # Return the prime number if valid

def is_prime(n, k=10):
    """
    Miller-Rabin primality test to determine if a number is prime.

    Parameters:
    - n (int): The number to test for primality.
    - k (int): The number of iterations for accuracy (default: 10).

    Returns:
    - bool: True if the number is probably prime, False otherwise.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Decompose n-1 into d * 2^s
    s, d = 0, n - 1
    while d % 2 == 0:
        d >>= 1  # Right shift to divide by 2
        s += 1

    # Perform Miller-Rabin test k times
    for _ in range(k):
        a = random.randint(2, n - 2)  # Random base 'a' in the range [2, n-2]
        x = pow(a, d, n)  # Compute a^d % n
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):  # Repeat squaring
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite number
    return True  # Probably prime

def mod_inverse(a, m):
    """
    Computes the modular multiplicative inverse of a modulo m.

    Parameters:
    - a (int): The number for which the inverse is calculated.
    - m (int): The modulus.

    Returns:
    - int: The modular inverse of a modulo m, or raises an exception if not found.
    """
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m  # Compute the quotient
        a, m = m, a % m  # Update a and m
        x0, x1 = x1 - q * x0, x0  # Update x0 and x1
    return x1 + m0 if x1 < 0 else x1  # Ensure the result is positive