from optimizacion.Codigo import Codigo


class Aritmetica(Codigo):
    
    def __init__(self, exp1, operador, exp2, linea, columna):
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna
    

    def Concatenar(self, codigo):
        return super().Concatenar(codigo)
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)