import os
from typing import TypedDict, List, Tuple
import logging
import os
import glob

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BoardLayout(TypedDict):
    rows: int
    columns: int


current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

INPUT_DIR = os.path.join(current_dir, "input")

def get_board_layout(rows_columns: List[str]) -> BoardLayout:
    board_layout = {}
    board_layout["rows"] = int(rows_columns[0])
    board_layout["columns"] = int(rows_columns[1])
    return board_layout

def convert_to_int_list(strings: List[str]) -> List[int]:
    int_list = []
    for string in strings:
        try:
            num = int(string)
            int_list.append(num)
        except ValueError:
            logger.error(f"Invalid number: {string}")
    return int_list

def get_row_column(position: int, board_layout: BoardLayout) -> Tuple[int, int]:
    row = (position - 1) // board_layout["columns"] + 1
    column = (position - 1) % board_layout["columns"] + 1 
    return row, column

def main():
    logger.info("Starting the program")
    logger.debug(INPUT_DIR)
    files = glob.glob(os.path.join(INPUT_DIR, "*.in"))
    logger.debug(f"Files: {files}")
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        logger.debug(f"File Path: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            list_numbers = content.split(" ")
            board_layout = get_board_layout(list_numbers[:2])
            amout_of_positions = int(list_numbers[2])
            positions = list_numbers[3:]
            logger.debug(f"List of positions before: {len(positions)}")
            positions = convert_to_int_list(positions)
            logger.debug(f"List of positions after: {len(positions)}")
            logger.debug(f"Board layout: {board_layout}")
            logger.debug(f"Amount positions: {amout_of_positions}")
            logger.debug(f"Positions: {positions}")
            tmp_sequence = []
            for position in positions:
                row, column = get_row_column(int(position), board_layout)
                logger.debug(f"Position: {position} Row: {row} Column: {column}")
                tmp_sequence.append(row)
                tmp_sequence.append(column)
        logger.info(f"Expected numbers: {amout_of_positions}")
        logger.info(f"Actual numbers: {len(tmp_sequence)}")
        final_sequence = " ".join([str(num) for num in tmp_sequence])
        logger.info(f"Final sequence for file {file_path}:\n{final_sequence}")

    logger.info("Ending the program")
        

if __name__ == "__main__":
    main()