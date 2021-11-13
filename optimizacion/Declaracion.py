from optimizacion.Codigo import Codigo
from optimizacion.Variable import Variable

class Declaracion(Codigo):

    def __init__(self, var, lista, tipo, linea, columna):
        self.var = var
        self.lista =lista
        self.tipo = tipo 
        self.linea = linea 
        self.columna = columna


    def Concatenar(self, codigo):
        
        cod = self.var+" "
        tam = len(self.lista)
        contador = 1
        for variable in self.lista:
            if isinstance(variable,Variable):
                cod+= variable.variable
                if contador < tam:
                    cod+= ","
            contador = contador + 1
        cod += " "+self.tipo+";\n"
        codigo.addCodigo(cod)

    def optimizar(self, codigo):
        return super().optimizar(codigo)