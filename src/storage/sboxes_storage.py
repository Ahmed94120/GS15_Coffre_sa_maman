import json

PATH = "./s_boxes"

def save_s_boxes_to_file(s_boxes, filename="s_boxes.json"):
    """Sauvegarde les S-Boxes dans un fichier JSON."""
    with open(filename, 'w') as file:
        json.dump(s_boxes, file, indent=4)
    print(f"S-Boxes sauvegardées dans le fichier : {filename}")

def load_s_boxes_from_file(filename="s_boxes.json"):
    """Charge les S-Boxes depuis un fichier JSON."""
    with open(filename, 'r') as file:
        s_boxes = json.load(file)
    print(f"S-Boxes chargées depuis le fichier : {filename}")
    return s_boxes