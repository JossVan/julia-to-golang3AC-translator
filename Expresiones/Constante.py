from Abstractas.Objeto import TipoObjeto
from Abstractas.NodoArbol import NodoArbol
from Objetos.Primitivos import Primitivo
from Abstractas.NodoAST import NodoAST
from Objetos.KeepData import KeepData
class Constante(NodoAST):

    def __init__(self, valor, fila, columna):
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def ejecutar(self, tree, table):
        if isinstance(self.valor,Primitivo):
            if self.valor.tipo == TipoObjeto.CADENA:
                return self.valor.toString()
            elif self.valor.tipo == TipoObjeto.ENTERO:
                return self.valor.getEntero()
            elif self.valor.tipo == TipoObjeto.DECIMAL:
                return self.valor.getFloat()
            elif self.valor.tipo == TipoObjeto.BOOLEANO:
                return self.valor.getBoolean()
            elif self.valor.tipo == TipoObjeto.NEGATIVO:
                resultado = self.valor.valor.ejecutar(tree,table)
                return resultado * (-1)
            elif self.valor.tipo == TipoObjeto.NOTHING:
                resultado = "nothing"
            return resultado
    
    def traducir(self, tree, table, keep):
        if isinstance(self.valor,Primitivo):
            if self.valor.tipo == TipoObjeto.CADENA:
                cad = self.valor.toString()
                keep.generarC3D_Cadenas(cad) 
                return cad
            elif self.valor.tipo == TipoObjeto.ENTERO:
                return self.valor.getEntero()
            elif self.valor.tipo == TipoObjeto.DECIMAL:
                return self.valor.getFloat()
            elif self.valor.tipo == TipoObjeto.BOOLEANO:
                valor = self.valor.getBoolean()
                return valor
            elif self.valor.tipo == TipoObjeto.NOTHING:
                self.generarC3D_Cadenas(keep,self.valor.toString())
                return "nothing"
            elif self.valor.tipo == TipoObjeto.NEGATIVO:
                Valor = self.valor.valor.traducir(tree,table,keep)
                temporal = keep.getNuevoTemporal()
                keep.addOperacion(temporal,Valor,"*","-1") 
                resultado = self.valor.valor.ejecutar(tree,table)
                return resultado * (-1)

            
                
    def getNodo(self):
        NuevoNodo = NodoArbol("Constante")
        if self.valor.tipo == TipoObjeto.CADENA:
            NuevoNodo.agregarHijo("String")
            NuevoNodo.agregarHijo(self.valor.toString())
        elif self.valor.tipo == TipoObjeto.ENTERO:
            NuevoNodo.agregarHijo("Int64")
            NuevoNodo.agregarHijo(str(self.valor.getEntero()))
        elif self.valor.tipo == TipoObjeto.DECIMAL:
            NuevoNodo.agregarHijo("Float64")
            NuevoNodo.agregarHijo(str(self.valor.getFloat()))
        elif self.valor.tipo == TipoObjeto.BOOLEANO:
            NuevoNodo.agregarHijo("Bool")
            NuevoNodo.agregarHijo(str(self.valor.getBoolean()))
        elif self.valor.tipo == TipoObjeto.NEGATIVO:
            if isinstance(self.valor, NodoAST):
                NuevoNodo.agregarHijoNodo("-"+ self.valor.getNodo())
        return NuevoNodo

    
