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
                            
                            #Hacemos una copia del puntero que queremos parsear
                            temp = keep.getNuevoTemporal()
                            temp2 = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                            codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                            codigo += keep.addIgual(keep.getValStack(temp2),temp)
                            codigo += keep.addOperacion("SP","SP","+",keep.getStack())
                            codigo += "Parse();\n"
                            totales = keep.Parse() 
                            temp3 = keep.getNuevoTemporal()
                            codigo += keep.addIgual(temp3,keep.getValStack("SP"))
                            codigo += keep.addIgual(keep.getValStack(apuntador),temp3)
                            codigo += keep.addOperacion("SP","SP","-",keep.getStack())
                            if not "Parse" in keep.listaFuncion:
                                keep.listaFuncion["Parse"] = keep.codigoFuncion  
                                keep.codigoFuncion = ""  
                            keep.addCodigo(codigo)            
                            #keep.liberarTemporales(temp)
                            #keep.liberarTemporales(temp2)
                            #keep.liberarTemporales(temp3)
                                            
                            return {"apuntador":apuntador,"tipo":"Int64","valor": int(valor)}
                        elif isinstance(valor,dict):
                            if "apuntador" in valor:
                                apuntador = valor["apuntador"]
                                tipo = valor["tipo"]
                                val = valor["valor"]
                                if tipo == "String":  
                                    #Hacemos una copia del puntero que queremos parsear
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    codigo += keep.addOperacion("SP","SP","+",keep.getStack())
                                    codigo += "Parse();\n"
                                    totales = keep.Parse("-1") 
                                    temp3 = keep.getNuevoTemporal()
                                    codigo += keep.addIgual(temp3,keep.getValStack("SP"))
                                    codigo += keep.addIgual(keep.getValStack(apuntador),temp3)
                                    codigo += keep.addOperacion("SP","SP","-",keep.getStack())
                                    if not "Parse" in keep.listaFuncion:
                                        keep.listaFuncion["Parse"] = keep.codigoFuncion
                                        keep.codigoFuncion = ""    
                                    keep.addCodigo(codigo)            
                                    #keep.liberarTemporales(temp)
                                    #keep.liberarTemporales(temp2)
                                    #keep.liberarTemporales(temp3)  
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
                            apuntador = keep.getStack()-1
                            
                            #Hacemos una copia del puntero que queremos parsear
                            temp = keep.getNuevoTemporal()
                            temp2 = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                            codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                            codigo += keep.addIgual(keep.getValStack(temp2),temp)
                            codigo += keep.addOperacion("SP","SP","+",keep.getStack())
                            codigo += "ParseFloat();\n"
                            keep.ParseFloat() 
                            temp3 = keep.getNuevoTemporal()
                            codigo += keep.addIgual(temp3,keep.getValStack("SP"))
                            codigo += keep.addIgual(keep.getValStack(apuntador),temp3)
                            codigo += keep.addOperacion("SP","SP","-",keep.getStack())
                            if not "ParseFloat" in keep.listaFuncion:
                                keep.listaFuncion["ParseFloat"] = keep.codigoFuncion   
                                keep.codigoFuncion = ""
                            keep.addCodigo(codigo)             
                            #keep.liberarTemporales(temp)
                            #keep.liberarTemporales(temp2)
                            #keep.liberarTemporales(temp3)
                            try:
                                return {"apuntador":apuntador,"tipo":"Float64","valor":float(valor)}
                            except:
                                return {"apuntador":apuntador,"tipo":"Float64","valor":None}
                        elif isinstance(valor,dict):
                           if "apuntador" in valor:
                                apuntador = valor["apuntador"]
                                tipo = valor["tipo"]
                                val = valor["valor"]
                                if tipo == "String":  
                                    #Hacemos una copia del puntero que queremos parsear
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    codigo += keep.addOperacion("SP","SP","+",keep.getStack())
                                    codigo += "ParseFloat();\n"
                                    keep.ParseFloat() 
                                    temp3 = keep.getNuevoTemporal()
                                    codigo += keep.addIgual(temp3,keep.getValStack("SP"))
                                    codigo += keep.addIgual(keep.getValStack(apuntador),temp3)
                                    codigo += keep.addOperacion("SP","SP","-",keep.getStack())
                                    if not "ParseFloat" in keep.listaFuncion:
                                        keep.listaFuncion["ParseFloat"] = keep.codigoFuncion   
                                        keep.codigoFuncion = ""
                                    keep.addCodigo(codigo)             
                                    #keep.liberarTemporales(temp)
                                    #eep.liberarTemporales(temp2)
                                    #keep.liberarTemporales(temp3)
                                    try:
                                        return {"apuntador":apuntador,"tipo":"Float64","valor":float(valor)}
                                    except:
                                        return {"apuntador":apuntador,"tipo":"Float64","valor":None}
                        err = Errores(str(valor),"Semántico","Se ha producido un error al castear a cadena", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                    except ValueError:
                        err = Errores(str(valor),"Semántico","Error al intentar convertir a Float64", self.fila,self.columna)
                        tree.insertError(err)
                        return err
                
        elif self.funcion == Tipo_Primitivas.TRUNC:
            if self.tipo == Tipo_Dato.ENTERO:
                valor = self.valor.traducir(tree,table,keep)
                if isinstance(valor,float):
                    


                    return int(valor)
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

    def traducir(self, tree, table, keep):
        if self.funcion == Tipo_Primitivas.LENGTH:
            if isinstance(self.valor, NodoAST):
                val = self.valor.traducir(tree,table,keep)
                if isinstance(val,dict):   
                    if "tipo" in val:
                        if val["tipo"] == "Array":
                            T1= keep.getNuevoTemporal()
                            T2= keep.getNuevoTemporal()
                            stack = keep.getStack()
                            codigo = keep.addOperacion(T1,"SP","+",val["apuntador"])
                            codigo += keep.addIgual(T2, keep.getValStack(T1))
                            codigo += keep.addOperacion(T1,"SP","+",stack)
                            codigo += keep.addIgual(keep.getValStack(T1),T2)
                            codigo += keep.addOperacion("SP","SP","+",stack)
                            codigo += "length();\n"

                            if not "length" in keep.listaFuncion:
                                cod = keep.codigo
                                keep.codigo = ""
                                keep.Length()
                                keep.listaFuncion["length"] = keep.codigo
                                keep.codigo = cod
                            codigo += keep.addOperacion("SP","SP","-",stack)
                            codigo += keep.addOperacion(T1,"SP","+",stack)
                            codigo += keep.addIgual(T2,keep.getValStack(T1))
                            keep.addCodigo(codigo)
                            keep.PS = stack
                            keep.incrementarStack()
                            return {"temp":T2, "tipo": "Int64", "valor":T2}
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
