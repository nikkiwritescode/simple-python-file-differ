# Simple Python File Differ
This Python script takes two input files and processes them, line by line, to see where the differences are. Optionally, it can log the output to file in addition to showing the output in the Terminal.

## How to Use
You can use this script as follows:

`python3 ./filediff.py --file1 ./sample/file1.txt --file2 ./sample/file2.txt --output ./outputlogs/log.txt`

## Explanation of Parameters
|    Long    | Short | Description                                               |
|:----------:|:-----:|:----------------------------------------------------------|
| `--file1`  | `-f1` | The path to the first input file.                         |
| `--file2`  | `-f2` | The path to the second input file.                        |
| `--output` |  `-o` | (Optional) Path to the file where logs should be written. |
