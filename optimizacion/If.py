from optimizacion.Codigo import Codigo


class If(Codigo):

    def __init__(self, condicion, salto, linea, columna):
        self.condicion = condicion 
        self.salto = salto
        self.linea = linea
        self.columna = columna
    
    
    