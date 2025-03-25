import os
import csv
import argparse


all_dicts = []

# opens strace file, parses syscall and count into dict{} and adds to all_dicts
def fileReader(fileToOpen):
    with open(fileToOpen, 'r', errors='ignore') as f:
        lines = f.readlines()[2:-1]
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
    fieldnames = set()
    fieldnames.update(*(d.keys() for d in all_dicts))
    print(fieldnames)
    with open(CSV_to_write, 'a', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=fieldnames)
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

def main():
    dirToRead = get_options()[0]
    CSV_to_write = get_options()[1]
    for f in os.listdir(dirToRead):
        print(os.path.join(dirToRead, f))
        fileReader(os.path.join(dirToRead, f))
    create_headers(CSV_to_write)

main()
