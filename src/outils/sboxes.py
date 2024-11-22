import random

def generate_s_box(size=16):
    """Génère une S-Box bijective."""
    s_box = list(range(size))
    random.shuffle(s_box)  # Permutation aléatoire
    return s_box

def generate_multiple_s_boxes(num_s_boxes=4, size=16):
    """Génère plusieurs S-Boxes."""
    s_boxes = []
    for _ in range(num_s_boxes):
        s_boxes.append(generate_s_box(size))
    return s_boxes

def invert_s_box(s_box):
    """Inverse une S-Box pour permettre le déchiffrement."""
    inverted = [0] * len(s_box)
    for i, val in enumerate(s_box):
        inverted[val] = i
    return inverted

def generate_inverse_s_boxes(s_boxes):
    """Génère les S-Boxes inverses pour toutes les S-Boxes données."""
    return [invert_s_box(s_box) for s_box in s_boxes]