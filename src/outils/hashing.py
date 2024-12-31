import struct

def sha256(message):
    """
    SHA-256 hash algorithm
    """

    # Constants
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    # Initial hash values
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    # Padding
    message_len = len(message) * 8
    message += b'\x80'  # Add a single '1' bit

    while len(message) % 64 != 56:
        message += b'\x00'

    message += struct.pack('>Q', message_len)

    # Process blocks
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        W = [0] * 64

        for t in range(16):
            W[t] = struct.unpack('>I', block[t * 4:t * 4 + 4])[0]

        for t in range(16, 64):
            s0 = (W[t - 15] >> 7 | W[t - 15] << 25) ^ (W[t - 15] >> 18 | W[t - 15] << 14) ^ (W[t - 15] >> 3)
            s1 = (W[t - 2] >> 17 | W[t - 2] << 15) ^ (W[t - 2] >> 19 | W[t - 2] << 13) ^ (W[t - 2] >> 10)
            W[t] = (W[t - 16] + s0 + W[t - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = H

        for t in range(64):
            S1 = (e >> 6 | e << 26) ^ (e >> 11 | e << 21) ^ (e >> 25 | e << 7)
            ch = (e & f) ^ (~e & g)
            temp1 = h + S1 + ch + K[t] + W[t]
            S0 = (a >> 2 | a << 30) ^ (a >> 13 | a << 19) ^ (a >> 22 | a << 10)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = S0 + maj

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    # Final hash
    return ''.join(format(h, '08x') for h in H)



def subkeys(hash_hex):
    # Step 1: Transform hash into bits
    hash_bits = bin(int(hash_hex, 16))[2:].zfill(256)  # Convert to binary and pad to 256 bits

    # Step 2: Split into 8 blocks of 32 bits
    subkeys = [int(hash_bits[i:i+32], 2) for i in range(0, 256, 32)]  # K0 to K7

    # Step 3: Define phi as a 32-bit binary
    phi = 1.61803398874989
    # Convert phi to 32-bit binary representation without struct
    phi_bits = int((phi - int(phi)) * (1 << 23))  # Simulate 32-bit IEEE-754 for fractional part
    phi_bits = (int(phi) << 23) + phi_bits  # Combine integer and fractional parts
    phi_bits = phi_bits & 0xFFFFFFFF  # Ensure 32-bit

    # Step 4: Generate 132 subkeys
    num_subkeys = 132
    for i in range(8, num_subkeys):
        w_i = (
            subkeys[i - 8] ^
            subkeys[i - 5] ^
            subkeys[i - 3] ^
            subkeys[i - 1] ^
            phi_bits ^
            i
        )
        # Perform left circular shift by 11 bits
        w_i = ((w_i << 11) | (w_i >> (32 - 11))) & 0xFFFFFFFF  # Ensure 32 bits
        subkeys.append(w_i)

    return [f"{key:032b}" for key in subkeys]

S_BOXES = [
    {i: format((i + 3) % 16, '04b') for i in range(16)},  # Example S-box 1
    {i: format((i * 7 + 5) % 16, '04b') for i in range(16)},  # Example S-box 2
    {i: format((i * 3 + 2) % 16, '04b') for i in range(16)},  # Example S-box 3
    {i: format((i ^ 9) % 16, '04b') for i in range(16)},  # Example S-box 4
]

def s_box_transform(value):
    # Apply S-box transformation using S_BOXES
    transformed_value = ""
    for i in range(8):  # Process 4 bits at a time
        nibble = int(value[i * 4:(i + 1) * 4], 2)  # Extract 4 bits
        s_box = S_BOXES[i % len(S_BOXES)]  # Select S-box
        transformed_nibble = s_box[nibble]  # Apply S-box
        transformed_value += transformed_nibble  # Append transformed nibble
    return transformed_value

def generate_tour_keys(subkeys):
    # Apply S-box transformation to each subkey
    transformed_subkeys = [s_box_transform(key) for key in subkeys]

    # Combine every 4 consecutive 32-bit subkeys into a 128-bit tower key
    tower_keys = []
    for i in range(0, len(transformed_subkeys), 4):
        if i + 3 < len(transformed_subkeys):
            tower_key = transformed_subkeys[i] + transformed_subkeys[i + 1] + transformed_subkeys[i + 2] + transformed_subkeys[i + 3]
            tower_keys.append(tower_key)

    return [f"{key}" for key in tower_keys]