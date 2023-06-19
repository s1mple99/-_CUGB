#应课程要求,合为一份代码
import os
#   设置相对路径
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#   文件读入及初始化
f = open(model_path + '/test.txt', encoding='utf-8')
lines = f.readlines()
line_num = 0
Col_num = 0
#   Scanner词法分析器部分
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

#   Parser  语法分析器部分
#   Synatx_analysis  语义分析器及中间代码生成部分
quadruples = []  # 四元式列表
temp_count = 1  # 临时变量计数器
nextquad = 0
def emit(op, arg1, arg2, result):
    global nextquad
    quadruple = [op, arg1, arg2, result]
    quadruples.append(quadruple)
    nextquad += 1
def newtemp():
    global temp_count
    temp_var = "t" + str(temp_count)
    temp_count += 1
    return temp_var
def limit(array,j):
    return 'n'+str(j)
def makelist(i):
    if(i != None):
        return [i]
    else:
        return []
def backpatch(nextlist,quad):
    for i in nextlist:
        quadruples[i][3] = quad
    return
def merge(l1,l2,l3):
    return l1+l2+l3

#   语句和数组
def stmts():
    rest0_inNextlist = stmt()
    stmts_nextlist = rest0(rest0_inNextlist)
    return stmts_nextlist
def rest0(rest0_inNextlist):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == 'if' or token == 'while' or judge_token(token) == 111:
        m_quad = m()
        backpatch(rest0_inNextlist,m_quad)
        rest0_inNextlist = stmt()
        rest0_nextlist = rest0(rest0_inNextlist)
        return rest0_nextlist
    else:
        rest0_nextlist = rest0_inNextlist
        return rest0_nextlist
def stmt():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == 'if':
        advance()
        advance()
        (bool_truelist,bool_falselist) = bool()
        advance()
        m1_quad = m()
        stmt1_nextlist = stmt()
        n_nextlist = n()
        advance()
        m2_quad = m()
        stmt2_nextlist = stmt()
        backpatch(bool_truelist, m1_quad)
        backpatch(bool_falselist, m2_quad)
        stmt_nextlist = merge( stmt1_nextlist ,n_nextlist,stmt2_nextlist)
        return stmt_nextlist
    elif token == 'while':
        advance()
        advance()
        m1_quad = m()
        (bool_truelist, bool_falselist) = bool()
        advance()
        m2_quad = m()
        stmt1_nextlist = stmt()
        backpatch(stmt1_nextlist,m1_quad)
        backpatch(bool_truelist,m2_quad)
        stmt_nextlist = bool_falselist
        emit('j','-','-',m1_quad)
        return stmt_nextlist
    elif judge_token(token) == 111:
        (loc_place,loc_offset) = loc()
        advance()
        expr_place = expr()
        advance()
        if(loc_offset == None):
            emit('=',expr_place,'-',loc_place)
        else:
            emit('[]=', expr_place, '-', loc_place+'['+loc.offset+']')
        stmt_nextlist = makelist(None)
        return stmt_nextlist
def loc():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if judge_token(token) == 111:
        resta_inArray = token
        advance()
        (loc_place,loc_offset) = resta(resta_inArray)
        return (loc_place,loc_offset)
def m():
    m_quad = nextquad;
    return m_quad
def n():
    n_nextlist = makelist(nextquad)
    emit('j','-','-',0)
    return n_nextlist
def resta(resta_inArray):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '[':
        advance()
        (elist_array,elist_offset) = elist(resta_inArray)
        resta_place = newtemp()
        emit('-',elist_array,'C',resta_place)
        resta_offset = newtemp()
        emit('*','w',elist_offset,resta_offset)
        return (resta_place,resta_offset)
        advance()

    else:
        resta_place = resta_inArray
        resta_offset = None
        return (resta_place,resta_offset)
def elist(elist_inArray):
    expr_place = expr()
    rest1_inArray = elist_inArray
    rest1_inNidm =1
    rest1_inPlace = expr_place
    (elist_array,elist_offset) = rest1(rest1_inArray,rest1_inNidm,rest1_inPlace)
    return(elist_array,elist_offset)
