# Define S-boxes
S_BOXES = [
    {i: format((i + 3) % 16, '04b') for i in range(16)},  # Example S-box 1
    {i: format((i * 7 + 5) % 16, '04b') for i in range(16)},  # Example S-box 2
    {i: format((i * 3 + 2) % 16, '04b') for i in range(16)},  # Example S-box 3
    {i: format((i ^ 9) % 16, '04b') for i in range(16)},  # Example S-box 4
]

INVERSE_S_BOXES = [{v: format(k, '04b') for k, v in sbox.items()} for sbox in S_BOXES]

def pad_binary_message(binary_message, block_size=128):
    """
    Pads the binary message to make its length a multiple of block_size.
    The padding length is encoded in the last block.
    """
    padding_length = block_size - (len(binary_message) % block_size)
    padding = '0' * (padding_length - 8) + format(padding_length, '08b')  # Last 8 bits store the padding length
    return binary_message + padding

def unpad_binary_message(binary_message, block_size=128):
    """
    Removes the padding from the binary message using the length encoded in the last block.
    """
    padding_length = int(binary_message[-8:], 2)  # Last 8 bits contain the padding length
    if padding_length > block_size:
        raise ValueError("Invalid padding length")
    return binary_message[:-(padding_length)]

def substitute_with_sboxes(binary_message):
    """
    Substitutes 4-bit blocks using S-boxes.
    """
    # Pad the binary message
    binary_message = pad_binary_message(binary_message)

    # Split into 128-bit blocks
    blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)]
    substituted_blocks = []

    for block in blocks:
        # Split each 128-bit block into 4-bit sub-blocks
        sub_blocks = [block[i:i + 4] for i in range(0, 128, 4)]
        # Substitute using S-boxes
        substituted_block = []
        for idx, sub_block in enumerate(sub_blocks):
            sbox_index = idx // 8  # Determine the S-box (1–7: 0, 8–15: 1, 16–23: 2, 24–31: 3)
            sbox = S_BOXES[sbox_index]
            substituted_block.append(sbox[int(sub_block, 2)])  # Substitute using S-box
        substituted_blocks.append(''.join(substituted_block))

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
    
    # Unpad the decoded message
    decoded_message = unpad_binary_message(decoded_message)

    return decoded_message
