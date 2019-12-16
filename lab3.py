import re

buildIn = {'sum' : lambda a, b : a + b,
        'mul' : lambda a, b : a * b,
        'div' : lambda a, b : a / b}

class Memory:
    def __init__(self):
        self.m = {}
    def write(self, key, value):
        if key in self.m.keys():
            if any([ f == value for f in self.m[key]] ):
                pass
            else:
                self.m.[key].append(value)
        else:
            self.m[key] = [value]
    def read(self, key):
        if key in self.m.keys():
            return self.m[key]
        else:
            return None
    def delete(self, key):
        del(self.m[key])
    def __str__(self):
        return str(self.m)

class Stack:
    def __init__(self):
        self.s = []
    def push(self, val):
        self.s.append(val)
    def pop(self):
        return self.s.pop()

def isSymbolT(val):
    return (val[1] == 'symbol')

def isNumT(val):
    return (val[1] == 'num')

def number(val):
    try:
        a = (float(val)) 
        return True
    except:
        return False





class Def:
    def __init__(self, name, args, expr):
        if isSymbolT(name):
            self.name = name[0]
        else:
            error('Name of function {} is not a symbol'.format(name[0]))
        if all([isSymbolT(arg) for arg in args]):
            self.args = [arg[0] for arg in args]
        else:
            error('Some args of function {} is not a symbol'.format(name[0]))

        self.expr = expr

    def __str__(self):
        return "def {} ({}) = {}".format(self.name, ' '.join(self.args), ' '.join([ expr[0] for expr in self.expr]))
    def __repr__(self):
        return self.__str__() 

    def t(self):
        return "def"

    def toEval(self, args):
        if len(args) == len(self.args):
            evalNew = lexToEval(self.expr) 
            evalNew.args = args
            return evalNew
        else:
            error("Not correct count of arguments")

class Eval:
    def __init__(self, name, args):
        if isSymbolT(name):
            self.name = name[0]
        else:
            error('{} is not a symbol'.format(name[0]))

        if all([isSymbolT(arg) or isNumT(arg) for arg in args]):
            self.args = [arg[0] for arg in args]
        else:
            error('Some args of function {} is not a symbol or nums'.format(name[0]))

    def __str__(self):
        return "{} ({})".format(self.name, ' '.join(self.args))
    def __repr__(self):
        return self.__str__() 

    def t(self):
        return "eval"

    def exe(self):
        if all( number(arg) for arg in self.args):
            floatArgs = [float(arg) for arg in self.args]
            return (buildIn[self.name](*floatArgs))
        else:
            error("Args is not numbers")


class Const:
    def __init__(self, val):
        if isNumT(val):
            self.val = val[0]
        else:
            error('{} is not a number'.format(val[0]))

    def __str__(self):
        return "{}".format(self.val)
    def __repr__(self):
        return self.__str__() 

    def t(self):
        return "const"

#TODO: rewrite to new system with pattern matching

class Process:
    def __init__(self, main = 'main'):
        self.mem = Memory()
        self.now = None
        self.main = main 

    def addDef(self, func):
        name = func.name
        if self.mem.read(name) == None:
            self.mem.write(name, func)
        else:
            error('{} was defined before'.format(name))
    def run(self):
        if self.now == None:
            if self.mem.read(self.main) != None:
                self.now = lexToEval(self.mem.read(self.main).expr)
                return self.next(self.now)
            else:
                error('Main function is not implemented')

    def next(self, expr):
        if self.mem.read(expr.name) != None:
            f = self.mem.read(expr.name)        
            newExpr = f.toEval(expr.args)
            return self.next(newExpr)
        else:
            #  expr.args = [self.next(arg) for arg in self.args]
            if all( number(arg) for arg in expr.args):
                return str(expr.exe())
            else:
                return expr






def splitBy(lst, splitter):
    acc = []
    accLocal = []
    for el in lst:
        if el == splitter:
            acc.append(accLocal)
            accLocal = []
        else:
            accLocal.append(el)
    if accLocal != []:
        acc.append(accLocal)

    return acc

def splitTupleBy(lst, splitter):
    a = []
    b = []
    toA = True
    for el in lst:
        if el == splitter:
            toA = False
        elif toA:
            a.append(el)
        else:
            b.append(el)

    return (a, b) 



def error(msg):
    raise Exception(msg)

def match(pattern, string):
    p = re.compile(pattern)
    matched = p.match(string)
    if matched:
        stringMatch = matched.group() 
        stringNew   = string[matched.end():]
        return (stringMatch, stringNew)
    else:
        #  return error("cant match correct")
        return None

applyT = ("=", "apply")
beginT = ("\(", "begin")
endT = ("\)", "end")
newlineT = ("\\n", "newline" )

expressions = [("[a-zA-Z]+[0-9]*'*", "symbol"), ("-*[0-9]+", "num"), ('".*"', "string"), applyT, beginT, endT, newlineT, ("\s+", "space") ]


def cycleLex(string, lexs):
    if string == "":
        filteredSpaces = [lex for lex in lexs if lex[1] != 'space']
        return filteredSpaces 
    else:
        for (pattern, lexem) in expressions:
            m = match(pattern, string)
            if m:
                strMatch, strNew = m
                lexs.append((strMatch, lexem))
                return cycleLex(strNew, lexs) 

def define(lstOfLex):
    acc = []
    returnList = []
    bracketsCounter = 0
    for lex in lstOfLex:
        if lex[1] == 'newline':
            continue
        elif lex[1] == 'begin':
            bracketsCounter += 1
        elif lex[1] == 'end' and bracketsCounter > 0:
            bracketsCounter -= 1 
        elif lex[1] == 'end' and bracketsCounter <= 0:
            error("Brackets error")

        acc.append(lex)

        if bracketsCounter == 0:
            newAcc = acc[1:-1]
            if newAcc[0][0] == 'def':
                name_args, block = splitTupleBy(newAcc[1:], applyT)
                returnList.append(Def(name_args[0], name_args[1:], block) )
                acc = []
            else:
                name, block = splitTupleBy(newAcc, applyT)
                returnList.append(Eval(name[0], block) )
                acc = []

    
    return returnList

def lexToEval(lstOfLex):
    acc = []
    bracketsCounter = 0
    for lex in lstOfLex:
        if lex[1] == 'newline':
            continue
        elif lex[1] == 'begin':
            bracketsCounter += 1
        elif lex[1] == 'end' and bracketsCounter > 0:
            bracketsCounter -= 1 
        elif lex[1] == 'end' and bracketsCounter <= 0:
            error("Brackets error")
        
        acc.append(lex)

        if bracketsCounter == 0:
            newAcc = acc[1:-1]
            print(newAcc)
            if isNumT(newAcc[0]) and len(newAcc) == 1:
                return Const(newAcc[0])
            else:
                return Eval(newAcc[0], newAcc[1:])

    




Bool = {"True" : 0, "False" : 1}
#  print([match(pattern, "function = 1") for (pattern, v) in expressions])
program = open("program", "r")
#  print(program.read())
lex = cycleLex(program.read(), [])
d = define(lex)

P = Process()
for f in d:
    P.addDef(f)

print(P.run())






