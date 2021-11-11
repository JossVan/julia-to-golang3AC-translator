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
        if isinstance(self.posicion, list):
            array = []
            for pos in self.posicion:
                posi = pos.traducir(tree,table,keep)
                array.append(posi)
            if len(array) == 2:
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
                T13 = keep.getNuevoTemporal()
                T14 = keep.getNuevoTemporal()
                if isinstance(array[0],int) or isinstance(array[0],float):
                    #si entra aqui es porque el primer indice es un número
                    indice1 = array[0]
                    codigo = "//***** Calculando el primer indice *****\n"
                elif isinstance(array[0],dict):
                    if "apuntador" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addOperacion(temp,"SP","+",array[0]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        codigo += "//***** Calculando el primer indice *****\n"
                        indice1 = temp
                    elif "temp" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addIgual(temp,array[0]["temp"])
                        codigo += "//***** Calculando el primer indice *****\n"
                        indice1 = temp
                    
                # guardando el apuntador del stack del arreglo
                codigo += "//Encuentro el índice del stack donde está almacenada la primera posición del heap\n"
                codigo += keep.addOperacion(T1,"SP","+",apuntador)
                # OBTENIENDO LA POSICIÓN DEL HEAP EN DONDE INICIA LA ESTRUCTURA
                codigo += "//Almaceno el valor de la primera posición del heap de la estructura.\n"
                codigo += keep.addIgual(T2,keep.getValStack(T1))
                # OBTENIENDO LA POSICIÓN DEL HEAP DONDE SE ENCUENTRA EL INF1
                codigo += "//Guardo la posición de donde se encuentra el valor inferior1 del array\n"
                codigo += keep.addOperacion(T3,T2,"+","1")            
                # SACANDO EL VALOR DE INF1 DEL HEAP
                codigo += "//Guardo el valor inferior1 del array\n"
                codigo += keep.addIgual(T4,keep.getValHeap(T3))
                #OBTENIENDO LA POSICIÓN DEL HEAP DONDE SE ENCUENTRA EL SUPERIOR 1
                codigo += "//Guardo el índice donde se encuentra el superior1 del array\n"
                codigo += keep.addOperacion(T13,T2,"+","2")
                # SACANDO EL VALOR DE SUPERIOR1 DEL HEAP
                codigo += "//Guardo el valor superior1 del array\n"
                codigo += keep.addIgual(T14,keep.getValHeap(T13))
                #AHORA SACAMOS EL INFERIOR Y SUPERIOR DE LA SEGUNDA DIM
                    #sacamos el inf2
                codigo += "//Guardo el índice de donde se encuentra el inferior2 del array\n"
                codigo += keep.addOperacion(T5,T2,"+","3")
                codigo += "//Guardo el valor del inferior2 del array\n"
                codigo += keep.addIgual(T6, keep.getValHeap(T5))
                    #sacamos el superior2
                codigo += "//Guardo el índice de donde se encuentra el superior2 del array\n"
                codigo += keep.addOperacion(T5,T2,"+","4")
                codigo += "//Guardo el valor del superior2 del array\n"
                codigo += keep.addIgual(T7, keep.getValHeap(T5))
                #ENCONTRAMOS N2
                codigo += "//Calculo N2 para la formula\n"
                codigo += keep.addOperacion(T8,T7,"-",T6)
                codigo += keep.addOperacion(T8,T8,"+","1")
                # ------------------APLICANDO LA FORMULA---------------------------
                codigo += "//****** Aplicando la fórmula para D2 ***** \n"
                codigo += keep.addOperacion(T9,indice1,"-",T4)
                codigo += keep.addOperacion(T10,T9,"*",T8)
                if isinstance(array[1],int) or isinstance(array[1],float):
                    indice2 = array[1]
                elif isinstance(array[1],dict):
                    if "apuntador" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[1]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        #codigo += keep.addOperacion(temp,temp,"-",1)
                        indice2 = temp
                    elif "temp" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[1]["temp"])
                        #codigo += keep.addOperacion(temp,temp,"-",1)
                        indice2 = temp
                L1 = keep.getNuevaEtiqueta()
                L2 = keep.getNuevaEtiqueta()
                L3 = keep.getNuevaEtiqueta()
                L4 = keep.getNuevaEtiqueta()
                L5 = keep.getNuevaEtiqueta()
                L6 = keep.getNuevaEtiqueta()
                codigo += "if "+str(indice1)+" >= 1 {goto "+L1+";}\n"
                codigo += "goto "+ L2+";\n"
                codigo += L1+":\n"
                codigo += keep.addOperacion(T14,T14,"+",1)
                codigo += "if "+str(indice1)+" <= "+T14+" {goto "+L3+";}\n"
                codigo += "goto "+ L2+";\n"
                codigo += L3+":\n"
                codigo += "if "+str(indice2)+" >= 1 {goto "+L4+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L4+":\n"
                #codigo += keep.addOperacion(T7,T7,"+",1)
                codigo += "if "+str(indice2)+" <= "+T7+"{goto "+L5+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L5+":\n"
                codigo += keep.addOperacion(T11,T10,"+",indice2)
                codigo += keep.addOperacion(T12,T11,"-",indice1)
                codigo += keep.addOperacion(T12,T12,"+",1)
                codigo += keep.addOperacion(T12,T2,"+",T12)        
                #keep.liberarTemporales(T2)
                #keep.liberarTemporales(T3)
                #keep.liberarTemporales(T4)
                #keep.liberarTemporales(T5)
                #keep.liberarTemporales(T6)
                #keep.liberarTemporales(T7)
                #keep.liberarTemporales(T8)
                #keep.liberarTemporales(T9)
                #keep.liberarTemporales(T10)
                #keep.liberarTemporales(T11)
                codigo += keep.addIgual(T1,keep.getValHeap(T12))
                codigo += "goto "+L6+";\n"
                codigo += L2+":\n"
                keep.addCodigo(codigo)
                if not "boundserror" in keep.listaFuncion:
                    cc = keep.codigo
                    keep.codigo = ""
                    keep.errorDimension()
                    keep.listaFuncion["boundserror"]= keep.codigo
                    keep.codigo = cc
                codigo = "boundserror();\n"
                codigo += L6+":\n"
                keep.addCodigo(codigo)
                return {"temp": T1, "valor":None, "tipo":"Float64"}
                #ARREGLO DE DOS DIMENSIONES
            elif len(array) == 3:
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
                T13 = keep.getNuevoTemporal()
                T14 = keep.getNuevoTemporal()

                # INICIANDO LA EXTRACCIÓN DE LOS DATOS NECESARIOS PARA ENCONTRAR LA POSICIÓN DEL ARREGLO
                codigo = "//********** ENCONTRANDO DATO EN EL ARREGLO 3D **********\n"
                codigo += keep.addOperacion(T1,"SP","+",apuntador)
                # posición inicial del heap donde está la estructura
                codigo += keep.addIgual(T1, keep.getValStack(T1))
                # indice del valor inferior1 
                codigo += keep.addOperacion(T2,T1,"+","1")
                # valor del inferior 1
                codigo += keep.addIgual(T3, keep.getValHeap(T2))
                # indice del valor superior 1
                codigo += keep.addOperacion(T4, T1,"+","2")
                # valor del superior 1
                codigo += keep.addIgual(T5,keep.getValHeap(T4))
                # indice del valor inferior2 
                codigo += keep.addOperacion(T6,T1,"+","3")
                # valor del inferior 2
                codigo += keep.addIgual(T7, keep.getValHeap(T6))
                # indice del valor superior 2
                codigo += keep.addOperacion(T8, T1,"+","4")
                # valor del superior 2
                codigo += keep.addIgual(T9,keep.getValHeap(T8))
                # indice del valor inferior3 
                codigo += keep.addOperacion(T10,T1,"+","5")
                # valor del inferior 3
                codigo += keep.addIgual(T11, keep.getValHeap(T10))
                # indice del valor superior 3
                codigo += keep.addOperacion(T12, T1,"+","6")
                # valor del superior 3
                codigo += keep.addIgual(T13,keep.getValHeap(T12))
                indice1 = None
                indice2 = None
                indice3 = None
                # INDICE 1
                if isinstance(array[0],int):
                    indice1 = array[0]
                elif isinstance(array[0],dict):
                    if "apuntador" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[0]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice1 = temp
                    elif "temp" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[0]["temp"])
                        indice1 = temp
                # INDICE 2 
                if isinstance(array[1],int):
                    indice2 = array[1]
                elif isinstance(array[1],dict):
                    if "apuntador" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[1]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice2 = temp
                    elif "temp" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[1]["temp"])
                        indice2 = temp
                # INDICE 3
                if isinstance(array[2],int):
                    indice3 = array[2]
                elif isinstance(array[2],dict):
                    if "apuntador" in array[2]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[2]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice3 = temp
                    elif "temp" in array[2]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[2]["temp"])
                        indice3 = temp
                L1 = keep.getNuevaEtiqueta()
                L2 = keep.getNuevaEtiqueta()
                L3 = keep.getNuevaEtiqueta()
                L4 = keep.getNuevaEtiqueta()
                L5 = keep.getNuevaEtiqueta()
                L6 = keep.getNuevaEtiqueta()
                L7 = keep.getNuevaEtiqueta()
                L8 = keep.getNuevaEtiqueta()
                temp = keep.getNuevoTemporal()
                temp2 = keep.getNuevoTemporal()
                temp3 = keep.getNuevoTemporal()
                codigo += keep.addOperacion(temp,indice1,"-","1")
                codigo += keep.addOperacion(temp2,indice2,"-","1")
                codigo += keep.addOperacion(temp3,indice3,"-","1")
                codigo += "if " + temp+ ">= 0 {goto "+L1+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L1+":\n"
                codigo += "if " + temp+ "<= "+T5+ "{goto "+L3+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L3+":\n"
                codigo += "if " + temp2+ ">= 0 {goto "+L4+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L4+":\n"
                codigo += "if " + temp2+ "<= "+T9+ "{goto "+L5+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L5+":\n"
                codigo += "if " + temp3+ ">= 0 {goto "+L6+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L6+":\n"
                codigo += "if " + temp3+ "<= "+T13+ "{goto "+L7+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L2+":\n"
                if not "boundserror" in keep.listaFuncion:
                    cc = keep.codigo
                    keep.codigo = ""
                    keep.errorDimension()
                    keep.listaFuncion["boundserror"]= keep.codigo
                    keep.codigo = cc
                codigo += "boundserror();\n"
                codigo += "goto "+L8+";\n"
                codigo += L7+":\n"
                codigo += "//****** APLICANDO FÓRMULA ******\n"
                # CALCULANDO NS
                n2 = keep.getNuevoTemporal()
                n3 = keep.getNuevoTemporal()
                codigo += keep.addOperacion(n2,T9,"-",T7)
                codigo += keep.addOperacion(n2,n2,"+",1)

                codigo += keep.addOperacion(n3,T13,"-",T11)
                codigo += keep.addOperacion(n3,n3,"+",1)
                codigo += keep.addOperacion(temp,temp,"-",T3)
                codigo += keep.addOperacion(temp,temp,"*",n2)
                codigo += keep.addOperacion(temp,temp,"+",temp2)
                codigo += keep.addOperacion(temp,temp,"-",T7)
                codigo += keep.addOperacion(temp,temp,"*",n3)
                codigo += keep.addOperacion(temp,temp,"+",temp3)
                codigo += keep.addOperacion(temp,temp,"-",T11)
                codigo += keep.addOperacion(temp,temp,"+",8)
                codigo += keep.addIgual(temp, keep.getValHeap(temp))
                codigo += L8+":\n"
                keep.addCodigo(codigo)
                #keep.liberarTemporales(T1)
                #keep.liberarTemporales(T2)
                #keep.liberarTemporales(T3)
                #keep.liberarTemporales(T4)
                #keep.liberarTemporales(T5)
                #keep.liberarTemporales(T6)
                #keep.liberarTemporales(T7)
                #keep.liberarTemporales(T8)
                #keep.liberarTemporales(T9)
                #keep.liberarTemporales(T10)
                #keep.liberarTemporales(T11)
                #keep.liberarTemporales(T12)
                #keep.liberarTemporales(T13)
                #keep.liberarTemporales(T14)
                #keep.liberarTemporales(temp2)
                #keep.liberarTemporales(temp3)
                #keep.liberarTemporales(n2)
                #keep.liberarTemporales(n3)
                return {"temp": temp, "valor":None, "tipo":"Float64"}
            else:
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
                                L3 = keep.getNuevaEtiqueta()
                                L4 = keep.getNuevaEtiqueta()
                                cod += "//***** INICIANDO ACCESO A LA POSICIÓN NÚMERO*****\n"
                                cod += "if "+str(valor)+"> 0 "+"{goto "+L3+";}\n"
                                cod += "goto "+L4+";\n"
                                cod += L3+":\n"
                                cod += "if "+str(valor)+"<= "+T12+"{goto "+L1+";}\n"
                                cod += L4+":\n"
                                keep.addCodigo(cod)
                                if not "boundserror" in keep.listaFuncion:
                                    cc = keep.codigo
                                    keep.codigo = ""
                                    keep.errorDimension()
                                    keep.listaFuncion["boundserror"]= keep.codigo
                                    keep.codigo = cc
                                cod = "boundserror();\n"
                                cod += "goto "+ L2+";\n"
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
                                    cod += "//***** INICIANDO ACCESO A LA POSICIÓN VARIABLE*****\n"
                                    cod += keep.addOperacion(T9,"SP","+",valor["apuntador"])
                                    cod += keep.addIgual(T10,keep.getValStack(T9))
                                    cod += keep.addOperacion(T10,T10,"-","1")
                                    L1 = keep.getNuevaEtiqueta()
                                    L2 = keep.getNuevaEtiqueta()
                                    L3 = keep.getNuevaEtiqueta()
                                    L4 = keep.getNuevaEtiqueta()
                                    cod += "if "+T10+"> 0 "+"{goto "+L3+";}\n"
                                    cod += "goto "+L4+";\n"
                                    cod += L3+":\n"
                                    cod += "if "+T10+"<= "+T12+"{goto "+L1+";}\n"
                                    cod += L4+":\n"
                                    keep.addCodigo(cod)
                                    if not "boundserror" in keep.listaFuncion:
                                        cc = keep.codigo
                                        keep.codigo = ""
                                        keep.errorDimension()
                                        keep.listaFuncion["boundserror"]= keep.codigo
                                        keep.codigo = cc
                                    cod = "boundserror();\n"
                                    cod += "goto "+ L2+";\n"
                                    cod += L1+":\n"
                                    cod += keep.addOperacion(T5,T10,"-",T4) #POSICIÓN DENTRO DE LA ESTRUCTURA
                                    cod += keep.addOperacion(T6,T2,"+","3") #PRIMERA POSICIÓN DEL ARREGLO
                                    cod += keep.addOperacion(T7,T6,"+",T5) #POSICIÓN REAL DEL HEAP
                                    cod += keep.addIgual(T8,keep.getValHeap(T7))
                                    cod += L2+":\n"
                                    keep.addCodigo(cod)
                                    return {"temp": T8, "valor":None, "tipo":valor["tipo"]}
                                elif "temp" in valor:
                                    cod = "//***** INICIANDO ACCESO A LA POSICIÓN DEL ARREGLO TEMPORAL*****\n"
                                    cod += keep.addOperacion(T10,valor["temp"],"-","1")
                                    L1 = keep.getNuevaEtiqueta()
                                    L2 = keep.getNuevaEtiqueta()
                                    L3 = keep.getNuevaEtiqueta()
                                    L4 = keep.getNuevaEtiqueta()
                                    cod += "if "+T10+"> 0 "+"{goto "+L3+";}\n"
                                    cod += "goto "+L4+";\n"
                                    cod += L3+":\n"
                                    cod += "if "+T10+"<= "+T12+"{goto "+L1+";}\n"
                                    cod += L4+":\n"
                                    keep.addCodigo(cod)
                                    if not "boundserror" in keep.listaFuncion:
                                        cc = keep.codigo
                                        keep.codigo = ""
                                        keep.errorDimension()
                                        keep.listaFuncion["boundserror"]= keep.codigo
                                        keep.codigo = cc
                                    cod = "boundserror();\n"
                                    cod += "goto "+ L2+";\n"
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
        
        if isinstance(self.posicion, list):
            array = []
            for pos in self.posicion:
                posi = pos.traducir(tree,table,keep)
                array.append(posi)
            if len(array) == 2:
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
                T13 = keep.getNuevoTemporal()
                T14 = keep.getNuevoTemporal()
                if isinstance(array[0],int) or isinstance(array[0],float):
                    #si entra aqui es porque el primer indice es un número
                    indice1 = array[0]
                    codigo = "//***** Calculando el primer indice *****\n"
                elif isinstance(array[0],dict):
                    if "apuntador" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addOperacion(temp,"SP","+",array[0]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        codigo += "//***** Calculando el primer indice *****\n"
                        indice1 = temp
                    elif "temp" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addIgual(temp,array[0]["temp"])
                        codigo += "//***** Calculando el primer indice *****\n"
                        indice1 = temp
                    
                # guardando el apuntador del stack del arreglo
                codigo += "//Encuentro el índice del stack donde está almacenada la primera posición del heap\n"
                codigo += keep.addOperacion(T1,"SP","+",apuntador)
                # OBTENIENDO LA POSICIÓN DEL HEAP EN DONDE INICIA LA ESTRUCTURA
                codigo += "//Almaceno el valor de la primera posición del heap de la estructura.\n"
                codigo += keep.addIgual(T2,keep.getValStack(T1))
                # OBTENIENDO LA POSICIÓN DEL HEAP DONDE SE ENCUENTRA EL INF1
                codigo += "//Guardo la posición de donde se encuentra el valor inferior1 del array\n"
                codigo += keep.addOperacion(T3,T2,"+","1")            
                # SACANDO EL VALOR DE INF1 DEL HEAP
                codigo += "//Guardo el valor inferior1 del array\n"
                codigo += keep.addIgual(T4,keep.getValHeap(T3))
                #OBTENIENDO LA POSICIÓN DEL HEAP DONDE SE ENCUENTRA EL SUPERIOR 1
                codigo += "//Guardo el índice donde se encuentra el superior1 del array\n"
                codigo += keep.addOperacion(T13,T2,"+","2")
                # SACANDO EL VALOR DE SUPERIOR1 DEL HEAP
                codigo += "//Guardo el valor superior1 del array\n"
                codigo += keep.addIgual(T14,keep.getValHeap(T13))
                #AHORA SACAMOS EL INFERIOR Y SUPERIOR DE LA SEGUNDA DIM
                    #sacamos el inf2
                codigo += "//Guardo el índice de donde se encuentra el inferior2 del array\n"
                codigo += keep.addOperacion(T5,T2,"+","3")
                codigo += "//Guardo el valor del inferior2 del array\n"
                codigo += keep.addIgual(T6, keep.getValHeap(T5))
                    #sacamos el superior2
                codigo += "//Guardo el índice de donde se encuentra el superior2 del array\n"
                codigo += keep.addOperacion(T5,T2,"+","4")
                codigo += "//Guardo el valor del superior2 del array\n"
                codigo += keep.addIgual(T7, keep.getValHeap(T5))
                #ENCONTRAMOS N2
                codigo += "//Calculo N2 para la formula\n"
                codigo += keep.addOperacion(T8,T7,"-",T6)
                codigo += keep.addOperacion(T8,T8,"+","1")
                # ------------------APLICANDO LA FORMULA---------------------------
                codigo += "//****** Aplicando la fórmula para D2 ***** \n"
                codigo += keep.addOperacion(T9,indice1,"-",T4)
                codigo += keep.addOperacion(T10,T9,"*",T8)
                if isinstance(array[1],int) or isinstance(array[1],float):
                    indice2 = array[1]
                elif isinstance(array[1],dict):
                    if "apuntador" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[1]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        #codigo += keep.addOperacion(temp,temp,"-",1)
                        indice2 = temp
                    elif "temp" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[1]["temp"])
                        #codigo += keep.addOperacion(temp,temp,"-",1)
                        indice2 = temp
                L1 = keep.getNuevaEtiqueta()
                L2 = keep.getNuevaEtiqueta()
                L3 = keep.getNuevaEtiqueta()
                L4 = keep.getNuevaEtiqueta()
                L5 = keep.getNuevaEtiqueta()
                L6 = keep.getNuevaEtiqueta()
                codigo += "if "+str(indice1)+" >= 1 {goto "+L1+";}\n"
                codigo += "goto "+ L2+";\n"
                codigo += L1+":\n"
                codigo += keep.addOperacion(T14,T14,"+",1)
                codigo += "if "+str(indice1)+" <= "+T14+" {goto "+L3+";}\n"
                codigo += "goto "+ L2+";\n"
                codigo += L3+":\n"
                codigo += "if "+str(indice2)+" >= 1 {goto "+L4+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L4+":\n"
                #codigo += keep.addOperacion(T7,T7,"+",1)
                codigo += "if "+str(indice2)+" <= "+T7+"{goto "+L5+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L5+":\n"
                codigo += keep.addOperacion(T11,T10,"+",indice2)
                codigo += keep.addOperacion(T12,T11,"-",indice1)
                codigo += keep.addOperacion(T12,T12,"+",1)
                codigo += keep.addOperacion(T12,T2,"+",T12)        
                #keep.liberarTemporales(T2)
                #keep.liberarTemporales(T3)
                #keep.liberarTemporales(T4)
                #keep.liberarTemporales(T5)
                #keep.liberarTemporales(T6)
                #keep.liberarTemporales(T7)
                #keep.liberarTemporales(T8)
                #keep.liberarTemporales(T9)
                #keep.liberarTemporales(T10)
                #keep.liberarTemporales(T11)
                #codigo += keep.addIgual(T1,keep.getValHeap(T12))
                ################## SE CALCULA EL VALOR QUE SE AGREGARÁ AL ARREGLO ###############
                keep.addCodigo(codigo)
                if isinstance(valor,NodoAST):
                    val = valor.traducir(tree,table,keep)
                    if isinstance(val,int) or isinstance(val,float):
                        codigo = keep.addIgual(keep.getValHeap(T12),val)
                    elif isinstance(val,dict):
                        if "apuntador" in val:
                            temp = keep.getNuevoTemporal()
                            codigo = keep.addOperacion(temp,"SP","+",val["apuntador"])
                            codigo += keep.addIgual(temp,keep.getValStack(temp))
                            codigo += keep.addIgual(keep.getValHeap(T12),temp)
                            keep.liberarTemporales(temp)
                        elif "temp" in val:
                            codigo = keep.addIgual(keep.getValHeap(T12),val["temp"])
                codigo += "goto "+L6+";\n"
                codigo += L2+":\n"
                keep.addCodigo(codigo)
                if not "boundserror" in keep.listaFuncion:
                    cc = keep.codigo
                    keep.codigo = ""
                    keep.errorDimension()
                    keep.listaFuncion["boundserror"]= keep.codigo
                    keep.codigo = cc
                codigo = "boundserror();\n"
                codigo += L6+":\n"
                keep.addCodigo(codigo)
                return {"temp": T1, "valor":None, "tipo":"Float64"}
            elif len(array) == 3:
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
                T13 = keep.getNuevoTemporal()
                T14 = keep.getNuevoTemporal()

                # INICIANDO LA EXTRACCIÓN DE LOS DATOS NECESARIOS PARA ENCONTRAR LA POSICIÓN DEL ARREGLO
                codigo = "//********** ENCONTRANDO DATO EN EL ARREGLO 3D **********\n"
                codigo += keep.addOperacion(T1,"SP","+",apuntador)
                # posición inicial del heap donde está la estructura
                codigo += keep.addIgual(T1, keep.getValStack(T1))
                # indice del valor inferior1 
                codigo += keep.addOperacion(T2,T1,"+","1")
                # valor del inferior 1
                codigo += keep.addIgual(T3, keep.getValHeap(T2))
                # indice del valor superior 1
                codigo += keep.addOperacion(T4, T1,"+","2")
                # valor del superior 1
                codigo += keep.addIgual(T5,keep.getValHeap(T4))
                # indice del valor inferior2 
                codigo += keep.addOperacion(T6,T1,"+","3")
                # valor del inferior 2
                codigo += keep.addIgual(T7, keep.getValHeap(T6))
                # indice del valor superior 2
                codigo += keep.addOperacion(T8, T1,"+","4")
                # valor del superior 2
                codigo += keep.addIgual(T9,keep.getValHeap(T8))
                # indice del valor inferior3 
                codigo += keep.addOperacion(T10,T1,"+","5")
                # valor del inferior 3
                codigo += keep.addIgual(T11, keep.getValHeap(T10))
                # indice del valor superior 3
                codigo += keep.addOperacion(T12, T1,"+","6")
                # valor del superior 3
                codigo += keep.addIgual(T13,keep.getValHeap(T12))
                indice1 = None
                indice2 = None
                indice3 = None
                # INDICE 1
                if isinstance(array[0],int):
                    indice1 = array[0]
                elif isinstance(array[0],dict):
                    if "apuntador" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[0]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice1 = temp
                    elif "temp" in array[0]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[0]["temp"])
                        indice1 = temp
                # INDICE 2 
                if isinstance(array[1],int):
                    indice2 = array[1]
                elif isinstance(array[1],dict):
                    if "apuntador" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[1]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice2 = temp
                    elif "temp" in array[1]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[1]["temp"])
                        indice2 = temp
                # INDICE 3
                if isinstance(array[2],int):
                    indice3 = array[2]
                elif isinstance(array[2],dict):
                    if "apuntador" in array[2]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addOperacion(temp,"SP","+",array[2]["apuntador"])
                        codigo += keep.addIgual(temp,keep.getValStack(temp))
                        indice3 = temp
                    elif "temp" in array[2]:
                        temp = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp,array[2]["temp"])
                        indice3 = temp
                L1 = keep.getNuevaEtiqueta()
                L2 = keep.getNuevaEtiqueta()
                L3 = keep.getNuevaEtiqueta()
                L4 = keep.getNuevaEtiqueta()
                L5 = keep.getNuevaEtiqueta()
                L6 = keep.getNuevaEtiqueta()
                L7 = keep.getNuevaEtiqueta()
                L8 = keep.getNuevaEtiqueta()
                temp = keep.getNuevoTemporal()
                temp2 = keep.getNuevoTemporal()
                temp3 = keep.getNuevoTemporal()
                codigo += keep.addOperacion(temp,indice1,"-","1")
                codigo += keep.addOperacion(temp2,indice2,"-","1")
                codigo += keep.addOperacion(temp3,indice3,"-","1")
                codigo += "if " + temp+ ">= 0 {goto "+L1+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L1+":\n"
                codigo += "if " + temp+ "<= "+T5+ "{goto "+L3+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L3+":\n"
                codigo += "if " + temp2+ ">= 0 {goto "+L4+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L4+":\n"
                codigo += "if " + temp2+ "<= "+T9+ "{goto "+L5+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L5+":\n"
                codigo += "if " + temp3+ ">= 0 {goto "+L6+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L6+":\n"
                codigo += "if " + temp3+ "<= "+T13+ "{goto "+L7+";}\n"
                codigo += "goto "+L2+";\n"
                codigo += L2+":\n"
                if not "boundserror" in keep.listaFuncion:
                    cc = keep.codigo
                    keep.codigo = ""
                    keep.errorDimension()
                    keep.listaFuncion["boundserror"]= keep.codigo
                    keep.codigo = cc
                codigo += "boundserror();\n"
                codigo += "goto "+L8+";\n"
                codigo += L7+":\n"
                codigo += "//****** APLICANDO FÓRMULA ******\n"
                # CALCULANDO NS
                n2 = keep.getNuevoTemporal()
                n3 = keep.getNuevoTemporal()
                codigo += keep.addOperacion(n2,T9,"-",T7)
                codigo += keep.addOperacion(n2,n2,"+",1)

                codigo += keep.addOperacion(n3,T13,"-",T11)
                codigo += keep.addOperacion(n3,n3,"+",1)
                codigo += keep.addOperacion(temp,temp,"-",T3)
                codigo += keep.addOperacion(temp,temp,"*",n2)
                codigo += keep.addOperacion(temp,temp,"+",temp2)
                codigo += keep.addOperacion(temp,temp,"-",T7)
                codigo += keep.addOperacion(temp,temp,"*",n3)
                codigo += keep.addOperacion(temp,temp,"+",temp3)
                codigo += keep.addOperacion(temp,temp,"-",T11)
                codigo += keep.addOperacion(temp,temp,"+",8)
                #codigo += keep.addIgual(temp, keep.getValHeap(temp))
                #keep.liberarTemporales(T1)
                #keep.liberarTemporales(T2)
                #keep.liberarTemporales(T3)
                #keep.liberarTemporales(T4)
                #keep.liberarTemporales(T5)
                #keep.liberarTemporales(T6)
                #keep.liberarTemporales(T7)
                #keep.liberarTemporales(T8)
                #keep.liberarTemporales(T9)
                #keep.liberarTemporales(T10)
                #keep.liberarTemporales(T11)
                #keep.liberarTemporales(T12)
                #keep.liberarTemporales(T13)
                #keep.liberarTemporales(T14)
                #keep.liberarTemporales(temp2)
                #keep.liberarTemporales(temp3)
                #keep.liberarTemporales(n2)
                #keep.liberarTemporales(n3)
                # CALCULANDO EL VALOR A SUSTITUIR 
                if isinstance(valor,NodoAST):
                    val = valor.traducir(tree,table,keep)
                    if isinstance(val,int) or isinstance(val,float):
                        codigo += keep.addIgual(keep.getValHeap(temp),val)
                    elif isinstance(val,dict):
                        if "apuntador" in val:
                            temporal = keep.getNuevoTemporal()
                            codigo += keep.addOperacion(temporal,"SP","+",val["apuntador"])
                            codigo += keep.addIgual(temporal,keep.getValStack(temporal))
                            codigo += keep.addIgual(keep.getValHeap(temp),temporal)
                            #keep.liberarTemporales(temporal)
                        elif "temp" in val:
                            codigo += keep.addIgual(keep.getValHeap(temp),val["temp"])
                codigo += L8+":\n"
                #keep.liberarTemporales(temp)
                keep.addCodigo(codigo)
                return
            else:
                T1 = keep.getNuevoTemporal()
                T2 = keep.getNuevoTemporal()
                T3 = keep.getNuevoTemporal()
                T4 = keep.getNuevoTemporal()
                T5 = keep.getNuevoTemporal()
                T6 = keep.getNuevoTemporal()
                T7 = keep.getNuevoTemporal()
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
                codigo += keep.addIgual(temp2,keep.getValHeap(temp))
                codigo += keep.addOperacion(temp2,temp2,"+","1")
                if isinstance(posi,int):      
                    L1 = keep.getNuevaEtiqueta()
                    L2 = keep.getNuevaEtiqueta()
                    L3 = keep.getNuevaEtiqueta()
                    L4 = keep.getNuevaEtiqueta()
                    codigo += "if "+str(posi-1)+"> 0 "+"{goto "+L3+";}\n"
                    codigo += "goto "+L4+";\n"
                    codigo += L3+":\n"
                    codigo += "if "+str(posi-1)+"<= "+temp2+"{goto "+L1+";}\n"
                    codigo += L4+":\n"
                    keep.addCodigo(codigo)
                    if not "boundserror" in keep.listaFuncion:
                        cc = keep.codigo
                        keep.codigo = ""
                        keep.errorDimension()
                        keep.listaFuncion["boundserror"]= keep.codigo
                        keep.codigo = cc
                    codigo = "boundserror();\n"
                    codigo += "goto "+L2+";\n"
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
                        L3 = keep.getNuevaEtiqueta()
                        L4 = keep.getNuevaEtiqueta()
                        codigo += "if "+T12+"> 0 "+"{goto "+L3+";}\n"
                        codigo += "goto "+L4+";\n"
                        codigo += L3+":\n"
                        codigo += "if "+T12+"<= "+temp2+"{goto "+L1+";}\n"
                        codigo += L4+":\n"
                        keep.addCodigo(codigo)
                        if not "boundserror" in keep.listaFuncion:
                            cc = keep.codigo
                            keep.codigo = ""
                            keep.errorDimension()
                            keep.listaFuncion["boundserror"]= keep.codigo
                            keep.codigo = cc
                        codigo = "boundserror();\n"
                        codigo += "goto "+L2+";\n"
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
                        L3 = keep.getNuevaEtiqueta()
                        L4 = keep.getNuevaEtiqueta()
                        codigo += "if "+T12+"> 0 "+"{goto "+L3+";}\n"
                        codigo += "goto "+L4+";\n"
                        codigo += L3+":\n"
                        codigo += "if "+T12+"<= "+temp2+"{goto "+L1+";}\n"
                        codigo += L4+":\n"
                        keep.addCodigo(codigo)
                        
                        if not "boundserror" in keep.listaFuncion:
                            cc = keep.codigo
                            keep.codigo = ""
                            keep.errorDimension()
                            keep.listaFuncion["boundserror"]= keep.codigo
                            keep.codigo = cc
                        codigo = "boundserror();\n"
                        codigo += "goto "+L2+";\n"
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
                        codigo += keep.addOperacion(T8,"SP","+",val["apuntador"])
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
        #keep.liberarTemporales(T1)
        #keep.liberarTemporales(T2)
        #keep.liberarTemporales(T3)
        #keep.liberarTemporales(T4)
        #keep.liberarTemporales(T5)
        #keep.liberarTemporales(T6)
        #keep.liberarTemporales(T7)
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
    