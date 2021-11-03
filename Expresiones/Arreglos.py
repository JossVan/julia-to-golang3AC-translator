from Abstractas.NodoArbol import NodoArbol
from Abstractas.NodoAST import NodoAST
class Arreglos(NodoAST):

    def __init__(self, contenido, fila, columna):
        self.contenido = contenido
        self.fila = fila 
        self.columna = columna
        self.contador = 0
    
    def ejecutar(self, tree, table):
        
        for dimension in self.contenido:
            if not isinstance(dimension,list):
                break
        arreglo = self.convertir(tree,table,self.contenido,[])
        return arreglo

    def traducir(self, tree, table, keep):
        
        arreglo = self.convertir(tree,table,self.contenido,[])
        cant = len(arreglo)
        inferior = 0
        sup = cant-1
        # GUARDANDO INFORMACIÓN DEL ARREGLO EN EL STACK Y HEAP
        T1 = keep.getNuevoTemporal()
        T2 = keep.getNuevoTemporal()
        cod = keep.addOperacion(T1,"SP","+",keep.getStack())
        cod += keep.addIgual(T2,"HP")
        cod += keep.addIgual(keep.getValHeap("HP"),"1")
        cod += keep.addOperacion("HP","HP","+","1")
        cod += keep.addIgual(keep.getValHeap("HP"),inferior)
        cod += keep.addOperacion("HP","HP","+","1")
        cod += keep.addIgual(keep.getValHeap("HP"),sup)
        cod += keep.addOperacion("HP","HP","+","1")
        
        for item in arreglo:
            if isinstance(item,NodoAST):
                val = item.traducir(tree,table,keep)
                if isinstance(val,int) or isinstance(val,float):
                    cod += keep.addIgual(keep.getValHeap("HP"),val)
                    cod += keep.addOperacion("HP","HP","+","1")
                elif isinstance(val,dict):
                    if "temp" in val:
                        cod += keep.addIgual(keep.getValHeap("HP"),val["temp"])
                        cod += keep.addOperacion("HP","HP","+","1")
                    elif "apuntador" in val:
                        T3 = keep.getNuevoTemporal()
                        T4 = keep.getNuevoTemporal()
                        cod += keep.addOperacion(T3,"SP","+",val["apuntador"])
                        cod += keep.addOperacion(T4,keep.getValStack(T3))
                        cod += keep.addIgual(keep.getValHeap("HP"),T4)
                        cod += keep.addOperacion("HP","HP","+","1")
                        keep.liberarTemporales(T3)
                        keep.liberarTemporales(T4)
        cod += keep.addIgual(keep.getValStack(T1),T2)
        keep.addCodigo(cod)
        keep.liberarTemporales(T1)
        keep.liberarTemporales(T2)
        return arreglo

    def convertir(self,tree,table,item,lista):

        if isinstance(item, list):
            for i in item:
                self.convertir(tree,table,i,lista)
        elif isinstance(item, Arreglos):
            valor = item.ejecutar(tree,table)
            lista.append(valor)
        else:
            lista.append(item)
        return lista

    def aumentar(self):
        self.contador+1
        
    def getLength(self):
        return len(self.contenido)

    def getNodo(self):
        NodoPadre = NodoArbol("Arreglo")
        NodoPadre.agregarHijo("[")
        cont = 1
        for dimension in self.contenido:
            if isinstance(dimension, NodoAST):
                nodo = dimension.getNodo()
                NodoPadre.agregarHijoNodo(nodo)
                if cont< len(self.contenido):
                    NodoPadre.agregarHijo(",")
                    cont = cont+1
        NodoPadre.agregarHijo("]")
        return NodoPadre