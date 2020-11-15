# Ethan Trott
# Professor Dufour
# COS 301
# Project 1

import re
import sys

# True - loads tests from testFiles
# False - prompts for one InputString in console
loadFromTestFiles = True

# files at each path contain test strings separated by new line characters
testFiles = ["ShouldWork.txt", "ShouldNotWork.txt", "additionaltests.txt"]


# global vars
inputString = ""    #stores string left to be parsed
nextToken = ""      #stores last token read in lex()


# Parser Code

def lex():
    # POST: - gets simple lexemes (terminals, signs, operators, variables, constants, and progname)
    #       - stores first lexeme in nextToken and removes from InputString

    global inputString
    global nextToken

    # list of terminals
    termList = ['program', 'if', 'then', 'else', 'while', 'do', 'begin', 'end', ':=', 'read', 'write', '(', ')', ';', ',']

    # catch empty string and returns, leaving empty nextToken
    if (inputString == '' or not inputString):
        nextToken = ""
        return

    # catches any one-word terminal and stores in nextToken
    # this is separate from variable/progname detection to account for non-alphanumeric terminals
    p = re.compile('([^ ]*) ')
    m = p.match(inputString)
    if (m != None):
        if (m.group(1) in termList):
            nextToken = m.group(1)
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    # catches either multiplying_operator and stores in nextToken
    p = re.compile('([\*/]) ')
    m = p.match(inputString)
    if (m != None):
        nextToken = '<multiplying_operator>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    # catches adding_operator or sign and stores in nextToken
    # <multiplying_operator> ::= * | / 
    p = re.compile('([+-]) ')
    m = p.match(inputString)
    if (m != None):
        # nextToken here refers to the token stored before this
        # if this follows a variable, constant, or expression, this is an operator
        if (nextToken == '<variable>' or nextToken == '<constant>' or nextToken == ')'):
            nextToken = '<adding_operator>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return
        #otherwise it's a sign
        else:
            nextToken = '<sign>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    # catches any relational_operator and stores in nextToken
    # <relational_operator> ::= = | <> | < | <= | >= | > 
    p = re.compile('([<>=]) ')
    m = p.match(inputString)
    if (m != None):
        nextToken = '<relational_operator>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return
    p = re.compile('([<>][=>]) ')
    m = p.match(inputString)
    if (m != None):
        if (m.group(1) != '>>'):
            nextToken = '<relational_operator>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    # catches any variable or progname and stores in nextToken
    # <variable> ::= <letter> { <letter> | <digit> } 
    # <progname> ::= <capital_letter> { <letter> | <digit> } 
    p = re.compile('([A-Za-z]\w*) ')
    m = p.match(inputString)
    if (m != None):
        p2 = re.compile('([A-Z]\w*) ')
        m2 = p2.match(inputString)

        #if it starts capital and comes after 'program', safe to assume its progname
        if (m2 != None and nextToken == 'program'):
            nextToken = '<progname>'
            inputString = inputString.replace(m2.group(1) + " ", "", 1)
            return

        #otherwise it's a variable  
        else:
            nextToken = '<variable>'
            inputString = inputString.replace(m.group(1) + " ", "", 1)
            return

    # catches constants and stores in nextToken
    # <constant> ::= <digit> { <digit> } 
    p = re.compile('([1-9]\d*) ')
    m = p.match(inputString)
    if ((m != None) or (inputString[0] == '0')):
        nextToken = '<constant>'
        inputString = inputString.replace(m.group(1) + " ", "", 1)
        return

    # if we've made it here without returning, this token is not valid.
    print("Unknown symbol encountered")
    print("InputString: " + inputString + " || nextToken: " + nextToken)
    sys.exit(1)

# <program> ::= program <progname> <compound stmt> 
def program():
    global inputString
    global nextToken

    #get next lexeme
    lex()

    #if it's "program"...
    if (nextToken == 'program'):
        #get next lexeme
        lex()

        #if it's a valid progname...
        if (nextToken == '<progname>'):
            lex()
            # leave the rest to compound_stmt() to see if the rest is valid
            compound_stmt()
            return
        else:
            print("Expected a program name; got " + nextToken)
            sys.exit(1)
    else:
        print("Expected 'program'; got " + nextToken)
        sys.exit(1)

