from pptree import *
from math import factorial
import copy
import os
import re

def isDigit(s):
    p = re.compile("-*[0-9]+")
    matched = p.match(s)
    if matched:
        return True


    


""" operations
"0-9" - numbers
"a-z" - symbols
functions:
    add(a, b)
    mul(a, b)
    pow(a, n)
    eql(a, b)

example:
    sum(mul(a, b), 3) = ab + 3 

            sum
           /   \
         mul    3
        /   \
       a     b

"""
class Tree:
    def __init__(self, node):
        self.node = node 
        self.a = None
        self.b = None

    
class Tokens:
    def __init__(self, add, mul, power):
        self.add = add 
        self.mul = mul 
        self.power = power 

tokens = Tokens('add', 'mul', 'pow')
class Val:
    def __init__(self, val = 'Nothing'):
        self.val = val

    def isConst(self):
        return True 

    def valInt(self):
        return int(self.val)

    def __str__(self):
        return '{}'.format(self.val)

    def __eq__(self, other):
        return (self.val == other.val)

    def __add__(self, other):
        return (self.val + other.val)

class Var:
    def __init__(self, var = 'Nothing', power = 1):
        self.var = var
        self.power = power
    def powerInc(self):
        self.power += 1
   
    def isConst(self):
        return False

    def __str__(self):
        if self.power > 1:
            return '{} sup {}'.format(self.var, self.power)
        else:
            return '{}'.format(self.var)

    def __eq__(self, other):
        return (self.var == other.var and self.power == other.power)


def error(msg):
    raise Exception(msg)

def head(xs):
    if xs == []:
        error('Can`t get head. Empty list')
    else:
        return xs[0]

def tail(xs):
    if xs == []:
        error('Can`t get tail. Empty list')
    else:
        return xs[1:]

def last(xs):
    if xs == []: error('Can`t get last. Not enaught symbols')
    else:
        return xs[-1]

def untilLast(xs):
    return xs[:-1]

def hasBracket(s):
    return (('(' in s) or (')' in s))

def bracketFind(c):
    if c == '(':
        return 1
    elif c == ')':
        return (-1)
    else:
        return 0


def filterBrackets(strInp):
    p = lambda x: x if (x != '(') and (x != ')') else '' 
    return ''.join(list(filter(p, strInp)))

def filterSpaces(strInp):
    p = lambda x: x if x != ' ' else '' 
    return ''.join(list(filter(p, strInp)))

def simpleParse(strInp, deep = 0, output = None, outputFlagSnd = False):
    if output == None:
        #fst = f tag, snd = arguments
        output = ['', '', '']

    if list(strInp) == []:
        returnOutput = (untilLast(output[0]), output[1], untilLast(output[2]))
        return returnOutput 

    else:
        x = head(strInp)
        xs = tail(strInp)
        bracket = bracketFind(x) 
        if (deep == 0) and (bracket < 0):
            error("Parsing brackets error")
        else:
            if (deep == 1) and (outputFlagSnd == False) and (x == ','):
                outputFlagSnd = True

            if deep == 0:
                output[0] += x 
            elif outputFlagSnd == False:
                output[1] += x
            else:
                if ((x != ',') or (deep != 1)):
                    output[2] += x 

            deep += bracket
            return simpleParse(xs, deep, output, outputFlagSnd)

def parse(inpStr):
    #  if inpStr == []:
    if hasBracket(inpStr):
        f, a, b = simpleParse(inpStr)
        #  print('a = ', a, ' b = ', b)
        ast = Tree(f)
        ap = parse(a)
        bp = parse(b)
        if ap != None:
            ast.a = ap 
        if bp != None:
            ast.b = bp 
        if ap == None: 
            ast.a = Tree(a)
        if bp == None:
            ast.b = Tree(b)
        return ast
        
    else:
        return None

# create tree for output
def createTree(tree, parent = None):
    if tree == None:
        return parent
    else:
        ast = Node(tree.node, parent)
        if tree.a != None:
            createTree(tree.a, ast)
        if tree.b != None:
            createTree(tree.b, ast)
        return ast

def printTree(tree):
    print_tree(createTree(tree))


