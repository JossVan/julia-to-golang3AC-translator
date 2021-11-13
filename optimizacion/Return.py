from optimizacion.Codigo import Codigo


class Return(Codigo):

    def __init__(self, linea, columna):
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        return {"return": "\treturn;\n"}
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)