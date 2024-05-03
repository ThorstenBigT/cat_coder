import os
from typing import TypedDict, List, Tuple, Dict
import logging
import os
import glob
import pandas as pd
import numpy as np

class BoundedMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.zeros((rows, cols))

    def __getitem__(self, index):
        row, col = index
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.matrix[row, col]
        else:
            raise IndexError("Index out of bounds")

    def __setitem__(self, index, value):
        row, col = index
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix[row, col] = value
        else:
            raise IndexError("Index out of bounds")
        
    def calculate_sum(self):
        return np.sum(self.matrix)
    
    def add_to_cell(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix[row, col] += value
        else:
            raise IndexError("Index out of bounds")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LawnSize(TypedDict):
    rows: int
    columns: int


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

def get_lawn_size(rows_columns: List[str]) -> LawnSize:
    lawn_size = {}
    lawn_size["columns"] = int(rows_columns[0])
    lawn_size["rows"] = int(rows_columns[1])
    return lawn_size

def get_row_column(position: int, lawn_size: LawnSize) -> Tuple[int, int]:
    row = position // lawn_size["columns"]
    column = position % lawn_size["columns"] 
    return row, column  

def main():
    logger.info("Starting the program")
    clean_result_dir()
    logger.debug(INPUT_DIR)
    files = glob.glob(os.path.join(INPUT_DIR, "*.in"))
    logger.debug(f"Files: {files}")
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        logger.debug(f"File Path: {file_path}")
        result_string = ""
        with open(file_path, 'r') as file:
            amount_of_lawn = file.readline().strip()
            for _ in range(int(amount_of_lawn)):
                lawn_size = file.readline().strip()
                lawn_size = get_lawn_size(lawn_size.split(" "))
                n = lawn_size["rows"]
                lines = [file.readline().strip() for _ in range(n)]
                tree_position = "".join(lines)
                tree_position = tree_position.index("X")
                tree_position_row, tree_postition_column = get_row_column(tree_position, lawn_size)
                path = file.readline().strip()

                valid_path = False
                amount_of_positions = lawn_size["rows"] * lawn_size["columns"]
                if len(path) != amount_of_positions - 2:
                        logger.error("Path is too long or to short")
                else:        
                    for i in range(amount_of_positions):
                        if i == tree_position:
                            continue
                        lawn_df = BoundedMatrix(lawn_size["rows"], lawn_size["columns"])
                        lawn_df.add_to_cell(tree_position_row, tree_postition_column, 1)
                        current_starting_position = i
                        start_row, start_column = get_row_column(current_starting_position, lawn_size=lawn_size)
                        current_position_machine_row = start_row
                        current_position_machine_column = start_column
                        lawn_df.add_to_cell(start_row, start_column, 1)
                        for direction in path:
                            try:
                                if direction == "W":
                                    current_position_machine_row -= 1
                                    lawn_df.add_to_cell(current_position_machine_row, current_position_machine_column, 1)
                                elif direction == "D":
                                    current_position_machine_column += 1
                                    lawn_df.add_to_cell(current_position_machine_row, current_position_machine_column, 1)
                                elif direction == "S":
                                    current_position_machine_row += 1
                                    lawn_df.add_to_cell(current_position_machine_row, current_position_machine_column, 1)
                                elif direction == "A":
                                    current_position_machine_column -= 1
                                    lawn_df.add_to_cell(current_position_machine_row, current_position_machine_column, 1)
                            except IndexError:
                                logger.error("Out of bounds")
                                break

                        matrix_sum = lawn_df.calculate_sum()
                        if matrix_sum == amount_of_positions:
                            valid_path = True
                            logger.info(f"Valid path found with starting position: {current_starting_position}")
                            break

                if valid_path:
                    result_string = result_string + "VALID\n"
                else:
                    result_string = result_string + "INVALID\n"
            
                break
    result_string = result_string.strip()

    new_filename = os.path.splitext(os.path.basename(file_path))[0]
    new_file_path = os.path.join(RESULT_DIR, f"{new_filename}.txt")
    with open(new_file_path, 'w') as result_file:
        result_file.write(result_string)

    logger.info("Ending the program")
        

if __name__ == "__main__":
    main()