def check(tree, startTree, tokens):
    add = tokens.add
    mul = tokens.mul
    power = tokens.power
    if tree.a == tree.b == None:
        return tree
    if (tree.node == add):
        if isDigit(tree.a.node):
            if int(tree.a.node) == 0:
                newTree = Tree(tree.b.node)
                #  return check(newTree, startTree, tokens)
                return newTree

        if isDigit(tree.b.node):
            if int(tree.b.node) == 0:
                newTree = Tree(tree.a.node)
                #  return check(newTree, startTree, tokens)
                return newTree

    elif (tree.node == mul):
        if isDigit(tree.a.node):
            a = int(tree.a.node) 
            if a == 0:
                newTree = Tree('0')
                #  return check(newTree, startTree, tokens)
                return newTree
            elif a == 1:
                newTree = Tree(tree.b.node)
                #  return check(newTree, startTree, tokens)
                return newTree

        if isDigit(tree.b.node):
            b = int(tree.b.node) 
            if b == 0:
                newTree = Tree('0')
                #  return check(newTree, startTree, tokens)
                return newTree
            elif b == 1:
                newTree = Tree(tree.a.node)
                #  return check(newTree, startTree, tokens)
                return newTree

        elif (tree.a.node == tree.b.node == add):
            fstSumA = tree.a.a 
            fstSumB = tree.a.b 
            sndSumA = tree.b.a 
            sndSumB = tree.b.b 

            newTree = Tree(add)

            newTree.a = Tree(add)
            newTree.b = Tree(add)

            newTree.a.a = Tree(mul) 
            newTree.a.b = Tree(mul) 
            newTree.b.a = Tree(mul) 
            newTree.b.b = Tree(mul) 


            newTree.a.a.a = fstSumA 
            newTree.a.a.b = sndSumA 

            newTree.a.b.a = fstSumA 
            newTree.a.b.b = sndSumB 

            newTree.b.a.a = fstSumB 
            newTree.b.a.b = sndSumA 

            newTree.b.b.a = fstSumB 
            newTree.b.b.b = sndSumB 

            #  return check(newTree, startTree, tokens)
            return newTree

        elif (tree.a.node == add or tree.b.node == add):
            if tree.a.node == add:
                fstSumA = tree.a.a
                fstSumB = tree.a.b
                snd     = tree.b
            elif tree.b.node == add:
                fstSumA = tree.b.a
                fstSumB = tree.b.b
                snd     = tree.a

            newTree = Tree(add)
            newTree.a = Tree(mul)
            newTree.b = Tree(mul)

            newTree.a.a = fstSumA
            newTree.a.b = snd 

            newTree.b.a = fstSumB
            newTree.b.b = snd 

            #  return check(newTree, startTree, tokens)
            return newTree

    elif tree.node == power:
        # check that power is integer and > 0
        power = 0
        if isDigit(tree.a.node):  
            power = int(tree.a.node)
            # if power is 1 - return just value
            if power == 1:
                #  return check(newTree, startTree, tokens)
                return tree.b 
            # if power == 0 - return just 1
            elif power == 0:
                newTree = Tree('1')
                #  return check(newTree, startTree, tokens)
                return newTree
            # if power >= 0 and power on add
            elif power >= 0 and tree.b.node == tokens.add:
                newTree = powerAdd(power, tree.b, tokens)
                #  return check(newTree, startTree, tokens)
                return newTree

            # if power >= 0 and power on mul
            #  elif power >= 0 and tree.b.node == tokens.mul:
            elif power >= 0 and tree.b.node == tokens.mul:
                newTree = powerMul(power, tree.b, tokens)
                #  return check(newTree, startTree, tokens)
                return newTree
            elif power >= 0 and tree.b.node != tokens.mul != tokens.add:
                newTree = justPower(power, tree.b)
        else:
            error('Power not integer or < 0')



    tree.a = check(tree.a, tree.a, tokens)
    tree.b = check(tree.b, tree.b, tokens)
    #  if tree == startTree:
    #      return tree
    #  else:
    #      return check(tree, startTree, tokens)
    return tree


def listToTree(lst, operator):
    def listToTree_(lst):
        if lst == []:
            return lst
        else:
            halfLen = len(lst)//2
            lst1 = lst[:halfLen]
            lst2 = lst[halfLen:]
            lstTrees = []
            for a, b in zip(lst1, lst2):
                newTree = Tree(operator)
                newTree.a = a
                newTree.b = b
                lstTrees.append(newTree)
            return lstTrees

    if lst == []:
        return tree
    elif len(lst) == 1:
        return head(lst)
    else:
        lstTrees = []
        if len(lst) % 2 == 1:
            lstTrees.append(head(lst)) 
            newLst = tail(lst)
            lstReturn = lstTrees + listToTree_(newLst) 
            return listToTree(lstReturn, operator)
        else:
            lstReturn = listToTree_(lst) 
            return listToTree(lstReturn, operator)
        
