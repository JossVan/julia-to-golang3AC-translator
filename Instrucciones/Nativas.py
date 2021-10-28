from Expresiones.Identificador import Identificador
from TablaSimbolos.Errores import Errores
from Expresiones.Arreglos import Arreglos
from Expresiones.Array import Array
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Dato, Tipo_Primitivas
from Abstractas.NodoAST import NodoAST
import numpy as np
class Nativas_conTipo(NodoAST):

    def __init__(self, funcion, tipo, valor,  fila, columna):
        self.funcion = funcion 
        self.tipo = tipo 
        self.valor = valor 
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):

        if self.funcion == Tipo_Primitivas.PARSE:
 
            if self.tipo != None:
    
                valor = self.valor.ejecutar(tree,table)
                if self.tipo == Tipo_Dato.BOOLEANO:
                    try:
                        if isinstance(valor,str):
                            return bool(self.valor)
                        err = Errores(str(valor),"Semántico","El parámetro debe ser una cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a booleano", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.CADENA:
                    try:
                        if isinstance(valor,str):
                            return valor
                        err = Errores(str(valor),"Semántico","El parámetro debe ser una cadena de texto", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.ENTERO:
                    try:
                        if isinstance(valor, str):
                            return int(valor)
                        err = Errores(str(valor),"Semántico","El segundo parámetro debe ser una cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Error al castear a Int64", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.DECIMAL:
                    try:
                        if isinstance(valor, str):
                            return float(valor)
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Error al intentar convertir a Float64", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.CARACTER:
                    try:
                        if isinstance(valor, str):
                            return chr(valor)
                        err = Errores(str(valor),"Semántico","El segundo parámetro debe ser una cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a Char", self.fila,self.columna)
                        tree.insertError(err)
                        return err
        elif self.funcion == Tipo_Primitivas.TRUNC:
            if self.tipo == Tipo_Dato.ENTERO:
                self.valor = self.valor.ejecutar(tree,table)
                return int(self.valor)
            else:
                err = Errores(str(self.tipo),"Semántico","Solo valores tipo Int64", self.fila,self.columna)
                tree.insertError(err)
                return err
    
    def traducir(self, tree, table, keep):
        apuntador = None
        tipo = None 
        val = None
        if self.funcion == Tipo_Primitivas.PARSE:
            if self.tipo != None:
                valor = self.valor.traducir(tree,table,keep)
                if self.tipo == Tipo_Dato.ENTERO:
                    try:
                        if isinstance(valor,str):
                            apuntador = keep.getStack()-1
                            codigo = "// *****MÉTODO PARSER*****\n"
                            temp = keep.getNuevoTemporal()
                            codigo += "// Variable que almacena el apuntador del stack\n"
                            codigo += keep.addIgual(temp,apuntador)
                            temp2 = keep.getNuevoTemporal()
                            temp3 = keep.getNuevoTemporal()
                            codigo += "// Variable que almacena el valor del stack\n"
                            codigo += keep.addIgual(temp2,keep.getValStack(temp))
                            codigo += "// Variable que almacena el valor del heap\n"
                            codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                            ei = keep.getNuevaEtiqueta()
                            ef = keep.getNuevaEtiqueta()
                            contador = keep.getNuevoTemporal()
                            unidades = keep.getNuevoTemporal()
                            totales = keep.getNuevoTemporal()
                            codigo += keep.addIgual(totales,"0")
                            codigo += keep.addIgual(contador,"0")
                            codigo += keep.addIgual(unidades,"1")
                            codigo += ei+":\n"
                            codigo += "if "+temp3+" == -1{goto "+ef+";}\n"
                            codigo += keep.addOperacion(contador,contador,"+","1")
                            codigo += "// Aumento la posición del heap\n"
                            codigo += keep.addOperacion(temp2,temp2,"+","1")
                            codigo += "// Variable que almacena el valor del heap\n"
                            codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                            codigo += "goto "+ei+";\n"
                            codigo += ef+":\n"
                            codigo += "//Posición del heap del últmo valor de la cadena\n"
                            codigo += keep.addOperacion(contador,contador,"-","1")
                            codigo += "// Variable que almacena el valor del stack\n"
                            codigo += keep.addIgual(temp2,keep.getValStack(temp))
                            codigo += "// Variable que almacena el valor del heap\n"
                            codigo += keep.addOperacion(contador,contador,"+",temp2)
                            codigo += keep.addIgual(temp3,keep.getValHeap(contador))
                            et = keep.getNuevaEtiqueta()
                            temp4 = keep.getNuevoTemporal()
                            #codigo += et+":\n"
                            codigo += keep.addOperacion(temp4,temp3,"-","48")
                            codigo += keep.addOperacion(temp4,temp4,"*", unidades)
                            codigo += keep.addOperacion(totales,totales,"+",temp4)
                            codigo += keep.addOperacion(unidades,unidades,"*",10)
                            codigo += "if "+contador+"== 0 {goto "+et+";}\n"
                            codigo += "goto "+ef+";\n"
                            codigo += et+":\n"
                            codigo += keep.addIgual(keep.getValStack(temp), totales)
                            keep.addCodigo(codigo)
                            keep.liberarTemporales(temp)
                            keep.liberarTemporales(temp2)
                            keep.liberarTemporales(temp3)
                            keep.liberarTemporales(temp4)
                            keep.liberarTemporales(contador)
                            keep.liberarTemporales(totales)
                            return {"apuntador":apuntador,"tipo":"Int64","valor": int(valor)}
                        elif isinstance(valor,dict):
                            if "apuntador" in valor:
                                apuntador = valor["apuntador"]
                                tipo = valor["tipo"]
                                val = valor["valor"]
                                if tipo == "String":
                                    codigo = "// *****MÉTODO PARSER*****\n"
                                    temp = keep.getNuevoTemporal()
                                    codigo += "// Variable que almacena el apuntador del stack\n"
                                    codigo += keep.addIgual(temp,apuntador)
                                    temp2 = keep.getNuevoTemporal()
                                    temp3 = keep.getNuevoTemporal()
                                    codigo += "// Variable que almacena el valor del stack\n"
                                    codigo += keep.addIgual(temp2,keep.getValStack(temp))
                                    codigo += "// Variable que almacena el valor del heap\n"
                                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                                    ei = keep.getNuevaEtiqueta()
                                    ef = keep.getNuevaEtiqueta()
                                    contador = keep.getNuevoTemporal()
                                    unidades = keep.getNuevoTemporal()
                                    totales = keep.getNuevoTemporal()
                                    codigo += keep.addIgual(totales,"0")
                                    codigo += keep.addIgual(contador,"0")
                                    codigo += keep.addIgual(unidades,"1")
                                    codigo += ei+":\n"
                                    codigo += "if "+temp3+" == -1{goto "+ef+";}\n"
                                    codigo += keep.addOperacion(contador,contador,"+","1")
                                    codigo += "// Aumento la posición del heap\n"
                                    codigo += keep.addOperacion(temp2,temp2,"+","1")
                                    codigo += "// Variable que almacena el valor del heap\n"
                                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                                    codigo += "goto "+ei+";\n"
                                    codigo += ef+":\n"
                                    codigo += "//Posición del heap del últmo valor de la cadena\n"
                                    codigo += keep.addOperacion(contador,contador,"-","1")
                                    codigo += "// Variable que almacena el valor del stack\n"
                                    codigo += keep.addIgual(temp2,keep.getValStack(temp))
                                    codigo += "// Variable que almacena el valor del heap\n"
                                    codigo += keep.addOperacion(contador,contador,"+",temp2)
                                    codigo += keep.addIgual(temp3,keep.getValHeap(contador))
                                    et = keep.getNuevaEtiqueta()
                                    temp4 = keep.getNuevoTemporal()
                                    #codigo += et+":\n"
                                    codigo += keep.addOperacion(temp4,temp3,"-","48")
                                    codigo += keep.addOperacion(temp4,temp4,"*", unidades)
                                    codigo += keep.addOperacion(totales,totales,"+",temp4)
                                    codigo += keep.addOperacion(unidades,unidades,"*",10)
                                    codigo += "if "+contador+"== 0 {goto "+et+";}\n"
                                    codigo += "goto "+ef+";\n"
                                    codigo += et+":\n"
                                    codigo += keep.addIgual(keep.getValStack(temp), totales)
                                    keep.addCodigo(codigo)
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    keep.liberarTemporales(temp3)
                                    keep.liberarTemporales(temp4)
                                    keep.liberarTemporales(contador)
                                    keep.liberarTemporales(totales)
                                    return {"apuntador":apuntador,"tipo":"Int64","valor":int(val)}
                                else:
                                    print("ERROR")
                        err = Errores(str(valor),"Semántico","El segundo parámetro debe ser una cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Error al castear a Int64", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.DECIMAL:
                    try:
                        if isinstance(valor, str):
                            return float(valor)
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Error al intentar convertir a Float64", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                elif self.tipo == Tipo_Dato.CARACTER:
                    try:
                        if isinstance(valor, str):
                            return chr(valor)
                        err = Errores(str(valor),"Semántico","El segundo parámetro debe ser una cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a Char", self.fila,self.columna)
                        tree.insertError(err)
                        return err
        elif self.funcion == Tipo_Primitivas.TRUNC:
            if self.tipo == Tipo_Dato.ENTERO:
                self.valor = self.valor.ejecutar(tree,table)
                return int(self.valor)
            else:
                err = Errores(str(self.tipo),"Semántico","Solo valores tipo Int64", self.fila,self.columna)
                tree.insertError(err)
                return err
    
    def getNodo(self):
        NodoNuevo = NodoArbol("Funciones_Nativas")

        if self.funcion == Tipo_Primitivas.PARSE:
            NodoNuevo.agregarHijo("Parse")
        elif self.funcion == Tipo_Primitivas.TRUNC:
            NodoNuevo.agregarHijo("Trunc")
        NodoNuevo.agregarHijo("(")
        if self.tipo == Tipo_Dato.CADENA:
            NodoNuevo.agregarHijo("String")
        elif self.tipo == Tipo_Dato.CARACTER:
            NodoNuevo.agregarHijo("Char")
        elif self.tipo == Tipo_Dato.ENTERO:
            NodoNuevo.agregarHijo("Int64")
        elif self.tipo == Tipo_Dato.DECIMAL:
            NodoNuevo.agregarHijo("Float64")
        elif self.tipo == Tipo_Dato.BOOLEANO:
            NodoNuevo.agregarHijo("Bool")
        NodoNuevo.agregarHijo(",")
        NodoNuevo.agregarHijoNodo(self.valor.getNodo())
        NodoNuevo.agregarHijo(")")
        return NodoNuevo
class Nativas_SinTipo(NodoAST):

    def __init__(self, funcion, valor, fila, columna):
        self.funcion = funcion
        self.valor = valor
        self.fila = fila 
        self.columna = columna

    def ejecutar(self, tree, table):

        valor = self.valor.ejecutar(tree,table)
        if self.funcion == Tipo_Primitivas.FLOAT:
            try:
                return float(valor)
            except ValueError:
                err = Errores(valor,"Semántico","Valor no permitido", self.fila,self.columna)
                tree.insertError(err)
                return err
        elif self.funcion == Tipo_Primitivas.STRING:
            return str(valor)
        elif self.funcion == Tipo_Primitivas.TYPEOF:
            if(isinstance(valor, bool)):
                return "Bool"
            elif (isinstance(valor,int)):
                return "Int64"
            elif(isinstance(valor,float)):
                return "Float64"
            elif(isinstance(valor,str)):
                return "String"
        elif self.funcion == Tipo_Primitivas.TRUNC:   
            if isinstance(valor,int) or isinstance(valor,float):
                return int(valor)
            else:
                err = Errores(valor,"Semántico","Valor no permitido, debe ser un número flotante", self.fila,self.columna)
                tree.insertError(err)
                return err

    def getNodo(self):
        NodoNuevo = NodoArbol("Funciones_Nativas")

        if self.funcion == Tipo_Primitivas.FLOAT:
            NodoNuevo.agregarHijo("Float")
        elif self.funcion == Tipo_Primitivas.STRING:
            NodoNuevo.agregarHijo("String")
        elif self.funcion == Tipo_Primitivas.TYPEOF:
            NodoNuevo.agregarHijo("Typeof")
        elif self.funcion == Tipo_Primitivas.TRUNC:
            NodoNuevo.agregarHijo("Trunc")
        NodoNuevo.agregarHijo("(")
        NodoNuevo.agregarHijoNodo(self.valor.getNodo())
        NodoNuevo.agregarHijo(")")
        return NodoNuevo

class Pilas(NodoAST):
    def __init__(self, funcion, id, valor, fila, columna):
        self.funcion = funcion
        self.id = id
        self.valor = valor
        self.fila = fila 
        self.columna = columna

    def ejecutar(self, tree, table):
        if self.funcion == Tipo_Primitivas.LENGTH:
            if isinstance(self.valor, NodoAST):
                val = self.valor.ejecutar(tree,table)
                if isinstance(val,list):   
                    return len(val)
        elif self.funcion == Tipo_Primitivas.PUSH:
            if not isinstance(self.id, Array):
                val = self.id.ejecutar(tree,table)
            else:
                val = self.id.insertar(self.valor,tree,table)
                return val
            if isinstance(val,list):
                if len(self.valor) == 1:
                    if isinstance(self.valor[0],Arreglos):
                        t = self.valor[0].ejecutar(tree,table)
                        val.append(t)
                        return val

                val.append(self.valor)

            return val
        elif self.funcion == Tipo_Primitivas.POP:
            result = self.id.ejecutar(tree,table)
            retorno = []
            if result != None:
                if isinstance(result,list):

                    tam = int(len(result)-1)
                    retorno = result[tam]
                    result.pop(tam)
                    table.actualizarValor(self.id.id,result)

                return retorno
                
    def getNodo(self):
        NodoNuevo = NodoArbol("Funciones_Arreglos")
        if self.funcion == Tipo_Primitivas.LENGTH:
            NodoNuevo.agregarHijo("Length")
            NodoNuevo.agregarHijo("(")
            NodoNuevo.agregarHijoNodo(self.valor.getNodo())
            NodoNuevo.agregarHijo(")")
            return NodoNuevo
        elif self.funcion == Tipo_Primitivas.PUSH:
            NodoNuevo.agregarHijo("push")
            NodoNuevo.agregarHijo("!")
            NodoNuevo.agregarHijo("(")
            NodoNuevo.agregarHijoNodo(self.id.getNodo())
            NodoNuevo.agregarHijo(",")
            if isinstance(self.valor,list):
                for i in self.valor:
                    NodoNuevo.agregarHijoNodo(i.getNodo())   
            elif isinstance(self.valor,NodoAST):
                NodoNuevo.agregarHijo(self.valor.getNodo())     
            NodoNuevo.agregarHijo(")")
            return NodoNuevo
        elif self.funcion == Tipo_Primitivas.POP:
            NodoNuevo.agregarHijo("pop")
            NodoNuevo.agregarHijo("!")
            NodoNuevo.agregarHijo("(")
            NodoNuevo.agregarHijoNodo(self.id.getNodo())
            NodoNuevo.agregarHijo(")")
            return NodoNuevo
    
    def getLen(self,array):

        if isinstance(array,list):
            for i in array:
                if isinstance(i, Arreglos):
                    return i.getLength()
                elif isinstance(i,list):
                    self.getLen(i)
        elif isinstance(array, Arreglos):
            return array.getLength()
        else :
            None
    
    def convertir(self,tree,table,item,lista):

        if isinstance(item, list):
            for i in item:
                self.convertir(tree,table,i,lista)
        elif isinstance(item, Arreglos):
            valor = item.ejecutar(tree,table)
            lista.append(valor)
            return lista
        return lista
