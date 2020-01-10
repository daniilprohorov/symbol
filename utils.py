
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

def splitBlocks(value, splt):
    acc = []
    returnList = []
    bracketsCounter = 0
    for char in value:
        if char == '(':
            acc.append(char)
            bracketsCounter += 1
        elif char == ')' and bracketsCounter > 0:
            acc.append(char)
            bracketsCounter -= 1
        elif char == ')' and bracketsCounter <= 0:
            error("Brackets error")
        elif char == splt and bracketsCounter == 0:
            returnList.append(acc)
            acc = [] 
        else:
            acc.append(char)

    if acc != []:
        returnList.append(acc)

    return returnList



def error(msg):
    raise Exception(msg)
