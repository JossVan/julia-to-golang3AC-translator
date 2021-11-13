from optimizacion.Codigo import Codigo


class Etiqueta(Codigo):

    def __init__(self, etiqueta, linea, columna):
        self.etiqueta = etiqueta
        self.linea = linea 
        self.columna = columna
    

    def optimizar(self, codigo):
        return super().optimizar(codigo)
    
    def Concatenar(self, codigo):
        
        return {"etiqueta":self.etiqueta,"linea":self.linea}