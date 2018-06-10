def load_befunge(filename):
    with open(filename) as infile:
        output = []
        for line in infile:
            linechars = []
            for char in line:
                if char != '\n':
                    linechars.append(char)
            output.append(linechars)
        maxlength = max([len(x) for x in output])
        for list_line in output:
            for _ in range(maxlength - len(list_line)):
                list_line.append(' ')
        return output
