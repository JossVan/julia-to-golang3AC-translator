from optimizacion.Codigo import Codigo


class Arreglo(Codigo):

    def __init__(self, id, int, indice, linea, columna):
        self.id = id
        self.int = int 
        self.indice = indice
        self.linea = linea
        self.columna = columna
    

    def Concatenar(self, codigo):
        
        if self.int == None:
            if isinstance(self.indice,Codigo):
                indice = self.indice.Concatenar(codigo)
            else:
                indice= self.indice
            cod = self.id+"["+str(indice)+"]"
            return cod
        else:
            if isinstance(self.indice,Codigo):
                indice = self.indice.Concatenar(codigo)
            else:
                indice= self.indice
            cod = self.id +"[int("+str(indice)+")]"
            return cod 
    def optimizar(self, codigo):
        return super().optimizar(codigo)