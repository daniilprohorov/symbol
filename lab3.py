import re
from utils import splitBy, splitTupleBy, splitBlocks, error 
from checker import match, isMatch, isExpression, isConst, isSymbolT, isConstT, getType

buildIn = {'sum' : lambda a, b : a + b,
        'mul' : lambda a, b : a * b,
        'div' : lambda a, b : a / b}

# data types : const, expr 
# const: Bool, Int 
# expr: f a b


        
class Memory:
    def __init__(self):
        self.m = {}
    def write(self, key, func):
        if key in self.m.keys():
            if any([ f == func for f in self.m[key]] ):
                pass
            else:
                self.m[key].append(func)
        else:
            self.m[key] = tuple([func])
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


def number(val):
    try:
        a = (float(val)) 
        return True
    except:
        return False

class Func:
    def __init__(self, args, expr):
        self.args = args
        self.expr = expr
    def __str__(self):
        return "({}) = {}".format(list(self.args), list(self.expr))
    def __repr__(self):
        return self.__str__() 

class Def:
    def __init__(self, name, argsTypes, outType):
        if isSymbolT(name):
            self.name = name[0]
        else:
            error('Name of function {} is not a symbol'.format(name[0]))
        self.argsTypes = [t[0] for t in argsTypes] 
        self.outType = outType[0]
        self.funcs = []

    def addFunc(self, args, out):
        print(out)
        if [getType(el) for el in args] == self.argsTypes and getType(out) == self.outType[0]:
            self.funcs.append(Func(zip(args, self.argsTypes), zip(out, self.outType)))
        else:
            error("Type matching in function")

    def __str__(self):
        return "def {} {}".format(self.name, (self.funcs))
    def __repr__(self):
        return self.__str__() 
#
#    def t(self):
#        return "def"
#
#    def toEval(self, args):
#        if len(args) == len(self.args):
#            evalNew = lexToEval(self.expr) 
#            evalNew.args = args
#            return evalNew
#        else:
#            error("Not correct count of arguments")

class Eval:
    def __init__(self, name, args):
        if isSymbolT(name):
            self.name = name[0]
        else:
            error('{} is not a symbol'.format(name[0]))

        if all([isSymbolT(arg) or isConstT(arg) for arg in args]):
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
        if isConstT(val):
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
                name = name_args[0][0]
                args = [el[0] for el in name_args[1:]]
                for defs in returnList:
                    if defs.name == name:
                        print(block)
                        defs.addFunc(args, ' '.join([b[0] for b in block[1:-1]]))
                acc = []
            elif newAcc[0][0] == 'typ':
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
            if isConstT(newAcc[0]) and len(newAcc) == 1:
                return Const(newAcc[0])
            else:
                return Eval(newAcc[0], newAcc[1:])

    




Bool = {"True" : 0, "False" : 1}
#  print([match(pattern, "function = 1") for (pattern, v) in expressions])
program = open("program", "r")
#  print(program.read())
lex = cycleLex(program.read(), [])
d = define(lex)
print(d)

#P = Process()
#for f in d:
#    P.addDef(f)

#print(P.run())

#print(isConst("-1"))
#print(isConst("100"))
#print(isConst("---"))
#print(isConst("-999"))
#print(isConst("998987asdf99"))
#print(isConst("99898abasd799f"))

#print(isConst("True"))
#print(isConst("234True"))
#print(isConst("asdlTrasdfue"))
#print(isConst("False"))
#print(isConst("lol"))

#print(isExpression("asdfsadf"))
#print(isExpression("(func (mul a b))"))
#print(isExpression("func (mul a b) (b c d)"))
#print(isExpression("1 (mul a b) (b c d)"))
#print(isExpression("a"))






