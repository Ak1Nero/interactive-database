import color

class Tokenizer:
    def __init__(self, str_to_proc):
        self.numerals = "1;2;3;4;5;6;7;8;9;0"
        self.literals = "A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z;a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r;s;t;u;v;w;x;y;z"
        self.operation_symbols = ";=;+;-;/;%;*;<;>;!;:"
        self.esc_characters = " ;\n"
        self.l_par = "("
        self.r_par = ")"
        self.quote = '"'
        self.comma = ","
        self.point = "."

        self.numerals = self.numerals.split(";")
        self.literals = self.literals.split(";")
        self.operation_symbols = self.operation_symbols.split(";")
        self.esc_characters = self.esc_characters.split(";")
        self.l_par = self.l_par.split(";")
        self.r_par = self.r_par.split(";")
        self.quote = self.quote.split(";")
        self.comma = self.comma.split(";")
        self.point = self.point.split(";")
        self.valid_alphabet = self.numerals + self.literals + self.operation_symbols + self.esc_characters + self.l_par + self.r_par + self.quote + self.comma + self.point

        self.states_num = 20
        self.fsm = []
        self.is_terminal = [False] * self.states_num
        self.is_terminal[8] = True
        self.predefined = {"or": "operation", "not": "operation", "and": "operation", "True": "const", "False": "const"}
        self.str_to_proc = str_to_proc
        self.token_list = []

        for i in range(self.states_num):
            self.fsm.append({})
        for i in self.fsm:
            for j in self.valid_alphabet:
                i[j] = 0
        for i in self.literals:
            self.fsm[0][i] = 1
        for i in self.operation_symbols:
            self.fsm[0][i] = 3
        for i in self.numerals:
            self.fsm[0][i] = 5
        for i in self.l_par:
            self.fsm[0][i] = 2
        for i in self.r_par:
            self.fsm[0][i] = 4
        for i in self.quote:
            self.fsm[0][i] = 6
        for i in self.comma:
            self.fsm[0][i] = 7
        for i in self.point:
            self.fsm[0][i] = 18
        self.fsm[0][" "] = 0
        self.fsm[0]["\n"] = 8

        for i in self.literals + self.numerals:
            self.fsm[1][i] = 1
        for i in self.operation_symbols:
            self.fsm[1][i] = 11
        for i in self.l_par:
            self.fsm[1][i] = 11
        for i in self.r_par:
            self.fsm[1][i] = 11
        for i in self.quote:
            self.fsm[1][i] = 11
        for i in self.comma:
            self.fsm[1][i] = 11
        for i in self.point:
            self.fsm[1][i] = 11
        self.fsm[1][" "] = 11
        self.fsm[1]["\n"] = 11

        for i in self.literals:
            self.fsm[2][i] = 12
        for i in self.operation_symbols:
            self.fsm[2][i] = 12
        for i in self.numerals:
            self.fsm[2][i] = 12
        for i in self.l_par:
            self.fsm[2][i] = 12
        for i in self.r_par:
            self.fsm[2][i] = 12
        for i in self.quote:
            self.fsm[2][i] = 12
        for i in self.comma:
            self.fsm[2][i] = 9
        for i in self.point:
            self.fsm[2][i] = 9
        self.fsm[2][" "] = 12
        self.fsm[2]["\n"] = 12

        for i in self.operation_symbols:
            self.fsm[3][i] = 3
        for i in self.literals:
            self.fsm[3][i] = 13
        for i in self.numerals:
            self.fsm[3][i] = 13
        for i in self.l_par:
            self.fsm[3][i] = 13
        for i in self.r_par:
            self.fsm[3][i] = 13
        for i in self.quote:
            self.fsm[3][i] = 13
        for i in self.comma:
            self.fsm[3][i] = 9
        for i in self.point:
            self.fsm[3][i] = 9
        self.fsm[3][" "] = 13
        self.fsm[3]["\n"] = 13

        for i in self.literals:
            self.fsm[4][i] = 14
        for i in self.operation_symbols:
            self.fsm[4][i] = 14
        for i in self.numerals:
            self.fsm[4][i] = 14
        for i in self.l_par:
            self.fsm[4][i] = 14
        for i in self.r_par:
            self.fsm[4][i] = 14
        for i in self.quote:
            self.fsm[4][i] = 14
        for i in self.comma:
            self.fsm[4][i] = 14
        for i in self.point:
            self.fsm[4][i] = 14
        self.fsm[4][" "] = 14
        self.fsm[4]["\n"] = 14

        for i in self.numerals:
            self.fsm[5][i] = 5
        for i in self.literals:
            self.fsm[5][i] = 9
        for i in self.quote:
            self.fsm[5][i] = 9
        for i in self.operation_symbols:
            self.fsm[5][i] = 15
        for i in self.l_par:
            self.fsm[5][i] = 15
        for i in self.r_par:
            self.fsm[5][i] = 15
        for i in self.comma:
            self.fsm[5][i] = 15
        for i in self.point:
            self.fsm[5][i] = 18
        self.fsm[5][" "] = 15
        self.fsm[5]["\n"] = 15

        for i in self.literals:
            self.fsm[6][i] = 6
        for i in self.numerals:
            self.fsm[6][i] = 6
        for i in self.operation_symbols:
            self.fsm[6][i] = 6
        for i in self.l_par:
            self.fsm[6][i] = 6
        for i in self.r_par:
            self.fsm[6][i] = 6
        for i in self.comma:
            self.fsm[6][i] = 6
        for i in self.quote:
            self.fsm[6][i] = 16
        for i in self.point:
            self.fsm[6][i] = 6
        self.fsm[6][" "] = 6
        self.fsm[6]["\n"] = 16

        for i in self.comma:
            self.fsm[7][i] = 9
        for i in self.literals:
            self.fsm[7][i] = 17
        for i in self.numerals:
            self.fsm[7][i] = 17
        for i in self.operation_symbols:
            self.fsm[7][i] = 9
        for i in self.l_par:
            self.fsm[7][i] = 17
        for i in self.r_par:
            self.fsm[7][i] = 17
        for i in self.quote:
            self.fsm[7][i] = 17
        for i in self.point:
            self.fsm[7][i] = 9
        self.fsm[7][" "] = 17
        self.fsm[7]["\n"] = 17

        for i in self.point:
            self.fsm[18][i] = 9
        for i in self.literals:
            self.fsm[18][i] = 9
        for i in self.numerals:
            self.fsm[18][i] = 18
        for i in self.operation_symbols:
            self.fsm[18][i] = 19
        for i in self.l_par:
            self.fsm[18][i] = 19
        for i in self.r_par:
            self.fsm[18][i] = 19
        for i in self.quote:
            self.fsm[18][i] = 9
        for i in self.comma:
            self.fsm[18][i] = 19
        self.fsm[18][" "] = 19
        self.fsm[18]["\n"] = 19

        for i in range(11,18):
            self.is_terminal[i] = True
        self.is_terminal[19] = True

        for i in self.valid_alphabet:
            self.fsm[9][i] = 9
        i = 0
        if str_to_proc == "":
            str_to_proc += "\n"
        if "\n" != str_to_proc[-1]:
            str_to_proc += "\n"
        while str_to_proc[i] != "\n":
            q = 0
            lex_s = ""
            while not self.is_terminal[q]:
                q = self.fsm[q][str_to_proc[i]]
                if self.is_terminal[q]:
                    break
                else:
                    lex_s += str_to_proc[i]
                    i += 1
            if q == 9:
                raise SyntaxError(color.red + f"Lexical Error in expression: {str_to_proc}" + color.reset)
            (token_type, lex_s, i) = self.flush(lex_s, q, i)
            token = token_type, lex_s
            self.token_list.append(token)

    def get_token_list(self):
        return [x for x in self.token_list]

    def flush(self, lex_s, q, i):
        match q:
            case 11:
                if lex_s.strip() in self.predefined:
                    return (self.predefined[lex_s.strip()], lex_s.strip(), i)
                else:
                    return ("variable", lex_s.strip(), i)
            case 12:
                return ("l_par", lex_s.strip(), i)
            case 13:
                return ("operation", lex_s.strip(), i)
            case 14:
                return ("r_par", lex_s.strip(), i)
            case 15:
                return ("integer", lex_s.strip(), i)
            case 16:
                return ("string", lex_s.strip() + "\"", i + 1)
            case 17:
                return ("comma", lex_s.strip(), i)
            case 19:
                return ("float", lex_s.strip(), i)
            case 8:
                return ("end", lex_s.strip(), i)
            

obj = Tokenizer("number == 5 or str >= \"psd\"")
print(obj.get_token_list())