# <compound stmt> ::= begin <stmt> {; <stmt>} end
def compound_stmt():
    #PRE: lex() should be consumed
    #POST: does not consume lex()

    global inputString
    global nextToken
    
    #check for valid begin
    if (nextToken == 'begin'):
        #get first (necessary) statement
        stmt()

        #get any additional statements
        while (nextToken == ';'):
            stmt()

        #check for valid end
        if (nextToken == 'end'):
            lex()
            return
        else:
            print("Error: Compound Statement does not end with 'end'. Instead ends with: "+nextToken)
            sys.exit(1)
    else:
        print("Error: Expected Compound Statement 'begin', got: ",nextToken)
        sys.exit(1)

# <stmt> ::= <simple stmt> | <structured stmt> 
def stmt():
    # PRE: lex() should not be consumed
    # POST: consumes lex()

    global inputString
    global nextToken

    lex()
    # if the first token in the statement is read, write, or a variable, it's a simple statement
    if (nextToken == 'read' or nextToken == 'write' or nextToken == '<variable>'):
        simple_stmt()
        return

    # if the first token in the statement is if, while, or a begin, it's a structured statement
    elif (nextToken == 'if' or nextToken == 'while' or nextToken == 'begin'):
        structured_stmt()
        return

    # if it's none of the above, it's an invalid statement
    else:
        print("Error: Expected statement start, got ", nextToken)
        sys.exit(1)

# <simple stmt> ::= <assignment stmt> | <read stmt> | <write stmt> 
def simple_stmt():
    #PRE: expects lex() consumed
    #POST: consumes lex()

    global inputString
    global nextToken

    #assignment statement
    if (nextToken == '<variable>'):
        assignment_stmt()
        return
    
    #read statement
    elif (nextToken == 'read'):
        read_stmt()
        return

    #write statement
    elif (nextToken == 'write'):
        write_stmt()
        return
    
    #this should never happen with our parser, but I put it here anyway :)
    else:
        print("Error: Expected simple statement start, got ", nextToken)
        sys.exit(1)

# <assignment stmt> ::= <variable> := <expression> 
def assignment_stmt():
    #PRE: expects lex() consumed
    #POST: consumes lex()

    global inputString
    global nextToken

    # make sure we're assigning to a variable
    if (nextToken == '<variable>'):
        lex()
        # make sure assignment operator is included
        if (nextToken == ':='):
            # leave the rest to expression()
            expression()
            return
        else:
            print("Error: Variable not followed by assignment operator in assignment stmt, got ", nextToken)
            sys.exit(1)
    else:
        print("Error: Assignment statement must start with a variable, got ", nextToken)
        sys.exit(1)

    return

# <read stmt> ::= read ( <variable> { , <variable> } ) 
def read_stmt():
    #PRE: expects lex() consumed
    #POST: consumes lex()

    if (nextToken == 'read'):
        lex()
        if (nextToken == '('):
            lex()
            if (nextToken == '<variable>'):
                lex()

                #get any additional variables entered
                while (nextToken == ','):
                    lex()
                    if (nextToken == '<variable>'):
                        lex()
                    else:
                        print("Error: Expected <variable> inside read statement after ',', got ", nextToken)
                        sys.exit(1)

                if (nextToken == ')'):
                    lex()
                    return
                else:
                    print("Error: Expected ')' to conclude read statement or ',' to continue, got ", nextToken)
                    sys.exit(1)
            else:
                print("Error: Expected <variable> inside read statement, got ", nextToken)
                sys.exit(1)
        else:
            print("Error: Expected '(' after 'read', got ", nextToken)
            sys.exit(1)
    
    #this shouldn't be possible with this parser, but puting here anyway..
    else:
        print("Expected 'read' to start read statement, got ", nextToken)
        sys.exit(1)

# <write stmt> ::= write ( <expression> { , <expression> } ) 
def write_stmt():
    #PRE: expects lex() consumed
    #POST: consumes lex()

    if (nextToken == 'write'):
        lex()
        if (nextToken == '('):
            #expects expression next
            expression()

            #get any additional expressions
            while (nextToken == ','):
                expression()

            if (nextToken == ')'):
                lex()
                return
            else:
                print("Error: Expected ')' to conclude write statement or ',' to continue, got ", nextToken)
                sys.exit(1)
        else:
            print("Error: Expected '(' after 'write', got ", nextToken)
            sys.exit(1)
    
    #this shouldn't be possible with this parser, but puting here anyway..
    else:
        print("Expected 'write' to start write statement, got ", nextToken)
        sys.exit(1)

