import re
import sys
sys.setrecursionlimit(5000)


reservadas = {
     'nothing' : 'R_NOTHING',
     'int64' : 'R_INT64',
     'float64' : 'R_FLOAT64',
     'string' : 'R_STRING',
     'char' : 'R_CHAR',
     'bool' : 'R_BOOL',
     'struct' : 'R_STRUCT',
     'uppercase' : 'R_UPPERCASE',
     'lowercase' : 'R_LOWERCASE',
     'log' : 'R_LOG',
     'log10' : 'R_LOG10',
     'sin' : 'R_SIN',
     'cos' : 'R_COS',
     'tan' : 'R_TAN',
     'sqrt' : 'R_SQRT',
     'print' : 'R_PRINT',
     'println' : 'R_PRINTLN',
     'global': 'R_GLOBAL',
     'local' : 'R_LOCAL',
     'function' : 'R_FUNCTION',
     'if' : 'R_IF',
     'elseif' :'R_ELSEIF',
     'else' : 'R_ELSE',
     'for' : 'R_FOR',
     'while' : 'R_WHILE',
     'trunc' : 'R_TRUNC',
     'parse' : 'R_PARSE',
     'float' : 'R_FLOAT',
     'typeof' : 'R_TYPEOF',
     'push' : 'R_PUSH',
     'pop' : 'R_POP',
     'length' : 'R_LENGTH',
     'end' : 'R_END',
     'in' : 'R_IN',
     'return' : 'R_RETURN',
     'break' : 'R_BREAK',
     'continue' : 'R_CONTINUE',
     'mutable': 'R_MUTABLE',
     'true' : 'R_TRUE',
     'false' : 'R_FALSE'
}

tokens  = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODAL',
    'POTENCIA',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'COMA',
    'PUNTO',
    'AND',
    'OR',
    'DIFERENTE',
    'DOSPUNTOS',
    'DOSPUNTITOS',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'DOLAR',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_CORIZQ   = r'\['
t_CORDER   = r'\]'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MODAL     = r'%'
t_POTENCIA  = r'\^'
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_MENORIGUAL= r'<='
t_MAYORIGUAL= r'>='
t_COMA      = r','
t_PUNTO     = r'\.'
t_DOSPUNTOS = r'\:\:'
t_DOSPUNTITOS = r'\:'
t_OR       = r'\|\|'
t_AND       = r'&&'
t_DIFERENTE = r'!'
t_DOLAR     = r'\$'

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
    r'\#\=(.|\n)*\=\#'
    t.lexer.lineno += t.value.count('\n')
# Comentario simple // ...

def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
#t_ignore = " \r"
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_IGNORAR(t):
    r'\ |\t|\r'
    global columna
   # if t.value == '\r':
    #   print("salto de linea")    
    
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
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALQUE', 'NIGUALQUE'),
    ('left', 'MENQUE','MAYQUE', 'MENORIGUAL','MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','MODAL'),
    ('left', 'POTENCIA'),
    ('right', 'DIFERENTE'),
    ('right','UMENOS'),
    )

# Definición de la gramática


def p_inicio(t):
    '''INICIO : INICIO INIT'''
    t[0] = "ok"

def p_iniciop(t):
    'INICIO : INIT'
    t[0] = "ok"
def p_iniciofi(t):
    '''INIT     : FUNCIONES
                | INSTRUCCIONES
                | STRUCTS '''
    
    t[0] = t[1]

def p_instrucciones(t):
    '''INSTRUCCIONES    : INSTRUCCIONES INSTRUCCION'''


def p_instruccionesp(t):
    'INSTRUCCIONES : INSTRUCCION'


def p_instruccionesI(t):
    '''INSTRUCCION :     IFS
                        | FORS
                        | WHILES
                        | ASIGNACION
                        | I
                        | LLAMADAS PTCOMA
                        | NATIVAS PTCOMA
                        | BREAK
                        | CONTINUE
                        | RETURN'''
    t[0] = t[1]

def p_impresion(t):

    '''I : R_PRINT PARIZQ IMPRESIONES PARDER PTCOMA'''
    
def p_println(t):
    'I : R_PRINTLN PARIZQ IMPRESIONES PARDER PTCOMA'
    
def p_printlmVacio(t):
    'I : R_PRINTLN PARIZQ PARDER PTCOMA'
    
