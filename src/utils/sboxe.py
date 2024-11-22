import random
import os

from storage.sboxes_storage import save_s_boxes_to_file


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


if __name__ == "__main__":
    # Génération de 4 S-Boxes de taille 16 (pour blocs de 4 bits)
    s_boxes = generate_multiple_s_boxes(num_s_boxes=4, size=16)

    # Affichage des S-Boxes
    for i, s_box in enumerate(s_boxes):
        print(f"S-Box {i+1} : {s_box}")

    save_s_boxes_to_file(s_boxes, filename="s_boxes.json")

