import os
from typing import TypedDict, List, Tuple, Dict
import logging
import os
import glob

logging.basicConfig(level=logging.INFO)
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

def convert_to_tuple_list(positions: List[int]) -> List[Tuple[int, int]]:
    position_tuples = [(positions[i], positions[i+1]) for i in range(0 , len(positions)-1, 2)]
    return position_tuples

def get_row_column(position: int, board_layout: BoardLayout) -> Tuple[int, int]:
    row = (position - 1) // board_layout["columns"] + 1
    column = (position - 1) % board_layout["columns"] + 1 
    return row, column

def match_tuples(tuples: List[Tuple[int, int]]) -> Dict[int, List[Tuple[int, int]]]:
    tuple_dict = {}
    for tuple in tuples:
        second_number = tuple[1]
        if second_number in tuple_dict:
            tuple_dict[second_number].append(tuple)
        else:
            tuple_dict[second_number] = [tuple]
    tuple_dict = dict(sorted(tuple_dict.items()))
    return tuple_dict

def calculate_manhattan_distance(positions: List[Tuple[int, int]], board_layout: BoardLayout) -> int:
    distance = 0
    row, column = get_row_column(positions[0][0], board_layout)
    target_row, target_column = get_row_column(positions[1][0], board_layout)
    distance = abs(row - target_row) + abs(column - target_column)
    return distance

def main():
    logger.info("Starting the program")
    logger.debug(INPUT_DIR)
    files = glob.glob(os.path.join(INPUT_DIR, "*.in"))
    logger.debug(f"Files: {files}")
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        logger.info(f"File Path: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            list_numbers = content.split(" ")
            board_layout = get_board_layout(list_numbers[:2])
            amout_of_positions = int(list_numbers[2])
            position_list = convert_to_int_list(list_numbers[3:])
            logger.debug(f"Board layout: {board_layout}")
            logger.debug(f"Amount positions: {amout_of_positions}")
            logger.debug(f"Position as list: {position_list}")
            position_tuples = convert_to_tuple_list(position_list)
            logger.debug(f"Position as tuples: {position_tuples}")
            matched_positions = match_tuples(position_tuples)
            logger.debug(f"Positions as matched dict: {matched_positions}")
            result_list = []
            for key in matched_positions.keys():
                result_list.append(str(calculate_manhattan_distance(matched_positions[key], board_layout=board_layout)))
                
            logger.debug(f"Result list: {result_list}")

        logger.info(f"Result: {" ".join(result_list)}")
    logger.info("Ending the program")
        

if __name__ == "__main__":
    main()