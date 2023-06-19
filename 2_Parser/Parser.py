from Scanner import *



#############################################################################
##加入语句和数组
def advance():
    global line_num, Col_num
    (token, line_num, Col_num) = get_token(line_num, Col_num, lines)

def stmts():
    print("stmts -> stmt rest0")
    stmt()
    rest0()


def rest0():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == 'if' or token == 'while' or judge_token(token) == 111:
        print("rest0 -> stmt rest0")
        stmt()
        rest0()
    else:
        print("rest0 -> ε")


def stmt():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == 'if':
        print("stmt -> if(bool) stmt else stmt")
        advance()
        advance()
        bool()
        advance()
        stmt()
        advance()
        stmt()
    elif token == 'while':
        print("stmt -> while(bool) stmt")
        advance()
        advance()
        bool()
        advance()
        stmt()
    elif judge_token(token) == 111:
        print("stmt -> loc = expr;")
        loc()
        advance()
        expr()
        advance()


def loc():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if judge_token(token) == 111:
        print("loc -> id resta")
        advance()
        resta()


def resta():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '[':
        print("resta -> [elist]")
        advance()
        elist()
        advance()
    else:
        print("resta -> ε")


def elist():
    print("elist -> expr rest1")
    expr()
    rest1()


def rest1():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == ',':
        print("rest1 -> ,expr rest1")
        advance()
        expr()
        rest1()
    else:
        print("rest1 -> ε")


#############################################################################


#############################################################################
##加入关系运算
def bool():
    print("bool -> equlity")
    equality()


def equality():
    print("equlity -> rel rest4")
    rel()
    rest4()


def rest4():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '==':
        print("rest4 -> ==rel rest4")
        advance()
        rel()
        rest4()
    elif token == '!=':
        print("rest4 -> !=rel rest4")
        advance()
        rel()
        rest4()
    else:
        print("rest4 -> ε")


def rel():
    print("rel -> expr rop_expr")
    expr()
    rop_expr()


def rop_expr():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '<':
        print("rop_expr -> <expr")
        advance()
        expr()
    elif token == '<=':
        print("rop_expr -> <=expr")
        advance()
        expr()
    elif token == '>':
        print("rop_expr -> >expr")
        advance()
        expr()
    elif token == '>=':
        print("rop_expr -> >=expr")
        advance()
        expr()
    else:
        print("rest5 -> ε")


#############################################################################
def expr():
    print("expr -> term rest5")
    term()
    rest5()


def rest5():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '+':
        print("rest5 -> +term rest5")
        advance()
        term()
        rest5()
    elif token == '-':
        print("rest5 -> -term rest5")
        advance()
        term()
        rest5()
    else:
        print("rest5 -> ε")


def term():
    print("term -> unary rest6")
    unary()
    rest6()


def rest6():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '*':
        print("rest6 -> *unary rest6")
        advance()
        unary()
        rest6()
    elif token == '/':
        print("rest6 -> /unary rest6")
        advance()
        unary()
        rest6()
    else:
        print("rest6 -> ε")

def unary():
    print("unary -> factor")
    factor()

def factor():
    global line_num, Col_num
    (token, line_num_, Col_num_) = get_token(line_num, Col_num, lines)
    if token == '(':
        print("factor -> (expr)")
        advance()
        expr()
        advance()
    elif token.isdigit():
        print("factor -> num")
        advance()
    elif judge_token(token) == 111:
        print("factor -> loc")
        loc()

    else:
        print("error")
        return
line_num = 0
Col_num = 0

import os
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
f = open(model_path + '/exp3_2.txt', encoding='utf-8')
lines = f.readlines()


#term()  #exp2_1
#expr()  #exp2_2
#bool    #exp3_1
stmts()  #test/exp3_2
