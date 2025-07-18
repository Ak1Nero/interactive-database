import people
import tokenizer_oop
import color

def SortByAttribute(obj_list, attr:str):
    n = len(obj_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(obj_list[j], "get_" + attr)() < getattr(obj_list[j + 1], "get_" + attr)():
                obj_list[j], obj_list[j + 1] = obj_list[j + 1], obj_list[j] #bug prone
    return obj_list

print(__name__)
if __name__ == "__main__":
    print("Parse.py")

    temp_tables = {}

    while True:

        user_input = input(">> ").split(" ")
        user_input.append("\n")

        if user_input[0] == "CREATE":
            temp_tables[user_input[1]] = []
            print(color.green + f"{user_input[1]} is created" + color.reset)

        elif user_input[0] == "FORGET":
            del temp_tables[user_input[1]]
            print(color.green + f"{user_input[1]} has been forgotten" + color.reset)

        elif user_input[0] == "TBLLIST":
            for i in temp_tables:
                print(color.cyan + f"{i} {len(temp_tables[i])}" + color.reset)

                #TODO сделать try и except для create, forget, tbllist

        elif user_input[0] == "LOAD":
            try:
                if user_input[2] != "AS":
                    raise SyntaxError(color.red + "After name of file AS is required" + color.reset)
                elif user_input[3] in temp_tables:
                    temp_tables[user_input[3]] = people.file_to_obj_list(user_input[1])
                    print(color.green + "Loading is successfully" + color.reset)
                else:
                    raise SyntaxError(color.red + "The entered table does not exist" + color.reset)
            except FileNotFoundError:
                print(color.red + f"No such file or directory: '{user_input[1]}'" + color.reset)
            except SyntaxError as e:
                print(e)

        elif user_input[0] == "SAVE":
            try:
                if user_input[1] in temp_tables:
                    people.obj_list_to_file(user_input[3], temp_tables[user_input[1]])
                    print(color.green + "Saving is successfully" + color.reset)
                    #TODO сделать исключение FileError
                else:
                    raise SyntaxError(color.red + "The entered table does not exist" + color.reset)        
            except SyntaxError as e:
                print(e)

        elif user_input[0] == "INSERT":
            try:
                if user_input[1] != "INTO":
                    raise SyntaxError(color.red + "After insert INTO is required" + color.reset)
                splitted_user_input = user_input[3].split(";")
                
                if splitted_user_input[0] == "PERSON" and len(splitted_user_input) == 3:
                    object = people.Person(splitted_user_input[1], int(splitted_user_input[2]))
                elif splitted_user_input[0] == "STUDENT" and len(splitted_user_input) == 5:
                    object = people.Student(splitted_user_input[1], int(splitted_user_input[2]),
                    splitted_user_input[3], int(splitted_user_input[4]))
                elif splitted_user_input[0] == "WORKER" and len(splitted_user_input) == 5:
                    object = people.Worker(splitted_user_input[1],
                    int(splitted_user_input[2]), splitted_user_input[3], int(splitted_user_input[4]))
                else:
                    raise ValueError(color.red + "object is not recognized" + color.reset)
                temp_tables[user_input[2]].append(object)
                print(color.green + "inserted" + color.reset)
            except SyntaxError as e:
                print(e)
            except ValueError as e:
                print(e)

        elif user_input[0] == "SELECT":
            try:
                if user_input[1] == "PERSON":
                    Type = people.Person
                elif user_input[1] == "STUDENT":
                    Type = people.Student
                elif user_input[1] == "WORKER":
                    Type = people.Worker
                else:
                    raise SyntaxError(color.red + "Object type has not been recognized" + color.reset)
                if user_input[2] != "FROM":
                    raise SyntaxError(color.red + "After object type FROM is required" + color.reset)
                tmp = []
                if user_input[3] in temp_tables:
                    for i in temp_tables[user_input[3]]:
                        if isinstance(i, Type):
                            tmp.append(i)
                else:
                    raise SyntaxError(color.red + "The entered table does not exist" + color.reset)
                if user_input[4] != "AS":
                    raise SyntaxError(color.red + "After table AS is required" + color.reset)
                step = 6
                expression = ""
                temp_tables[user_input[5]] = []
                if user_input[5] == "\n" or user_input[5] == "WHERE":
                    raise SyntaxError(color.red + "After AS table is required" + color.reset)
                if user_input[step] == "WHERE" :
                    step += 1
                    while step < len(user_input) and user_input[step] != "ORDER":
                        expression += user_input[step] + " "
                        step += 1
                    expression += "\n"
                    t = tokenizer_oop.Tokenizer(expression)
                    for j in range(len(tmp)):
                        t_list = t.get_token_list()
                        for i in range(len(t_list)):
                            if t_list[i][0] == "variable":
                                t_list[i] = (t_list[i][0], "getattr(tmp[j], " + "\"" + "get_" + t_list[i][1] + "\"" + ")" + "()")
                        packed_str = " ".join([x[1] for x in t_list])
                        #print(packed_str)
                        try:
                            if eval(packed_str) == True:
                                temp_tables[user_input[5]].append(tmp[j])
                        except Exception:
                            raise SyntaxError(color.red + "Error in logical expression after WHERE" + color.reset)

                elif user_input[step] == "ORDER":
                    temp_tables[user_input[5]] = tmp
                    step += 1
                    if user_input[step] != "BY":
                        raise SyntaxError(color.red + "After order BY is required" + color.reset)
                    else:
                        step += 1
                        SortByAttribute(temp_tables[user_input[5]], user_input[step])
                        if user_input[step + 1] != "\n":
                            raise SyntaxError(color.red + "ORDER BY must be last" + color.reset)
                elif user_input[step] == "\n":
                    temp_tables[user_input[5]] = tmp
                else: 
                    raise SyntaxError(color.red + "Select option not recognized" + color.reset)
            except SyntaxError as e:
                print(e)

        elif user_input[0] == "UPDATE":
            try:
                if user_input[1] in temp_tables:
                    if user_input[2] == "SET":
                        step = 3
                        string = ""
                        while user_input[step] != "WHERE" and user_input[step] != "\n":
                            string += user_input[step] + " "
                            step += 1
                        if user_input[step] != "\n":
                            t = tokenizer_oop.Tokenizer(string)
                            t_list1 = t.get_token_list()
                            if t_list1 != []:
                                t_list1.pop()
                            if len(t_list1) != 2:
                                raise SyntaxError(color.red + "SET requires two arguments: attr name and value" + color.reset)
                            if t_list1[0][0] == "variable":
                                expression = ""
                                i = step + 1
                                while i < len(user_input):
                                    expression += user_input[i] + " "
                                    i += 1
                                expression += "\n"
                                t = tokenizer_oop.Tokenizer(expression)
                                for j in range(len(temp_tables[user_input[1]])):
                                    t_list = t.get_token_list()
                                    for i in range(len(t_list)):
                                        if t_list[i][0] == "variable":
                                            t_list[i] = (t_list[i][0], "getattr(temp_tables[user_input[1]][j], " + "\"" + "get_" + t_list[i][1] + "\"" + ")" + "()")
                                    packed_str = " ".join([x[1] for x in t_list])

                                    if hasattr(temp_tables[user_input[1]][j], "set_" + t_list1[0][1]):
                                        try:
                                            b = eval(packed_str)
                                            assert type(b) is bool
                                        except Exception:
                                            raise SyntaxError(color.red + "Error in logical expression after WHERE" + color.reset)
                                        if b == True:
                                            if t_list1[1][0] == "integer":
                                                getattr(temp_tables[user_input[1]][j], "set_" + t_list1[0][1])(int(t_list1[1][1]))
                                            elif t_list1[1][0] == "float":
                                                getattr(temp_tables[user_input[1]][j], "set_" + t_list1[0][1])(float(t_list1[1][1]))
                                            elif t_list1[1][0] == "string":
                                                getattr(temp_tables[user_input[1]][j], "set_" + t_list1[0][1])(str(t_list1[1][1]).strip("\""))
                                            else:
                                                raise ValueError(color.red + "Invalid Value after SET" + color.reset)          
                            else:
                                raise SyntaxError(color.red + "The attr should be variable" + color.reset)                                    
                        else:
                            raise SyntaxError(color.red + "WHERE is required after SET arguments" + color.reset)                                        
                    else:
                        raise SyntaxError(color.red + "After table SET is required" + color.reset)
                else:
                    raise SyntaxError(color.red + "The entered table does not exist" + color.reset)
            except Exception as e:
                print(e)
        elif user_input[0] == "SHOW":
            try:
                if user_input[1] in temp_tables:
                    for i in temp_tables[user_input[1]]:
                        print(color.cyan + f"{i}" + color.reset)
                else:
                    raise SyntaxError(color.red + "The entered table does not exist" + color.reset)
            except SyntaxError as e:
                print(e)
        
        else:
            try:
                raise SyntaxError(color.red + "query not recognized" + color.reset)
            except SyntaxError as e:
                print(e)