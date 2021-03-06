# Parser for Faux Grammar
 Parser for a Faux Grammar - written in Python

This is fairly straight-forward to use.

'loadFromTestFiles = True' at the top of parser.py will enable loading tests from files  (False will use console input)
the List 'testFiles' contains paths to the files you'd like to test, you can add as many files there as you'd like

Currently these are configured to run my test cases (contained in ShouldWork.txt and ShouldNotWork.txt).

Once you have modified these options to your liking, run parser.py in Python 3.x

-Ethan

The Grammar: 
```<program> ::= program <progname> <compound stmt>
<compound stmt> ::= begin <stmt> {; <stmt>} end 
<stmt> ::= <simple stmt> | <structured stmt> 
<simple stmt> ::= <assignment stmt> | <read stmt> | <write stmt>
<assignment stmt> ::= <variable> := <expression>
<read stmt> ::= read ( <variable> { , <variable> } ) 
<write stmt> ::= write ( <expression> { , <expression> } )
<structured stmt> ::= <compound stmt> | <if stmt> | <while stmt>
<if stmt> ::= if <expression> then <stmt> | if <expression> then <stmt> else <stmt> 
<while stmt> ::= while <expression> do <stmt> <expression> ::= <simple expr> | <simple expr> <relational_operator> <simple expr> 
<simple expr> ::= [ <sign> ] <term> { <adding_operator> <term> } 
<term> ::= <factor> { <multiplying_operator> <factor> } 
<factor> ::= <variable> | <constant> | ( <expression> ) 
<sign> ::= + | - 
<adding_operator> ::= + | - 
<multiplying_operator> ::= * | / 
<relational_operator> ::= = | <> | < | <= | >= | > 
<variable> ::= <letter> { <letter> | <digit> }
<constant> ::= <digit> { <digit> } 
<progname> ::= <capital_letter> { <letter> | <digit> } 
<capital_letter> ::= A | B | C | ... | Z 
<letter> ::= a | b | c | ... | z | <capital_letter>
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ```
