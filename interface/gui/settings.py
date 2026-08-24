import webcolors


WIDTH = 1280
HEIGHT = 720
MAPDIR = "../maps"


def rainbow() -> list[tuple[int, int, int]]:
    return [
        webcolors.hls_to_rgb(((index % 7) * (360.0 / 7) / 360.0, 0.5, 1.0))
        for index in range(7)
    ]


#                      DIMENSION DES SPRITES C'EST 120 (H) X 80 (V) SCAN + IDLE
#                           DIMENSION DES SPRITES C'EST 120 (H) X 100 (V) DEATH
#                           DIMENSION DES SPRITES C'EST 120 (H) X 100 (V) DEATH
# color theme:
# Arrière-plans
COLOR_BG_MAIN = "#0F172A"       # Fond de fenêtre
COLOR_BG_SURFACE = "#1E293B"    # Cartes & Panneaux

# Boutons & Éléments cliquables
COLOR_BTN_DEFAULT = "#334155"   # Bouton standard
COLOR_BTN_ACCENT = "#F97316"    # Bouton orange principal
COLOR_BTN_HOVER = "#FB923C"     # Bouton orange survolé
COLOR_BORDER = "#475569"        # Bordures

# Textes
COLOR_TEXT_PRIMARY = "#F8FAFC"  # Texte principal (Blanc cassé)
COLOR_TEXT_MUTED = "#94A3B8"    # Texte secondaire (Gris clair)
