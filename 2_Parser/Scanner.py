import os
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
f = open(model_path + '/test.txt', encoding='utf-8')
lines = f.readlines()
line_num = 0
Col_num = 0



def tokenize(code, index):
    operators = ['++', '--', '+', '-', '*', '/', '%', '=', '>', '>=', '<', '<=', '==', '!=', '&&', '||', '!']
    delimiters = [',', '(', ')', ';', '{', '}', '[', ']']
    keywords = {'main', 'int', 'char', 'if', 'else', 'for', 'while', 'return', 'void'}
    i = index

    while i < len(code):
        if code[i].isspace() or code[i] == '\n':
            return ('', i + 1)  # 返回空标记和更新后的索引

        if code[i:i + 2] in operators:
            return (code[i:i + 2], i + 2)  # 返回运算符标记和更新后的索引

        if code[i] in operators:
            return (code[i], i + 1)  # 返回运算符标记和更新后的索引

        if code[i] in delimiters:
            return (code[i], i + 1)  # 返回分隔符标记和更新后的索引

        if code[i].isalpha() or code[i] == '_':
            j = i + 1
            while j < len(code) and (code[j].isalnum() or code[j] == '_'):
                j += 1
            token = code[i:j]
            if token in keywords:
                return (token, j)  # 返回关键字标记和更新后的索引
            else:
                return (token, j)  # 返回标识符标记和更新后的索引

        if code[i].isdigit():
            j = i + 1
            while j < len(code) and code[j].isdigit():
                j += 1
            return (code[i:j], j)  # 返回数字标记和更新后的索引

    return ('', i)  # 返回空标记和当前索引


keywords = {'main': 1, 'int': 5, 'char': 3, 'if': 17, 'else': 15, 'for': 6, 'while': 20, 'return': 8, 'void': 9}

symbols = {'<=': 50, '==': 51, '!=': 52, '&&': 53, '||': 54, '!': 55, '++': 56, '--': 57,
           '+': 41, '-': 42, '*': 43, '/': 44, '%': 45, '=': 46, '>': 47, '>=': 48, '<': 49, '(': 81, ')': 82,
           ',': 83, ';': 84, '{': 86, '}': 87, '[': 88, ']': 89}


def judge_token(s):
    if s[0].isalpha() and s in keywords:
        return keywords[s]  # 返回关键字代码
    elif s[0].isalpha() and s not in keywords and s.isalnum():
        return 111  # 返回标识符代码
    elif s.isdigit():
        return 20  # 返回数字代码
    elif s in symbols:
        return symbols[s]  # 返回符号代码
    else:
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            return 50  # 返回字符串代码
        else:
            return 'Notfound'  # 返回 'Notfound'



def get_token(line_num, col_num, lines):
    if line_num == len(lines):
        return ('%%done', -1, -1)

    (token, col_num) = tokenize(lines[line_num], col_num)

    if token == '':
        if col_num < len(lines[line_num]):
            return get_token(line_num, col_num, lines)
        else:
            return get_token(line_num + 1, 0, lines)
    else:
        if col_num < len(lines[line_num]):
            return (token, line_num, col_num)
        else:
            return (token, line_num + 1, 0)


def advance():
    global line_num, Col_num
    (token, line_num, Col_num) = get_token(line_num, Col_num, lines)




if __name__ == '__main__':
    global token
    for i in range(40):
        (token, line_num, Col_num) = get_token(line_num, Col_num,lines)
        if(token == '%%done'):
            break
        else:
            print("<",judge_token(token),",",token,">")
