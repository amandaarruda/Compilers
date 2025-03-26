grammar Arithmetic;

// Regras do Parser
program     : statement+ EOF ;
statement   : assignment | expr ;
assignment  : VAR ASSIGN expr ;

expr        : term ((PLUS | MINUS) term)* ;
term        : factor ((MUL | DIV) factor)* ;
factor      : INT
            | VAR
            | LPAREN expr RPAREN ;

// Regras do Lexer
PLUS    : '+' ;
MINUS   : '-' ;
MUL     : '*' ;
DIV     : '/' ;
ASSIGN  : '=' ;
INT     : [0-9]+ ;
VAR     : [a-zA-Z]+ ;
LPAREN  : '(' ;
RPAREN  : ')' ;
WS      : [ \t\r\n]+ -> skip ;
