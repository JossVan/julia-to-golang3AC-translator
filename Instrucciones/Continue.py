from Abstractas.NodoAST import NodoAST
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Errores import Errores
class Continue(NodoAST):

    def __init__(self, fila, columna):
        self.fila = fila 
        self.columna = columna
    
    def ejecutar(self, tree, table):
        return self
    
    def traducir(self, tree, table, keep):
        
        if keep.etiquetaContinue != "":
            return {"continue":self,"cad":"goto "+keep.etiquetaContinue+";\n"}
        else:
            return Errores("Error de sentencia","Semántico","No se puede usar continue en esta sentencia",self.fila,self.columna)
    
    def getNodo(self):
        NuevoNodo = NodoArbol("CONTINUE")
        NuevoNodo.agregarHijo("continue")
        NuevoNodo.agregarHijo(";")
        return NuevoNodo
