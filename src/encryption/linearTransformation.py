def circular_left_shift(binary_str, shift_amount):
    # Perform the circular shift
    return binary_str[shift_amount:] + binary_str[:shift_amount]

def circular_right_shift(binary_str, shift_amount):
    # Perform the circular shift
    return binary_str[-shift_amount:] + binary_str[:-shift_amount]

def left_shift(binary_str, shift_amount):
    # Perform the shift and pad with zeros on the right
    return binary_str[shift_amount:] + '0' * shift_amount

def xor_strings(str1, str2):
    return ''.join(str(int(str1[i]) ^ int(str2[i])) for i in range(len(str1)))

def encode_linear_transformation(binary_message):
    blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)]

    encrypted = []
    for block in blocks:
        A = block[:32]  # First 32 bits
        B = block[32:64]  # Second 32 bits
        C = block[64:96]  # Third 32 bits
        D = block[96:]  # Fourth 32 bits

        #1st row
        A = circular_left_shift(A, 13)
        C = circular_left_shift(C, 3)

        #2nd row
        B = xor_strings(B, A)
        B = xor_strings(B, C)

        #3rd row
        D = xor_strings(D, C)
        D = xor_strings(D, left_shift(A, 3))

        #4th row
        B = circular_left_shift(B, 1)
        D = circular_left_shift(D, 7)

        #5th row
        A = xor_strings(A, B)
        A = xor_strings(A, D)

        #6th row
        C = xor_strings(C, D)
        C = xor_strings(C, left_shift(B, 7))
        A = circular_left_shift(A, 5)

        #7th row
        C = circular_left_shift(C, 22)

        encrypted.append(A + B + C + D)

    return ''.join(encrypted)




def decode_linear_transformation(binary_message):
    blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)]

    decrypted = []
    for block in blocks:
        A = block[:32]  # First 32 bits
        B = block[32:64]  # Second 32 bits
        C = block[64:96]  # Third 32 bits
        D = block[96:]  # Fourth 32 bits

        #7th row
        C = circular_right_shift(C, 22)

        #6th row
        A = circular_right_shift(A, 5)
        C = xor_strings(C, left_shift(B, 7))
        C = xor_strings(C, D)

        #5th row
        A = xor_strings(A, D)
        A = xor_strings(A, B)

        #4th row
        D = circular_right_shift(D, 7)
        B = circular_right_shift(B, 1)

        #3rd row
        D = xor_strings(D, left_shift(A, 3))
        D = xor_strings(D, C)

        #2nd row
        B = xor_strings(B, C)
        B = xor_strings(B, A)

        #1st row
        C = circular_right_shift(C, 3)
        A = circular_right_shift(A, 13)

        decrypted.append(A + B + C + D)

    return ''.join(decrypted)