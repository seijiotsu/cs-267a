from QueryLexer import tokenize, TokenType
from Expression import *
from PrettyPrintVisitor import PrettyPrintVisitor
from LispifyVisitor import LispifyVisitor

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currTokenIdx = 0

    def isDone(self):
        return self.peekToken().type == TokenType.EOF
    
    def peekToken(self):
        return self.tokens[self.currTokenIdx]

    def nextToken(self):
        if not self.isDone():
            self.currTokenIdx += 1
        return self.previousToken()

    def previousToken(self):
        return self.tokens[self.currTokenIdx - 1]     

    def checkType(self, tokenType):
        return self.peekToken().type == tokenType
    
    def matchAnyOf(self, *tokenTypes):
        for tokenType in tokenTypes:
            if self.checkType(tokenType):
                token = self.nextToken()
                return token
        return None
        
    def expect(self, tokenType):
        if self.checkType(tokenType):
            return self.nextToken()
        raise SyntaxError(f'Expected {tokenType} but got {self.peekToken().type} instead')
    
    def entry(self):
        sentence = self.sentence()
        self.expect(TokenType.EOF)
        return Entry(sentence)
    
    def sentence(self):
        orClause = self.orClause()
        return Sentence(orClause)
    
    def orClause(self):
        andClauses = [self.andClause()]
        while self.matchAnyOf(TokenType.VERTICAL_BAR, TokenType.LOGICAL_OR):
            andClause = self.andClause()
            andClauses.append(andClause)
        return OrClause(andClauses)
    
    def andClause(self):
        clauses = [self.clause()]
        while self.matchAnyOf(TokenType.AMPERSAND, TokenType.LOGICAL_AND):
            clause = self.clause()
            clauses.append(clause)
        return AndClause(clauses)
    
    def clause(self):
        if self.matchAnyOf(TokenType.OCTOTHORPE, TokenType.EXISTS):
            identifier = self.expect(TokenType.IDENTIFIER)
            clause = self.clause()
            return ExistsClause(identifier, clause)
        elif self.matchAnyOf(TokenType.AT_SIGN, TokenType.FORALL):
            identifier = self.expect(TokenType.IDENTIFIER)
            clause = self.clause()
            return ForallClause(identifier, clause)
        elif self.matchAnyOf(TokenType.TILDE, TokenType.LOGICAL_NOT):
            clause = self.clause()
            return NotClause(clause)
        elif self.matchAnyOf(TokenType.L_PAREN):
            sentence = self.sentence()
            self.expect(TokenType.R_PAREN)
            return NestedSentence(sentence)
        else:
            atom = self.atom()
            return AtomClause(atom)

    def atom(self):
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.L_BRAC)
        arguments = [self.argument()]
        while self.matchAnyOf(TokenType.COMMA):
            argument = self.argument()
            arguments.append(argument)
        self.expect(TokenType.R_BRAC)
        return Atom(identifier, arguments)
    
    def argument(self):
        if token := self.matchAnyOf(TokenType.STRING):
            return StringArgument(token.literal)
        elif token := self.matchAnyOf(TokenType.IDENTIFIER):
            return VariableArgument(token.value)
        raise SyntaxError('Invalid argument during parsing')


def parseQuery(queryText):
    tokens = tokenize(queryText)
    parser = Parser(tokens)
    entry = parser.entry()
    return entry

testString = '∃x ∃y (Smoker[x] ∧ Friend[x, y]) ∨ ∀x1 ∀y1 ∀x2 ∀y2 (S[x1, y2] ∨ R[y1] ∨ S[x2, y2] ∨ T[y2])'
testString2 = "@a #variable Smoker[variable] & ~ @b Friend[x, 'Bob the Really Cool Guy Next Door']"
testString3 = "a[a] | b[b] | c[c] & d[d] | e[e] & Friend[f1, 'f2', 'f3'] & g[g]"
testString4 = "#x Friend[x]"
print(tokenize(testString3))
parsed = parseQuery(testString3)

print(LispifyVisitor().visitEntry(parsed))

