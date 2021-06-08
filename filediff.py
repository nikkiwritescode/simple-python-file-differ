import argparse
import sys
firstinputfile = ""
secondinputfile = ""

parser = argparse.ArgumentParser(
    description='Compare two files line-by-line for differences.'
)
parser.add_argument('-f1', '--file1', help='the first input file')
parser.add_argument('-f2', '--file2', help='the second input file')
args = parser.parse_args()


def main(argv):
    lineCount = 0
    diffCount = 0
    sameCount = 0

    if(args.file1 is None):  # if its the default value
        ShowFileMissingError()
        sys.exit(2)
    else:
        firstinputfile = args.file1

    if(args.file2 is None):
        ShowFileMissingError()
        sys.exit(2)
    else:
        secondinputfile = args.file2

    try:
        with open(firstinputfile) as f1, open(secondinputfile) as f2:
            print("---File Details---")
            for x, y in zip(f1, f2):
                if(x == y):
                    print(x.rstrip())  # if the lines match, print it
                    sameCount += 1
                else:
                    print("File 1: " +
                          f"Line {lineCount + 1}: {x.rstrip()} | ", end="")
                    print("File 2: " +
                          f"Line {lineCount + 1}: {y.rstrip()}")
                    diffCount += 1
                lineCount += 1
    except FileNotFoundError:
        ShowFileNotFoundError()
        sys.exit(2)

    print("------Results------")
    print(f"The total line count was {lineCount}.")
    print(f"There were {diffCount} differing lines.")
    print(f"{sameCount} lines were identical between these files.")
    print('--------------------')


def ShowFileMissingError():
    print("---Error Details---")
    print("Please enter two files to compare! Use the -h flag for help.")
    print('-------------------')


def ShowFileNotFoundError():
    print("---Error Details---")
    print('One or more of the specified input files does not exist!')
    print('-------------------')


if __name__ == "__main__":
    main(sys.argv[1:])
