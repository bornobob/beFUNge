class Chars:
    ADD = "+"  # addition
    SUB = "-"  # subtraction
    MUL = "*"  # multiplication
    DIV = "/"  # integer division
    MOD = "%"  # modulo
    NOT = "!"  # NOT
    GRT = "`"  # greater than
    M_R = ">"  # move right
    M_D = "v"  # move down
    M_L = "<"  # move left
    M_U = "^"  # move up
    RAN = "?"  # random direction
    REZ = "_"  # horizontal if condition
    DEZ = "|"  # vertical if condition
    SSM = "\""  # switch stringmode
    DUP = ":"  # duplicate top element of stack
    SWP = "\\"  # swap top elements of stack
    PAD = "$"  # pop and discard top element of stack
    POI = "."  # pop and output top element of stack as integer
    POC = ","  # pop and output top element of stack as character
    BRD = "#"  # bridge
    PUT = "p"  # put
    GET = "g"  # get
    INI = "&"  # input integer
    INC = "~"  # input character
    END = "@"  # end program

    texmap = {
        ADD: '\\texttt{+}',
        SUB: '\\texttt{-}',
        MUL: '\\texttt{*}',
        DIV: '\\texttt{/}',
        MOD: '\\texttt{\\%}',
        NOT: '\\texttt{!}',
        GRT: '\\texttt{`}',
        M_R: '\\texttt{>}',
        M_D: '\\lor',
        M_L: '\\texttt{<}',
        M_U: '\\land',
        RAN: '\\texttt{?}',
        REZ: '\\texttt{\\_}',
        DEZ: '\\texttt{|}',
        SSM: '\\texttt{"}',
        DUP: '\\texttt{:}',
        SWP: '\\setminus',
        PAD: '\\texttt{\\$}',
        POI: '\\texttt{.}',
        POC: '\\texttt{,}',
        BRD: '\\texttt{\\#}',
        PUT: '\\texttt{p}',
        GET: '\\texttt{g}',
        INI: '\\texttt{\\&}',
        INC: '\\sim',
        END: '\\texttt{@}',
        '1': '\\texttt{1}',
        '2': '\\texttt{2}',
        '3': '\\texttt{3}',
        '4': '\\texttt{4}',
        '5': '\\texttt{5}',
        '6': '\\texttt{6}',
        '7': '\\texttt{7}',
        '8': '\\texttt{8}',
        '9': '\\texttt{9}',
        ' ': '\\texttt{" "}'
    }
