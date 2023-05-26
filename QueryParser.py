from QueryLexer import tokenize
import abc

class Expr(abc.ABC):
    pass

def parseQuery(queryText):
    pass

testString = '$x $y (Smoker(x) & Friend(x, y)) | @x1 @y1 @x2 @y2 (S(x1, y2) | R(y1) | S(x2, y2) | T(y2))'
testString2 = "$variable Smoker(variable) & Friend(x, 'Bob the Really Cool Guy Next Door')"
print(tokenize(testString2))
