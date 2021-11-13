from optimizacion.Codigo import Codigo


class Salto(Codigo):

    def __init__(self, etiqueta, linea, columna):
        self.etiqueta = etiqueta
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        return {"goto": self.etiqueta, "linea":self.linea}
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)
