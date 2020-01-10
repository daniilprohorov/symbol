import re
from utils import splitBlocks, error 

def match(pattern, string):
    p = re.compile(pattern)
    matched = p.match(string)
    if matched:
        stringMatch = matched.group() 
        stringNew   = string[matched.end():]
        return (stringMatch, stringNew)
    else:
        return None

def isMatch(pattern, value):
    m = match(pattern, value)
    if m == None:
        return False
    elif m[0] == value:
        return True
    else:
        return False

def isConst(value):
    patternInt = "-?[0-9]+"
    patternBool = "(?:True|False)"
    if isMatch(patternInt, value) or isMatch(patternBool, value):
        return True
    else:
        return False

def isExpression(value):
    patternBrackets = "\(.*\)"
    patternSymbol = "[a-zA-Z]+[0-9]*'*"
    #check brackets
    if isMatch(patternBrackets, value):
        return isExpression(value[1:-1])
    else:
        splitted = splitBlocks(value, ' ')
        splitted = [''.join(el) for el in splitted]
        if isMatch(patternSymbol, splitted[0]):
            result = all([isExpression(el) or isConst(el) for el in splitted[1:]])
            return result
        else:
            return False

def getType(value):
    if isConst(value):
        return "Const"
    elif isExpression(value):
        return "Expr"
    else:
        error("Cant match type")

def isSymbolT(val):
    return (val[1] == 'symbol')

def isConstT(val):
    return (isConst(val[0]))

