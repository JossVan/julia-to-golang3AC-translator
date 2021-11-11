from optimizacion.Codigo import Codigo


class Pila(Codigo):

    def __init__(self, nombre, numero, tipo, linea,columna):
        self.nombre = nombre 
        self.numero = numero 
        self.tipo = tipo 
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        cod ="var " +self.nombre+"["+ str(self.numero)+"] "+self.tipo+";\n"
        codigo.addCodigo(cod)

    def optimizar(self, codigo):
        return super().optimizar(codigo)