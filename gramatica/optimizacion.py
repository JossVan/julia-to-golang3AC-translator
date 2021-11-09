import re
import sys
sys.setrecursionlimit(5000)


reservadas = {
    'package':'R_PAQUETES',
    'fmt' : 'R_FMT',
    'main' : 'R_MAIN',
    'import' : 'R_IMPORT',
    'var' :"R_VAR",
    'int':'R_INT',
    'float64': 'R_FLOAT',
    'int' : 'R_INT',
    'printf' : 'R_PRINTF',
    'if' : 'R_IF',
    'goto': 'R_GOTO',
    'func' : 'R_FUNCION',
    'math':'R_MATH',
    'mod': 'R_MOD',
    'return' : 'R_RETURN'
}

tokens  = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'COMA',
    'PUNTO',
    'DOSPUNTITOS',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_CORIZQ   = r'\['
t_CORDER   = r'\]'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_LLAVEIZQ  = r'\{'
t_LLAVEDER  = r'\}'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_MENORIGUAL= r'<='
t_MAYORIGUAL= r'>='
t_COMA      = r','
t_PUNTO     = r'\.'
t_DOSPUNTITOS = r'\:'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'\/\*(.|\n)*\*\/'
    t.lexer.lineno += t.value.count('\n')
# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\//.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
#t_ignore = " \r"
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_IGNORAR(t):
    r'\ |\t|\r'
    global columna
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()
lexer.lineno = 1

# Asociación de operadores y precedencia
precedence = (
    ('left', 'IGUALQUE', 'NIGUALQUE'),
    ('left', 'MENQUE','MAYQUE', 'MENORIGUAL','MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('right','UMENOS'),
    )

# Definición de la gramática

def p_inicio(t):
    '''INICIO :   R_PAQUETES R_MAIN PTCOMA IMPORTES PILA_HEAP PILA_STACK DECLARACIONES FUNCIONES'''
    t[0]= "OK"
def p_paquetitos(t):
    '''IMPORTES : R_IMPORT PARIZQ LISTAIMPORTES PARDER PTCOMA'''

def p_listaimportes(t):
    '''LISTAIMPORTES : LISTAIMPORTES LISTAIMPORTE'''
def p_listaimportes2(t):
    '''LISTAIMPORTES : LISTAIMPORTE'''
def p_listaimporte(t):
    '''LISTAIMPORTE : PTCOMA CADENA '''
def p_listaimporte2(t):
    '''LISTAIMPORTE : CADENA'''
def p_pilastack(t):
    '''PILA_HEAP : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA'''
    t[0] = t[1]
def p_pilaheap(t):
    ' PILA_STACK : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA'
def p_declaraciones(t):
    'DECLARACIONES : DECLARACIONES DECLARACION'
def p_declaraciones2(t):
    'DECLARACIONES : DECLARACION'

def p_declaracion(t):
    ' DECLARACION : R_VAR LISTAS R_FLOAT PTCOMA'

def p_listas(t):
    'LISTAS : LISTAS COMA LISTA'
def p_listas2(t):
    'LISTAS : LISTA'
def p_lista(t):
    'LISTA : ID'

def p_funciones(t):
    'FUNCIONES : FUNCIONES FUNCION'

def p_funciones2(t):
    'FUNCIONES : FUNCION'
def p_funcion(t):
    '''FUNCION : R_FUNCION ID PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER 
                | R_FUNCION R_MAIN PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER '''

def p_instrucciones(t):
    'INSTRUCCIONES : INSTRUCCIONES INSTRUCCION'

def p_instrucciones2(t):
    'INSTRUCCIONES : INSTRUCCION'

def p_instruccion(t):
    '''INSTRUCCION : INSTRUCCION ASIGNACION
                    | INSTRUCCION PRINTS
                    | INSTRUCCION ETIQUETAS
                    | INSTRUCCION SALTOS
                    | INSTRUCCION LLAMADAS
                    | INSTRUCCION IFS 
                    | INSTRUCCION RETURN'''

def p_instruccion2(t):
    '''INSTRUCCION : ASIGNACION
                    | PRINTS
                    | ETIQUETAS 
                    | SALTOS 
                    | LLAMADAS
                    | IFS
                    | RETURN'''

def p_return(t):
    'RETURN : R_RETURN PTCOMA'
def p_println(t):
    'PRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA E PARDER PTCOMA'
def p_println2(t):
    'PRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA R_INT PARIZQ E PARDER PARDER PTCOMA'

def p_etiquetas(t):
    'ETIQUETAS : ID DOSPUNTITOS'  

def p_saltos (t):
    'SALTOS : R_GOTO ID PTCOMA'
def p_asignacion(t):
    '''ASIGNACION : ID IGUAL E PTCOMA
                    | ARREGLOS IGUAL E PTCOMA'''
def p_expresiones(t):
    '''E : E MAS E
        | E MENOS E
        | E POR E
        | E DIVIDIDO E'''
def p_expresion_parentesis(t):
    'E : PARIZQ E PARDER'
def p_expresion_modal(t):
    'E : R_MATH PUNTO R_MOD PARIZQ E COMA E PARDER'
def p_expresion_unaria(t):
    'E : MENOS E %prec UMENOS'
def p_constantes(t):
    '''E : ID
        | DECIMAL
        | ENTERO
        | CADENA
        | ARREGLOS'''

def p_ifs(t):
    '''IFS : R_IF  RE LLAVEIZQ SALTOS LLAVEDER '''
def p_relacionales(t):
    ''' RE :  RE MENQUE RE
            | RE MAYQUE RE
            | RE IGUALQUE RE
            | RE NIGUALQUE RE
            | RE MENORIGUAL RE
            | RE MAYORIGUAL RE'''
def p_relacionales2(t):
    'RE : PARIZQ RE PARDER'
def p_relacioneales3(t):
    '''RE : E'''
def p_llamaditas(t):
    ' LLAMADAS : ID PARIZQ PARDER PTCOMA'     
def p_arreglos(t):
    'ARREGLOS : ID LISTASARREGLOS'
def p_listasarreglos(t):
    'LISTASARREGLOS : LISTASARREGLOS LISTAARREGLOS'
def p_listasarreglos2(t):
    'LISTASARREGLOS : LISTAARREGLOS'
def p_listaarreglos(t):
    '''LISTAARREGLOS : CORIZQ R_INT PARIZQ E PARDER CORDER'''
def p_listaarreglos2(t):
    '''LISTAARREGLOS : CORIZQ  E  CORDER'''

def p_error(t):
    print("Error sintáctico en '%s'" % str(t))

import ply.yacc as yacc
parser = yacc.yacc()

from TablaSimbolos.TablaSimbolos import TablaSimbolos
from TablaSimbolos.Arbolito import Arbolito
from Instrucciones.Funciones import Funciones
def parse(input) :
    global lexer
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    instrucciones=parser.parse(input)
    print(instrucciones)
    return instrucciones

    