def p_printVacio(t):
    'I : R_PRINT PARIZQ PARDER PTCOMA'
    
def p_contImpresion(t):
    'IMPRESIONES : IMPRESIONES COMA IMPRESION'

def p_contimpresiones(t):
    'IMPRESIONES : IMPRESION'
    t[0] = [t[1]]

def p_contimpresionCont(t):
    '''IMPRESION    : ARREGLOS
                    | LO'''
    t[0] = t[1]

def p_cont_impresionDolar(t):
    '''IMPRESION : DOLAR PARIZQ E PARDER
                 | DOLAR PARIZQ ARREGLOS PARDER
                 | DOLAR PARIZQ NATIVAS PARDER'''

def p_arreglos(t):
    'ARREGLOS : ARREGLOS COMA ARREGLO'    


def p_arreglosp(t):
    'ARREGLOS : ARREGLO'
    t[0]  = [t[1]]

def p_arreglito(t):
    'ARREGLO : CORIZQ LISTAS CORDER'
    
def p_listas(t):
    'LISTAS : LISTAS COMA LISTA'

def p_listasp(t):
    'LISTAS : LISTA'


def p_lista(t):
    '''LISTA : ARREGLOS
            | LO'''

def p_asignaciones(t):
    '''ASIGNACION : R_GLOBAL E IGUAL LISTA DOSPUNTOS TIPO PTCOMA
                  | R_LOCAL E IGUAL LISTA DOSPUNTOS TIPO PTCOMA
                  | R_GLOBAL E IGUAL LISTA DOSPUNTOS ID PTCOMA
                  | R_LOCAL E IGUAL LISTA DOSPUNTOS ID PTCOMA'''

def p_asignacionesp(t):
    '''ASIGNACION : E IGUAL LISTA DOSPUNTOS TIPO PTCOMA
                    | E IGUAL LISTA DOSPUNTOS ID PTCOMA'''

def p_asginacionesp2(t):
    '''ASIGNACION : R_GLOBAL E IGUAL LISTA PTCOMA
                  | R_LOCAL E IGUAL LISTA PTCOMA'''

def p_asginacionesp3(t):
    '''ASIGNACION :  E IGUAL LISTA PTCOMA'''

def p_asignacionesp4(t):
    '''ASIGNACION : R_GLOBAL E PTCOMA
                  | R_LOCAL E PTCOMA'''
def p_break(t):
    'BREAK : R_BREAK PTCOMA'
   
def p_tipo(t):
    '''TIPO : R_NOTHING
            | R_INT64
            | R_FLOAT64
            | R_STRING
            | R_CHAR
            | R_BOOL'''


def p_llamadas(t):
    'LLAMADAS : ID PARIZQ LISTAS PARDER'
    
def p_llamadassinparametro(t):
    'LLAMADAS : ID PARIZQ PARDER'
    
def p_expresiones(t):
    '''E    : E MAS E 
            | E MENOS E
            | E POR E
            | E DIVIDIDO E
            | E MODAL E
            | E POTENCIA E'''
    
    
def p_expresion_unaria(t):
    'E : MENOS E %prec UMENOS'
  
def p_expresionespar(t):
    'E : PARIZQ E PARDER'
  
def p_expresionesesp(t):
    '''E : R_LOG10 PARIZQ E PARDER'''  
  
def p_expresiones_seno(t):
    'E : R_SIN PARIZQ E PARDER'
 
def p_expresiones_coseno(t):
    'E : R_COS PARIZQ E PARDER'
  
def p_expresiones_tangente(t):
    'E : R_TAN PARIZQ E PARDER'
   
def p_expresiones_sqrt(t):
    'E : R_SQRT PARIZQ E PARDER'
    
def p_expresiones_upper(t):
    'E : R_UPPERCASE PARIZQ E PARDER'
    
def p_expresiones_lower(t):
    'E : R_LOWERCASE PARIZQ E PARDER'
   
def p_expresiones_log(t):
    'E : R_LOG PARIZQ E COMA E PARDER'
    
def p_expresiones_decimal(t):
    'E : DECIMAL'

def p_expresiones_entero(t):
    'E : ENTERO'
 
def p_expresiones_booleanas(t):
    '''E : R_TRUE
        | R_FALSE'''
  
def p_expresiones_nothing (t):
    'E : R_NOTHING'
    
def p_expresiones_cadena(t):
    'E : CADENA'
   
