import re
import sys
from Abstractas.Objeto import TipoObjeto
from optimizacion.Arreglo import Arreglo
from optimizacion.Codigo import Codigo
from optimizacion.Declaracion import Declaracion
from optimizacion.Encabezado import Encabezado
from optimizacion.General import General
from optimizacion.Llamada import Llamada
from optimizacion.Pila import Pila
from optimizacion.Print import Print
from optimizacion.Relacional import Relacional
from optimizacion.Return import Return
from optimizacion.Variable import Variable
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

from optimizacion.Aritmetica import Aritmetica
from optimizacion.Asignacion import Asignacion
from optimizacion.Etiqueta import Etiqueta
from optimizacion.Funcion import Funcion
from optimizacion.If import If
from optimizacion.Salto import Salto
from TablaSimbolos.Tipos import Tipo_Aritmetico, Tipo_Relacional, Tipo_Dato
from optimizacion.Primitivo import Primitivo
from optimizacion.Constante import Constante
# Definición de la gramática

def p_inicio(t):
    '''INICIO :   R_PAQUETES R_MAIN PTCOMA IMPORTES PILA_HEAP PILA_STACK DECLARACIONES FUNCIONES'''
    t[0]= [Encabezado(t[2],t[4],t[5],t[6],t[7],t[8])]
def p_paquetitos(t):
    '''IMPORTES : R_IMPORT PARIZQ LISTAIMPORTES PARDER PTCOMA'''
    t[0] = t[3]
def p_listaimportes2(t):
    '''LISTAIMPORTES : LISTAIMPORTES PTCOMA CADENA'''
    if t[3] != "":
       t[1].append(t[3])
    t[0] = t[1]
def p_listaimporte2(t):
    '''LISTAIMPORTES : CADENA'''
    t[0] = [t[1]]
def p_pilastack(t):
    '''PILA_HEAP : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA'''
    t[0]= Pila(t[2],t[4],t[6],t.lineno(0), t.lexpos(0))
def p_pilaheap(t):
    ' PILA_STACK : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA'
    t[0]= Pila(t[2],t[4],t[6],t.lineno(0), t.lexpos(0))
def p_declaraciones(t):
    'DECLARACIONES : DECLARACIONES DECLARACION'
    if t[2] != "":
       t[1].append(t[2])
    t[0] = t[1]
def p_declaraciones2(t):
    'DECLARACIONES : DECLARACION'
    t[0] = [t[1]]
def p_declaracion(t):
    ' DECLARACION : R_VAR LISTAS R_FLOAT PTCOMA'
    t[0] = Declaracion(t[1],t[2],t[3],t.lineno(0), t.lexpos(0))
def p_listas(t):
    'LISTAS : LISTAS COMA LISTA'
    if t[3] != "":
       t[1].append(t[3])
    t[0] = t[1]
def p_listas2(t):
    'LISTAS : LISTA'
    t[0] = [t[1]]
def p_lista(t):
    'LISTA : ID'
    t[0] = Variable(t[1],t.lineno(0), t.lexpos(0))
def p_funciones(t):
    'FUNCIONES : FUNCIONES FUNCION'
    if t[2] != "":
       t[1].append(t[2])
    t[0] = t[1]
def p_funciones2(t):
    'FUNCIONES : FUNCION'
    t[0] = [t[1]]

def p_funcion(t):
    '''FUNCION : R_FUNCION ID PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER 
                | R_FUNCION R_MAIN PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER '''
    t[0] = Funcion(t[2],t[6],t.lineno(0), t.lexpos(0))
def p_instrucciones(t):
    'INSTRUCCIONES : INSTRUCCIONES INSTRUCCION'
    if t[2] != "":
       t[1].append(t[2])
    t[0] = t[1]
def p_instrucciones2(t):
    'INSTRUCCIONES : INSTRUCCION'
    t[0] = [t[1]]
def p_instruccion2(t):
    '''INSTRUCCION : ASIGNACION
                    | PRINTS
                    | ETIQUETAS 
                    | SALTOS 
                    | LLAMADAS
                    | IFS
                    | RETURN'''
    t[0] = t[1]
def p_return(t):
    'RETURN : R_RETURN PTCOMA'
    t[0] = Return(t.lineno(0), t.lexpos(0))
def p_println(t):
    'PRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA E PARDER PTCOMA'
    t[0] = Print(t[5],t[7],None,t.lineno(0), t.lexpos(0))
def p_println2(t):
    'PRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA R_INT PARIZQ E PARDER PARDER PTCOMA'
    t[0] = Print(t[5],t[9],t[7],t.lineno(0), t.lexpos(0))
def p_etiquetas(t):
    'ETIQUETAS : ID DOSPUNTITOS'  
    t[0] = Etiqueta(t[0],t.lineno(0), t.lexpos(0))
