
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftIGUALQUENIGUALQUEleftMENQUEMAYQUEMENORIGUALMAYORIGUALleftMASMENOSleftPORDIVIDIDOrightUMENOSCADENA COMA CORDER CORIZQ DECIMAL DIVIDIDO DOSPUNTITOS ENTERO ID IGUAL IGUALQUE LLAVEDER LLAVEIZQ MAS MAYORIGUAL MAYQUE MENORIGUAL MENOS MENQUE NIGUALQUE PARDER PARIZQ POR PTCOMA PUNTO R_FLOAT R_FMT R_FUNCION R_GOTO R_IF R_IMPORT R_INT R_MAIN R_MATH R_MOD R_PAQUETES R_PRINTF R_RETURN R_VARINICIO :   R_PAQUETES R_MAIN PTCOMA IMPORTES PILA_HEAP PILA_STACK DECLARACIONES FUNCIONESIMPORTES : R_IMPORT PARIZQ LISTAIMPORTES PARDER PTCOMALISTAIMPORTES : LISTAIMPORTES PTCOMA CADENALISTAIMPORTES : CADENAPILA_HEAP : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA PILA_STACK : R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMADECLARACIONES : DECLARACIONES DECLARACIONDECLARACIONES : DECLARACION DECLARACION : R_VAR LISTAS R_FLOAT PTCOMALISTAS : LISTAS COMA LISTALISTAS : LISTALISTA : IDFUNCIONES : FUNCIONES FUNCIONFUNCIONES : FUNCIONFUNCION : R_FUNCION ID PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER \n                | R_FUNCION R_MAIN PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER INSTRUCCIONES : INSTRUCCIONES INSTRUCCIONINSTRUCCIONES : INSTRUCCIONINSTRUCCION : ASIGNACION\n                    | PRINTS\n                    | ETIQUETAS \n                    | SALTOS \n                    | LLAMADAS\n                    | IFS\n                    | RETURNRETURN : R_RETURN PTCOMAPRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA E PARDER PTCOMAPRINTS : R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA R_INT PARIZQ E PARDER PARDER PTCOMAETIQUETAS : ID DOSPUNTITOSSALTOS : R_GOTO ID PTCOMAASIGNACION : ID IGUAL E PTCOMA\n                    | ARREGLOS IGUAL E PTCOMAE : E MAS E\n        | E MENOS E\n        | E POR E\n        | E DIVIDIDO EE : PARIZQ E PARDERE : R_MATH PUNTO R_MOD PARIZQ E COMA E PARDERE : MENOS E %prec UMENOSE : IDE : DECIMALE : ENTEROE : ARREGLOSIFS : R_IF  RE LLAVEIZQ SALTOS LLAVEDER  RE :  RE MENQUE RE\n            | RE MAYQUE RE\n            | RE IGUALQUE RE\n            | RE NIGUALQUE RE\n            | RE MENORIGUAL RE\n            | RE MAYORIGUAL RERE : PARIZQ RE PARDERRE : E LLAMADAS : ID PARIZQ PARDER PTCOMAARREGLOS : ID CORIZQ E CORDERARREGLOS : ID CORIZQ R_INT PARIZQ E PARDER CORDER'
    
