from befungechars import Chars
from inputbefunge import load_befunge
from math import floor
from random import choice
from sys import argv, stdout


class Stack:
    stack = []

    def pop(self):
        if len(self.stack) == 0:
            return 0
        item = self.stack[-1]
        self.stack = self.stack[:-1]
        return item

    def push(self, item: int):
        self.stack.append(item)

    def __str__(self):
        return str(self.stack)


def texify_list(input_list):
    temp_list = []
    if type(input_list) is list:
        return '({})'.format(', '.join(list(map(lambda x: str(x), input_list))))
    elif type(input_list) is dict:
        for i in input_list.values():
            if type(i) is int:
                temp_list.append(str(i))
            else:
                if i == ' ':
                    temp_list.append('\\texttt{" "}')
                elif len(i) == 1:
                    temp_list.append('\\texttt{{{}}}'.format(str(i)))
                else:
                    temp_list.append(str(i))
        return '({})'.format(', '.join(temp_list))


directions = [0, 1, 2, 3]
direction_map = {0: '\\rightarrow',
                 1: '\\downarrow',
                 2: '\\leftarrow',
                 3: '\\uparrow'}

conf_format = '$$\\left<\\left({0}, {1} \\right), {2}, {3}, {4}, {5}, \\texttt{{{6}}}, P{7}\\right>$$'
rule_format = '$$\\xRightarrow{{}}_{{sos}}\\left[{0}_{{sos}}\\right]\\indent\\text{{because }}P{4}_{{{1},{2}}}={3}$$'
rule_format_2 = '$$\\xRightarrow{{}}_{{sos}}\\left[{0}_{{sos}}\\right]\\indent' \
                '\\text{{because }}P{4}_{{{1},{2}}}\\neq{3}$$'


def nextpos(direction, x, y, board):
    if direction == 0:
        return (x + 1) % len(board[0]), y
    elif direction == 1:
        return x, (y + 1) % len(board)
    elif direction == 2:
        return (x - 1) % len(board[0]), y
    elif direction == 3:
        return x, (y - 1) % len(board)


