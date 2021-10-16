from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Errores import Errores
from Abstractas.NodoAST import NodoAST

class Identificador(NodoAST):

    def __init__(self, id, fila, columna):
        self.id = id 
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):
        id = self.id
        self.id = self.id.lower()
        resultado = table.BuscarIdentificador(self.id)
        if resultado == None:
            tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
            return
        b = resultado.getValor()
        return b
    
    def traducir(self, tree, table, keep):
        id = self.id
        self.id = self.id.lower()
        resultado = table.BuscarIdentificador(self.id)
        if resultado == None:
            tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
            return
        apuntador = resultado.getApuntador()
        tipo = resultado.getTipo()
        return {"apuntador":apuntador, "tipo":tipo}

    def getNodo(self):
        NuevoNodo = NodoArbol("ID")
        NuevoNodo.agregarHijo(self.id)
        return NuevoNodo
        