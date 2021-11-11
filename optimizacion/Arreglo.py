from optimizacion.Codigo import Codigo


class Arreglo(Codigo):

    def __init__(self, id, int, indice, linea, columna):
        self.id = id
        self.int = int 
        self.indice = indice
        self.linea = linea
        self.columna = columna
    

    def Concatenar(self, codigo):
        return super().Concatenar(codigo)
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)