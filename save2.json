import arcade
from PIL import Image


def load_sheet(filename, frame_count):
    try:
        sheet = Image.open(filename).convert("RGBA")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filename} est introuvable.")
        return []


    w, h = sheet.size
    frame_w = w // frame_count
    textures = []
    for i in range(frame_count):
        left = i * frame_w
        right = left + frame_w
        frame = sheet.crop((left, 0, right, h))
        tex = arcade.Texture(name=f"{filename}_{i}", image=frame)
        textures.append(tex)
    return textures