_lr_action_items = {'R_PAQUETES':([0,],[2,]),'$end':([1,22,24,33,73,88,],[0,-1,-14,-13,-15,-16,]),'R_MAIN':([2,25,],[3,35,]),'PTCOMA':([3,13,14,20,32,36,45,48,67,77,83,84,85,86,89,91,94,110,115,127,128,129,130,131,140,144,149,151,],[4,21,-4,31,-3,42,49,52,87,96,-40,-41,-42,-43,112,114,117,-39,-54,-37,-33,-34,-35,-36,-55,147,-38,152,]),'R_IMPORT':([4,],[6,]),'R_VAR':([5,7,10,15,16,23,31,42,49,52,],[8,11,17,17,-8,-7,-2,-9,-5,-6,]),'PARIZQ':([6,34,35,53,66,69,72,75,79,81,90,93,95,98,99,100,101,102,103,106,107,108,109,116,132,136,138,142,143,145,],[9,40,41,71,79,90,90,90,79,90,90,116,118,79,79,79,79,79,79,90,90,90,90,90,136,90,90,145,90,90,]),'ID':([8,11,17,25,37,50,51,54,55,56,57,58,59,60,61,62,65,66,68,69,70,72,74,75,79,81,87,90,96,98,99,100,101,102,103,106,107,108,109,112,114,116,117,135,136,138,143,145,147,152,],[12,18,28,34,28,53,53,53,-18,-19,-20,-21,-22,-23,-24,-25,77,83,53,83,-29,83,-17,83,83,83,-26,83,-30,83,83,83,83,83,83,83,83,83,83,-31,-53,83,-32,-44,83,83,83,83,-27,-28,]),'CADENA':([9,21,118,],[14,32,134,]),'CORIZQ':([12,18,53,83,],[19,29,72,72,]),'PARDER':([13,14,32,40,41,71,80,83,84,85,86,104,105,110,113,115,120,121,122,123,124,125,126,127,128,129,130,131,133,140,141,146,148,149,150,],[20,-4,-3,46,47,91,-52,-40,-41,-42,-43,126,127,-39,127,-54,-45,-46,-47,-48,-49,-50,-51,-37,-33,-34,-35,-36,137,-55,144,149,150,-38,151,]),'R_FUNCION':([15,16,22,23,24,33,42,73,88,],[25,-8,25,-7,-14,-13,-9,-15,-16,]),'ENTERO':([19,29,66,69,72,75,79,81,90,98,99,100,101,102,103,106,107,108,109,116,136,138,143,145,],[30,38,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,]),'R_FLOAT':([26,27,28,39,43,44,],[36,-11,-12,45,-10,48,]),'COMA':([26,27,28,43,83,84,85,86,110,115,127,128,129,130,131,134,139,140,149,],[37,-11,-12,-10,-40,-41,-42,-43,-39,-54,-37,-33,-34,-35,-36,138,143,-55,-38,]),'CORDER':([30,38,83,84,85,86,92,110,115,127,128,129,130,131,137,140,149,],[39,44,-40,-41,-42,-43,115,-39,-54,-37,-33,-34,-35,-36,140,-55,-38,]),'LLAVEIZQ':([46,47,78,80,83,84,85,86,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[50,51,97,-52,-40,-41,-42,-43,-39,-54,-45,-46,-47,-48,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'R_FMT':([50,51,54,55,56,57,58,59,60,61,62,68,70,74,87,96,112,114,117,135,147,152,],[64,64,64,-18,-19,-20,-21,-22,-23,-24,-25,64,-29,-17,-26,-30,-31,-53,-32,-44,-27,-28,]),'R_GOTO':([50,51,54,55,56,57,58,59,60,61,62,68,70,74,87,96,97,112,114,117,135,147,152,],[65,65,65,-18,-19,-20,-21,-22,-23,-24,-25,65,-29,-17,-26,-30,65,-31,-53,-32,-44,-27,-28,]),'R_IF':([50,51,54,55,56,57,58,59,60,61,62,68,70,74,87,96,112,114,117,135,147,152,],[66,66,66,-18,-19,-20,-21,-22,-23,-24,-25,66,-29,-17,-26,-30,-31,-53,-32,-44,-27,-28,]),'R_RETURN':([50,51,54,55,56,57,58,59,60,61,62,68,70,74,87,96,112,114,117,135,147,152,],[67,67,67,-18,-19,-20,-21,-22,-23,-24,-25,67,-29,-17,-26,-30,-31,-53,-32,-44,-27,-28,]),'IGUAL':([53,63,115,140,],[69,75,-54,-55,]),'DOSPUNTITOS':([53,],[70,]),'LLAVEDER':([54,55,56,57,58,59,60,61,62,68,70,74,87,96,112,114,117,119,135,147,152,],[73,-18,-19,-20,-21,-22,-23,-24,-25,88,-29,-17,-26,-30,-31,-53,-32,135,-44,-27,-28,]),'PUNTO':([64,82,],[76,111,]),'R_MATH':([66,69,72,75,79,81,90,98,99,100,101,102,103,106,107,108,109,116,136,138,143,145,],[82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,]),'MENOS':([66,69,72,75,79,80,81,83,84,85,86,89,90,92,94,98,99,100,101,102,103,105,106,107,108,109,110,113,115,116,127,128,129,130,131,133,136,138,139,140,141,143,145,146,148,149,],[81,81,81,81,81,107,81,-40,-41,-42,-43,107,81,107,107,81,81,81,81,81,81,107,81,81,81,81,-39,107,-54,81,-37,-33,-34,-35,-36,107,81,81,107,-55,107,81,81,107,107,-38,]),'DECIMAL':([66,69,72,75,79,81,90,98,99,100,101,102,103,106,107,108,109,116,136,138,143,145,],[84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,]),'R_INT':([72,138,],[93,142,]),'R_PRINTF':([76,],[95,]),'MENQUE':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[98,-52,-40,-41,-42,-43,98,-52,-39,-54,-45,-46,98,98,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'MAYQUE':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[99,-52,-40,-41,-42,-43,99,-52,-39,-54,-45,-46,99,99,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'IGUALQUE':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[100,-52,-40,-41,-42,-43,100,-52,-39,-54,-45,-46,-47,-48,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'NIGUALQUE':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[101,-52,-40,-41,-42,-43,101,-52,-39,-54,-45,-46,-47,-48,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'MENORIGUAL':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[102,-52,-40,-41,-42,-43,102,-52,-39,-54,-45,-46,102,102,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'MAYORIGUAL':([78,80,83,84,85,86,104,105,110,115,120,121,122,123,124,125,126,127,128,129,130,131,140,149,],[103,-52,-40,-41,-42,-43,103,-52,-39,-54,-45,-46,103,103,-49,-50,-51,-37,-33,-34,-35,-36,-55,-38,]),'MAS':([80,83,84,85,86,89,92,94,105,110,113,115,127,128,129,130,131,133,139,140,141,146,148,149,],[106,-40,-41,-42,-43,106,106,106,106,-39,106,-54,-37,-33,-34,-35,-36,106,106,-55,106,106,106,-38,]),'POR':([80,83,84,85,86,89,92,94,105,110,113,115,127,128,129,130,131,133,139,140,141,146,148,149,],[108,-40,-41,-42,-43,108,108,108,108,-39,108,-54,-37,108,108,-35,-36,108,108,-55,108,108,108,-38,]),'DIVIDIDO':([80,83,84,85,86,89,92,94,105,110,113,115,127,128,129,130,131,133,139,140,141,146,148,149,],[109,-40,-41,-42,-43,109,109,109,109,-39,109,-54,-37,109,109,-35,-36,109,109,-55,109,109,109,-38,]),'R_MOD':([111,],[132,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'INICIO':([0,],[1,]),'IMPORTES':([4,],[5,]),'PILA_HEAP':([5,],[7,]),'PILA_STACK':([7,],[10,]),'LISTAIMPORTES':([9,],[13,]),'DECLARACIONES':([10,],[15,]),'DECLARACION':([10,15,],[16,23,]),'FUNCIONES':([15,],[22,]),'FUNCION':([15,22,],[24,33,]),'LISTAS':([17,],[26,]),'LISTA':([17,37,],[27,43,]),'INSTRUCCIONES':([50,51,],[54,68,]),'INSTRUCCION':([50,51,54,68,],[55,55,74,74,]),'ASIGNACION':([50,51,54,68,],[56,56,56,56,]),'PRINTS':([50,51,54,68,],[57,57,57,57,]),'ETIQUETAS':([50,51,54,68,],[58,58,58,58,]),'SALTOS':([50,51,54,68,97,],[59,59,59,59,119,]),'LLAMADAS':([50,51,54,68,],[60,60,60,60,]),'IFS':([50,51,54,68,],[61,61,61,61,]),'RETURN':([50,51,54,68,],[62,62,62,62,]),'ARREGLOS':([50,51,54,66,68,69,72,75,79,81,90,98,99,100,101,102,103,106,107,108,109,116,136,138,143,145,],[63,63,63,86,63,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,]),'RE':([66,79,98,99,100,101,102,103,],[78,104,120,121,122,123,124,125,]),'E':([66,69,72,75,79,81,90,98,99,100,101,102,103,106,107,108,109,116,136,138,143,145,],[80,89,92,94,105,110,113,80,80,80,80,80,80,128,129,130,131,133,139,141,146,148,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> INICIO","S'",1,None,None,None),
  ('INICIO -> R_PAQUETES R_MAIN PTCOMA IMPORTES PILA_HEAP PILA_STACK DECLARACIONES FUNCIONES','INICIO',8,'p_inicio','optimizacion.py',168),
  ('IMPORTES -> R_IMPORT PARIZQ LISTAIMPORTES PARDER PTCOMA','IMPORTES',5,'p_paquetitos','optimizacion.py',171),
  ('LISTAIMPORTES -> LISTAIMPORTES PTCOMA CADENA','LISTAIMPORTES',3,'p_listaimportes2','optimizacion.py',174),
  ('LISTAIMPORTES -> CADENA','LISTAIMPORTES',1,'p_listaimporte2','optimizacion.py',179),
  ('PILA_HEAP -> R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA','PILA_HEAP',7,'p_pilastack','optimizacion.py',182),
  ('PILA_STACK -> R_VAR ID CORIZQ ENTERO CORDER R_FLOAT PTCOMA','PILA_STACK',7,'p_pilaheap','optimizacion.py',185),
  ('DECLARACIONES -> DECLARACIONES DECLARACION','DECLARACIONES',2,'p_declaraciones','optimizacion.py',188),
  ('DECLARACIONES -> DECLARACION','DECLARACIONES',1,'p_declaraciones2','optimizacion.py',193),
  ('DECLARACION -> R_VAR LISTAS R_FLOAT PTCOMA','DECLARACION',4,'p_declaracion','optimizacion.py',196),
  ('LISTAS -> LISTAS COMA LISTA','LISTAS',3,'p_listas','optimizacion.py',199),
  ('LISTAS -> LISTA','LISTAS',1,'p_listas2','optimizacion.py',204),
  ('LISTA -> ID','LISTA',1,'p_lista','optimizacion.py',207),
  ('FUNCIONES -> FUNCIONES FUNCION','FUNCIONES',2,'p_funciones','optimizacion.py',210),
  ('FUNCIONES -> FUNCION','FUNCIONES',1,'p_funciones2','optimizacion.py',215),
  ('FUNCION -> R_FUNCION ID PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER','FUNCION',7,'p_funcion','optimizacion.py',219),
  ('FUNCION -> R_FUNCION R_MAIN PARIZQ PARDER LLAVEIZQ INSTRUCCIONES LLAVEDER','FUNCION',7,'p_funcion','optimizacion.py',220),
  ('INSTRUCCIONES -> INSTRUCCIONES INSTRUCCION','INSTRUCCIONES',2,'p_instrucciones','optimizacion.py',223),
  ('INSTRUCCIONES -> INSTRUCCION','INSTRUCCIONES',1,'p_instrucciones2','optimizacion.py',228),
  ('INSTRUCCION -> ASIGNACION','INSTRUCCION',1,'p_instruccion2','optimizacion.py',231),
  ('INSTRUCCION -> PRINTS','INSTRUCCION',1,'p_instruccion2','optimizacion.py',232),
  ('INSTRUCCION -> ETIQUETAS','INSTRUCCION',1,'p_instruccion2','optimizacion.py',233),
  ('INSTRUCCION -> SALTOS','INSTRUCCION',1,'p_instruccion2','optimizacion.py',234),
  ('INSTRUCCION -> LLAMADAS','INSTRUCCION',1,'p_instruccion2','optimizacion.py',235),
  ('INSTRUCCION -> IFS','INSTRUCCION',1,'p_instruccion2','optimizacion.py',236),
  ('INSTRUCCION -> RETURN','INSTRUCCION',1,'p_instruccion2','optimizacion.py',237),
  ('RETURN -> R_RETURN PTCOMA','RETURN',2,'p_return','optimizacion.py',240),
  ('PRINTS -> R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA E PARDER PTCOMA','PRINTS',9,'p_println','optimizacion.py',243),
  ('PRINTS -> R_FMT PUNTO R_PRINTF PARIZQ CADENA COMA R_INT PARIZQ E PARDER PARDER PTCOMA','PRINTS',12,'p_println2','optimizacion.py',246),
  ('ETIQUETAS -> ID DOSPUNTITOS','ETIQUETAS',2,'p_etiquetas','optimizacion.py',249),
  ('SALTOS -> R_GOTO ID PTCOMA','SALTOS',3,'p_saltos','optimizacion.py',252),
  ('ASIGNACION -> ID IGUAL E PTCOMA','ASIGNACION',4,'p_asignacion','optimizacion.py',255),
  ('ASIGNACION -> ARREGLOS IGUAL E PTCOMA','ASIGNACION',4,'p_asignacion','optimizacion.py',256),
  ('E -> E MAS E','E',3,'p_expresiones','optimizacion.py',259),
  ('E -> E MENOS E','E',3,'p_expresiones','optimizacion.py',260),
  ('E -> E POR E','E',3,'p_expresiones','optimizacion.py',261),
  ('E -> E DIVIDIDO E','E',3,'p_expresiones','optimizacion.py',262),
  ('E -> PARIZQ E PARDER','E',3,'p_expresion_parentesis','optimizacion.py',272),
  ('E -> R_MATH PUNTO R_MOD PARIZQ E COMA E PARDER','E',8,'p_expresion_modal','optimizacion.py',275),
  ('E -> MENOS E','E',2,'p_expresion_unaria','optimizacion.py',278),
  ('E -> ID','E',1,'p_constantes','optimizacion.py',281),
  ('E -> DECIMAL','E',1,'p_constantes2','optimizacion.py',284),
  ('E -> ENTERO','E',1,'p_constentes3','optimizacion.py',287),
  ('E -> ARREGLOS','E',1,'p_constantes4','optimizacion.py',290),
  ('IFS -> R_IF RE LLAVEIZQ SALTOS LLAVEDER','IFS',5,'p_ifs','optimizacion.py',293),
  ('RE -> RE MENQUE RE','RE',3,'p_relacionales','optimizacion.py',296),
  ('RE -> RE MAYQUE RE','RE',3,'p_relacionales','optimizacion.py',297),
  ('RE -> RE IGUALQUE RE','RE',3,'p_relacionales','optimizacion.py',298),
  ('RE -> RE NIGUALQUE RE','RE',3,'p_relacionales','optimizacion.py',299),
  ('RE -> RE MENORIGUAL RE','RE',3,'p_relacionales','optimizacion.py',300),
  ('RE -> RE MAYORIGUAL RE','RE',3,'p_relacionales','optimizacion.py',301),
  ('RE -> PARIZQ RE PARDER','RE',3,'p_relacionales2','optimizacion.py',318),
  ('RE -> E','RE',1,'p_relacioneales3','optimizacion.py',321),
  ('LLAMADAS -> ID PARIZQ PARDER PTCOMA','LLAMADAS',4,'p_llamaditas','optimizacion.py',324),
  ('ARREGLOS -> ID CORIZQ E CORDER','ARREGLOS',4,'p_arreglos','optimizacion.py',327),
  ('ARREGLOS -> ID CORIZQ R_INT PARIZQ E PARDER CORDER','ARREGLOS',7,'p_arreglos2','optimizacion.py',330),
]
