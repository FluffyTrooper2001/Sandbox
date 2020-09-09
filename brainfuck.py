"""
Brainfuck String Processing
+ increment
- decrement
< move one cell left
> move one cell right
, pull character from input as ascii value, return 0 if no input.
. push cell value to output as character.
[ while cell != 0 loop code between this character and matching ]
] if cell = 0, exit loop, else go back to matching [
! separate code and input
"""

def brainfuck(codeinput):
    if codeinput == '[':
        return "```bf\nInvalid Syntax: The whole code is just '[', you fool\n```"
    code = codeinput.split(sep='!')[0]
    after_code = 0; user_input = [0]
    for char in codeinput:
        if not after_code:
            if char == '!':
                after_code = 1
        else:
            if user_input[0]:
                user_input.append(ord(codeinput[0]))
            else:
                user_input = [ord(codeinput[0])]
        codeinput = codeinput[1:]
    if user_input == None:
        user_input = [0]
    # code and input are now split. Now, compile the code with input.
    class Data:
        cell_memory = [0]
        cell_pointer = 0
        input = user_input
    #def compile
    def bfcompile(code, Data):
        if len(code) > 0:
            if code[0] == ']':
                return "```bf\nInvalid Syntax: Started with end_of_loop ']'\n```", Data
            elif len(code) != 1:
                if code[-1] == '[':
                    return "```bf\nInvalid Syntax: Ended with begin loop '['\n```", Data
            if code == '[':
                return "```bf\nInvalid Syntax: Entire code is just '[', you fool\n```"
            num_left = len(code); output = [0]
            while num_left:
                this = code[0]; print(this)
                if len(code) != 1:
                    code = code[1:]
                else:
                    code = [0]
                    num_left = 0
                if this == '+':
                    Data.cell_memory[Data.cell_pointer] += 1
                elif this == '-':
                    Data.cell_memory[Data.cell_pointer] -= 1
                elif this == '<':
                    if Data.cell_pointer == 0:
                        temp = Data.cell_memory; Data.cell_memory = [0]
                        for cell in temp:
                            Data.cell_memory.append(cell)
                    else:
                        Data.cell_pointer -= 1
                elif this == '>':
                    if Data.cell_pointer == len(Data.cell_memory)-1:
                        Data.cell_memory.append(0)
                    Data.cell_pointer += 1
                elif this == ',':
                    Data.cell_memory[Data.cell_pointer] = Data.input[0]
                    if Data.input != [0]:
                        if len(Data.input) == 1:
                            Data.input = [0]
                        else:
                            Data.input = Data.input[1:]
                elif this == '.':
                    if output[0]:
                        output.append(Data.cell_memory[Data.cell_pointer])
                    else:
                        output = [Data.cell_memory[Data.cell_pointer]]
                elif this == '[': # loop
                    nest_count = 1; temp_code = ''
                    while nest_count:
                        if len(code)-1:
                            this = code[0]
                            code = code[1:]
                            temp_code = temp_code + this
                            if this == '[':
                                nest_count += 1
                            elif this == ']':
                                nest_count -= 1
                        elif code != ']':
                            return "```bf\nInvalid Syntax: mismatched '[' detected\n```", Data
                        else: # must be ']' and last char
                            nest_count = 0
                    if len(temp_code) > 1:
                        if temp_code[-1] == ']':
                            temp_code = temp_code[:-1]
                            while len(temp_code) > 1 and temp_code[-1] == ']':
                                temp_code = temp_code[:-1]
                    if temp_code == ']':
                        temp_code = ''
                    if temp_code != '':
                        while Data.cell_memory[Data.cell_pointer] != 0:
                            temp_output, Data = bfcompile(temp_code,Data)
                            for char in temp_output:
                                if str(char) != char:
                                    output.append(char)
                                else:
                                    output.append(ord(char))
                    if code == ']':
                        code = ' '
                elif this == ']':
                    if output == '' or output == [0]:
                        output = list("```bf\nInvalid Syntax: mismatched '[' detected\n```")
                    return output, Data
            return output, Data
        else:
            return [0], Data
    # finish defining and run
    rare_output, _ = bfcompile(code,Data)
    output = ''
    for char in rare_output:
        if char != 0 and char != str(char):
            if chr(char) == '\b' and len(output) > 1:
                output = output[:-1]
            elif char == 127:
                pass
            else:
                output = output + chr(char)
        elif char == str(char):
            output = output + char
    return output

try:
    print(brainfuck(input("bf> ")))
except:
    BrainfuckError = RuntimeError
    raise BrainfuckError("ERROR IN THE BRAINFUCKING")
