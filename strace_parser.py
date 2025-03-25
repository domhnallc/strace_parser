import os
"""
This script parses the output of `strace` command from files in a specified directory
and generates a CSV file containing the parsed data.
Functions:
    fileReader(fileToOpen):
        Reads a single strace file, parses system call counts, and stores the data in a dictionary.
        Skips processing if the input is a directory.
    create_headers(CSV_to_write):
        Creates a CSV file with headers based on the parsed data and writes the data to the file.
    get_options():
        Parses command-line arguments to get the input directory and output CSV file path.
    check_input_dir_exits(dirToRead):
        Verifies if the specified input directory exists. Exits the program if it does not.
    check_output_file(CSV_to_write):
        Checks if the specified output CSV file already exists. Exits the program if it does.
    main():
        Main function that orchestrates the parsing of strace files and the creation of the CSV file.
Command-line Usage:
    python strace_parser.py -d <strace_directory_to_read> -o <output_csv_file>
Arguments:
    -d, --dir: Directory containing strace files to be parsed.
    -o, --output: Path to the output CSV file.
Global Variables:
    all_dicts: A list to store dictionaries containing parsed data from each strace file.
"""
import csv
import argparse


all_dicts = []

# opens strace file, parses syscall and count into dict{} and adds to all_dicts
def fileReader(fileToOpen):
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

def create_headers(CSV_to_write):
    fieldnames = sorted({key for d in all_dicts for key in d.keys() if key != 'filename'})
    fieldnames.insert(0, 'filename')  # Ensure 'filename' is at the start
    print(fieldnames)
    with open(CSV_to_write, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, escapechar="\\")
        writer.writeheader()
        for d in all_dicts:
            writer.writerow(d)

def get_options():
    
    parser = argparse.ArgumentParser(description='Parse strace output to CSV')
    parser.usage = "python strace_parser.py -d <strace_directory_to_read> -o <output_csv_file>"
    parser.add_argument('-d', '--dir', help='Directory to read strace files from', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file', required=True)
    args = parser.parse_args()
    dirToRead = args.dir
    CSV_to_write = args.output

    return dirToRead, CSV_to_write

def check_input_dir_exits(dirToRead):
    if not os.path.isdir(dirToRead):
        print("Directory does not exist")
        exit()
    else:
        return dirToRead
    
def check_output_file(CSV_to_write):
    if os.path.exists(CSV_to_write):
        print("Error: CSV file already exists")
        exit()
    else:
        return CSV_to_write

def main():
    dirToRead = check_input_dir_exits(get_options()[0])
    CSV_to_write = check_output_file(get_options()[1])
    for f in os.listdir(dirToRead):
        print(os.path.join(dirToRead, f))
        fileReader(os.path.join(dirToRead, f))
    create_headers(CSV_to_write)

main()
