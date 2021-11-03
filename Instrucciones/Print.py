from Expresiones.Constante import Constante
from Objetos.Primitivos import Primitivo
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from TablaSimbolos.Errores import Errores
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Primitivas, Tipo_Print
from Abstractas.Objeto import TipoObjeto
from Abstractas.NodoAST import NodoAST

class Print(NodoAST):

    def __init__(self, tipo, contenido, fila, columna):
        self.tipo = tipo 
        self.contenido= contenido
        self.fila = fila 
        self.columna = columna

    def ejecutar(self, tree, table):

        if self.tipo == Tipo_Print.PRINT:  
            if self.contenido != "":
                for instrucciones in self.contenido:
                    resultado = instrucciones.ejecutar(tree,table)
                    if isinstance(resultado,list):
                        array = self.imprime(tree,table,resultado,[])
                        if len(array) == 0:
                            tree.updateConsola(str(resultado))
                        else:
                            tree.updateConsola(str(array))
                    elif isinstance(resultado, NodoAST):
                        val = resultado.ejecutar(tree,table)
                        if not isinstance(val,list):
                            tree.updateConsola(str(val))
                        else:
                            array = self.imprime(tree,table,resultado,[])
                            if array !=None:
                                if len(array) == 1:
                                    tree.updateConsola(str(array[0])+" ")
                            else:
                                tree.updateConsola(str(array))
                    elif isinstance(resultado, Errores):
                        return resultado
                    elif isinstance(resultado, TablaSimbolos):
                        cadena =self.imprimirTablaSimbolo(resultado)
                        tree.updateConsola(str(cadena))
                    else:
                        tree.updateConsola(str(resultado))
        if self.tipo == Tipo_Print.PRINTLN:
            if self.contenido != "":
                for instrucciones in self.contenido:
                    resultado = instrucciones.ejecutar(tree,table)
                    if isinstance(resultado,list):
                        array = self.imprime(tree,table,resultado,[])
                        if len(array) == 0:
                            tree.updateConsola(str(resultado))
                        else:
                            tree.updateConsola(str(array))
                    elif isinstance(resultado, NodoAST):
                        val = resultado.ejecutar(tree,table)
                        if not isinstance(val,list):
                            tree.updateConsola(str(val))
                        else:
                            array = self.imprime(tree,table,resultado,[])
                            if array !=None:
                                tree.updateConsola(str(array))
                            else:
                                tree.updateConsola(str(array))
                    elif isinstance(resultado, Errores):
                        return resultado
                    elif isinstance(resultado, TablaSimbolos):
                        cadena =self.imprimirTablaSimbolo(resultado)
                        tree.updateConsola(str(cadena))
                    else:
                        tree.updateConsola(str(resultado))
            tree.updateConsola("\n")


    def traducir(self, tree, table, keep):
        if self.tipo == Tipo_Print.PRINT:  
            if self.contenido != "":
                for instrucciones in self.contenido:
                    resultado = instrucciones.traducir(tree,table,keep)
                    if isinstance(resultado,bool):
                        if len(keep.etiquetas) == 0:
                            keep.booleanos(resultado)
                        else:
                            es = keep.getNuevaEtiqueta()
                            ev = keep.etiquetas.pop()
                            ef = keep.etiquetas.pop()
                            keep.addCodigo(ev+":\n")
                            keep.booleanos(True)
                            keep.addCodigo("goto "+es+";\n")
                            keep.addCodigo(ef+":\n")
                            keep.booleanos(False)
                            keep.addCodigo(es+":\n")
                    elif isinstance(resultado, float):
                        result=keep.imprimir(resultado,"f")
                        keep.addCodigo(result)
                    elif isinstance(resultado,int):
                        result=keep.imprimir(resultado,"d")
                        keep.addCodigo(result)
                    elif isinstance(resultado,str):
                        #CAMBIO FORMAL DE ENTORNO
                        temp = keep.getNuevoTemporal()
                        temp2 = keep.getNuevoTemporal()
                        temp3 = keep.getNuevoTemporal()
                        result = keep.addOperacion(temp3,"SP","+",keep.getStack()-1)
                        result += keep.addIgual(temp,keep.getValStack(temp3))
                        result += keep.addOperacion(temp2,"SP","+",keep.getStack())
                        result += keep.addIgual(keep.getValStack(temp2),temp)
                        result += keep.addOperacion("SP","SP","+",keep.getStack())
                        result += keep.llamada("Native_PrintString")
                        result += keep.addOperacion("SP","SP","-",keep.getStack())
                        keep.addCodigo(result)
                    elif isinstance(resultado, dict):
                        if "apuntador" in resultado:
                            #guardo el valor actual del stack
                            actual = keep.getStack()
                            #obtengo la posicion del stack de donde está la variable
                            puntero = resultado['apuntador']
                            #obtengo el tipo de variable
                            tipo = resultado['tipo']
                    
                            if tipo == "String" or tipo == "nothing":
                                #CAMBIO FORMAL DE ENTORNO
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                result = keep.addOperacion(temp3,"SP","+",puntero)
                                result += keep.addIgual(temp,keep.getValStack(temp3))
                                temp4 = keep.getNuevoTemporal()
                                result += keep.addOperacion(temp4,"SP","+",keep.getStack())
                                result += keep.addIgual(keep.getValStack(temp4),temp)
                                result += keep.addOperacion("SP","SP","+",keep.getStack())
                                result += keep.llamada("Native_PrintString")
                                result += keep.addOperacion("SP","SP","-",keep.getStack())
                                keep.addCodigo(result)
                            elif tipo == "Int64":
                                cod = "//*****IMPRESIÓN DE NÚMERO*****\n"
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod += keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp, keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                result=keep.imprimir(temp,"d")
                                keep.addCodigo(result)
                            elif tipo == "Float64":
                                cod = "//*****IMPRESIÓN DE NÚMERO*****\n"
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod += keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp, keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                result=keep.imprimir(temp,"f")
                                keep.addCodigo(result)
                            elif tipo == "Bool":
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod = keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp,keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                keep.comparar(temp)
                                return
                            #keep.addCodigo(keep.addIgual("SP",actual))
                            keep.liberarTemporales(temp)
                            #keep.PS = actual
                        elif "temp" in resultado:
                            result=keep.imprimir(resultado['temp'],"f")
                            keep.addCodigo(result)
                        elif "etiquetas" in resultado:
                            e1 = keep.getNuevaEtiqueta()
                            result = resultado["etiquetas"][0]+":\n"
                            keep.addCodigo(result)
                            keep.booleanos(True)
                            keep.addCodigo("goto "+e1+";\n")
                            result = resultado["etiquetas"][1]+":\n"
                            keep.addCodigo(result)
                            keep.booleanos(False)
                            keep.addCodigo("goto "+e1+";\n")
                            keep.addCodigo(e1+":\n")
                            keep.etiquetaFalsa = ""
                            keep.etiquetaVerdadera=""
                    
                
        if self.tipo == Tipo_Print.PRINTLN:
            if self.contenido != "":
                for instrucciones in self.contenido:
                    resultado = instrucciones.traducir(tree,table,keep)
                    if isinstance(resultado, float):
                        result=keep.imprimir(resultado,"f")
                        keep.addCodigo(result)
                    elif isinstance(resultado,bool):
                        if len(keep.etiquetas) == 0:
                            keep.booleanos(resultado)
                        else:
                            es = keep.getNuevaEtiqueta()
                            ev = keep.etiquetas.pop()
                            ef = keep.etiquetas.pop()
                            keep.addCodigo(ev+":\n")
                            keep.booleanos(True)
                            keep.addCodigo("goto "+es+";\n")
                            keep.addCodigo(ef+":\n")
                            keep.booleanos(False)
                            keep.addCodigo(es+":\n")                       
                    elif isinstance(resultado,int):
                        result=keep.imprimir(resultado,"d")
                        keep.addCodigo(result)                       
                    elif isinstance(resultado,str):
                        #CAMBIO FORMAL DE ENTORNO
                        temp = keep.getNuevoTemporal()
                        temp2 = keep.getNuevoTemporal()
                        temp3 = keep.getNuevoTemporal()
                        result = keep.addOperacion(temp3,"SP","+",keep.getStack()-1)
                        result += keep.addIgual(temp,keep.getValStack(temp3))
                        result += keep.addOperacion(temp2,"SP","+",keep.getStack())
                        result += keep.addIgual(keep.getValStack(temp2),temp)
                        result += keep.addOperacion("SP","SP","+",keep.getStack())
                        result += keep.llamada("Native_PrintString")
                        result += keep.addOperacion("SP","SP","-",keep.getStack())
                        keep.addCodigo(result)
                       
                    elif isinstance(resultado, dict):
                        if "apuntador" in resultado:
                            #guardo el valor actual del stack
                            actual = keep.getStack()
                            #obtengo la posicion del stack de donde está la variable
                            puntero = resultado['apuntador']
                            #obtengo el tipo de variable
                            tipo = resultado['tipo']
                    
                            if tipo == "String" or tipo == "nothing":
                                #CAMBIO FORMAL DE ENTORNO
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                result = keep.addOperacion(temp3,"SP","+",puntero)
                                result += keep.addIgual(temp,keep.getValStack(temp3))
                                temp4 = keep.getNuevoTemporal()
                                result += keep.addOperacion(temp4,"SP","+",keep.getStack())
                                result += keep.addIgual(keep.getValStack(temp4),temp)
                                result += keep.addOperacion("SP","SP","+",keep.getStack())
                                result += keep.llamada("Native_PrintString")
                                result += keep.addOperacion("SP","SP","-",keep.getStack())
                                keep.addCodigo(result)
                            elif tipo == "Bool":
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod = keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp,keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                keep.comparar(temp)
                            elif tipo == "Int64":
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod = keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp, keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                result=keep.imprimir(temp,"d")
                                keep.addCodigo(result)
                                
                            elif tipo == "Float64":
                                temp = keep.getNuevoTemporal()
                                temp3 = keep.getNuevoTemporal()
                                cod = keep.addOperacion(temp3,"SP","+",puntero)
                                cod += keep.addIgual(temp, keep.getValStack(temp3))
                                keep.addCodigo(cod)
                                result=keep.imprimir(temp,"f")
                                keep.addCodigo(result)
                        elif "temp" in resultado:
                            result=keep.imprimir(resultado['temp'],"f")
                            keep.addCodigo(result)
                        elif "etiquetas" in resultado:
                            e1 = keep.getNuevaEtiqueta()
                            result = resultado["etiquetas"][0]+":\n"
                            keep.addCodigo(result)
                            keep.booleanos(True)
                            keep.addCodigo("goto "+e1+";\n")
                            result = resultado["etiquetas"][1]+":\n"
                            keep.addCodigo(result)
                            keep.booleanos(False)
                            keep.addCodigo("goto "+e1+";\n")
                            keep.addCodigo(e1+":\n")
                            keep.etiquetaFalsa = ""
                            keep.etiquetaVerdadera=""
                keep.addCodigo(keep.imprimir("10","c"))

    def getNodo(self):
        
        NodoNuevo = NodoArbol("Impresión")

        if self.tipo == Tipo_Print.PRINT:
            NodoNuevo.agregarHijo("Print")
        elif self.tipo == Tipo_Print.PRINTLN:
            NodoNuevo.agregarHijo("Println")
        
        NodoNuevo.agregarHijo("(")
        cont = 0
        for instruccion in self.contenido:
            NodoNuevo.agregarHijoNodo(instruccion.getNodo())
            if cont < (len(self.contenido)-1):
                NodoNuevo.agregarHijo(",")
                cont = cont +1
        NodoNuevo.agregarHijo(")")
        NodoNuevo.agregarHijo(";")
        return NodoNuevo
    
    
    def imprime(self,tree,table,resultado,array):

        if isinstance(resultado, list):
            for i in resultado:
                if isinstance(i, NodoAST):
                    result = i.ejecutar(tree,table)
                    self.imprime(tree,table,result,array)
                elif isinstance(i,list):
                    self.imprime(tree,table,i,array)
            return array
        elif isinstance(resultado,NodoAST):
            val = resultado.ejecutar(tree,table)
            return self.imprime(tree,table,val,array)
            
        else:
            array.append(resultado)
    
    def imprimirTablaSimbolo(self,resultado):
        if isinstance(resultado, TablaSimbolos):
            cadena = resultado.nombre+"("
            contador = 1
            for v in  resultado.tabla:
                res = resultado.tabla[v]
                if isinstance(res,TablaSimbolos):
                    cadena +=self.imprimirTablaSimbolo(res)
                else:
                    cadena+= str(resultado.tabla[v])
                if contador < len(resultado.tabla):
                    cadena+=","
                contador = contador +1
            cadena+=")"
        return cadena