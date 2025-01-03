# test_import.py
from colors import BLACK, CYAN, tetris_color_to_rgb

print(BLACK)  # Should print: TetrisColor.BLACK
print(CYAN)   # Should print: TetrisColor.CYAN
print(tetris_color_to_rgb(CYAN))  # Should print: (0, 255, 255)