def p_saltos (t):
    'SALTOS : R_GOTO ID PTCOMA'
    t[0] = Salto(t[2],t.lineno(0), t.lexpos(0))
def p_asignacion(t):
    '''ASIGNACION : ID IGUAL E PTCOMA
                    | ARREGLOS IGUAL E PTCOMA'''
    t[0] = Asignacion(t[1],t[3],t.lineno(0), t.lexpos(0))       
def p_expresiones(t):
    '''E : E MAS E
        | E MENOS E
        | E POR E
        | E DIVIDIDO E'''
    if t[2] == '+':
        t[0] = Aritmetica(t[1],Tipo_Aritmetico.SUMA, t[2],t.lineno(0), t.lexpos(0))
    elif t[2] ==  '-':
        t[0] = Aritmetica(t[1],Tipo_Aritmetico.RESTA, t[2],t.lineno(0), t.lexpos(0))
    elif t[2] == '*':
        t[0] = Aritmetica(t[1],Tipo_Aritmetico.MULTIPLICACION, t[2],t.lineno(0), t.lexpos(0))
    elif t[2] == '/':
        t[0] = Aritmetica(t[1],Tipo_Aritmetico.DIVISION, t[2],t.lineno(0), t.lexpos(0))
def p_expresion_parentesis(t):
    'E : PARIZQ E PARDER'
    t[0] = t[2]
def p_expresion_modal(t):
    'E : R_MATH PUNTO R_MOD PARIZQ E COMA E PARDER'
    t[0] = Aritmetica(t[5], Tipo_Aritmetico.MODAL, t[7],t.lineno(0), t.lexpos(0))
def p_expresion_unaria(t):
    'E : MENOS E %prec UMENOS'
    t[0] = Constante(Primitivo(TipoObjeto.NEGATIVO,t[2]),t.lineno(0), t.lexpos(0))
def p_constantes(t):
    'E : ID'
    t[0] = Variable(t[1],t.lineno(0), t.lexpos(0))
def p_constantes2(t):
    'E : DECIMAL'
    t[0] = Constante(Primitivo(Tipo_Dato.DECIMAL,t[1]),t.lineno(0), t.lexpos(0))
def p_constentes3(t):
    'E : ENTERO'
    t[0] = Constante(Primitivo(Tipo_Dato.ENTERO,t[1]),t.lineno(0), t.lexpos(0))
def p_constantes4(t):
    'E : ARREGLOS'
    t[0] = t[1]
def p_ifs(t):
    '''IFS : R_IF  RE LLAVEIZQ SALTOS LLAVEDER '''
    t[0] = If(t[2],t[4],t.lineno(0), t.lexpos(0))
def p_relacionales(t):
    ''' RE :  RE MENQUE RE
            | RE MAYQUE RE
            | RE IGUALQUE RE
            | RE NIGUALQUE RE
            | RE MENORIGUAL RE
            | RE MAYORIGUAL RE'''

    if t[2] == ">=":
        t[0] = Relacional(t[1],Tipo_Relacional.MAYOR_IGUAL,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == "<=":
        t[0] = Relacional(t[1],Tipo_Relacional.MENOR_IGUAL,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == ">":
        t[0] = Relacional(t[1],Tipo_Relacional.MAYOR,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == "<":
        t[0] = Relacional(t[1],Tipo_Relacional.MENOR,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == "<=":
        t[0] = Relacional(t[1],Tipo_Relacional.MENOR_IGUAL,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == "==":
        t[0] = Relacional(t[1],Tipo_Relacional.IGUAL,t[3],t.lineno(0), t.lexpos(0))
    elif t[2] == "!=":
        t[0] = Relacional(t[1],Tipo_Relacional.DIFERENTE,t[3],t.lineno(0), t.lexpos(0))
def p_relacionales2(t):
    'RE : PARIZQ RE PARDER'
    t[1] = t[2]
def p_relacioneales3(t):
    '''RE : E'''
    t[0] = t[1]
def p_llamaditas(t):
    ' LLAMADAS : ID PARIZQ PARDER PTCOMA'    
    t[0] = Llamada(t[1],t.lineno(0), t.lexpos(0)) 
def p_arreglos(t):
    'ARREGLOS : ID CORIZQ E CORDER'
    t[0] = Arreglo(t[1],None,t[3],t.lineno(0), t.lexpos(0))
def p_arreglos2(t):
    'ARREGLOS : ID CORIZQ R_INT PARIZQ E PARDER CORDER'
    t[0] = Arreglo(t[1],t[3],t[5],t.lineno(0), t.lexpos(0))

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
    
    general = General()

    for instruccion in instrucciones:

        if isinstance(instruccion,Codigo):
            instruccion.Concatenar(general)
    

    return general.codigo