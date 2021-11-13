from optimizacion.Codigo import Codigo
from optimizacion.Pila import Pila
from optimizacion.Declaracion import Declaracion
from optimizacion.Funcion import Funcion
class Encabezado(Codigo):

    def __init__(self, paquete,importaciones,heap,stack,declaraciones,funciones):
        self.paquete = paquete
        self.importaciones = importaciones
        self.heap = heap 
        self.stack = stack 
        self.declaraciones = declaraciones
        self.funciones = funciones 
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)

    def Concatenar(self,codigo):
        codigo.addCodigo("package main;\n")
        codigo.addCodigo("import (")
        cod = ""
        print(self.importaciones)
        tam = len(self.importaciones)
        contador = 1
        for importe in self.importaciones:
            cod += "\""+importe+"\""
            if contador< tam:
                cod+= ";"
            contador = contador+1
        cod += ");\n"
        codigo.addCodigo(cod) 
        if isinstance(self.heap,Pila):
            self.heap.Concatenar(codigo)
        if isinstance(self.stack,Pila):
            self.stack.Concatenar(codigo)
        
        for declaracion in self.declaraciones:
            if isinstance(declaracion,Declaracion):
                declaracion.Concatenar(codigo)


        for funcion in self.funciones:
            if isinstance(funcion,Funcion):
                funcion.Concatenar(codigo)