def powerAdd(n, tree, tokens):
    listOfMuls = [ tree for i in range(n)]

    return listToTree(listOfMuls, tokens.mul)

def powerMul(n, tree, tokens):
    a = tree.a
    b = tree.b
    listOfMulsA = [a for i in range(n)] 
    listOfMulsB = [b for i in range(n)] 
    listOfMuls = listOfMulsA + listOfMulsB
    return listToTree(listOfMuls, tokens.mul)

def justPower(n, tree):
    outLst = [tree for i in range(n)] 
    print(outLst)
    newLst =  listToTree(outLst, tokens.mul)
    printTree(newLst)
    return newLst 

def equal(treeA, treeB):
    if treeA == None or treeB == None:
        return True

    if treeA.node == treeB.node:
        return (equal(treeA.a, treeB.a) and equal(treeA.b, treeB.b) or equal(treeA.a, treeB.b) and equal(treeA.b, treeB.a) ) 
    else:
        return False

def calculate(tree, tokens):
    if tree.a == None or tree.b == None:
        return tree
    a = tree.a
    b = tree.b
    if isDigit(a.node) and isDigit(b.node):
       num_a = int(a.node) 
       num_b = int(b.node) 
       operation = tree.node
       if operation == tokens.add:
           return Tree(str(num_a + num_b))
       elif operation == tokens.mul:
           return Tree(str(num_a * num_b))

    else:
        newTree = Tree(tree.node)
        newTree.a = calculate(tree.a, tokens) 
        newTree.b = calculate(tree.b, tokens) 
        if equal(newTree, tree):
            return newTree
        else:
            return calculate(newTree, tokens) 

def binTreeConvert(tree, lastNode, buff):
    if tree.a == tree.b == None:
        #  if tree.node == lastNode:
            #  return [[tree.node]]
        #  else:
        return [tree.node]
    if tree.node != lastNode:
        return [buff + binTreeConvert(tree.a, tree.node, []) + binTreeConvert(tree.b, tree.node, [])]
    else:
        #  buff += (binTreeConvert(tree.a, lastNode, []))
        #  buff += (binTreeConvert(tree.b, lastNode, []))
        buff += (binTreeConvert(tree.a, lastNode, []))
        buff += (binTreeConvert(tree.b, lastNode, []))
        return buff 





def isConst(v):
    if isDigit(v):
        return True 
    else:
        return False 

def count(lst, v):
    return sum([1 for el in lst if el == v])

def list2struct(lst):
    def _toStruct(lst, buff):
        if lst == []:
            return buff
        x = head(lst)
        if isConst(x):
            buff.append(Val(x))
            return _toStruct(tail(lst), buff)
        else:
            x_count = count(lst, x)
            lstNew = list(filter(lambda y: y != x, lst))
            buff.append(Var(x, x_count))
            return _toStruct(lstNew, buff)
    def constsMul(lst, valsL, varsS):
        if lst == []:
            product = 1
            for c in valsL:
                product *= c.valInt()
            return (Val(product), varsS) 

        x = head(lst)
        xs = tail(lst)
        if x.isConst():
            valsL.append(x)
            return constsMul(xs, valsL, varsS)
        else:
            varsS.append(x)
            return constsMul(xs, valsL, varsS) 

    structList = []
    for expr in lst:
        structList.append(_toStruct(expr, []))
    structListOut = [constsMul(expr, [], []) for expr in structList]
    return structListOut 

def toSetVar(lst):
    listGen = [el.var for el in lst]
    return set(listGen)

def toSetVal(lst):
    listGen = [el.val for el in lst]
    return set(listGen)


def equalList(lst1, lst2):
    if len(lst1) == len(lst2):
        #  return set(lst1) == set(lst2)
        return all([el in lst2 for el in lst1]) and all([el in lst1 for el in lst2])
    else:
        return False

