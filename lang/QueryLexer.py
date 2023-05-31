from enum import Enum, auto

class TokenType(Enum):
    L_PAREN = auto()
    R_PAREN = auto()
    L_BRAC = auto()
    R_BRAC = auto()
    COMMA = auto()
    AMPERSAND = auto()
    VERTICAL_BAR = auto()
    TILDE = auto()
    AT_SIGN = auto()
    OCTOTHORPE = auto()
    LOGICAL_OR = auto()
    LOGICAL_AND = auto()
    LOGICAL_NOT = auto()
    EXISTS = auto()
    FORALL = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    EOF = auto()

class Token:
    def __init__(self, tokenType, value, line, literal = None):
        self.type = tokenType
        self.value = value
        self.line = line
        self.literal = literal
    
    def __str__(self):
        if self.literal:
            return f'Token[{self.type}, {self.value}, {self.line}, {self.literal}]'
        return f'Token[{self.type}, {self.value}, {self.line}]'

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, input):
        self.input = input
        self.inputLength = len(input)
        self.output = []
        self.currentStart = 0
        self.cursor = 0
        self.currentLine = 0

    def isDone(self):
        return self.cursor >= self.inputLength
    
    def eat(self):
        nextChar = self.input[self.cursor]
        self.cursor += 1
        return nextChar
    
    def peek(self):
        if self.isDone():
            return None
        return self.input[self.cursor]
    
    def scanNext(self):
        currentChar = self.eat()
        match currentChar:
            case '(':
                self.output.append(Token(TokenType.L_PAREN, self.getCurrValue(), self.currentLine))
            case ')':
                self.output.append(Token(TokenType.R_PAREN, self.getCurrValue(), self.currentLine))
            case '[':
                self.output.append(Token(TokenType.L_BRAC, self.getCurrValue(), self.currentLine))
            case ']':
                self.output.append(Token(TokenType.R_BRAC, self.getCurrValue(), self.currentLine))
            case ',':
                self.output.append(Token(TokenType.COMMA, self.getCurrValue(), self.currentLine))
            case '&':
                self.output.append(Token(TokenType.AMPERSAND, self.getCurrValue(), self.currentLine))
            case '|':
                self.output.append(Token(TokenType.VERTICAL_BAR, self.getCurrValue(), self.currentLine))
            case '~':
                self.output.append(Token(TokenType.TILDE, self.getCurrValue(), self.currentLine))
            case '#':
                self.output.append(Token(TokenType.OCTOTHORPE, self.getCurrValue(), self.currentLine))
            case '@':
                self.output.append(Token(TokenType.AT_SIGN, self.getCurrValue(), self.currentLine))
            case '∨':
                self.output.append(Token(TokenType.LOGICAL_OR, self.getCurrValue(), self.currentLine))
            case '∧':
                self.output.append(Token(TokenType.LOGICAL_AND, self.getCurrValue(), self.currentLine))
            case '∃':
                self.output.append(Token(TokenType.EXISTS, self.getCurrValue(), self.currentLine))
            case '∀':
                self.output.append(Token(TokenType.FORALL, self.getCurrValue(), self.currentLine))
            case '¬':
                self.output.append(Token(TokenType.LOGICAL_NOT, self.getCurrValue(), self.currentLine))
            case '\n':
                self.currentLine += 1
            case ' ' | '\r' | '\t':
                pass
            case '\'':
                self.scanString()
            case _ if currentChar.isalnum():
                self.scanIdentifier()
            case _:
                raise Exception(f'Lexer encountered unexpected character "{currentChar}"')

    def scanString(self):
        while self.peek() != '\'' and not self.isDone():
            if self.peek() == '\n':
                self.currentLine += 1
            self.eat()
        if self.isDone():
            raise Exception('A string is missing a closing \'')
        self.eat()
        stringValue = self.input[self.currentStart : self.cursor]
        stringLiteral = self.input[self.currentStart + 1 : self.cursor - 1]
        self.output.append(Token(TokenType.STRING, stringValue, self.currentLine, stringLiteral))

    def scanIdentifier(self):
        while (not self.isDone() and self.isValidIdentifierChar(self.peek())):
            self.eat()
        identifierValue = self.input[self.currentStart : self.cursor]
        self.output.append(Token(TokenType.IDENTIFIER, identifierValue, self.currentLine))

    def isValidIdentifierChar(self, ch):
        return ch.isalnum() or ch == '-'

    def getCurrValue(self):
        return self.input[self.currentStart : self.cursor]
    
    def tokenize(self):
        while not self.isDone():
            self.currentStart = self.cursor
            self.scanNext()
        eofToken = Token(TokenType.EOF, '', self.currentLine)
        self.output.append(eofToken)
        return self.output

def tokenize(input):
    return Lexer(input).tokenize()