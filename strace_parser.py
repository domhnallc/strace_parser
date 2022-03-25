import os
import csv

dirToRead = '/media/dcarlin/6TB/straces/arm_and_x86_straces'
all_dicts = []
CSV_to_write = '/media/dcarlin/6TB/straces/arm_and_x86_straces.csv'

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

def main():
    for f in os.listdir(dirToRead):
        print(os.path.join(dirToRead, f))
        fileReader(os.path.join(dirToRead, f))
    create_headers()

main()
