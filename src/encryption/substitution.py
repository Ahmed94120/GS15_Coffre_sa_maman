# Substitution des octets d'un bloc avec une S-Box
def substitution(block, s_box):
    return [s_box[b] for b in block]