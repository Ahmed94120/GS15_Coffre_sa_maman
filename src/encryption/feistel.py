
def tabulate_f():
    # Initialise le tableau des résultats pour f(x)
    Z = [0] * 256  # 256 entrées pour les valeurs 0 à 255
        
    for x in range(256):
        inv1 = pow(x + 1, -1, 257)  # pow(a, -1, m) calcule l'inverse modulaire de a mod m

        Z[x] = inv1
        
    return Z

def simple_prng(value, a=1664525, c=1013904223, m=2**32):
    # Generate a pseudo-random number using LCG
    output = (a * value + c) % m
    return output % 256

def F(Kn, R):

    #Etape 1
    Z = tabulate_f()    # Pré-calculé Z

    #Separate in blocks
    blocks = [R[i:i+8] for i in range(0, len(R), 8)]
    #Invert order of the bits inside each blocks
    inv_blocks = [bloc[::-1] for bloc in blocks]

    processed_blocks = [ format(Z[int(block, 2)], '08b') for block in inv_blocks]
    processed_blocks = ''.join(processed_blocks)

    #Etape 2
    #X[n] ← X[p[n]]
    #Généré par 
    #permutation_table = list(range(64))
    #random.shuffle(permutation_table)
    X = [36, 20, 5, 56, 50, 59, 0, 52, 30, 14, 9, 21, 27, 54, 38, 6, 37, 24, 25, 41, 47, 19, 32, 46, 57, 15, 34, 1, 39, 40, 44, 61, 12, 35, 48, 63, 31, 18, 28, 4, 11, 13, 53, 7, 23, 55, 33, 10, 62, 3, 49, 26, 2, 58, 51, 22, 17, 42, 60, 8, 43, 45, 29, 16]
    #Inverse de X au cas ou
    #Y = [6, 27, 52, 49, 39, 2, 15, 43, 59, 10, 47, 40, 32, 41, 9, 25, 63, 56, 37, 21, 1, 11, 55, 44, 17, 18, 51, 12, 38, 62, 8, 36, 22, 46, 26, 33, 0, 16, 14, 28, 29, 19, 57, 60, 30, 61, 23, 20, 34, 50, 4, 54, 7, 42, 13, 45, 3, 24, 53, 5, 58, 31, 48, 35]
    shuffled_bits = ''.join(processed_blocks[X[n]] for n in range(len(X)))

    #Etape 3
    blocks = [shuffled_bits[i:i+8] for i in range(0, len(shuffled_bits), 8)]
    result = ''.join(format(simple_prng(int(block, 2)), '08b') for block in blocks)
    
    return ''.join(str(int(result[i]) ^ int(Kn[i])) for i in range(len(result)))
    

def feistel(blocks, W):
    """
    Encode the input binary string using the described method.
    """

    iterations = 3  # Number of Feistel-like iterations
        
    encoded_blocks = []

    for block in blocks:
        # Split block into L and R
        L, R = block[:64], block[64:]
        
        for i in range(iterations):
            Kn = W[i % len(W)]

            # Perform iteration
            new_L = R
            F_result = F(Kn, R)
            new_R = ''.join(str(int(L[i]) ^ int(F_result[i])) for i in range(64))
                
            # Swap L and R for next iteration
            L, R = new_L, new_R
            
        # Combine final L and R to form the encoded block
        encoded_blocks.append(L + R)
        
    return ''.join(encoded_blocks)


def feistel_decode(binary_message, W):
    iterations=3
    decoded_blocks = []

    blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)]

    for block in blocks:
        # Split block into L and R
        L, R = block[:64], block[64:]

        # Perform iterations in reverse
        for j in range(iterations):
            # Select the current key (reverse order)
            Kn = W[(iterations - 1 - j) % len(W)]
            
            # Reverse Feistel iteration
            F_result = F(Kn, L)
            new_R = L
            new_L = ''.join(str(int(R[i]) ^ int(F_result[i])) for i in range(64))

            # Update L and R for the next round
            L, R = new_L, new_R

        # Combine final L and R to form the decoded block
        decoded_blocks.append(L + R)

    # Return the decoded blocks as a single binary string
    return decoded_blocks