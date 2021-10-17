from TablaSimbolos.Errores import Errores
from TablaSimbolos.Tipos import Tipo_Aritmetico
from Abstractas.NodoArbol import NodoArbol
from Abstractas.NodoAST import NodoAST

class Aritmetica(NodoAST):

    def __init__(self, operador1,operacion,operador2, fila,columna):
        self.operador1 = operador1
        self.operador2 = operador2
        self.operacion = operacion
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):
        if self.operador1!=None and self.operador2!= None:
            result1 = self.operador1.ejecutar(tree,table)
            result2 = self.operador2.ejecutar(tree,table)
            if isinstance(result1,Errores) or isinstance(result2,Errores):
                return Errores("operación no permitida","Semántico","F", self.fila,self.columna)
                
            if self.operacion == Tipo_Aritmetico.SUMA:
                if isinstance(result1, str) or isinstance(result2,str) and result1!=None and result2 !=None:
                    return str(result1)+str(result2)  
                elif result1 == None:
                    err = Errores(result1,"Semántico","El valor es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                elif result2 == None:
                    err = Errores(result2,"Semántico","El valor es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                else:
                    return result1+result2
            if self.operacion == Tipo_Aritmetico.RESTA:
                if result1 == None:
                    err = Errores(result1,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                elif result2 == None:
                    err = Errores(result2,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                else:
                    return result1-result2
            if self.operacion == Tipo_Aritmetico.MULTIPLICACION:
                if result1 == None:
                    err = Errores(result1,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                elif result2 == None:
                    err = Errores(result2,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                else:
                    if isinstance(result1,str) or isinstance(result2,str):
                        return str(result1)+str(result2)
                    return result1*result2
            if self.operacion == Tipo_Aritmetico.DIVISION:
                if result2==0:
                    err = Errores(str(result2),"Semántico","No se puede dividir entre 0 duuh", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                if result1 == None:
                    err = Errores(result1,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                elif result2 == None:
                    err = Errores(result2,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                else:
                    return result1/result2
            if self.operacion == Tipo_Aritmetico.MODAL:
                if result2==0:
                    err = Errores(result2,"Semántico","División por 0", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                if result1 == None:
                    err = Errores(result1,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                elif result2 == None:
                    err = Errores(result2,"Semántico","El operador es indefinido", self.fila,self.columna)
                    tree.insertError(err)
                    return err
                else:
                    return result1%result2
            if self.operacion == Tipo_Aritmetico.POTENCIA:
                if (isinstance(result1,int) or isinstance(result1,float)) and (isinstance(result2,int) or isinstance(result2,float)):
                    return pow(result1,result2)
                elif(isinstance(result2,float) or isinstance(result2,int)):
                    cadena=""
                    for i in range(result2):
                        cadena+=result1
                    return cadena
    
    def traducir(self, tree, table, keep):
        if self.operador1 != None and self.operador2!=None:

            if isinstance(self.operador1,dict):
                if "apuntador" in self.operador1:
                    apuntador = int(self.operador1["apuntador"])
                    tipo = self.operador1["tipo"]
                    if tipo == "Float64" or tipo =="Int64":
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                        keep.addCodigo(codigo)
                        op1 = temp
                elif "temp" in self.operador1:
                    op1 = self.operador1['temp']
                elif "error" in self.operador1:
                    return self.operador1
            if isinstance(self.operador2,dict):
                if "apuntador" in self.operador2:
                    apuntador = int(self.operador2["apuntador"])
                    tipo = self.operador2["tipo"]
                    if tipo == "Float64" or tipo =="Int64":
                        temp = keep.getNuevoTemporal()
                        codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                        keep.addCodigo(codigo)
                        op2 = temp
                elif "temp" in self.operador2:
                    op2 = self.operador2['temp']
                elif "error" in self.operador2:
                    return self.operador2
            if not isinstance(self.operador1,dict):
                op1 = self.operador1.traducir(tree,table,keep)
                #pos1 = keep.getStack()-1
                if isinstance(op1,dict):
                    if "apuntador" in op1:
                        apuntador = int(op1["apuntador"])
                        tipo = op1["tipo"]
                        if tipo == "Float64" or tipo =="Int64":
                            temp = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                            keep.addCodigo(codigo)
                            op1 = temp
                    elif "temp" in op1:
                        op1= op1['temp']
                    elif "error" in op1:
                        return op1
            if not isinstance(self.operador2,dict):
                op2 = self.operador2.traducir(tree,table,keep)
                #pos2 = keep.getStack()-1
                if isinstance(op2,dict):
                    if "apuntador" in op2:
                        apuntador = int(op2["apuntador"])
                        tipo = op2["tipo"]
                        if tipo == "Float64" or tipo =="Int64":
                            temp = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                            keep.addCodigo(codigo)
                            op2 = temp
                    elif "temp" in op2:
                        op2= op2['temp']
                    elif "error" in op2:
                        return op2
            if self.operacion == Tipo_Aritmetico.SUMA:                
                temp = keep.getNuevoTemporal()
                codigo = keep.addOperacion(temp,op1,"+",op2)
                keep.addCodigo(codigo)
                return {"temp":temp}  
            elif self.operacion == Tipo_Aritmetico.RESTA:                
                temp = keep.getNuevoTemporal()
                codigo = keep.addOperacion(temp,op1,"-",op2)
                keep.addCodigo(codigo)
                return {"temp":temp}    
            elif self.operacion == Tipo_Aritmetico.MULTIPLICACION:                
                temp = keep.getNuevoTemporal()
                codigo = keep.addOperacion(temp,op1,"*",op2)
                keep.addCodigo(codigo)
                return {"temp":temp} 
            elif self.operacion == Tipo_Aritmetico.DIVISION:                
                
                #COMPROVACION DE DIVISIÓN POR 0
                ef = keep.getNuevaEtiqueta()
                es = keep.getNuevaEtiqueta()
                codigo = ""
                aux2 = op2
                if isinstance(op1,int) or isinstance(op1,float):
                    temp1 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp1,str(op1))
                    op1 = temp1
                if isinstance(op2,int) or isinstance(op2,float):
                    temp2 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp2,str(op2))
                    op2 = temp2
                temp = keep.getNuevoTemporal()
                codigo += "if ("+str(op2)+" != 0){\n\tgoto "+ef+"\n}\n"
                codigo += self.generarC3D_Cadenas(keep,"MATH ERROR")
                codigo += "goto "+ es+"\n"
                codigo += ef+":\n"
                codigo += keep.addOperacion(temp,"float64("+str(op1)+")","/","float64("+str(op2)+")")
                codigo += es+":\n"
                keep.addCodigo(codigo)
                if aux2 != 0:
                    return {"temp":temp}      
                else:
                    return {"error": "error"}      
            elif self.operacion == Tipo_Aritmetico.POTENCIA:
                temp0 = keep.getNuevoTemporal()
                temp1 = keep.getNuevoTemporal()
                temp2 = keep.getNuevoTemporal()
                temp3 = keep.getNuevoTemporal()
                codigo = keep.addIgual(temp0,op1)
                codigo += keep.addIgual(temp1,op2)
                codigo += keep.addIgual(temp2,1)
                codigo += keep.addIgual(temp3,op1)
                ei = keep.getNuevaEtiqueta()
                ev = keep.getNuevaEtiqueta()
                es = keep.getNuevaEtiqueta()
                codigo += ei+":\n"
                codigo += "if ("+temp2+"<"+temp1+"){\n\tgoto "+ ev+"\n}\ngoto "+es+"\n"
                codigo += ev+":\n"
                codigo += keep.addOperacion(temp3,temp3,"*",temp0)
                codigo += keep.addOperacion(temp2,temp2,"+","1")
                codigo += "goto "+ei+"\n"
                codigo += es +":\n"
                keep.addCodigo(codigo)
                keep.liberarTemporales(temp0)
                keep.liberarTemporales(temp1)
                keep.liberarTemporales(temp2)
                return {"temp":temp3}
    def getNodo(self):
        NuevoNodo = NodoArbol("Operación_Aritmetica")
        NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
        if self.operacion == Tipo_Aritmetico.SUMA:
            NuevoNodo.agregarHijo("+")
        elif self.operacion == Tipo_Aritmetico.RESTA:
            NuevoNodo.agregarHijo("-")
        elif self.operacion == Tipo_Aritmetico.MULTIPLICACION:
            NuevoNodo.agregarHijo("*")
        elif self.operacion == Tipo_Aritmetico.DIVISION:
            NuevoNodo.agregarHijo("/")
        elif self.operacion == Tipo_Aritmetico.MODAL:
            NuevoNodo.agregarHijo("%")
        elif self.operacion == Tipo_Aritmetico.POTENCIA:
            NuevoNodo.agregarHijo("^")
        NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        return NuevoNodo

    def getValor(self,tree, table, array):

        for i in array:
            if isinstance(i,NodoAST):
                val = i.ejecutar(tree,table)
    

    def generarC3D_Cadenas(self,keep,cadena):

        codigo = ""

        for caracter in cadena:

            codigoascii = ord(caracter)
            codigo += keep.imprimir(codigoascii,"c")

        return codigo