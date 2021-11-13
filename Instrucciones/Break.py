
from Abstractas.NodoArbol import NodoArbol
from Abstractas.NodoAST import NodoAST

from Abstractas.NodoAST import NodoAST
from TablaSimbolos.Errores import Errores

class Break(NodoAST):

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def ejecutar(self, tree, table):
        return self
    def traducir(self, tree, table, keep):
        
        if keep.etiquetaBreak != "":
            return {"break":self,"cad":"goto "+keep.etiquetaBreak+";\n"}
        else:
            return Errores("Error de sentencia","Semántico","No se puede usar break en esta sentencia",self.fila,self.columna)


    def getNodo(self):
        NuevoNodo = NodoArbol("BREAK")
        NuevoNodo.agregarHijo("break")
        NuevoNodo.agregarHijo(";")
        return NuevoNodo