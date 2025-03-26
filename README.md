# strace_parser
Parses a folder of strace outputs, counts syscalls and returns a CSV.

The outputs should be yielded from strace -c:

```$ strace -c ls > /dev/null
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 89.76    0.008016           4      1912           getdents
  8.71    0.000778           0     11778           lstat
  0.81    0.000072           0      8894           write
  0.60    0.000054           0       943           open
  0.11    0.000010           0       942           close
  0.00    0.000000           0         1           read
  0.00    0.000000           0       944           fstat
  0.00    0.000000           0         8           mmap
  0.00    0.000000           0         4           mprotect
  0.00    0.000000           0         1           munmap
  0.00    0.000000           0         7           brk
  0.00    0.000000           0         3         3 access
  0.00    0.000000           0         1           execve
  0.00    0.000000           0         1           sysinfo
  0.00    0.000000           0         1           arch_prctl
------ ----------- ----------- --------- --------- ----------------
100.00    0.008930                 25440         3 total
```

## Features
- Parses multiple strace output files in a specified folder.
- Counts occurrences of each system call.
- Outputs the results in a CSV format for easy analysis.

*NOTE*: this does not create the strace files, it simply parses them.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/strace_parser.git
    ```
2. Navigate to the project directory:
    ```bash
    cd strace_parser
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the script with the folder containing strace outputs:
    ```bash
    python strace_parser.py -d /path/to/strace_outputs -o /path/to/output.csv -l label_to_apply (optional)
    ```
2. The resulting CSV file, `output.csv`, will be saved in the directory you specify when running the script.

## Example
```bash
python strace_parser.py -d ./examples/straces -o ./examples/output/example.csv
```
### Output (truncated):
| Filename                  | access | alarm | arch_prctl | brk | close | close_range | connect | execve | fcntl | futex | getdents64 |
|---------------------------|--------|-------|------------|-----|-------|-------------|---------|--------|-------|-------|------------|
| ./examples/example3.strace | 1      |       | 2          | 3   | 9     |             | 2       | 1      |       |       |            |
| ./examples/example2.strace | 2      | 15    | 2          | 3   | 9     |             | 1       | 10     |       |       |            |
| ./examples/example1.strace | 2      |       | 2          | 3   | 9     |             | 1       |        |       | 2     |            |
| ./examples/example4.strace | 2      |       | 2          | 7   | 21    | 1           | 2       | 1      |       | 17    |            |


## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.