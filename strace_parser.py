import os
import csv
import argparse


dirToRead = './' #default or user input
all_dicts = []
CSV_to_write = './straces.csv' #default or user input

# opens strace file, parses syscall and count into dict{} and adds to all_dicts
def fileReader(fileToOpen):
    with open(fileToOpen, 'r', errors='ignore') as f:
        lines = f.readlines()[2:-1]
        dict = {}
        for line in lines:
            tokens = line.split()
            if len(tokens) == 6:
                dict[tokens[5]] = tokens[3]
            elif len(tokens) == 5:
                dict[tokens[4]] = tokens[3]
        dict.update({'filename': str(fileToOpen)})
        print(dict)
        all_dicts.append(dict)

def create_headers():
    fieldnames = set()
    fieldnames.update(*(d.keys() for d in all_dicts))
    #fieldnames.add(str("filename"))
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

def main():
    get_options()
    for f in os.listdir(dirToRead):
        print(os.path.join(dirToRead, f))
        fileReader(os.path.join(dirToRead, f))
    create_headers()

main()