# <structured stmt> ::= <compound stmt> | <if stmt> | <while stmt>
def structured_stmt():
    #PRE: expects lex() consumed
    #POST: does not consume lex()

    global inputString
    global nextToken

    #compound statement
    if (nextToken == 'begin'):
        compound_stmt()
        return

    #if statement
    elif (nextToken == 'if'):
        if_stmt()
        return

    #while statement
    elif (nextToken == 'while'):
        while_stmt()
        return

    #this should never happen with our parser, but I put it here anyway :)
    else:
        print("Error: Expected structured statement start, got ", nextToken)
        sys.exit(1)

# <if stmt> ::= if <expression> then <stmt> | if <expression> then <stmt> else <stmt>
def if_stmt():
    #PRE: lex() should be consumed
    #POST: consumes lex()

    if (nextToken == 'if'):
        expression()                # checks if expression is valid
        if (nextToken == 'then'):
            stmt()                  # checks if statement is valid

            #else is optional
            if (nextToken == 'else'):
                stmt()              # checks if statement is valid
        else:
            print("Error: Expected 'then' after <expression> in <if statement>, got", nextToken)
            sys.exit(1)
    else:
        print("Error: Expected 'if', got ", nextToken)
        sys.exit(1)

# <while stmt> ::= while <expression> do <stmt>
def while_stmt():
    #PRE: lex() should be consumed
    #POST: consumes lex()

    if (nextToken == 'while'):
        expression()                # checks if expression is valid
        if (nextToken == 'do'):
            stmt()                  # checks if statement is valid
        else:
            print("Error: Expected 'do' inside <while stament>, got ", nextToken)
            sys.exit(1)
    else:
        print("Error: Expected 'while', got ", nextToken)
        sys.exit(1)

# <expression> ::= <simple expr> | <simple expr> <relational_operator> <simple expr> 
def expression():
    #PRE: lex() should not be consumed
    #POST: consumes lex()

    simple_expr()           # checks if simple_expr is valid

    #if there's a relational operator, expect another simple_expr
    if (nextToken == '<relational_operator>'):
        simple_expr()       # checks if simple_expr is valid

    return

# <simple expr> ::= [ <sign> ] <term> { <adding_operator> <term> } 
def simple_expr():
    #PRE: does not expect lex() consumed
    #POST: consumes lex()

    #consume optional sign if exists
    lex()
    if (nextToken == '<sign>'):
        lex()
    
    #verify first term
    term()

    #verify any added terms
    while (nextToken == '<adding_operator>'):
        lex()
        term()

    return

# <term> ::= <factor> { <multiplying_operator> <factor> } 
def term():
    #PRE: expects lex() to be consumed
    #POST: consumes lex()

    #verify first factor
    factor()

    #verify any multiplied factors
    while (nextToken == '<multiplying_operator>'):
        lex()
        factor()
    
    return

# <factor> ::= <variable> | <constant> | ( <expression> ) 
def factor():
    #PRE: expects lex() to be consumed
    #POST: consumes lex()

    # variable is a valid factor
    if (nextToken == '<variable>'):
        lex()
        return

    # constant is a valid factor
    elif (nextToken == '<constant>'):
        lex()
        return

    # expression surrounded by parenthesis is a valid factor
    elif (nextToken == '('):
        expression()                # checks if expression is valid
        if (nextToken == ')'):
            lex()
            return
        else:
            print("Error: Expected ')' after expression in factor. Instead got ", nextToken)
            sys.exit(1)
    else:
        print("Error: Expected factor, got ", nextToken)
        sys.exit(1)


# Running and Testing

# loads tests from file at filePath
def testFromFile(filePath):
    global inputString

    print("\n** Testing from "+filePath+" **")

    # open file and get tests (separated by line)
    testFile = open(filePath, 'r') 
    tests = testFile.readlines() 
    
    count = 1
    # for each test:
    for test in tests: 
        # remove any new line characters generated by file
        # note: this will break cases that rely on failure due to new line
        test = test.replace("\n","")
        test = test.replace("\r","")
        print("\nTest "+str(count)+": "+test)

        #store the test in inputString
        inputString = test

        # if we can run program() without failure, the statement is correct
        try:
            program()
            print("Result: Statement is syntactically correct :)")
        except:
            print("Result: Statement is NOT syntactically correct :(")
        
        count += 1

# if we don't want to load tests from file, default to CLI input
if not loadFromTestFiles:
    # get input
    inputString = input("Enter a string: ")
    # try program
    program()
    # if we get here, the statement is valid
    print("The string is syntactically correct! :)")

#otherwise load from files
else:
    for testFile in testFiles:
        testFromFile(testFile)