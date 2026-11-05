"""An example of drawings kept in a Python module, as sprite_tool.py's export command prints them.

ROWS_NAME is the grid as strings of one-character keys; KEYS_NAME maps each key to #rrggbb. '#' is ink
(#000000) and '.' is clear. sprite_tool.py reads them back as MODULE.py:NAME, for example (from the skill folder):

    python3 scripts/sprite_tool.py check examples/python-module/tangerine.py:TANGERINE16,TANGERINE24

These are the approved 16px and 24px tangerines (1f34a) from the kirupa.com Pixel set: artwork under the free
license in assets/LICENSE.md, not the MIT license that covers this code.
"""

# tangerine (1f34a), 16px: '#' is ink, '.' is clear
ROWS_TANGERINE16 = [
    "....##....#####.",
    "....#a#..#fffc#.",
    ".....#a##ccc##..",
    "....##ggge##....",
    "...#ghhggeee#...",
    "..#ghhhhggeee#..",
    "..#hhiihggeee#..",
    ".#ghhihhggeeee#.",
    ".#gghhhgggeeee#.",
    ".#gggggggeeeed#.",
    ".#eeggggeeeedd#.",
    "..#eeeeeeeedd#..",
    "..#eeeeeeeddb#..",
    "...#eeeeeddb#...",
    "....##eedd##....",
    "......####......",
]
KEYS_TANGERINE16 = {"#": "#000000", "a": "#5b3417", "b": "#a54806", "c": "#3f9a25", "d": "#d4690a", "e": "#f58f0c", "f": "#7ccf3a", "g": "#ffae3d", "h": "#ffd28c", "i": "#ffffff"}

# tangerine (1f34a), 24px: '#' is ink, '.' is clear
ROWS_TANGERINE24 = [
    "........#.......#####...",
    ".......#c#....##ggggg#..",
    "........#c#..#ggggdddd#.",
    ".........#c##ggddddaa#..",
    "........####dddaaaa##...",
    "......##hhhh#######.....",
    ".....#hhhiihhfffff#.....",
    "....#hhhiiiihhfffff#....",
    "...#hhhijjiihfffffff#...",
    "...#hhhijiihfffffffe#...",
    "..#hhhhiiiihfffffffee#..",
    "..#hhhhhiihffffffffee#..",
    "..#fhhhhhhfffffffffee#..",
    "..#ffhhhhfffffffffeee#..",
    "..#fffhhffffffffffeeb#..",
    "..#ffffffffffffffeeeb#..",
    "..#fffffffffffffeeebb#..",
    "..#ffffffffffffeeebbb#..",
    "...#fffffffffeeeeebb#...",
    "...#efffffffeeeeebbb#...",
    "....#eefffffeeeeebb#....",
    ".....#eeeeeeeeebbb#.....",
    "......##eeeeeebb##......",
    "........########........",
]
KEYS_TANGERINE24 = {"#": "#000000", "a": "#2f7a35", "b": "#b8430a", "c": "#965c34", "d": "#4f9e3a", "e": "#e2660c", "f": "#f4900c", "g": "#86c44a", "h": "#ffb03a", "i": "#ffd47a", "j": "#fff4d6"}
