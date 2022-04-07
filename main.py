import string
import scanner
import sys
import glob
import os.path
from tabulate import tabulate
import io
from string import punctuation

def define_lists():
    digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    posdigit = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    arithmetic = ["+", "-", "*", "/"]
    # a-z & A-Z
    letter = list(string.ascii_letters)
    specialLetter = list(punctuation)
    specialLetter.remove("\"")
    specialLetter.remove("\'")

    keyword = ["if", "else", "while", "return", "class",
               "true", "false", "int", "String", "char", "boolean"]

    comparison = ["<", ">", "==", "!=", "<=", ">="]
    whitespace = ["\t", "\n", " "]

    return digit, posdigit, letter, keyword, arithmetic, comparison, whitespace, specialLetter


if __name__ == "__main__":
    digit, posdigit, letter, keyword, arithmetic, comparison, whitespace, specialLetter = define_lists()

    try:
        filename = sys.argv[1]
        file_detected = os.path.isfile(filename)
        if (file_detected):

            # Đọc file
            f = open(filename, "r")
            input_file = f.read()
            f.close()

            # Scan
            symbol_table = scanner.scan(input_file, digit, posdigit, letter,
                                        keyword, arithmetic, comparison, whitespace, specialLetter)

            headers = "Token name", "Token value"
            # Xóa trùng
            res = []
            newRes = []
            for c in symbol_table:
                res.append(c)
            for i in res:
                if i not in newRes:
                    newRes.append(i)
            table = tabulate(newRes, headers)

            # Ghi bảng ra file
            try:
                with io.open('output.vctok', 'w', encoding="utf-8") as f:
                    f.write(table)
                print('Result was written in output file output.vctok')
            except (UnicodeEncodeError):
                print("UnicodeEncodeError occurred.")
        else:
            print('Invalid argument')
    except(IndexError):
        print("IndexError: input missing, please give input file via command: py lexical_analyzer.py input_file")
    
