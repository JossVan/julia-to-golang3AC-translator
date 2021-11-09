
from Instrucciones.Funciones import Funciones
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
            tipo = ""
            apuntador = 0
            tipo2 = ""
            apuntador2 = 0
            valor = ""
            valor2 = ""
            cadena = False
            cadena2 = False
            if isinstance(self.operador1,dict):
                if "apuntador" in self.operador1:
                    apuntador = int(self.operador1["apuntador"])
                    tipo = self.operador1["tipo"]
                    valor = self.operador1["valor"]
                    if tipo == "Float64" or tipo =="Int64":
                        temp = keep.getNuevoTemporal()
                        temp2 = keep.getNuevoTemporal()
                        codigo = keep.addOperacion(temp2,"SP","+",apuntador)
                        codigo += keep.addIgual(temp,keep.getValStack(temp2))
                        keep.addCodigo(codigo)
                        op1 = temp
                elif "temp" in self.operador1:
                    op1 = self.operador1['temp']
                    valor = op1
                    tipo = self.operador1['tipo']
                elif "error" in self.operador1:
                    return self.operador1
            if isinstance(self.operador2,dict):
                if "apuntador" in self.operador2:
                    apuntador2 = int(self.operador2["apuntador"])
                    tipo2 = self.operador2["tipo"]
                    valor2 = self.operador2["valor"]
                    if tipo2 == "Float64" or tipo2 =="Int64":
                        temp = keep.getNuevoTemporal()
                        temp2 = keep.getNuevoTemporal()
                        codigo = keep.addOperacion(temp2,"SP","+",apuntador2)
                        codigo += keep.addIgual(temp,keep.getValStack(temp2))
                        keep.addCodigo(codigo)
                        op2 = temp
                elif "temp" in self.operador2:
                    op2 = self.operador2['temp']
                    tipo2 = self.operador2['tipo']
                    valor2 = op2
                elif "error" in self.operador2:
                    return self.operador2
            if not isinstance(self.operador1,dict):
                if isinstance(self.operador1,NodoAST):
                    op1 = self.operador1.traducir(tree,table,keep)
                # si es un diccionario quiere decir que es ID
                if isinstance(op1,dict):
                    if "apuntador" in op1:
                        apuntador = int(op1["apuntador"])
                        tipo = op1["tipo"]
                        valor = op1["valor"]
                        if tipo == "Float64" or tipo =="Int64":
                            temp = keep.getNuevoTemporal()
                            temp2 = keep.getNuevoTemporal()
                            codigo = keep.addOperacion(temp2,"SP","+",apuntador)
                            codigo += keep.addIgual(temp,keep.getValStack(temp2))
                            keep.addCodigo(codigo)
                            op1 = temp
                    elif "temp" in op1:
                        valor = op1['temp']
                        tipo = op1['tipo']
                        op1= op1['temp']
                    elif "error" in op1:
                        return op1
                elif isinstance(op1,str):
                    tipo = "String"
                    apuntador = keep.getStack()-1
                    valor = op1
                    cadena = True
                elif isinstance(op1,bool):
                    valor = op1 
                elif isinstance(op1,int):
                    apuntador= op1 
                    if valor == "":
                        valor = op1 
                    tipo = "Int64"
                elif isinstance(op1,float):
                    apuntador= op1 
                    if valor == "":
                        valor = op1 
                    tipo = "Float64"
                elif isinstance(op1,Funciones):
                    id = op1.nombre
                    res = table.BuscarIdentificador("return-"+id)
                    if res == None:
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador = res.getApuntador()
                    tipo = res.getTipo()
                    valor =res.getValor()
                    T1 = keep.getNuevoTemporal()
                    T2 = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(T1,"SP","+", keep.apuntador_return)
                    codigo += keep.addIgual(T2,keep.getValStack(T1))
                    keep.addCodigo(codigo)
                    op1 = T2
            if not isinstance(self.operador2,dict):
                if isinstance(self.operador2,NodoAST):
                    op2 = self.operador2.traducir(tree,table,keep)
                #pos2 = keep.getStack()-1
                if isinstance(op2,dict):
                    if "apuntador" in op2:
                        apuntador2 = int(op2["apuntador"])
                        tipo2 = op2["tipo"]
                        valor2 = op2["valor"]
                        if tipo2 == "Float64" or tipo2 =="Int64":
                            temp = keep.getNuevoTemporal()
                            temp2 = keep.getNuevoTemporal()
                            codigo = keep.addOperacion(temp2,"SP","+",apuntador2)
                            codigo += keep.addIgual(temp,keep.getValStack(temp2))
                            keep.addCodigo(codigo)
                            op2 = temp
                    elif "temp" in op2:
                        valor2 = op2['temp']
                        tipo2 = op2['tipo']
                        op2= op2['temp']
                    elif "error" in op2:
                        return op2       
                elif isinstance(op2,str):
                    tipo2 = "String"
                    apuntador2 = keep.getStack()-1
                    valor2 = op2
                    cadena2 = True  
                elif isinstance(op2,bool):
                    valor2 = op2
                elif isinstance(op2,int):
                    apuntador2= op2
                    if valor2 == "":
                        valor2 = op2
                    tipo2 = "Int64"
                elif isinstance(op2,float):
                    apuntador2= op2
                    if valor2 == "":
                        valor2 = op2
                    tipo2 = "Float64"
                elif isinstance(op2,Funciones):
                    id = op2.nombre
                    res = table.BuscarIdentificador("return-"+id)
                    if res == None:
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador2 = res.getApuntador()
                    tipo2 = res.getTipo()
                    valor2 =res.getValor()
                    T1 = keep.getNuevoTemporal()
                    T2 = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(T1,"SP","+", keep.apuntador_return)
                    codigo += keep.addIgual(T2,keep.getValStack(T1))
                    keep.addCodigo(codigo)
                    op2 = T2
            if self.operacion == Tipo_Aritmetico.SUMA:    
                result = self.Concatenacion(keep,tipo,tipo2,apuntador,apuntador2,valor,valor2,cadena,cadena2)
                if not result:
                    temp = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(temp,op1,"+",op2)
                    keep.addCodigo(codigo)
                    if tipo == "Int64" and tipo2 == "Int64":
                        tipo = "Int64"
                    else:
                        tipo = "Float64"
                    return {"temp":temp, "valor": -1, "tipo":tipo}  
                else:
                    return result
            elif self.operacion == Tipo_Aritmetico.RESTA:                
                temp = keep.getNuevoTemporal()
                codigo = keep.addOperacion(temp,op1,"-",op2)
                keep.addCodigo(codigo)
                if tipo == "Int64" and tipo2 == "Int64":
                        tipo = "Int64"
                else:
                    tipo = "Float64"
                return {"temp":temp , "valor":-1,"tipo":tipo}    
            elif self.operacion == Tipo_Aritmetico.MULTIPLICACION:  
                result = self.Concatenacion(keep,tipo,tipo2,apuntador,apuntador2,valor,valor2,cadena,cadena2)
                if not result:              
                    temp = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(temp,op1,"*",op2)
                    keep.addCodigo(codigo)
                    
                    return {"temp":temp,"valor": -1, "tipo":"Float64"} 
                else:
                    return result
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
                codigo += "if "+str(op2)+" != 0 {\n\tgoto "+ef+";\n}\n"
                codigo += self.generarC3D_Cadenas(keep,"MATH ERROR")
                codigo += "goto "+ es+";\n"
                codigo += ef+":\n"
                codigo += keep.addOperacion(temp,str(op1),"/",str(op2))
                codigo += es+":\n"
                keep.addCodigo(codigo)
                if aux2 != 0:
                    
                    return {"temp":temp, "valor": -1, "tipo":"Float64"}      
                else:
                    return {"error": "error"}      
            elif self.operacion == Tipo_Aritmetico.POTENCIA:
                if tipo == "String":
                    return self.multiplicidad(keep,valor,valor2)
                elif tipo != "String" and tipo2 != "String":
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
                    codigo += "if "+temp2+"<"+temp1+" {\n\tgoto "+ ev+";\n}\ngoto "+es+";\n"
                    codigo += ev+":\n"
                    codigo += keep.addOperacion(temp3,temp3,"*",temp0)
                    codigo += keep.addOperacion(temp2,temp2,"+","1")
                    codigo += "goto "+ei+";\n"
                    codigo += es +":\n"
                    keep.addCodigo(codigo)
                    #keep.liberarTemporales(temp0)
                    #keep.liberarTemporales(temp1)
                    #keep.liberarTemporales(temp2)
                    if tipo == "Int64" and tipo2 == "Int64":
                        tipo = "Int64"
                    else:
                        tipo = "Float64"
                    return {"temp":temp3, "valor": -1, "tipo":tipo}
            elif self.operacion == Tipo_Aritmetico.MODAL:
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
                codigo += "if "+str(op2)+" != 0 {\n\tgoto "+ef+";\n}\n"
                codigo += self.generarC3D_Cadenas(keep,"MATH ERROR")
                codigo += "goto "+ es+";\n"
                codigo += ef+":\n"
                codigo += keep.addIgual(temp,"math.Mod("+str(op1)+","+str(op2)+")")
                codigo += es+":\n"
                keep.addCodigo(codigo)
                if aux2 != 0:
                    if tipo == "Int64" and tipo2 == "Int64":
                        tipo = "Int64"
                    else:
                        tipo = "Float64"
                    return {"temp":temp, "valor": -1, "tipo":tipo}      
                else:
                    return {"error": "error"}  
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
    
    def concatenar(self,keep,apuntador):
        codigo="//INICIO DE LA CONCATENACIÓN DE SUMA\n"
        # CRANDO VARIABLES TEMPORALES PARA ALMACENAR EL APUNTADO Y VALOR DEL STACK EN ESA POSICION
        temp = keep.getNuevoTemporal()
        codigo += keep.addOperacion(temp,"SP","+",apuntador)
        temp2 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp2,keep.getValStack(temp))
        # AQUÍ EMPIEZA EL ACCESO AL HEAP
        # GENERO UNA ETIQUETA NUEVA
        etiquetaNueva = keep.getNuevaEtiqueta()
        etiquetaSalida = keep.getNuevaEtiqueta()
        codigo += etiquetaNueva+":\n"
        temp3 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
        codigo += "if "+temp3+"== -1 {\n\tgoto "+etiquetaSalida+";\n}\n"
        codigo += keep.addIgual(keep.getValHeap("HP"), temp3)
        codigo += keep.addOperacion(temp2,temp2,"+","1")
        codigo += keep.addOperacion("HP","HP","+","1")
        keep.incrementarHeap()
        codigo += "goto "+ etiquetaNueva+";\n"
        codigo += etiquetaSalida+":\n"
        #codigo += keep.addOperacion("SP","SP","+","1")
        #incrementamos el valor del stack para la siguiente entrada
        #keep.incrementarStack()
        keep.addCodigo(codigo)
        #keep.liberarTemporales(temp)
        #keep.liberarTemporales(temp2)
        #keep.liberarTemporales(temp3)
    
 
    def Concatenacion(self, keep,tipo,tipo2,apuntador,apuntador2,valor,valor2,cadena,cadena2):
        codigo = ""
        if tipo == "String":
            temp = keep.getNuevoTemporal()
            keep.addCodigo(keep.addIgual(temp,"HP"))
            self.concatenar(keep,apuntador)
            if tipo2 == "String":
                self.concatenar(keep,apuntador2)
                codigo += keep.addIgual(keep.getValHeap("HP"),"-1")
                codigo += keep.addOperacion("HP","HP","+","1")
                temp2 = keep.getNuevoTemporal()
                codigo += keep.addOperacion(temp2,"SP","+",apuntador)
                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                keep.addCodigo(codigo)
                return {"valor":valor+valor2,"apuntador":apuntador,"tipo":tipo}     
              
        return False        
    
    def multiplicidad(self,keep,cadena, cantidad):
        temp = keep.getNuevoTemporal()
        codigo = ""
        temp2 = keep.getNuevoTemporal()
        temp3 = keep.getNuevoTemporal()
        etiquetaRetorno = keep.getNuevaEtiqueta()
        codigo += keep.addIgual(temp2,cantidad)
        codigo += keep.addIgual(temp3,"0")
        codigo += keep.addIgual(temp,"HP")
        codigo += etiquetaRetorno+":\n"
        for caracter in cadena:
            codigoascii = ord(caracter)
            valor = keep.addIgual(keep.getValHeap("HP"),codigoascii)
            valor += keep.addOperacion("HP","HP","+","1")
            codigo+=valor
            keep.incrementarHeap()
        codigo += keep.addOperacion(temp3,temp3,"+","1")
        codigo += "if "+temp3+" <"+temp2+" {\n\tgoto "+etiquetaRetorno+";\n}\n"
        codigo += keep.addIgual(keep.getValHeap("HP"),"-1")
        keep.incrementarHeap()
        codigo += keep.addOperacion("HP","HP","+","1")
        temp4 = keep.getNuevoTemporal()
        codigo += keep.addOperacion(temp4,"SP","+",keep.getStack())
        codigo += keep.addIgual(keep.getValStack(temp4),temp)
        #codigo += keep.addOperacion("SP","SP","+","1")
        keep.incrementarStack()
        keep.addCodigo(codigo)
        #keep.liberarTemporales(temp)
        #keep.liberarTemporales(temp2)
        #keep.liberarTemporales(temp3)
        cad  =""
        for i in range(cantidad):
            cad+=cadena
        return cad
         