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
RESULT_DIR = os.path.join(current_dir, "result")

def clean_result_dir():
    logger.info("Cleaning the result directory")
    files = glob.glob(os.path.join(RESULT_DIR, "*.txt"))
    for file in files:
        os.remove(file)
    logger.info("Result directory cleaned")

def convert_to_int_list(strings: List[str]) -> List[int]:
    int_list = []
    for string in strings:
        try:
            num = int(string)
            int_list.append(num)
        except ValueError:
            logger.error(f"Invalid number: {string}")
    return int_list

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
                character_count = {"W": 0, "D": 0, "S": 0, "A": 0}
                for char in line.strip():
                    if char in character_count:
                        character_count[char] += 1
                    else:
                        character_count[char] = 1

                new_filename = os.path.splitext(os.path.basename(file_path))[0]
                new_file_path = os.path.join(RESULT_DIR, f"{new_filename}.txt")
                mode = 'a' if os.path.exists(new_file_path) else 'w'
                with open(new_file_path, mode) as result_file:
                    if mode == 'a':
                        result_file.write(f"\n")
                        for i, count in enumerate(character_count.items()):
                            if i != len(character_count)-1:
                                result_file.write(f"{count[1]} ")
                            else:
                                result_file.write(f"{count[1]}")
                    else:
                        for i, count in enumerate(character_count.items()):
                            if i != len(character_count) -1:
                                result_file.write(f"{count[1]} ")
                            else:
                                result_file.write(f"{count[1]}")

        logger.info(f"Result saved in {new_file_path}")
        
    logger.info("Ending the program")
        

if __name__ == "__main__":
    main()