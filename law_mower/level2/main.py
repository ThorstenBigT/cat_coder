import os
from typing import TypedDict, List, Tuple
import logging
import os
import glob

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

INPUT_DIR = os.path.join(current_dir, "input")
RESULT_DIR = os.path.join(current_dir, "result")

def clean_result_dir():
    logger.info("Cleaning the result directory")
    files = glob.glob(os.path.join(RESULT_DIR, "*.txt"))
    for file in files:
        os.remove(file)
    logger.info("Result directory cleaned")

def generate_grid_layout(path: str, file_path:str):
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    x = y = 0
    for move in path:
        if move == 'W':
            y += 1
        elif move == 'A':
            x -= 1
        elif move == 'S':
            y -= 1
        elif move == 'D':
            x += 1
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    board_layout = {"width": width, "height": height}

    new_filename = os.path.splitext(os.path.basename(file_path))[0]
    new_file_path = os.path.join(RESULT_DIR, f"{new_filename}.txt")
    mode = 'a' if os.path.exists(new_file_path) else 'w'
    with open(new_file_path, mode) as result_file:
        if mode == 'a':
            result_file.write(f"\n")
            for i, count in enumerate(board_layout.items()):
                if i != len(board_layout)-1:
                    result_file.write(f"{count[1]} ")
                else:
                    result_file.write(f"{count[1]}")
        else:
            for i, count in enumerate(board_layout.items()):
                if i != len(board_layout) -1:
                    result_file.write(f"{count[1]} ")
                else:
                    result_file.write(f"{count[1]}")

def main():
    logger.info("Starting the program")
    clean_result_dir()
    logger.debug(INPUT_DIR)
    files = glob.glob(os.path.join(INPUT_DIR, "*.in"))
    logger.debug(f"Files: {files}")
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        logger.debug(f"File Path: {file_path}")
        with open(file_path, 'r') as file:
            path_amount = file.readline().strip()
            for line in file:
                #count_characters(line=line, file_path=file_path)
                generate_grid_layout(line, file_path=file_path)
        
    logger.info("Ending the program")
        

if __name__ == "__main__":
    main()