def parse(befunge, startdir=0, startx=0, starty=0, debug=False, input_dict=None, outfile=None):
    x, y, direction = startx, starty, startdir
    char = befunge[y][x]

    if debug and not outfile:
        stdout.write("Did not get an outfile!")
        return

    stack = Stack()
    output = ""
    stringmode = False

    output_dict = {}
    output_dict_c = 0

    if debug and not input_dict:
        input_dict = {}

    input_dict_c = len(input_dict) - 1

    if debug:
        with open(outfile, "a+") as f:
            f.write(conf_format.format(x + 1,
                                       y + 1,
                                       direction_map[direction],
                                       texify_list(output_dict),
                                       texify_list(input_dict),
                                       texify_list(stack.stack),
                                       "normal",
                                       ''))
            f.write('\n')

    substitutions = []

    old_x, old_y = 0, 0

    while not char == Chars.END:
        bridge = False
        string = False

        # HANDLE CURRENT ROUND
        if char == Chars.SSM:
            stringmode = not stringmode
            rule = Chars.texmap[char] + ('^1' if stringmode else '^2')
            latex_char = Chars.texmap[char]
        elif stringmode:
            stack.push(ord(befunge[y][x]))
            rule = Chars.texmap[Chars.SSM] + '^3'
            latex_char = Chars.texmap[Chars.SSM]
            string = True
        elif char == Chars.ADD:
            fst = stack.pop()
            snd = stack.pop()
            stack.push(fst + snd)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.BRD:
            bridge = True
            old_x, old_y = x, y
            x, y = nextpos(direction, x, y, befunge)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.DEZ:
            fst = stack.pop()
            if fst == 0:
                direction = 1
            else:
                direction = 3
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.DIV:
            fst = stack.pop()
            snd = stack.pop()
            if snd == 0:
                stack.push(0)
            else:
                stack.push(int(floor(snd / fst)))
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.DUP:
            fst = stack.pop()
            stack.push(fst)
            stack.push(fst)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.GET:
            fst = stack.pop()
            snd = stack.pop()
            stack.push(ord(befunge[fst - 1][snd - 1]))
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.GRT:
            fst = stack.pop()
            snd = stack.pop()
            if snd > fst:
                stack.push(1)
            else:
                stack.push(0)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.INC:
            if debug:
                character = ord(input_dict[input_dict_c])
                stack.push(character)
                del input_dict[input_dict_c]
                input_dict_c -= 1
            else:
                character = input(str(x + 1) + "," + str(y + 1) + " asks for char: ")
                stack.push(ord(character))
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.INI:
            if debug:
                integer = input_dict[input_dict_c]
                del input_dict[input_dict_c]
                input_dict_c -= 1
            else:
                integer = input(str(x + 1) + "," + str(y + 1) + " asks for int: ")
            stack.push(int(integer))
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.M_D:
            direction = 1
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.M_L:
            direction = 2
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.M_R:
            direction = 0
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.M_U:
            direction = 3
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.MOD:
            fst = stack.pop()
            snd = stack.pop()
            if fst == 0:
                stack.push(0)
            else:
                stack.push(snd % fst)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.MUL:
            fst = stack.pop()
            snd = stack.pop()
            stack.push(fst * snd)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.NOT:
            fst = stack.pop()
            if fst == 0:
                stack.push(1)
            else:
                stack.push(0)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.PAD:
            stack.pop()
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.POC:
            fst = stack.pop()
            stdout.write(chr(fst))
            output += chr(fst)
            rule = Chars.texmap[char]
            latex_char = rule
            if debug:
                output_dict[output_dict_c] = '\\xi^{{-1}}({})'.format(fst)
                output_dict_c += 1
        elif char == Chars.POI:
            fst = stack.pop()
            stdout.write(str(fst))
            output += str(fst)
            rule = Chars.texmap[char]
            latex_char = rule
            if debug:
                output_dict[output_dict_c] = fst
                output_dict_c += 1
        elif char == Chars.PUT:
            fst = stack.pop()
            snd = stack.pop()
            v = stack.pop()
            befunge[fst - 1][snd - 1] = chr(v)
            substitutions.append('\\left[P_{{{0},{1}}}\\mapsto{2}\\right]'.format(fst, snd, Chars.texmap[chr(v)]))
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.RAN:
            direction = choice(directions)
            rule = Chars.texmap[char]
            if direction == 0:
                rule += '^1'
            elif direction == 1:
                rule += '^4'
            elif direction == 2:
                rule += '^2'
            elif direction == 3:
                rule += '^3'
            latex_char = rule
        elif char == Chars.REZ:
            fst = stack.pop()
            if fst == 0:
                direction = 0
            else:
                direction = 2
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.SUB:
            fst = stack.pop()
            snd = stack.pop()
            stack.push(snd - fst)
            rule = Chars.texmap[char]
            latex_char = rule
        elif char == Chars.SWP:
            fst = stack.pop()
            snd = stack.pop()
            stack.push(fst)
            stack.push(snd)
            rule = Chars.texmap[char]
            latex_char = rule
        elif not char == ' ':
            stack.push(int(befunge[y][x]))
            rule = '\\texttt{number}'
            latex_char = '\\texttt{{{}}}'.format(char)
        else:
            rule = Chars.texmap[char]
            latex_char = rule

        # SETUP NEXT ROUND

        if debug:
            with open(outfile, 'a+') as p:
                if bridge:
                    p.write(rule_format.format(rule, old_x + 1, old_y + 1, latex_char, ''.join(substitutions)))
                else:
                    if string:
                        p.write(rule_format_2.format(rule, x + 1, y + 1, latex_char, ''.join(substitutions)))
                    else:
                        p.write(rule_format.format(rule, x + 1, y + 1, latex_char, ''.join(substitutions)))
                p.write('\n')
        x, y = nextpos(direction, x, y, befunge)
        if debug:
            with open(outfile, 'a+') as p:
                p.write(conf_format.format(x + 1,
                                           y + 1,
                                           direction_map[direction],
                                           texify_list(output_dict),
                                           texify_list(input_dict),
                                           texify_list(stack.stack),
                                           "string" if stringmode else "normal",
                                           ''.join(substitutions)))
                p.write('\n')
        char = befunge[y][x]
    with open(outfile, "a+") as p:
        p.write(rule_format.format('\\texttt{@}', x + 1, y + 1, '\\texttt{@}', ''.join(substitutions)))
        p.write('\n')
        p.write('$$\\left({}, P{}\\right)$$'.format(texify_list(output_dict), ''.join(substitutions)))
    return output


def run_befunge(filename, debug, input_dict, outfile):
    befungecode = load_befunge(filename)
    return parse(befungecode, debug=debug, input_dict=input_dict, outfile=outfile)


if __name__ == "__main__":
    if len(argv) != 2:
        stdout.write("You need to supply one argument (the file to be executed)")
    else:
        run_befunge(argv[1], debug=True, input_dict={}, outfile="out.txt")

run_befunge('random.befunge', debug=True, input_dict={0: ' ', 1: 'z', 2: 13}, outfile="out.txt")
