from Abstractas.NodoAST import NodoAST
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Errores import Errores
from Expresiones.Arreglos import Arreglos

class Array(NodoAST):

    def __init__(self, id, posicion, fila, columna):
        self.id = id 
        self.posicion = posicion
        self.fila = fila 
        self.columna = columna
    

    def ejecutar(self, tree, table):
        
        id = self.id
        self.id = self.id.lower()
        resultado = table.BuscarIdentificador(self.id)
        if resultado == None:
            tree.insertError(Errores(id,"Semántico","No definida", self.fila,self.columna))
            return
        b = resultado.getValor()
        array = []
        if isinstance(self.posicion, list):    
            for posi in self.posicion:
                if isinstance(posi, NodoAST):
                    valor = posi.ejecutar(tree,table)
                    array.append(valor)
                elif isinstance(posi, int):
                    array.append(valor)
                else:
                    err = Errores(posi,"Semántico","Valor no reconocido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
        if len(array) == 1:
            if isinstance(b, list):
                if array[0] -1 >= 0:
                    h = self.desanidar(tree,table,b)
                    nodito = h[array[0]-1]
                    if isinstance(nodito, NodoAST):
                        nodito = nodito.ejecutar(tree,table)
                        return nodito
                    return nodito
                    
                else : 
                    err = Errores(str(array[0]-1),"Semántico","Desbordamiento de arreglo", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            else:
                err = Errores(b,"Semántico","Valor no reconocido", self.fila,self.columna)
                tree.insertError(err)
                return err
        elif len(array) == 2:
            if isinstance(b, list):
                pos1 = array[0]-1
                pos2 = array[1]-1
                if pos1 >= 0 and pos2 >=0:
                    nodito = b[pos1][pos2]
                    if isinstance(nodito, NodoAST):
                        nodito = nodito.ejecutar(tree,table)
                        return nodito
                    return nodito  
                else : 
                    err = Errores(str(array[0]-1),"Semántico","Desbordamiento de arreglo", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            else:
                err = Errores(b,"Semántico","Valor no reconocido", self.fila,self.columna)
                tree.insertError(err)
                return err

        elif len(array) == 3:
            if isinstance(b, list):
                pos1 = array[0]-1
                pos2 = array[1]-1
                pos3 = array[2]-1
                if pos1 >= 0 and pos2 >=0 and pos3 >=0:
                    nodito = b[pos1][pos2][pos3]
                    if isinstance(nodito, NodoAST):
                        nodito = nodito.ejecutar(tree,table)
                        return nodito
                    elif isinstance(nodito,list):
                        lista = []
                        for v in nodito :
                            if isinstance(v,NodoAST):
                                valor = v.ejecutar(tree,table)
                                lista.append(valor)
                            else:
                                lista.append(v)
                        return lista
                    return nodito  
                else : 
                    err = Errores(str(array[0]-1),"Semántico","Desbordamiento de arreglo", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            else:
                err = Errores(b,"Semántico","Valor no reconocido", self.fila,self.columna)
                tree.insertError(err)
                return err

    def traducir(self, tree, table, keep):    
        id = self.id
        self.id = self.id.lower()
        resultado = table.BuscarIdentificador(self.id)
        if resultado == None:
            tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
            return
        apuntador = resultado.getApuntador()
        tipo = resultado.getTipo()
        T1 = keep.getNuevoTemporal()
        T2 = keep.getNuevoTemporal()
        T3 = keep.getNuevoTemporal()
        T4 = keep.getNuevoTemporal()
        T5 = keep.getNuevoTemporal()
        T6 = keep.getNuevoTemporal()
        T7 = keep.getNuevoTemporal()
        T8 = keep.getNuevoTemporal()
        T9 = keep.getNuevoTemporal()
        T10 = keep.getNuevoTemporal()
        T11 = keep.getNuevoTemporal()
        T12 = keep.getNuevoTemporal()
        #T13 = keep.getNuevoTemporal()
        cod = "//***** INICIANDO ACCESO A LA POSICIÓN DEL ARREGLO*****\n"
        cod += keep.addOperacion(T1,"SP","+",apuntador)
        cod += keep.addIgual(T2,keep.getValStack(T1))
        #PARA VERIFICAR EL LÍMITE SUPERIOR
        cod += keep.addOperacion(T11,T2,"+","2")
        # ACCEDIENDO AL VALOR DEL LÍMITE SUPERIOR
        cod += keep.addIgual(T12,keep.getValHeap(T11))
        cod += keep.addOperacion(T12,T12,"+","1")

        cod += keep.addOperacion(T3,T2,"+","1")
        #accediendo al límite inferior
        cod += keep.addIgual(T4,keep.getValHeap(T3))
        # ACCEDER AL PARÁMETRO SOLICITADO
        if isinstance(self.posicion,list):
            for pos in self.posicion:
                if isinstance(pos,NodoAST):
                    valor = pos.traducir(tree,table,keep)
                    if isinstance(valor,int) or isinstance(valor,float):
                        L1 = keep.getNuevaEtiqueta()
                        L2 = keep.getNuevaEtiqueta()
                        cod += "if "+str(valor)+"<= "+T12+"{goto "+L1+";}\n"
                        keep.addCodigo(cod)
                        keep.errorDimension()
                        cod = "goto "+ L2+";\n"
                        cod += L1+":\n"
                        cod += keep.addOperacion(T5,(valor-1),"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA
                        cod += keep.addOperacion(T6,T2,"+","3") #PRIMERA POSICIÓN DEL ARREGLO
                        cod += keep.addOperacion(T7,T6,"+",T5) #POSICIÓN REAL DEL HEAP
                        cod += keep.addIgual(T8,keep.getValHeap(T7))
                        if isinstance(valor,int):
                            valor = "Int64"
                        elif isinstance(valor,float):
                            valor = "Float64"
                        cod += L2+":\n"
                        keep.addCodigo(cod)
                        return {"temp": T8, "valor":None, "tipo":valor}
                    elif isinstance(valor,dict):
                        if "apuntador" in valor:
                            cod += keep.addOperacion(T9,"SP","+",valor["apuntador"])
                            cod += keep.addIgual(T10,keep.getValStack(T9))
                            cod += keep.addOperacion(T10,T10,"-","1")
                            L1 = keep.getNuevaEtiqueta()
                            L2 = keep.getNuevaEtiqueta()
                            cod += "if "+T10+"<= "+T12+"{goto "+L1+";}\n"
                            keep.errorDimension()
                            keep.addCodigo(cod)
                            cod = "goto "+ L2+";\n"
                            cod += L1+":\n"
                            cod += keep.addOperacion(T5,T10,"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA
                            cod += keep.addOperacion(T6,T2,"+","3") #PRIMERA POSICIÓN DEL ARREGLO
                            cod += keep.addOperacion(T7,T6,"+",T5) #POSICIÓN REAL DEL HEAP
                            cod += keep.addIgual(T8,keep.getValHeap(T7))
                            cod += L2+":\n"
                            keep.addCodigo(cod)
                            return {"temp": T8, "valor":None, "tipo":valor["tipo"]}
                        elif "temp" in valor:
                            cod += keep.addOperacion(T10,valor["temp"],"-","1")
                            L1 = keep.getNuevaEtiqueta()
                            L2 = keep.getNuevaEtiqueta()
                            cod += "if "+T10+"<= "+T12+"{goto "+L1+";}\n"
                            keep.errorDimension()
                            keep.addCodigo(cod)
                            cod = "goto "+ L2+";\n"
                            cod += L1+":\n"
                            cod += keep.addOperacion(T5,T10,"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA
                            cod += keep.addOperacion(T6,T2,"+","3") #PRIMERA POSICIÓN DEL ARREGLO
                            cod += keep.addOperacion(T7,T6,"+",T5) #POSICIÓN REAL DEL HEAP
                            cod += keep.addIgual(T8,keep.getValHeap(T7))
                            cod += L2+":\n"
                            keep.addCodigo(cod)
                            return {"temp": T8, "valor":None, "tipo":valor["tipo"]}
        keep.liberarTemporales(T1)
        keep.liberarTemporales(T2)
        keep.liberarTemporales(T3)
        keep.liberarTemporales(T4)
        keep.liberarTemporales(T5)
        keep.liberarTemporales(T6)
        keep.liberarTemporales(T7)
        keep.liberarTemporales(T8)
        keep.liberarTemporales(T9)
        keep.liberarTemporales(T10)

    def actualizar(self, valor, tree, table, keep):
        id = self.id
        self.id = self.id.lower()
        resultado = table.BuscarIdentificador(self.id)
        if resultado == None:
            tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
            return
        apuntador = resultado.getApuntador()
        tipo = resultado.getTipo()
        T1 = keep.getNuevoTemporal()
        T2 = keep.getNuevoTemporal()
        T3 = keep.getNuevoTemporal()
        T4 = keep.getNuevoTemporal()
        T5 = keep.getNuevoTemporal()
        T6 = keep.getNuevoTemporal()
        T7 = keep.getNuevoTemporal()
        
        if isinstance(self.posicion, list):
            array = []
            for pos in self.posicion:
                posi = pos.traducir(tree,table,keep)
                array.append(posi)
            if len(array) == 2:
                val = valor.ejecutar(tree,table)
                resultado = table.actualiarValorPosicionMatriz(val,array[0],array[1],self.id,tree)
            elif len(array) == 3:
                val = valor.ejecutar(tree,table)
                resultado = table.actualiarValorPosicionDimension3(val,array[0],array[1],array[2],self.id,tree)
            else:
                # VERIFICAMOS EL INDICE EN LA QUE SE QUIERE INGRESAR LA INFORMACIÓN
                val = valor.traducir(tree,table,keep)
                temp = keep.getNuevoTemporal()
                temp2 = keep.getNuevoTemporal()
                codigo = "// *****ASIGNANDO NUEVO VALOR A UN INDICE DEL ARREGLO*****\n"
                codigo += keep.addOperacion(T1,"SP","+", apuntador)
                codigo += keep.addIgual(T2,keep.getValStack(T1)) #SE OBTIENE EL VALOR DEL STACK
                codigo += keep.addOperacion(T3,T2,"+","1") # SE OBTIENE LA POSICIÓN DONDE SE ALMANCENA EL VALOR INFERIOR DEL ARRAY
                codigo += keep.addIgual(T4,keep.getValHeap(T3)) #SE OBTIENE EL VALOR INFERIOR DEL ARREGLO
                codigo += keep.addOperacion(temp,T2,"+","2")
                codigo += keep.addIgual(temp2,keep.getValStack(temp))
                codigo += keep.addOperacion(temp2,temp2,"+","1")
                if isinstance(posi,int):      
                    L1 = keep.getNuevaEtiqueta()
                    L2 = keep.getNuevaEtiqueta()
                    codigo += "if "+str(posi-1)+"<= "+temp2+"{goto "+L1+";}\n"
                    keep.addCodigo(codigo)
                    keep.errorDimension()
                    codigo  = "goto "+L2+";\n"
                    codigo += L1+":\n"
                    codigo += keep.addOperacion(T5,(posi-1),"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA LINEAL DE DATOS
                elif isinstance(posi,dict):
                    if "apuntador" in posi:
                        T10 = keep.getNuevoTemporal()
                        T11 = keep.getNuevoTemporal()
                        T12 = keep.getNuevoTemporal()
                        codigo += "// *****ACCEDIENDO A LA VARIABLE APUNTADOR*****\n"
                        codigo += keep.addOperacion(T10,"SP","+",posi["apuntador"])
                        codigo += keep.addIgual(T11,keep.getValStack(T10))
                        codigo += keep.addOperacion(T12,T11,"-","1")
                        L1 = keep.getNuevaEtiqueta()
                        L2 = keep.getNuevaEtiqueta()
                        codigo += "if "+T12+"<= "+temp2+"{goto "+L1+";}\n"
                        keep.addCodigo(codigo)
                        keep.errorDimension()
                        codigo = "goto "+L2+";\n"
                        codigo += L1+":\n"
                        codigo += keep.addOperacion(T5,T12,"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA LINEAL DE DATOS
                        keep.liberarTemporales(T10)
                        keep.liberarTemporales(T11)
                        keep.liberarTemporales(T12)
                    elif "temp" in posi:
                        T12 = keep.getNuevoTemporal()
                        codigo += keep.addIgual(T12,posi["temp"],"-","1")
                        L1 = keep.getNuevaEtiqueta()
                        L2 = keep.getNuevaEtiqueta()
                        codigo += "if "+T12+"<= "+temp2+"{goto "+L1+";}\n"
                        keep.addCodigo(codigo)
                        keep.errorDimension()
                        codigo = "goto "+L2+";\n"
                        codigo += L1+":\n"
                        codigo += keep.addOperacion(T5,T12,"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA LINEAL DE DATOS
                        keep.liberarTemporales(T12)
                codigo += keep.addOperacion(T6, T5,"+",T2)
                codigo += keep.addOperacion(T7,T6,"+","3")
                if isinstance(val,int):
                    codigo += keep.addIgual(keep.getValHeap(T7),val) #se actualiza el valor
                    keep.addCodigo(codigo)
                elif isinstance(val,dict):
                    if "apuntador" in val:
                        T8 = keep.getNuevoTemporal()
                        T9 = keep.getNuevoTemporal()
                        codigo += keep.addIOperacion(T8,"SP","+",val["apuntador"])
                        codigo += keep.addIgual(T9, keep.getValStack(T8))
                        codigo += keep.addIgual(keep.getValHeap(T7),T9) #se actualiza el valor
                        keep.addCodigo(codigo)
                        keep.liberarTemporales(T8)
                        keep.liberarTemporales(T9)
                    elif "temp" in val:
                        codigo += keep.addIgual(keep.getValHeap(T7),val["temp"]) #se actualiza el valor
                        keep.addCodigo(codigo)
            if resultado == None:
                    err = Errores(id,"Semántico","Variable indefinida", self.fila,self.columna)
                    tree.insertError(err)
                    return err
        keep.addCodigo(L2+":\n")
        keep.liberarTemporales(T1)
        keep.liberarTemporales(T2)
        keep.liberarTemporales(T3)
        keep.liberarTemporales(T4)
        keep.liberarTemporales(T5)
        keep.liberarTemporales(T6)
        keep.liberarTemporales(T7)
    def insertar(self,valor,tree,table):
        #id = self.id
        self.id = self.id.lower()
        posi = 0
        if isinstance(self.posicion, list):
            array = []
            for pos in self.posicion:
                posi = pos.ejecutar(tree,table)
                array.append(posi)
        
        traerValor = table.BuscarIdentificador(self.id)
        if isinstance(traerValor.valor, list):
            h = self.desanidar(tree,table,traerValor.valor)
            if len(array) == 1:
                nueva = []
                if isinstance(valor, list):
                    for i in valor:
                        if isinstance(i,Arreglos):
                            v = i.contenido
                            if isinstance(v,list):
                                for val in v:
                                    if isinstance(val,NodoAST):
                                        valorcito = val.ejecutar(tree,table)
                                        nueva.append(valorcito)
                            else:
                                nueva.append(v)
                        else:
                            nueva.append(i)
                    valor = nueva
                h[posi-1].append(valor)
                traerValor.valor = h
                table.actualizarValor(self.id,traerValor.valor)
            return traerValor.valor

    def getNodo(self):
        nodoPadre = NodoArbol("Array")
        nodoId = NodoArbol("Identificador")
        nodoId.agregarHijo(self.id)
        nodoPadre.agregarHijoNodo(nodoId)
        nodopos = NodoArbol("Posición")
        nodopos.agregarHijo("[")
        if isinstance(self.posicion,list):
            for pos in self.posicion:
                nodopos.agregarHijoNodo(pos.getNodo())     
        nodopos.agregarHijo("]")    
        nodoPadre.agregarHijoNodo(nodopos)
        return nodoPadre
    
    
    def desanidar(self,tree,table,item):
        contador = 0
        if isinstance(item,list):
            for i in item:
                if isinstance(i,list):
                    self.desanidar(tree,table,i)
                elif isinstance(i,Arreglos):
                    result = i.ejecutar(tree,table)
                    
                    item[contador] = result 

                contador = contador +1
            return item
            
    def ejecutarMatriz(self,tree,table,array,nuevo):

        if isinstance(array,list):
            for arreglo in array:
                if isinstance(arreglo,Arreglos):
                    contenido = arreglo.ejecutar(tree,table)
                    nuevo.append(contenido)
                elif isinstance(arreglo,list):
                    self.ejecutarMatriz(tree,table,arreglo,nuevo)
        elif isinstance(array, Arreglos):
            contenido = array.ejecutar(tree,table)
            nuevo.append(contenido)

        return nuevo
    