def rest1(rest1_inArray,rest1_inNidm,rest1_inPlace):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == ',':
        advance()
        expr_place = expr()
        t = newtemp()
        m = rest1_inNidm + 1
        emit('*',rest1_inPlace,limit(rest1_inArray,m),t)
        emit('+',t,expr_place,t)
        rest1_inArray = rest1_inArray
        rest1_inNidm = m
        rest1_inPlace = t
        (rest1_array,rest1_offset) = rest1(rest1_inArray,rest1_inNidm,rest1_inPlace)
        return (rest1_array,rest1_offset)

    else:
        rest1_array = rest1_inArray
        rest1_offset = rest1_inPlace
        return(rest1_array,rest1_offset)

#   关系运算
def bool():
    (bool_truelist,bool_falselist) = equality()
    return (bool_truelist,bool_falselist)

def equality():
    (rest4_inTruelist,rest4_inFalselist)= rel()
    (equality_truelist,equality_falselist) = rest4(rest4_inTruelist,rest4_inFalselist)
    return (equality_truelist,equality_falselist)

def rest4(rest4_inTruelist,rest4_inFalselist):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '==':
        advance()
        rel()
        rest4()
    elif token == '!=':
        advance()
        rel()
        rest4()
    else:
        (rest4_truelist,rest4_inFalselist) = (rest4_inTruelist,rest4_inFalselist)
        return (rest4_truelist,rest4_inFalselist)

def rel():
    rop_expr_inPlace = expr()
    (rel_truelist,rel_falselist) = rop_expr(rop_expr_inPlace)
    return (rel_truelist,rel_falselist)

def rop_expr(rop_expr_inPlace):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '<':
        advance()
        rop_expr_truelist = makelist(nextquad)
        rop_expr_falselist = makelist(nextquad + 1)
        expr_place = expr()
        emit('j<',rop_expr_inPlace , expr_place, '-');
        emit('j', '-', '-', '-')
    elif token == '<=':
        advance()
        rop_expr_truelist = makelist(nextquad)
        rop_expr_falselist = makelist(nextquad + 1)
        expr_place = expr()
        emit('j<=', rop_expr_inPlace, expr_place, '-');
        emit('j', '-', '-', '-')
    elif token == '>':
        advance()
        rop_expr_truelist = makelist(nextquad)
        rop_expr_falselist = makelist(nextquad + 1)
        expr_place = expr()
        emit('j>', rop_expr_inPlace, expr_place, '-');
        emit('j', '-', '-', '-')
    elif token == '>=':
        advance()
        rop_expr_truelist = makelist(nextquad)
        rop_expr_falselist = makelist(nextquad + 1)
        expr_place = expr()
        emit('j>=', rop_expr_inPlace, expr_place, '-');
        emit('j', '-', '-', '-')
    else:
        rop_expr_truelist = makelist(nextquad)
        rop_expr_falselist = makelist(nextquad + 1)
        emit('jnz', rop_expr_inPlace, '-', '-');
        emit('j', '-', '-', '-')
    return (rop_expr_truelist,rop_expr_falselist)


#   加减运算
def expr():
    place = term()
    return rest5(place)


def rest5(rest5_in):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '+':
        advance()
        term_place = term()
        rest51_in = newtemp()
        emit('+',rest5_in, term_place,rest51_in)
        return rest5(rest51_in)
    elif token == '-':
        advance()
        term_place = term()
        rest51_in = newtemp()
        emit('-', rest5_in, term_place, rest51_in)
        return rest5(rest51_in)
    else:
        return rest5_in

#   包含乘除的算法表达式
def term():
    place = unary()
    return rest6(place)
def rest6(rest6_in):
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '*':
        advance()
        unary_place = unary()
        rest61_in = newtemp()
        emit('*', rest6_in, unary_place, rest61_in)
        return rest6(rest61_in)

    elif token == '/':
        advance()
        unary_place = unary()
        rest61_in = newtemp()
        emit('/',rest6_in,unary_place,rest61_in)
        return rest6(rest61_in)
    else:
        return rest6_in
def unary():
    return factor()
def factor():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '(':
        advance()
        expr_ = expr()
        advance()
        return expr_
    elif token.isdigit():
        token_ = token
        advance()
        return token_
    elif judge_token(token) == 111:
        (loc_place,loc_offset) = loc()
        if(loc_offset == None):
            factor_place = loc_place
        else:
            factor_place = newtemp()
            emit('=[]',loc_place+'['+loc_offset+']','-',factor_place)
        return factor_place

    else:
        print("error")
        return

#   主函数
stmts()
index = 0
for q in quadruples:
    output = "{:2d} : [{:>3},{:>3},{:>3},{:>3}]".format(index, q[0], q[1], q[2], q[3])
    print(output)
    index += 1


