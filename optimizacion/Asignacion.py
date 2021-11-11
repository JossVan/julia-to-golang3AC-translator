from optimizacion.Codigo import Codigo


class Asignacion(Codigo):

    def __init__(self, id, expresion, linea, columna):
        self.id = id
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
        
    
    def Concatenar(self, codigo):
        
        if isinstance(self.id, Codigo):
            id  = self.id.Concatenar(codigo)

        if isinstance(self.expresion,Codigo):
            expresion = self.Concatenar(codigo)
    

    def optimizar(self, codigo):
        return super().optimizar(codigo)