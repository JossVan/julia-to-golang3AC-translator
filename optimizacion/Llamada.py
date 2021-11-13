from optimizacion.Codigo import Codigo


class Llamada(Codigo):

    def __init__(self, id, linea, columna):
        self.id = id
        self.linea = linea
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        if isinstance(self.id,Codigo):
            id = self.id.Concatenar(codigo)
        else:
            id = self.id
        
        cod = "\t"+id+"();\n"
        return {"funcion":cod}
    def optimizar(self, codigo):
        return super().optimizar(codigo)