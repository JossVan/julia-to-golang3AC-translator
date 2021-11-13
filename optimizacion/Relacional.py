from TablaSimbolos.Tipos import Tipo_Relacional
from optimizacion.Codigo import Codigo


class Relacional(Codigo):

    def __init__(self, op1, tipo, op2, linea, columna):
        self.op1 = op1
        self.op2 = op2
        self.tipo = tipo 
        self.linea = linea
        self.columna = columna
        
    
    def Concatenar(self, codigo):
        
        if isinstance(self.op1,Codigo):
            val1 = self.op1.Concatenar(codigo)
        else:
            val1 = self.op1
        if isinstance(self.op2,Codigo):
            val2 = self.op2.Concatenar(codigo)
        else: 
            val2 = self.op2 

        if self.tipo == Tipo_Relacional.MAYOR:
            tipo = ">"
        elif self.tipo == Tipo_Relacional.MAYOR_IGUAL:
            tipo = ">="
        elif self.tipo == Tipo_Relacional.MENOR:
            tipo = "<"
        elif self.tipo == Tipo_Relacional.MENOR_IGUAL:
            tipo = "<="
        elif self.tipo == Tipo_Relacional.DIFERENTE:
            tipo = "!="
        elif self.tipo == Tipo_Relacional.IGUAL:
            tipo = "=="

        cod = str(val1)+" "+str(tipo)+" "+str(val2)
        return cod
    def optimizar(self, codigo):
        return super().optimizar(codigo)