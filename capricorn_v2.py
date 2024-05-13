import os
import sys
from multiprocessing import Pool, cpu_count
import argparse

# Function to print colored text
def colored_text(text, color_code):
    return f"\033[{color_code}m{text}\033[00m"

# Simple progress bar function
def progress_bar(current, total, bar_length=20):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '*'# + '*'
    padding = (bar_length - len(arrow)) * ' '
    return f'[{arrow}{padding}] {current}/{total}'

# Function to handle file writing in multiprocessing
def write_block(block_data):
    filename, start, end, output_path, buffer, total_blocks = block_data
    with open(output_path, "wb") as bf:
        bf.write(buffer[start:end])
    # Correctly calculate the current block index
    current_block = start // (end - start) + 1
    print(colored_text(progress_bar(current_block, total_blocks), "93"))

# CAPRICORN CLASS
class Capricorn:
    def __init__(self, filename: str, block_size: int, output_format: str):
        self.filename = filename
        self.block_size = block_size
        self.output_format = output_format
        try:
            with open(filename, "rb") as file:
                self.buffer = file.read()
        except FileNotFoundError:
            print(colored_text(f"Error: The file {filename} could not be found.", "91"))
            sys.exit(1)
        except IOError as e:
            print(colored_text(f"Error: Unable to read the file {filename}. {e}", "91"))
            sys.exit(1)

    def split(self, output_directory):
        total_size = len(self.buffer)
        blocks = (total_size + self.block_size - 1) // self.block_size
        print(f"Starting to split {self.filename} into {blocks} blocks...")

        pool = Pool(cpu_count())
        tasks = []
        for b in range(blocks):
            start = b * self.block_size
            end = min(start + self.block_size, total_size)
            output_path = os.path.join(output_directory, self.output_format.format(filename=self.filename, block=b + 1))
            tasks.append((self.filename, start, end, output_path, self.buffer, blocks))

        pool.map(write_block, tasks)
        pool.close()
        pool.join()

        print(colored_text("Splitting completed successfully.", "92"))

# START SCRIPT
def main(args):
    if args.interactive:
        filename = input("Enter the filename: ")
        block_size = int(input("Enter the block size: "))
        output_format = input("Enter the output format (e.g., '{filename}_block_{block}'): ")
    else:
        filename = args.filename
        block_size = args.block_size
        output_format = args.output_format

    splitter = Capricorn(filename, block_size, output_format)
    splitter.split(os.getcwd())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capricorn File Splitter")
    parser.add_argument('filename', type=str, nargs='?', help='The file to split')
    parser.add_argument('block_size', type=int, nargs='?', help='The size of each block')
    parser.add_argument('-f', '--output_format', type=str, default='{filename}_block_{block}', help='Output filename format')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()

    if not args.filename or not args.block_size:
        args.interactive = True

    main(args)
