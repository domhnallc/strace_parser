# strace_parser
Parses a folder of strace outputs, counts syscalls and returns a CSV.
## Features
- Parses multiple strace output files in a specified folder.
- Counts occurrences of each system call.
- Outputs the results in a CSV format for easy analysis.

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
    python strace_parser.py -d /path/to/strace_outputs -o /path/to/output.csv
    ```
2. The resulting CSV file, `output.csv`, will be saved in the directory you specify when running the script.
## Example
```bash
python strace_parser.py -d /examples -o ./examples.csv
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