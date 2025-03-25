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
    python strace_parser.py /path/to/strace_outputs
    ```
2. The resulting CSV file, `output.csv`, will be saved in the directory you specify when running the script.
## Example
```bash
python strace_parser.py ./strace_logs
```
Output:
```
Filename, syscall1,syscall2,syscall3
<File>, count,count,count
...
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.