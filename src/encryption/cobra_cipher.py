import numpy as np

def add_round_key(block, key):
    return np.bitwise_xor(block, key)

def substitution(block, s_box):
    return [s_box[b] for b in block]
