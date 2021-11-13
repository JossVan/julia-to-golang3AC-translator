from optimizacion.Codigo import Codigo


class Aritmetica(Codigo):
    
    def __init__(self, exp1, operador, exp2, linea, columna):
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna
    

    def Concatenar(self, codigo):
        exp1 = self.exp1.Concatenar(codigo)
        exp2 = self.exp2.Concatenar(codigo)
        return {"expresion1": exp1,"operador":self.operador,"expresion2": exp2}
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)