def toStandart(lstStruct):

    def printLol__(stdStruct):
        for (c, v) in stdStruct:
            print(str(c), " ", " ".join([str(el) for el in v]))

    stdStruct = []
    for (const, varsS) in lstStruct:
        if stdStruct == []:
            stdStruct.append((const, varsS))
        else:
            flag = False
            for (constStd, varsStd) in stdStruct:
                #  print("was 1 ", [str(v) for v in varsStd])
                #  print("is 1 ", [str(v) for v in varsS])
                if equalList(varsStd, varsS):
                    flag = True
                    #  print("was ", [str(v) for v in varsStd])
                    #  print("is ", [str(v) for v in varsS])
                    stdStruct.remove((constStd, varsStd))
                    stdStruct.append((Val(constStd.val + const.val), varsS))
                    break

            if not flag:
                stdStruct.append((Val(const.val), varsS))

            #  print("-------------")
            #  printLol__(stdStruct)
            #  print("-------------")
    return stdStruct


def outputStruct(struct):
    #  print(len(struct))
    strPrint = [] 
    for (const, st) in struct:
        if const.val == 1 and st != []:
            output = ""
        else:
            output = str(const)
        for el in st:
            output += ' ' + str(el)
    
        strPrint.append(output)
    return (' + '.join(strPrint))


def process(inpStr, tokens, isPrint = False):
    n = len(inpStr)
    s1 = parse(filterSpaces(inpStr))
    if isPrint:
        printTree(s1)
    printTree(s1)
    for i in range(n):
        s1 = check(s1, s1, tokens)
    for i in range(n):
        s1 = calculate(s1, tokens)

    printTree(s1)
    if isPrint:
        printTree(s1)
    preMuls = binTreeConvert(s1, s1.node, [])
    muls = []
    for el in preMuls:
        if isinstance(el, list):
            muls.append(el) 
        else:
            muls.append([el])
    print(muls)
    lstStruct = list2struct(muls)
    #  print(lstStruct)
    std = toStandart(lstStruct)
    if isPrint:
        print(outputStruct(std))
    return std

def compare(s1_, s2_, prnt = False):
    print(s1_)
    print(s2_)
    std1 = process(s1_, tokens, prnt)
    std2 = process(s2_, tokens, prnt)
    
    str1 = outputStruct(std1)
    str2 = outputStruct(std2)
    print(str1)
    delimer = ''
    if equalList(std1, std2):
        delimer = '='
    else:
        delimer = '!='
    return ('{} {} {}\n'.format(str1, delimer, str2))

#  "add(0, -1)"
v0 = 'add(add(mul(5, a), mul(mul(-1, 7), b)), mul(-1, add( mul(7, a) , mul(-1, mul(5, b)) )))'
#  v0 = 'add(mul(1, -1), x)'
s0 = 'add(y, x)'

v1 = 'add(add(mul(11, mul(a, a)) , mul(7, a)) , add(mul(9, mul(a, a)), mul(-1, mul(5, a) )) )'
s1 = 'add(add(a, 1), add(b, 2))'

v2 = 'add(add(mul(x, mul(x, x)), mul(mul(3, x), mul(x, y))), add(mul(mul(3, y), mul(y, x)), mul(y, mul(y, y))))'
s2 = 'pow(3, add(x, y))'

v3 = 'add(mul(add(x, y), add(y, x)), mul(add(x, y), add(z, x)))' 
v33 = 'add(mul(a, mul(b, c)), add(mul(e, mul(f, g)), mul(k, mul(m, l))))' 
s3 = 'add(mul(add(x, y), add(y, x)), mul(add(x, y), add(z, x)))' 

v4 = 'add(mul(mul(y, x), add(x, y)), mul(pow(2, add(2, y)), mul(2, x)))' 
s4 = 'add(mul(mul(y, x), add(x, y)), mul(pow(2, add(2, y)), mul(2, x)))' 

v5 = 'pow(2, add(x, y))'
s5 = 'add(mul(x,x),add(mul(2,mul(y,x)),mul(y, y)))'


compareLst = [(v0, s0),(v1, s1),(v2, s2),(v3, s3), (v4, s4), (v5, s5)]
with open('output.ms', 'w') as output:
    for inp in compareLst:
        output.write('.EQ\n')
        output.write(compare(inp[0], inp[1]))
        output.write('.EN\n\n')

os.system("eqn output.ms -Tpdf | groff -ms -Tpdf > output.pdf")
