import argparse
import sys
import os
import pathlib
firstinputfile = ""
secondinputfile = ""
outputfile = ""
log_file = ""

parser = argparse.ArgumentParser(
    description='Compare two files line-by-line for differences.'
)
parser.add_argument('-f1', '--file1', help='the first input file')
parser.add_argument('-f2', '--file2', help='the second input file')
parser.add_argument('-o', '--output', help='(optional) the output file name')
args = parser.parse_args()

outputfile = args.output
if(os.path.isdir(pathlib.Path(outputfile).parent.absolute()) is False):  # if the referenced log folder does not exist
    os.makedirs(pathlib.Path(outputfile).parent.absolute(), mode=0o755, exist_ok=False)  # create it

if(os.path.isfile(args.file1) is False):  # if the log file does not exist
    log_file = open(outputfile, "x")  # create it
elif(os.path.isfile(args.file1) is True):  # but f it does exist,
    log_file = open(outputfile, "a")  # append to it


def main(argv):
    lineCount = 0
    diffCount = 0
    sameCount = 0

    if(os.path.isfile(args.file1) is False):  # if its the default value
        ShowFileMissingError()
        sys.exit(2)
    else:
        firstinputfile = args.file1

    if(os.path.isfile(args.file2) is False):
        ShowFileMissingError()
        sys.exit(2)
    else:
        secondinputfile = args.file2

    try:
        with open(firstinputfile) as f1, open(secondinputfile) as f2:
            printing("---File Details---")
            for x, y in zip(f1, f2):
                if(x == y):  # if the lines match, print it
                    printing(x.rstrip(), fail=False, success=True)
                    sameCount += 1
                else:  # and if they don't, print the data from both
                    printing(f"Line {lineCount + 1}: ", no_newline=True)
                    printing(f"File 1: ", no_newline=True)
                    printing(x.rstrip(), no_newline=True, fail=True)
                    printing(" | ", no_newline=True)
                    printing(f"File 2: ", no_newline=True)
                    printing(y.rstrip(), fail=True)
                    diffCount += 1
                lineCount += 1
        printing("------Results------")
        printing(f"The total line count was ", no_newline=True)
        printing(f"{lineCount}.", no_newline=False, fail=False, success=True)
        printing(f"There were ", no_newline=True)
        printing(f"{diffCount}", no_newline=True, fail=True, success=False)
        printing(" differing lines.")
        printing(f"{sameCount}", no_newline=True, fail=False, success=True)
        printing(" lines were identical between these files.")
        printing('--------------------')
        if(log_file != ""):
            log_file.close()
    except FileNotFoundError:
        ShowFileNotFoundError()
        sys.exit(2)


def ShowFileMissingError():
    printing("---Error Details---")
    printing("Please enter two files to compare! Use the -h flag for help.")
    printing('-------------------')


def ShowFileNotFoundError():
    printing("---Error Details---")
    printing('One or more of the specified input files does not exist!')
    printing('-------------------')


def printing(text, no_newline=False, fail=False, success=False):
    if(success and fail):
        print("Supplying both Fail and Success as true makes no sense!")
        print("Exiting application.")
        sys.exit(2)
    if(no_newline):
        print(ApplyFailOrSuccessColor(text, fail, success), end="")       
    else:
        print(ApplyFailOrSuccessColor(text, fail, success))  
 
    if(log_file != ""):
        if(no_newline):
            log_file.write(text)
        else:
            log_file.write(text + "\n")


def ApplyFailOrSuccessColor(text, fail, success):
    if(fail):
        return f"{bcolors.FAIL}{text}{bcolors.ENDC}"
    elif(success):
        return f"{bcolors.OKGREEN}{text}{bcolors.ENDC}"
    else:
        return text

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == "__main__":
    main(sys.argv[1:])
