import string
from tabulate import tabulate


# Scans given input for tokens and returns a symbol table with found token token names and values.
# If invalid input is found, prints it to the console.
def scan(input, digit, posdigit, letter, keyword, arithmetic, comparison, whitespace, specialLetter):
    symbol_table = []

    temp_token = ""  # temp_token will be used to test if input matches tokens
    i = 0
    # Starting to scan input:
    while i < len(input):

        # Skip whitespace
        if input[i] in whitespace:
            pass

        # Keyword và biến
        elif input[i] in letter:
            # Nếu ký tự là letter (a-z and A-Z) thì đọc tiếp
            while input[i] in letter:
                temp_token += input[i]
                i += 1
            # Ký tự tiếp theo khác letter thì check đoạn trước đó
            else:
                i -= 1
                # Nếu trong danh sách keyword thì kết thúc và set lại temp_token
                if temp_token in keyword:
                    symbol_table += [["KEYWORD", temp_token]]
                    temp_token = ""

                # Nếu không trong danh sách keyword thì check xem có phải là biến không
                else:
                    # Nếu ký tự tiếp là _ hoặc số thì check tiếp
                    if input[i+1] == "_" or input[i+1] in digit:
                        i += 1
                        while input[i] in letter or input[i] in digit or input[i] == "_":
                            temp_token += input[i]
                            i += 1
                        else:
                            i -= 1
                            symbol_table += [["IDENTIFIER", temp_token]]
                            temp_token = ""
                    # Nếu ký tự tiếp khác _ hoặc số thì xác định đoạn temp_token là biến
                    else:
                        symbol_table += [["IDENTIFIER", temp_token]]
                        temp_token = ""

        # Biến nhưng bắt đầu bằng _
        elif input[i] == "_":
            temp_token += input[i]
            i += 1
            while input[i] in letter or input[i] in digit or input[i] == "_":
                temp_token += input[i]
                i += 1
            else:
                i -= 1
                symbol_table += [["IDENTIFIER", temp_token]]
                temp_token = ""

        # Số cả float, int, ... (chưa hoàn thiện)
        elif input[i] in digit:
            temp_token += input[i]
            i += 1
            while input[i] in digit:
                temp_token += input[i]
                i += 1
            else:
                if input[i] == '.':
                    temp_token += input[i]
                    i += 1
                    if input[i] in digit:
                        while input[i] in digit:
                            temp_token += input[i]
                            i += 1
                        # 1234.1 = CONSTANT
                        else:
                            symbol_table += [["CONSTANT", temp_token]]
                            i -= 1
                            temp_token = ""
                    # 123. = CONSTANT
                    else:
                        symbol_table += [["CONSTANT", temp_token]]
                        i -= 1
                        temp_token = ""

                elif input[i] == 'E' or input[i] == 'e':
                    temp_token += input[i]
                    i += 1
                    if input[i] == '+' or input[i] == '-':
                        temp_token += input[i]
                        i += 1
                        if input[i] in digit:
                            while input[i] in digit:
                                temp_token += input[i]
                                i += 1
                            # 1234E+1 = CONSTANT
                            else:
                                i -= 1
                                symbol_table += [["CONSTANT", temp_token]]
                                temp_token = ""
                        # 1234E+? = UNKNOWN
                        else:
                            i -= 1
                            symbol_table += [["UNKNOWN", temp_token]]
                            temp_token = ""
                    else:
                        if input[i] in digit:
                            while input[i] in digit:
                                temp_token += input[i]
                                i += 1
                            # 1234E1 = CONSTANT
                            else:
                                i -= 1
                                symbol_table += [["CONSTANT", temp_token]]
                                temp_token = ""
                        # 1234E? = Unknown
                        else:
                            symbol_table += [["UNKNOWN", temp_token]]
                            i -= 1
                            temp_token = ""
                # 1234 = CONSTANT
                else:
                    symbol_table += [["CONSTANT", temp_token]]
                    i -= 1
                    temp_token = ""
        # Số có dấu chấm ở đầu
        elif input[i] == ".":
            temp_token += input[i]
            i += 1
            if input[i] in digit:
                while input[i] in digit:
                    temp_token += input[i]
                    i += 1
                # .123 = CONSTANT
                else:
                    symbol_table += [["CONSTANT", temp_token]]
                    i -= 1
                    temp_token = ""
            # . = UNKNOWN
            else:
                symbol_table += [["UNKNOWN", temp_token]]
                i -= 1
                temp_token = ""

        # Số có dấu +/- ở đầu
        elif input[i] == "-" or input[i] == "+":
            temp_token += input[i]
            i += 1
            if input[i] in digit:
                while input[i] in digit:
                    temp_token += input[i]
                    i += 1
                # +123 = CONSTANT
                else:
                    symbol_table += [["CONSTANT", temp_token]]
                    i -= 1
                    temp_token = ""
            # + / - = ARITHMETIC
            else:
                symbol_table += [["ARITHMETIC", temp_token]]
                i -= 1
                temp_token = ""

        # Các phép toán * /
        elif input[i] in arithmetic:
            symbol_table += [["ARITHMETIC", input[i]]]

        # Phép gán và so sánh bằng
        elif input[i] == "=":
            if input[i+1] == "=":
                symbol_table += [["COMPARISON", "=="]]
                i += 1
            else:
                symbol_table += [["ASSIGN", input[i]]]

        # So sánh khác
        elif input[i] == "<" or input[i] == ">" or input[i] == "!":
            temp_token += input[i]
            if input[i+1] == "=":
                temp_token += "="
            symbol_table += [["COMPARISON", temp_token]]
            temp_token = ""
            i += 1

        # Chuỗi
        elif input[i] == "\"":
            temp_token += input[i]
            i += 1
            while input[i] in letter or input[i] in digit or input[i] == " " or input[i] in specialLetter:
                temp_token += input[i]
                i += 1
            else:
                # End:
                if input[i] == "\"":
                    temp_token += "\""
                    symbol_table += [["STRING", temp_token]]
                # Gặp dấu '
                else:
                    print("ERROR: Invalid input for STRING: ", input[i])
                    # Bỏ qua:
                    while input[i] != "\"":
                      i += 1
            temp_token = ""

        # Ký tự đơn lẻ
        elif input[i] == "\'":
            temp_token += input[i]
            i += 1
            if input[i] in digit or input[i] in letter or input[i] == " " or input[i] in specialLetter:
                temp_token += input[i]  
                i += 1
                if input[i] == "\'":
                  temp_token += input[i]
                  symbol_table += [["CHAR", temp_token]]
                else:
                  print("ERROR: Invalid input for CHAR: ", input[i])
                  while input[i] != "\'":
                      i += 1
            elif input[i] == "\'":
                temp_token += input[i]
                symbol_table += [["CHAR", temp_token]]
            else:
                print("ERROR: Invalid input for CHAR: ", input[i])
                while input[i] != "\'":
                      i += 1
        temp_token = ""
        i += 1

    # When scanning is ready:
    return symbol_table
