import argparse
import sys
import os
import platform
import pathlib

# Declaring the Variables

firstinputfile = ""
secondinputfile = ""
outputfile = ""
log_file = ""
logging_to_file = False

# Parsing the Input Parameters

parser = argparse.ArgumentParser(
    description='Compare two files line-by-line for differences.'
)
parser.add_argument('-f1', '--file1', help='the first input file')
parser.add_argument('-f2', '--file2', help='the second input file')
parser.add_argument('-o', '--output', help='(optional) the output file name')
args = parser.parse_args()

outputfile = args.output
# if the outputfile variable is not blank
if(outputfile != "" and outputfile is not None):
    # but the proposed log directory does not already exist
    if(os.path.isdir(pathlib.Path(outputfile).parent.absolute()) is False):
        # create it
        os.makedirs(
            pathlib.Path(outputfile).parent.absolute(),
            mode=0o755, exist_ok=False)

    if(os.path.isfile(args.output) is False):  # if the log file does not exist
        log_file = open(outputfile, "x")  # create it
    elif(os.path.isfile(args.output) is True):  # but if it does already exist,
        log_file = open(outputfile, "a")  # append to the existing file

    logging_to_file = True


def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.__code__.co_argcount

        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a, t)
            return f(*args, **kwds)
        new_f.__name__ = f.__name__
        return new_f
    return check_accepts


# The Actual Program™

def main(argv):
    lineCount = 0
    diffCount = 0
    sameCount = 0

    if(args.file1 is not None and args.file2 is not None):
        if(os.path.isfile(args.file1) is False and 
           os.path.isfile(args.file2) is False):
            ShowFileMissingError(True, "both", "both")
            sys.exit(2)
        if(os.path.isfile(args.file1) is False):  # if its the default value
            ShowFileMissingError(False, "file1", "f1")
            sys.exit(2)
        if(os.path.isfile(args.file2) is False):  # if its the default value
            ShowFileMissingError(False, "file2", "f2")
            sys.exit(2)
    else:
        ShowFileMissingError()
        sys.exit(2)

    firstinputfile = args.file1
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
                    printing("File 1: ", no_newline=True)
                    printing(x.rstrip(), no_newline=True, fail=True)
                    printing(" | ", no_newline=True)
                    printing("File 2: ", no_newline=True)
                    printing(y.rstrip(), fail=True)
                    diffCount += 1
                lineCount += 1
        printing("------Results------")
        printing("The total line count was ", no_newline=True)
        printing(f"{lineCount}.", no_newline=False, fail=False, success=True)
        printing("There were ", no_newline=True)
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


# Error printing

def ShowFileMissingError(bothFailed=False, longArg="not set", shortArg="none"):
    if(bothFailed is True):
        printing("---Error Details---")
        printing("Neither of the referenced input files could be found! ", no_newline=True)
        printing("Please check the file paths and try again.")
        printing('-------------------')
    elif(longArg != "not set"):
        printing("---Error Details---")
        printing(f"The file passed in using the -{shortArg} or --{longArg} " +
                 "parameter could not be found! Please check the path " +
                 "and try again.")
        printing('-------------------')
    else:
        printing("---Error Details---")
        printing("Please enter two files to compare! Type -h for help.")
        printing('-------------------')


def ShowFileNotFoundError():
    printing("---Error Details---")
    printing('One or more of the specified input files does not exist!')
    printing('-------------------')


# Custom printing function to make colorizing values easier

def printing(text, no_newline=False, fail=False, success=False):
    if(success and fail):
        print("Supplying both Fail and Success as true makes no sense!")
        print("Exiting application.")
        sys.exit(2)
    if(no_newline):
        print(ApplyFailOrSuccessColor(text, fail, success), end="")
    else:
        print(ApplyFailOrSuccessColor(text, fail, success))

    if(logging_to_file):
        if(no_newline):
            log_file.write(text)
        else:
            log_file.write(text + "\n")


def ApplyFailOrSuccessColor(text, fail, success):
    if(platform.system() == "Windows"):  # this isn't supported in
        return text                      # Windows terminals, sadly.
    if(fail):
        return f"{bcolors.FAIL}{text}{bcolors.ENDC}"
    elif(success):
        return f"{bcolors.OKGREEN}{text}{bcolors.ENDC}"
    else:
        return text


# Color definitions

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Program entrance

if __name__ == "__main__":
    main(sys.argv[1:])