def p_expresion_llamada(t):
    'E : LLAMADAS'
    
def p_expresion_accesos(t):
    'E : ACCESOS'
   
def p_expresiones_id(t):
    'E : ID'
 
def p_expresiones_array(t):
    'E : ID ARRAYS'
  
def p_idarrays(t):
    'ARRAYS : ARRAYS ARRAY'
   
def p_idarraysp(t):
    'ARRAYS : ARRAY'
    
def p_idarray(t):
    'ARRAY : CORIZQ E CORDER'
    
def p_expresiones_nativas(t):
    'E : NATIVAS'
    
def p_expresiones_relacionales(t):
    ''' RE :  RE MENQUE RE
            | RE MAYQUE RE
            | RE IGUALQUE RE
            | RE NIGUALQUE RE
            | RE MENORIGUAL RE
            | RE MAYORIGUAL RE'''
    

def p_expresionesE_par(t):
    'RE : PARIZQ RE PARDER'
    
def p_expresionesE(t):
    'RE : E'
   
def p_expresiones_logicas(t):
    '''LO :   LO AND LO
            | LO OR LO'''
    
def p_expresiones_logicas_diferente(t):
    'LO : DIFERENTE LO'
   
def p_expresiones_logicas_par(t):
    'LO : PARIZQ LO PARDER'
  
def p_expresiones_logicas_re(t):
    'LO : RE'
  
def p_nativas(t):
    '''NATIVAS :  R_PARSE PARIZQ TIPO COMA LISTA PARDER
                | R_TRUNC PARIZQ TIPO COMA LISTA PARDER'''
    
  
def p_nativasp(t):
    '''NATIVAS :  R_FLOAT   PARIZQ LISTA PARDER
                | R_STRING PARIZQ LISTA PARDER
                | R_TYPEOF  PARIZQ LISTA PARDER
                | R_TRUNC PARIZQ LISTA PARDER'''

    
def p_nativaspush(t):
    ' NATIVAS : R_PUSH  DIFERENTE PARIZQ E COMA LISTA PARDER'

def p_nativaspop(t):
    'NATIVAS : R_POP DIFERENTE PARIZQ E PARDER'
  
def p_nativas_length(t):
    'NATIVAS :  R_LENGTH PARIZQ E PARDER'
    
def p_returns(t):
    'RETURN : R_RETURN LISTA PTCOMA'
    
def p_returnUnico(t):
    'RETURN : R_RETURN PTCOMA'
    
def p_funciones(t):
    'FUNCIONES : R_FUNCTION ID PARIZQ PARAMETROS PARDER INSTRUCCIONES R_END PTCOMA'
    
def p_funciones_parametros_vacia(t):
    'FUNCIONES : R_FUNCTION ID PARIZQ PARAMETROS PARDER  R_END PTCOMA'
    
def p_funciones_proce(t):
    'FUNCIONES : R_FUNCTION ID PARIZQ  PARDER INSTRUCCIONES R_END PTCOMA'
    
def p_funciones_proc_vacia(t):
    'FUNCIONES : R_FUNCTION ID PARIZQ  PARDER  R_END PTCOMA'
   
def p_parametros(t):
    'PARAMETROS : PARAMETROS COMA PARAMETRO'

def p_parametros2(t):
    'PARAMETROS : PARAMETRO'
    t[0] = [t[1]]
def p_parametro(t):
    '''PARAMETRO : ID'''
  
################################ EMPIEZAN LOS IFS ######################################
def p_if_solo(t) :
    'IFS : R_IF LO INSTRUCCIONES R_END PTCOMA'
 
def p_if_else(t) :
    'IFS : R_IF LO  INSTRUCCIONES R_ELSE INSTRUCCIONES R_END PTCOMA'
   
def p_if_elseif(t) :
    'IFS : R_IF LO INSTRUCCIONES ELSEIF'
  
################################ IFS VACIOS ############################################
def p_if_solo2(t) :
    'IFS : R_IF LO  R_END PTCOMA'
  
def p_if_else2(t) :
    'IFS : R_IF LO  R_ELSE INSTRUCCIONES R_END PTCOMA'

def p_if_elseif2(t) :
    'IFS : R_IF LO ELSEIF'
   
def p_if_else3(t) :
    'IFS : R_IF LO INSTRUCCIONES R_ELSE  R_END PTCOMA'
  
