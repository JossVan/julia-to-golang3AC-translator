from optimizacion.Codigo import Codigo


class Variable(Codigo):

    def __init__(self, variable, linea, columna):
        self.variable = variable
        self.linea = linea
        self.columna = columna

    def Concatenar(self, codigo):
        return self.variable
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)