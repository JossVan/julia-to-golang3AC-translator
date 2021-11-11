from optimizacion.Asignacion import Asignacion
from optimizacion.Codigo import Codigo


class Funcion(Codigo):

    def __init__(self, nombre, instrucciones, linea, columna) -> None:
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        cod = self.nombre+"(){\n"
        codigo.addCodigo(cod)
        anterior = None 
        contador = 0
        tam = len(self.instrucciones)
        while contador < tam:
            if isinstance(self.instrucciones[contador],Codigo):
                resultado = self.instrucciones[contador].Concatenar(codigo)
                if isinstance(resultado,Asignacion):
                    if (contador+1) < tam:
                        resultado2 = self.instrucciones[contador + 1].Concatenar(codigo)
                        if isinstance(resultado2,Asignacion):
                            print("")
        codigo.addCodigo("}")

    def optimizar(self, codigo):
        return super().optimizar(codigo)
    