from GAME.entity.enemy import Enemy
from GAME.textures.load_sheet import load_sheet


TEXTURES = {
    # "idle": "GAME/textures/enemy/exploser/exploser_idle.png",      <= Il faut rajouter ce fichier
    "run": "GAME/textures/enemy/exploser/exploser_run.png",
    "attack": "GAME/textures/enemy/exploser/exploser_attack.png"
}

# idle_textures = load_sheet(TEXTURES["idle"], idk)        <= A CHANGER DCP
run_textures = load_sheet(TEXTURES["run"], 6)
attack_textures = load_sheet(TEXTURES["attack"], 4)

