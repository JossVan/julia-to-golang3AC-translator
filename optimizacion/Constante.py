from optimizacion.Codigo import Codigo
class Constante(Codigo):

    def __init__(self, valor, linea, columna):
        self.valor = valor 
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        return super().Concatenar(codigo)
    

    def optimizar(self, codigo):
        return super().optimizar(codigo)