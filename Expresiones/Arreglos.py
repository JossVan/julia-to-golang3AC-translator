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
        cont = 0
        for i in arreglo:
            if isinstance(i,list):
                cont= cont+1
                for j in i:
                    if isinstance(j,list):
                        cont = cont+1
                        for k in j:
                            if isinstance(k,list):
                                cont = cont+1
                                break
                        break
                break
        if cont == 0:
            inferior = 0
            sup = len(arreglo)-1
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
        elif cont == 1:
            dim = 2
            # ASIGNANDO ESPACIOS EN EL HEAP
            T1 = keep.getNuevoTemporal()
            codigo = "// ***** ASIGNANDO ESPACIO EN EL HEAP PARA ARRAY 2D ******\n"
            codigo += keep.addIgual(T1,"HP")
            #ALMACENANDO DIMENSIÓN EN EL HEAP
            codigo += keep.addIgual(keep.getValHeap("HP"),dim)
            codigo += keep.addOperacion("HP","HP","+","1")
            #ALMACENANDO EL VALOR INFERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),0)
            codigo += keep.addOperacion("HP","HP","+","1")
            primerosuperior = len(arreglo)
            #ALMACENANDO EL VALOR SUPERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),primerosuperior-1)
            codigo += keep.addOperacion("HP","HP","+","1")
            #ALMACENANDO EL VALOR INFERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),0)
            codigo += keep.addOperacion("HP","HP","+","1")
            for dim in arreglo:
                if isinstance(dim,list):
                    superior = 0
                    for valor in dim:
                        superior = superior+1
                    #ALMACENANDO EL VALOR SUPERIOR DE LA DIMENSIÓN
                    codigo += keep.addIgual(keep.getValHeap("HP"),superior)
                    codigo += keep.addOperacion("HP","HP","+","1")
                    break
            codigo += keep.addIgual(keep.getValHeap("HP"),len(arreglo))
            codigo += keep.addOperacion("HP","HP","+","1")
            for dim in arreglo:
                if isinstance(dim,list):
                    for valor in dim:
                        if isinstance(valor,NodoAST):
                            resultado = valor.traducir(tree,table,keep)
                            if isinstance(resultado,int) or isinstance(resultado,float):
                                #ALMACENANDO EL VALOR SUPERIOR DE LA DIMENSIÓN
                                codigo += keep.addIgual(keep.getValHeap("HP"),resultado)
                                codigo += keep.addOperacion("HP","HP","+","1")
                            elif isinstance(resultado,dict):
                                if "apuntador" in resultado:
                                    T2 = keep.getNuevoTemporal()
                                    T3 = keep.getNuevoTemporal()
                                    codigo+= keep.addOperacion(T2,"SP","+",resultado["apuntador"])
                                    codigo += keep.addIgual(T3,keep.getValStack(T2))
                                    codigo += keep.addIgual(keep.getValHeap("HP"),T3)
                                    codigo += keep.addOperacion("HP","HP","+","1")
                                    keep.liberarTemporales(T2)
                                    keep.liberarTemporales(T3)
                                elif "temp" in resultado:
                                    codigo += keep.addIgual(keep.getValHeap("HP"),resultado["temp"])
                                    codigo += keep.addOperacion("HP","HP","+","1")
            temp = keep.getNuevoTemporal()
            codigo += keep.addOperacion(temp,"SP","+",keep.getStack())
            codigo += keep.addIgual(keep.getValStack(temp),T1)
            keep.liberarTemporales(temp)
            keep.liberarTemporales(T1)
            keep.addCodigo(codigo)  
        elif cont == 2:
            dim = 3
            # ASIGNANDO ESPACIOS EN EL HEAP
            T1 = keep.getNuevoTemporal()
            codigo = "// ***** ASIGNANDO ESPACIO EN EL HEAP PARA ARRAY 3D ******\n"
            codigo += keep.addIgual(T1,"HP")
            #ALMACENANDO DIMENSIÓN EN EL HEAP
            codigo += keep.addIgual(keep.getValHeap("HP"),dim)
            codigo += keep.addOperacion("HP","HP","+","1")
            #ALMACENANDO EL VALOR INFERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),0)
            codigo += keep.addOperacion("HP","HP","+","1")
            primerosuperior = len(arreglo)
            #ALMACENANDO EL VALOR SUPERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),primerosuperior-1)
            codigo += keep.addOperacion("HP","HP","+","1")
            #ALMACENANDO EL VALOR INFERIOR DE LA DIMENSIÓN
            codigo += keep.addIgual(keep.getValHeap("HP"),0)
            codigo += keep.addOperacion("HP","HP","+","1")
            for dim in arreglo:
                if isinstance(dim,list):
                    superior = 0
                    for valor in dim:
                        superior = superior+1
                        superior2 = 0
                        for val in valor:
                            superior2 = superior2 +1
                    #ALMACENANDO EL VALOR SUPERIOR 2 DE LA DIMENSIÓN
                    codigo += keep.addIgual(keep.getValHeap("HP"),superior-1)
                    codigo += keep.addOperacion("HP","HP","+","1")  
                    #ALMACENANDO EL VALOR INFERIOR 3 DE LA DIMENSIÓN
                    codigo += keep.addIgual(keep.getValHeap("HP"),0)
                    codigo += keep.addOperacion("HP","HP","+","1") 
                    #ALMACENANDO EL VALOR SUPERIOR 3 DE LA DIMENSIÓN
                    codigo += keep.addIgual(keep.getValHeap("HP"),superior2-1)
                    codigo += keep.addOperacion("HP","HP","+","1")   
                    break
            codigo += keep.addIgual(keep.getValHeap("HP"),len(arreglo))
            codigo += keep.addOperacion("HP","HP","+","1")
            for dim in arreglo:
                if isinstance(dim,list):
                    for valor in dim:
                        for val in valor:
                            if isinstance(val,NodoAST):
                                resultado = val.traducir(tree,table,keep)
                                if isinstance(resultado,int) or isinstance(resultado,float):
                                    #ALMACENANDO EL VALOR SUPERIOR DE LA DIMENSIÓN
                                    codigo += keep.addIgual(keep.getValHeap("HP"),resultado)
                                    codigo += keep.addOperacion("HP","HP","+","1")
                                elif isinstance(resultado,dict):
                                    if "apuntador" in resultado:
                                        T2 = keep.getNuevoTemporal()
                                        T3 = keep.getNuevoTemporal()
                                        codigo+= keep.addOperacion(T2,"SP","+",resultado["apuntador"])
                                        codigo += keep.addIgual(T3,keep.getValStack(T2))
                                        codigo += keep.addIgual(keep.getValHeap("HP"),T3)
                                        codigo += keep.addOperacion("HP","HP","+","1")
                                        keep.liberarTemporales(T2)
                                        keep.liberarTemporales(T3)
                                    elif "temp" in resultado:
                                        codigo += keep.addIgual(keep.getValHeap("HP"),resultado["temp"])
                                        codigo += keep.addOperacion("HP","HP","+","1")
            temp = keep.getNuevoTemporal()
            codigo += keep.addOperacion(temp,"SP","+",keep.getStack())
            codigo += keep.addIgual(keep.getValStack(temp),T1)
            keep.liberarTemporales(temp)
            keep.liberarTemporales(T1)
            keep.addCodigo(codigo)
            print("DIMENSIÓN 3")
        
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