def p_if_else4(t) :
    'IFS : R_IF LO  R_ELSE  R_END PTCOMA'
   
#************************************ELSIF EMPIEZAN****************************************
def p_elseif_solo(t) :
    'ELSEIF : R_ELSEIF LO INSTRUCCIONES R_END PTCOMA'
    
def p_elseif_else(t) :
    'ELSEIF : R_ELSEIF LO  INSTRUCCIONES R_ELSE INSTRUCCIONES R_END PTCOMA'
    
def p_elseif_elseif(t) :
    'ELSEIF : R_ELSEIF LO INSTRUCCIONES ELSEIF'
  
################################ ELSEIF VACIOS ############################################
def p_elseif_solo2(t) :
    'ELSEIF : R_ELSEIF LO  R_END PTCOMA'
   
def p_elseif_else2(t) :
    'ELSEIF : R_ELSEIF LO  R_ELSE INSTRUCCIONES R_END PTCOMA'
   
def p_elseif_elseif2(t) :
    'ELSEIF : R_ELSEIF LO ELSEIF'
    
def p_elseif_else3(t) :
    'ELSEIF : R_ELSEIF LO INSTRUCCIONES R_ELSE  R_END PTCOMA'
    
def p_elseif_else4(t) :
    'ELSEIF : R_ELSEIF LO  R_ELSE  R_END PTCOMA'
    
def p_continue12(t):
    'CONTINUE : R_CONTINUE PTCOMA'
   
#*************************************ELSEIF TERMINAN******************************************
def p_instrucciones_loop(t):
    '''INSTRUCCIONES_LOOP :   INSTRUCCIONES_LOOP INSTRUCCION_LOOP'''
   
def p_instruccion_loopp(t):
    'INSTRUCCIONES_LOOP : INSTRUCCION_LOOP'
    
def p_instrucciones_loop_inst(t):
    '''INSTRUCCION_LOOP :   IFS
                            | FORS
                            | WHILES
                            | ASIGNACION
                            | I
                            | LLAMADAS PTCOMA
                            | NATIVAS PTCOMA
                            | BREAK
                            | CONTINUE'''

def p_whiles(t):
    'WHILES : R_WHILE LO INSTRUCCIONES_LOOP R_END PTCOMA'
    
def p_whiles_vacios(t):
    'WHILES :  R_WHILE LO R_END PTCOMA'
    
def p_fors(t):
    'FORS : R_FOR ID R_IN RANGO INSTRUCCIONES_LOOP R_END PTCOMA'
    
def p_fors_vacios(t):
    'FORS : R_FOR ID R_IN RANGO  R_END PTCOMA'
    
def p_rango(t):
    '''RANGO :    E DOSPUNTITOS E'''
   
def p_rango_unaExpresion(t):
    '''RANGO : E
            | ARREGLOS'''
def p_rango_arreglos(t):
    'RANGO : ID CORIZQ E DOSPUNTOS E CORDER'
    
def p_structs(t):
    'STRUCTS : R_MUTABLE R_STRUCT ID ELEMENTOS  R_END PTCOMA'
    
def p_structs2(t):
    'STRUCTS : R_STRUCT ID ELEMENTOS  R_END PTCOMA'
    
def p_structs_mutables(t):
    'STRUCTS : R_MUTABLE R_STRUCT ID R_END PTCOMA'
    
def p_structs_vacios(t):
    'STRUCTS : R_STRUCT ID R_END PTCOMA'
   
def p_elementos(t):
    'ELEMENTOS : ELEMENTOS ELEMENTO'
    
def p_elementos_elemento(t):
    'ELEMENTOS : ELEMENTO'
   

def p_elemento(t):
    'ELEMENTO  : ID PTCOMA'
    
def p_elemento_declaraciontipo(t):
    'ELEMENTO : ID DOSPUNTOS TIPO PTCOMA'
   
def p_elemento_declaracion_tipo(t):
    'ELEMENTO : ID DOSPUNTOS ID PTCOMA'
    
def p_acceso1(t):
    'ACCESOS : ACCESOS PUNTO ACCESO'
   
def p_acceso2(t):
    'ACCESOS : ACCESO'
    
def p_acceso3(t):
    'ACCESO : ID'
   
def p_error(t):
    print("Error sintáctico en '%s'" % str(t))

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    global lexer
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    instrucciones=parser.parse(input)

   
    return instrucciones