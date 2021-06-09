# Simple Python File Differ
This Python script takes two input files and processes them, line by line, to see where the differences are. Optionally, it can log the output to file in addition to showing the output in the Terminal.

## How to Use
You can use this script as follows:

`python3 ./filediff.py -f1 ./sample_input_files/file1.txt -f2 ./sample_input_files/file2.txt -o log.txt`

## Explanation of Parameters
|    Long    | Short | Description                                               |
|:----------:|:-----:|:----------------------------------------------------------|
| `--file1`  | `-f1` | The path to the first input file.                         |
| `--file2`  | `-f2` | The path to the second input file.                        |
| `--output` |  `-o` | (Optional) Path to the file where logs should be written. |

## Output
Successful output should look like this if you use the included sample files, though on Windows terminals the output will not feature any color.

![ImageOfSuccessfulOutput](https://i.imgur.com/siRPp3D.png)

Errors are mostly handled, as well, so depending on what the issue is you should get an error message in plain English like so:

![ImageOfErrorOutput](https://i.imgur.com/NRjKbHo.png)
