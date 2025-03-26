
import os
'''
This script processes strace output files from a specified directory and writes the parsed data to a CSV file. 
It includes functions for reading and parsing files, validating input and output paths, and generating a CSV 
with appropriate headers.
Functions:
    - fileReader(fileToOpen): Reads a file, extracts syscall data, and appends it to a global list of dictionaries.
    - create_headers(CSV_to_write): Creates a CSV file with headers and writes the parsed data to it.
    - get_options(): Parses command-line arguments for input directory and output CSV file.
    - check_input_dir_exits(dirToRead): Validates the existence of the input directory.
    - check_output_file(CSV_to_write): Ensures the output CSV file does not already exist.
    - main(): Orchestrates the overall process of reading files, parsing data, and writing to the CSV.
Usage:
    python strace_parser.py -d <strace_directory_to_read> -o <output_csv_file>
    - The script assumes a specific format for the strace output files.
    - The global variable `all_dicts` is used to store parsed data from all files.
    - The script exits with an error message if the input directory does not exist or the output file already exists.
'''
import csv
import argparse


all_dicts = []

# opens strace file, parses syscall and count into dict{} and adds to all_dicts
def fileReader(fileToOpen):
    """
    Reads a file, processes its content, and extracts specific information into a dictionary.
    Args:
        fileToOpen (str): The path to the file to be read.
    Returns:
        None: The function does not return a value. Instead, it prints the resulting dictionary
        and appends it to the global list `all_dicts`.
    Behavior:
        - If the provided path is a directory, the function prints an error message and skips processing.
        - Reads the file while ignoring encoding errors.
        - Skips the first two and last two lines of the file.
        - Processes each line, splitting it into tokens and extracting specific fields based on the number of tokens.
        - Populates a dictionary with the extracted data, including the filename.
        - Prints the dictionary and appends it to the global list `all_dicts`.
    Notes:
        - Assumes the file has a specific format where lines contain either 5 or 6 tokens.
        - The global variable `all_dicts` must be defined before calling this function.
    """

    if os.path.isdir(fileToOpen):
        print("Error: File is a directory, skipping")
        return  # Skip processing if the file is a directory
    else:
        with open(fileToOpen, 'r', errors='ignore') as f:
            lines = f.readlines()[2:-2]
            dict = {}
            dict.update({'filename': str(fileToOpen)})
            for line in lines:
                tokens = line.split()
                if len(tokens) == 6:
                    dict[tokens[5]] = tokens[3]
                elif len(tokens) == 5:
                    dict[tokens[4]] = tokens[3]
        
        print(dict)
        all_dicts.append(dict)

def create_headers(CSV_to_write, label=None):
    """
    Creates a CSV file with headers and writes the contents of a list of dictionaries to it.
    This function generates a sorted list of unique keys from a global list of dictionaries 
    (`all_dicts`), excluding the key 'filename'. It ensures that 'filename' is always the 
    first column in the CSV file. The function then writes these headers and the contents 
    of `all_dicts` to the specified CSV file.
    Args:
        CSV_to_write (str): The file path of the CSV file to write to.
    Raises:
        NameError: If the global variable `all_dicts` is not defined.
        IOError: If there is an issue opening or writing to the specified file.
    Notes:
        - The global variable `all_dicts` must be a list of dictionaries where each dictionary 
          represents a row to be written to the CSV file.
        - The function appends to the specified CSV file if it already exists.
    """

    fieldnames = sorted({key for d in all_dicts for key in d.keys() if key != 'filename'})
    fieldnames.insert(0, 'filename')  # Ensure 'filename' is the first column
    fieldnames.insert(1, 'label')  # Ensure 'label' is the second column
    if label:
        for d in all_dicts:
            d['label'] = label  # Set a default value for the 'label' column for all rows
    print(fieldnames)
    with open(CSV_to_write, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, escapechar="\\")
        writer.writeheader()
        for d in all_dicts:
            writer.writerow(d)

def get_options():
    """
    Parses command-line arguments for the strace parser script.
    This function uses argparse to define and parse the following arguments:
    - `-d` or `--dir`: Specifies the directory containing strace files to read (required).
    - `-o` or `--output`: Specifies the output CSV file to write the parsed data to (required).
    Returns:
        tuple: A tuple containing:
            - dirToRead (str): The directory to read strace files from.
            - CSV_to_write (str): The path to the output CSV file.
    """
    
    parser = argparse.ArgumentParser(description='Parse strace output to CSV')
    parser.usage = "python strace_parser.py -d <strace_directory_to_read> -o <output_csv_file>"
    parser.add_argument('-d', '--dir', help='Directory to read strace files from', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file', required=True)
    parser.add_argument('-l','--label', help='Label to add to the label column of the CSV file for ML. '
    'Default includes column and zero for all.', required=False)
    args = parser.parse_args()
    
    return args.known_args()
    
def check_input_dir_exits(dirToRead):
    """
    Checks if the specified directory exists.
    Parameters:
    dirToRead (str): The path to the directory to check.
    Returns:
    str: The path to the directory if it exists.
    Raises:
    SystemExit: Exits the program if the directory does not exist.
    """

    if not os.path.isdir(dirToRead):
        print("Directory does not exist")
        exit()
    else:
        return dirToRead
    
def check_output_file(CSV_to_write):
    """
    Checks if the specified CSV file already exists.
    If the file exists, an error message is printed, and the program exits.
    Otherwise, the function returns the file path.
    Args:
        CSV_to_write (str): The path to the CSV file to check.
    Returns:
        str: The path to the CSV file if it does not already exist.
    Raises:
        SystemExit: If the CSV file already exists.
    """

    if os.path.exists(CSV_to_write):
        print("Error: CSV file already exists")
        exit()
    else:
        return CSV_to_write

def main():
    """
    Main function to process files in a specified directory and write results to a CSV file.
    This function performs the following steps:
    1. Reads the input directory path and output CSV file path from command-line options.
    2. Validates the existence of the input directory and the output file.
    3. Iterates through all files in the input directory, processing each file.
    4. Creates headers for the output CSV file.
    Note:
        - The `check_input_dir_exits` function ensures the input directory exists.
        - The `check_output_file` function validates or prepares the output file.
        - The `fileReader` function processes individual files.
        - The `create_headers` function writes headers to the output CSV file.
    Raises:
        Any exceptions raised by the helper functions used within this function.
    """

    dirToRead = check_input_dir_exits(get_options().args.dir)
    CSV_to_write = check_output_file(get_options().args.output)
    if get_options().args.label:
        label = get_options().args.label
    else:
        label = None
    for f in os.listdir(dirToRead):
        print(os.path.join(dirToRead, f))
        fileReader(os.path.join(dirToRead, f))
    create_headers(CSV_to_write, label)

main()
