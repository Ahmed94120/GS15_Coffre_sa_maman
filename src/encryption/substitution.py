# Define S-boxes
S_BOXES = [
    {i: format((i + 3) % 16, '04b') for i in range(16)},  # Example S-box 1
    {i: format((i * 7 + 5) % 16, '04b') for i in range(16)},  # Example S-box 2
    {i: format((i * 3 + 2) % 16, '04b') for i in range(16)},  # Example S-box 3
    {i: format((i ^ 9) % 16, '04b') for i in range(16)},  # Example S-box 4
]

print(S_BOXES)

INVERSE_S_BOXES = [{v: format(k, '04b') for k, v in sbox.items()} for sbox in S_BOXES]

def substitute_with_sboxes(binary_message):
    """
    Substitutes 4-bit blocks using S-boxes.
    """
    #print(S_BOXES)
    # Pad the binary message to make its length a multiple of 128
    if len(binary_message) % 128 != 0:
        binary_message = binary_message.ljust(len(binary_message) + (128 - len(binary_message) % 128), '0')

    # Split into 128-bit blocks
    blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)]
    substituted_blocks = []

    for block in blocks:
        # Split each 128-bit block into 4-bit sub-blocks
        sub_blocks = [block[i:i + 4] for i in range(0, 128, 4)]
        #print("Sub_blocks : ",sub_blocks)
        # Substitute using S-boxes
        substituted_block = []
        for idx, sub_block in enumerate(sub_blocks):
            sbox_index = idx // 8  # Determine the S-box (1–7: 0, 8–15: 1, 16–23: 2, 24–31: 3)
            sbox = S_BOXES[sbox_index]
            substituted_block.append(sbox[int(sub_block, 2)])  # Substitute using S-box
        substituted_blocks.append(''.join(substituted_block))
        #print("Substituted_blocks : ", substituted_blocks)

    return substituted_blocks


def decode_substituted_blocks(substituted_blocks):
    """
    Decodes substituted blocks by reversing the S-box substitutions.
    """
    decoded_message = ''

    for block in substituted_blocks:
        # Split each 128-bit block into 4-bit sub-blocks
        sub_blocks = [block[i:i + 4] for i in range(0, 128, 4)]
        
        # Reverse the substitution using inverse S-boxes
        decoded_block = []
        for idx, sub_block in enumerate(sub_blocks):
            sbox_index = idx // 8  # Determine the S-box (1–7: 0, 8–15: 1, 16–23: 2, 24–31: 3)
            inverse_sbox = INVERSE_S_BOXES[sbox_index]
            decoded_block.append(inverse_sbox[sub_block])  # Reverse substitute using inverse S-box
        decoded_message += ''.join(decoded_block)
    
    return decoded_message