from pptree import *
""" operations
"0-9" - numbers
"a-z" - symbols
functions:
    sum(a, b)
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
    if xs == []:
        error('Can`t get last. Not enaught symbols')
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

def parseTest(inp, buf):
    if inp == []:
        return [] 
    else:
        x, xs = head(inp), tail(inp) 
        if x == '(':
            if last(xs) == ')':
                xsNew = untilLast(xs) 
                out = ''.join(buf)
                return (out, xsNew) 
            else:
                raise Exception('Brackets error')
        else:
            bufNew = buf + [x]
            return parseTest(xs, bufNew)


def parse(inpStr):
    if inpStr == []:
        error('kek')
    if hasBracket(inpStr):
        f, a, b = simpleParse(inpStr)
        print('a = ', a, ' b = ', b)
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


def printTree(tree, parent = None):
    if tree == None:
        return parent
    else:
        ast = Node(tree.node, parent)
        if tree.a != None:
            printTree(tree.a, ast)
        if tree.b != None:
            printTree(tree.b, ast)
        return ast
#  print(parseTest('123()', []))
#  print(parseTest('123(456(1, 2), 123)', []))
#  s = '123'
#  s1 = '123('
s2 = 'mul(sum(pow(1, sum(9, 10)), 2), 5)'
s3 = 'mul(sum(pow(1, sum(9, 10)), 2), sum(8, 9))'
s4 = 'mul(sum(kek, lol), 2)' 
#  s4 = '(123)()'
#  inp = [s2, s3]
#  output = [ parse(filterSpaces(el)) for el in inp]
#  lol = parse(s3)
lol2 = parse(filterSpaces(s3))
print_tree(printTree(lol2))




