"""
Bibliothèque d'illustrations pixel art vectorielles pour « Angle Mort ».
Chaque illustration est générée en SVG pur, avec un style cyber-rétro pixelisé
parfaitement net, sans recourir à la génération d'images par IA.
"""

def _grid_to_svg(grid, palette, size=32, scale=4, glow_color=None):
    """
    Convertit une matrice de caractères (pixel grid) en SVG avec rendu pixelisé net.
    """
    width = size * scale
    height = size * scale
    rects = []
    
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in palette and palette[char]:
                color = palette[char]
                rects.append(
                    f'<rect x="{x*scale}" y="{y*scale}" width="{scale}" height="{scale}" fill="{color}" />'
                )
    
    filter_def = ""
    glow_attr = ""
    if glow_color:
        filter_def = f'''
        <defs>
          <filter id="pix-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="{glow_color}" flood-opacity="0.45" />
          </filter>
        </defs>'''
        glow_attr = 'filter="url(#pix-glow)"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" shape-rendering="crispEdges">
      {filter_def}
      <g {glow_attr}>
        {''.join(rects)}
      </g>
    </svg>'''


def get_pixel_illustration(kind="radar_eye", accent="#5CC8FF"):
    """
    Retourne l'illustration SVG pixel art adaptée au sujet.
    """
    # Palette dynamique
    DARK = "#1E293B"
    MID = "#475569"
    LIGHT = "#94A3B8"
    WHITE = "#FFFFFF"
    ACC = accent
    RED = "#FF5A4D"
    GOLD = "#F5B83D"

    # 1. SERVEUR EN DANGER / CRASH (menace, panne, cloud)
    if kind in ("server_alert", "menace", "crash", "panne"):
        p = {"#": RED, "=": WHITE, "D": DARK, "M": MID, "L": LIGHT, "G": GOLD}
        # Grille 24x24
        g = [
            "........................",
            ".........######.........",
            "........#======#........",
            ".......#==####==#.......",
            ".......#==####==#.......",
            "........#======#........",
            ".........######.........",
            "..........####..........",
            "..DDDDDDDDDDDDDDDDDDDD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DM##MMLLLLLLLLMM##MD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DDDDDDDDDDDDDDDDDDDD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DM##MMLLLLLLLLMM##MD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DDDDDDDDDDDDDDDDDDDD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DMGGMMLLLLLLLLMM##MD..",
            "..DMMMMMMMMMMMMMMMMMMD..",
            "..DDDDDDDDDDDDDDDDDDDD..",
            "........................",
            "........................",
            "........................",
        ]
        return _grid_to_svg(g, p, size=24, scale=6, glow_color=RED)

    # 2. FUSÉE / LANCEMENT / VITESSE (opportunité, builder, vite)
    elif kind in ("rocket", "opportunite", "launch", "fast"):
        p = {"#": GOLD, "=": WHITE, "A": ACC, "R": RED, "D": DARK, "L": LIGHT}
        g = [
            "...................##...",
            "..................####..",
            ".................#====#.",
            "................#======#",
            "...............#===AA==#",
            "..............#===AAAA=#",
            ".............#===AAAA==#",
            "............#===AAAA==#.",
            "...........#===AAAA==#..",
            "..........#===AAAA==#...",
            ".........#===AAAA==#....",
            "........#===AAAA==#.....",
            "..###..#===AAAA==#......",
            ".#===##===AAAA==#.......",
            "#=====##=AAAA==#........",
            "#======##AAAA==#........",
            ".#======#AAAA==#........",
            "..#====#RAAAA==#........",
            "...###.RRAAAAA==#.......",
            "......RRRRAAAA==#.......",
            ".....RRRRRRAAAA==#......",
            "....RRRRRRRRAAAA=#......",
            "...RRRRRRRRRR##.........",
            "..RRRRRRRR..............",
        ]
        return _grid_to_svg(g, p, size=24, scale=6, glow_color=GOLD)

    # 3. PUCE IA / HARDWARE / GPU / PROCESSEUR
    elif kind in ("ai_chip", "chip", "hardware", "ia", "modele"):
        p = {"#": ACC, "=": WHITE, "D": DARK, "M": MID, "G": GOLD}
        g = [
            "....##..##..##..##......",
            "...################.....",
            ".##DMMMMMMMMMMMMMMD##...",
            "...DMMMMMMMMMMMMMMD.....",
            ".##DMM#G######G#MMD##...",
            "...DMM#G======G#MMD.....",
            ".##DMM#G======G#MMD##...",
            "...DMM#G======G#MMD.....",
            ".##DMM#G======G#MMD##...",
            "...DMM#G######G#MMD.....",
            ".##DMMMMMMMMMMMMMMD##...",
            "...DMMMMMMMMMMMMMMD.....",
            ".##DMMMMMMMMMMMMMMD##...",
            "...################.....",
            "....##..##..##..##......",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
        ]
        return _grid_to_svg(g, p, size=24, scale=6, glow_color=ACC)

    # 4. PAR DÉFAUT : RADAR D'ANGLE MORT / CYBER EYE (le logo emblématique)
    else:
        p = {"#": ACC, "=": WHITE, "D": DARK, "M": MID, "G": GOLD, "R": RED}
        g = [
            "..######........######..",
            ".#======#......#======#.",
            "#========#....#========#",
            "#==####==#....#==####==#",
            "#=#....#=#....#=#....#=#",
            "#=#....#=#....#=#....#=#",
            "........#======#........",
            ".......#========#.......",
            "......#===####===#......",
            ".....#===#====#===#.....",
            "....#===#======#===#....",
            "...#===#===##===#===#...",
            "...#===#==####==#===#...",
            "...#===#===##===#===#...",
            "....#===#======#===#....",
            ".....#===#====#===#.....",
            "......#===####===#......",
            ".......#========#.......",
            "........#======#........",
            "#=#....#=#....#=#....#=#",
            "#=#....#=#....#=#....#=#",
            "#==####==#....#==####==#",
            "#========#....#========#",
            ".#======#......#======#.",
        ]
        return _grid_to_svg(g, p, size=24, scale=6, glow_color=ACC)
