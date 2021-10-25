from TablaSimbolos.Errores import Errores
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Logico, Tipo_Relacional
from Abstractas.NodoAST import NodoAST

class Relacional(NodoAST):

    def __init__(self, operador1, operador2, tipooperacion, fila, columna):
        self.operador1 = operador1
        self.operador2 = operador2
        self.tipooperacion = tipooperacion
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):
        if self.operador1!=None and self.operador2!=None:
            resultado1 = self.operador1.ejecutar(tree,table)
            resultado2 = self.operador2.ejecutar(tree,table)
            if isinstance(resultado1,Errores) or isinstance(resultado2,Errores):
                return False
            if self.tipooperacion == Tipo_Relacional.MAYOR:
                if resultado1>resultado2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MENOR:
               
                if resultado1<resultado2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MENOR_IGUAL:
                if resultado1<= resultado2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MAYOR_IGUAL:
                if resultado1>= resultado2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.IGUAL:
                if resultado1 == resultado2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.DIFERENTE:
                if resultado1 != resultado2:
                    return True
                return False
            
    def traducir(self, tree, table, keep):
        if self.operador1!=None and self.operador2!=None:
            resultado1 = self.operador1.traducir(tree,table,keep)
            tipo = ""
            apuntador = None
            tipo2 = ""
            apuntador2 = None
            valor = ""
            valor2 = ""
            etiquetas = []
            etiquetas2 = []
            temp1 = None
            temp2 = None
            tip = False
            tip2 = False
            if isinstance(resultado1,dict):
                if "apuntador" in resultado1:
                    apuntador = int(resultado1["apuntador"])
                    tipo = resultado1["tipo"]
                    valor = resultado1["valor"]             
                    tip = True
                elif "temp" in resultado1:
                    op1 = resultado1['temp']
                    valor = int(resultado1['valor'])
                    tipo = resultado1['tipo']
                elif "bool" in resultado1:
                    valor = resultado1["bool"]
                    etiquetas = resultado1["etiquetas"]
                    tipo = "Bool"
                    et = keep.getNuevaEtiqueta()
                    codigo = etiquetas[0]+":\n"
                    temp1 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp1,"1")
                    codigo += "goto "+et+";\n"
                    codigo += etiquetas[1]+":\n"
                    codigo += keep.addIgual(temp1,"0")
                    codigo += et+":\n"
                    keep.addCodigo(codigo)
                elif "error" in resultado1:
                    return resultado1
            if not isinstance(resultado1,dict):
                if isinstance(resultado1,NodoAST):
                    op1 = resultado1.traducir(tree,table,keep)
                else: 
                    op1 = resultado1 
                # si es un diccionario quiere decir que es ID
                if isinstance(op1,dict):
                    if "apuntador" in op1:
                        apuntador = int(op1["apuntador"])
                        tipo = op1["tipo"]
                        valor = op1["valor"]
                        Tip = True
                    elif "temp" in op1:
                        valor = int(op1['valor'])
                        op1= op1['temp']
                        tipo = "Float64"
                    elif "bool" in op1:
                        valor = op1["bool"]
                        etiquetas = op1["etiquetas"]
                        tipo = "Bool"
                        et = keep.getNuevaEtiqueta()
                        codigo = etiquetas[0]+":\n"
                        temp1 = keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp1,"1")
                        codigo += "goto "+et+";\n"
                        codigo += etiquetas[1]+":\n"
                        codigo += keep.addIgual(temp1,"0")
                        codigo += et+":\n"
                        keep.addCodigo(codigo)
                    elif "error" in op1:
                        return op1
                elif isinstance(op1,str):
                    tipo = "String"
                    apuntador = keep.getStack()-1
                    valor = op1
                elif isinstance(op1,bool):
                    valor = op1
                    tipo == "Bool"
                    temp1 = str(int(valor))
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
            resultado2 = self.operador2.traducir(tree,table,keep)
            if isinstance(resultado2,dict):
                if "apuntador" in resultado2:
                    apuntador2 = int(resultado2["apuntador"])
                    tipo2 =  resultado2["tipo"]
                    valor2 = resultado2["valor"]
                    tip2 = True
                elif "temp" in resultado2:
                    op2 = resultado2['temp']
                    valor2 = int(resultado2['valor'])
                    tipo2 = resultado2['tipo']
                elif "bool" in resultado2:
                    valor = resultado2["bool"]
                    tipo2 = "Bool"
                    etiquetas = resultado2["etiquetas"]
                    et = keep.getNuevaEtiqueta()
                    codigo = etiquetas[0]+":\n"
                    temp2 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp2,"1")
                    codigo += "goto "+et+";\n"
                    codigo += etiquetas[1]+":\n"
                    codigo += keep.addIgual(temp2,"0")
                    codigo += et+":\n"
                    keep.addCodigo(codigo)
                elif "error" in resultado2:
                    return resultado2
            
            if not isinstance(resultado2,dict):
                if isinstance(resultado2,NodoAST):
                    op2 = resultado2.traducir(tree,table,keep)
                else: 
                    op2 = resultado2 
                #pos2 = keep.getStack()-1
                if isinstance(op2,dict):
                    if "apuntador" in op2:
                        apuntador2 = int(op2["apuntador"])
                        tipo2 = op2["tipo"]
                        valor2 = op2["valor"]                    
                        tip2 = True
                    elif "temp" in op2:
                        valor2 = int(op2['valor'])
                        op2= op2['temp']
                        tipo2 = "Float64"
                    elif "bool" in op2:
                        valor = op2["bool"]
                        tipo = "Bool"
                        etiquetas = op2["etiquetas"]
                        et = keep.getNuevaEtiqueta()
                        codigo = etiquetas[0]+":\n"
                        temp2= keep.getNuevoTemporal()
                        codigo += keep.addIgual(temp2,"1")
                        codigo += "goto "+et+";\n"
                        codigo += etiquetas[1]+":\n"
                        codigo += keep.addIgual(temp2,"0")
                        codigo += et+":\n"
                        keep.addCodigo(codigo)
                    elif "error" in op2:
                        return op2       
                elif isinstance(op2,str):
                    tipo2 = "String"
                    apuntador2 = keep.getStack()-1
                    valor2 = op2
                elif isinstance(op2,bool):
                    valor2 = op2 
                    tipo2 = "Bool"
                    temp2 = str(int(valor2))
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
            if isinstance(resultado1,Errores) or isinstance(resultado2,Errores):
                return False
            if self.tipooperacion == Tipo_Relacional.MAYOR:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,">",valor2,valor,tip,tip2,temp1,temp2)
                    if valor>valor2:
                        return {"bool":True,"etiquetas": etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.longitud(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
            elif self.tipooperacion == Tipo_Relacional.MENOR:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"<",valor2,valor,tip,tip2,temp1,temp2)
                    if valor<valor2:
                        return {"bool":True,"etiquetas":etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.longitud(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
            elif self.tipooperacion == Tipo_Relacional.MENOR_IGUAL:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"<=",valor2,valor,tip,tip2,temp1,temp2)
                    if valor<= valor2:
                        return {"bool":True,"etiquetas":etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.longitud(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
            elif self.tipooperacion == Tipo_Relacional.MAYOR_IGUAL:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,">=",valor2,valor,tip,tip2,temp1,temp2)
                    if valor>= valor2:
                        return {"bool":True,"etiquetas":etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.longitud(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
            elif self.tipooperacion == Tipo_Relacional.IGUAL:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"==",valor2,valor,tip,tip2,temp1,temp2)
                    if valor == valor2:
                        return {"bool":True,"etiquetas": etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.Igual(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
            elif self.tipooperacion == Tipo_Relacional.DIFERENTE:
                if tipo != "String" and tipo2 != "String":
                    etiquetas = self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"!=",valor2,valor,tip,tip2,temp1,temp2)
                    if valor != valor2:
                        return {"bool":True,"etiquetas":etiquetas}
                    return {"bool":False,"etiquetas":etiquetas}
                else:
                    return self.Igual(keep,apuntador,valor,apuntador2,valor2,self.tipooperacion)
    def getNodo(self):
        NuevoNodo = NodoArbol("Lógicas")
        if self.tipooperacion == Tipo_Relacional.MAYOR:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo(">")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Relacional.MENOR:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("<")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Relacional.MAYOR_IGUAL:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo(">=")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Relacional.MENOR_IGUAL:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("<=")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Relacional.IGUAL:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("==")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Relacional.DIFERENTE:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("!=")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        return NuevoNodo
    
    def revisar(self,keep,puntero,tipo,puntero2,tipo2, operador,valor2,valor,tip,tip2,temp1,temp22):
        if keep.etiquetaVerdadera == "" and keep.etiquetaFalsa == "":
            ef = keep.getNuevaEtiqueta()
            ev = keep.getNuevaEtiqueta()
        elif keep.etiquetaFalsa != "" and keep.etiquetaVerdadera == "":
            ev = keep.getNuevaEtiqueta()
            ef = keep.etiquetaFalsa
        elif keep.etiquetaVerdadera != "" and keep.etiquetaFalsa == "":
            ev = keep.etiquetaVerdadera
            ef = keep.getNuevaEtiqueta()
        elif keep.etiquetaVerdadera != "" and keep.etiquetaFalsa != "":
            ev = keep.etiquetaVerdadera
            ef = keep.etiquetaFalsa
        if temp1 != None and temp22 != None:
            codigo = "//OPERACIÓN RELACIONAL BOOLEANA\n"
            codigo += "if "+temp1+operador+temp22+" {goto "+ev +";}\ngoto "+ef+";\n"
            keep.addCodigo(codigo)
            return [ev,ef]
        if tip and tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,keep.getValStack(puntero))
            codigo += keep.addIgual(temp2,keep.getValStack(puntero2))
            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {goto "+ev +";}\ngoto "+ef+";\n"
                keep.addCodigo(codigo)
                return [ev,ef]
            else:
                print("paso por una cadena")
        elif tip and not tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,keep.getValStack(puntero))
            codigo += keep.addIgual(temp2,valor2)

            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {goto "+ev +";}\ngoto "+ef+";\n"
                keep.addCodigo(codigo)
                return [ev,ef]
            else:
                print("paso por una cadena")
        elif not tip and tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,valor)
            codigo += keep.addIgual(temp2,keep.getValStack(puntero2))

            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {goto "+ev +";}\ngoto "+ef+";\n"
                keep.addCodigo(codigo)
                return [ev,ef]
            else:
                print("paso por una cadena")
        elif not tip and not tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,valor)
            codigo += keep.addIgual(temp2,valor2)
            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {goto "+ev +";}\ngoto "+ef+";\n"
                keep.addCodigo(codigo)
                return [ev,ef]
            elif tipo == "Bool" and tipo2 == "Bool":
                codigo += "if "+temp+operador+temp2+" {goto "+ev +";}\ngoto "+ef+";\n"
                keep.addCodigo(codigo)
                return [ev,ef]
            else:
                print("paso por una cadena")
        
    #Método para comparar cadenas
    def Igual(self,keep,apuntador1,valor1,apuntador2,valor2,operador):
        codigo = "//**********COMPARACIÓN DE CADENAS**********\n"
        #if tip1 and tip2:
        #OBTENGO LA PRIMERA POSICION DEL HEAP
        temp = keep.getNuevoTemporal()
        temp2 = keep.getNuevoTemporal()
        codigo += "//Obtengo del stack, la posición del heap\n"
        codigo += keep.addIgual(temp,keep.getValStack(apuntador1))
        codigo += "//Obtengo el valor del primer caracter del heap\n"
        temp3 = keep.getNuevoTemporal()
        #codigo += keep.addIgual(tempIndice,temp)
        codigo += keep.addIgual(temp3,keep.getValHeap(temp))
        codigo += "//Obtengo del stack, la posición del heap\n"
        codigo += keep.addIgual(temp2,keep.getValStack(apuntador2))
        codigo += "//Obtengo el valor del primer caracter del heap\n"
        temp4 = keep.getNuevoTemporal()
        #codigo += keep.addIgual(tempIndice2,temp2)
        codigo += keep.addIgual(temp4,keep.getValHeap(temp2))
        
        #CREO UNA ETIQUETA PARA INICIAR EL CICLO 
        ei = keep.getNuevaEtiqueta()
        eo = keep.getNuevaEtiqueta()
        es = keep.getNuevaEtiqueta()
        codigo += ei+":\n" 
        ev = keep.getNuevaEtiqueta()
        ef = keep.getNuevaEtiqueta()
        codigo += "if "+temp3+"=="+temp4+" {goto "+eo+";}\ngoto "+es+";\n"
        codigo += eo+":\n"
        #AQUI SE HACE EL AUMENTO A LAS PILAS
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp3,keep.getValHeap(temp))
        codigo += keep.addOperacion(temp2,temp2,"+","1")
        codigo += keep.addIgual(temp4,keep.getValHeap(temp2))
        codigo += "if "+temp3+" == -1" +"{goto "+ev+";}\ngoto "+ei+";\n"     
        codigo += ev+":\n"
        ev2 = keep.getNuevaEtiqueta()
        #ef2 = keep.getNuevaEtiqueta()
        codigo += "if "+temp4+" == -1" +"{goto "+ef+";}\ngoto "+ei+";\n"

        keep.addCodigo(codigo)
        if operador == Tipo_Relacional.IGUAL:
            return {"bool":valor1 == valor2,"etiquetas":[ef,es]}
        elif operador == Tipo_Relacional.DIFERENTE:
            return {"bool":valor1 == valor2,"etiquetas":[es,ef]}

    def longitud(self,keep,apuntador1,valor1,apuntador2,valor2,operador):
        codigo = "//**********COMPARACIÓN DE CADENAS**********\n"
        #if tip1 and tip2:
        #OBTENGO LA PRIMERA POSICION DEL HEAP
        contador = keep.getNuevoTemporal()
        temp = keep.getNuevoTemporal()
        temp2 = keep.getNuevoTemporal()
        codigo += keep.addIgual(contador,"0")
        codigo += "//Obtengo del stack, la posición del heap\n"
        codigo += keep.addIgual(temp,keep.getValStack(apuntador1))
        codigo += "//Obtengo el valor del primer caracter del heap\n"
        temp3 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp3,keep.getValHeap(temp))
        
        #CREO UNA ETIQUETA PARA INICIAR EL CICLO 
        ei = keep.getNuevaEtiqueta()
        es = keep.getNuevaEtiqueta()
        codigo += ei+":\n" 
        ef = keep.getNuevaEtiqueta()
        codigo += "if "+temp3+" != -1" +"{goto "+ef+";}\ngoto "+es+";\n"
        #AQUI SE HACE EL AUMENTO A LAS PILAS
        codigo += ef+":\n"
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp3,keep.getValHeap(temp))
        codigo += keep.addOperacion(contador,contador,"+","1")
        codigo += "goto "+ei+";\n"
        codigo += es+":\n"
        temp2 = keep.getNuevoTemporal()
        contador2 = keep.getNuevoTemporal()
        codigo += keep.addIgual(contador2,"0")
        codigo += "//Obtengo del stack, la posición del heap\n"
        codigo += keep.addIgual(temp2,keep.getValStack(apuntador2))
        codigo += "//Obtengo el valor del primer caracter del heap\n"
        temp4 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp4,keep.getValHeap(temp2))

        ei2 = keep.getNuevaEtiqueta()
        es2 = keep.getNuevaEtiqueta()
        codigo += ei2+":\n" 
        ef2 = keep.getNuevaEtiqueta()
        codigo += "if "+temp4+" != -1" +"{goto "+ef2+";}\ngoto "+es2+";\n"
        #AQUI SE HACE EL AUMENTO A LAS PILAS
        codigo += ef2+":\n"
        codigo += keep.addOperacion(temp2,temp2,"+","1")
        codigo += keep.addIgual(temp4,keep.getValHeap(temp2))
        codigo += keep.addOperacion(contador2,contador2,"+","1")
        codigo += "goto "+ei2+";\n"
        codigo += es2+":\n"

        evv = keep.getNuevaEtiqueta()
        eff = keep.getNuevaEtiqueta()
        if operador == Tipo_Relacional.MAYOR:
            codigo += "if "+contador+">"+contador2+" {goto "+evv+";}\ngoto "+eff+";\n"
        elif operador == Tipo_Relacional.MAYOR_IGUAL:
            codigo += "if "+contador+">="+contador2+" {goto "+evv+";}\ngoto "+eff+";\n"
        elif operador == Tipo_Relacional.MENOR:
            codigo += "if "+contador+"<"+contador2+" {goto "+evv+";}\ngoto "+eff+";\n"
        elif operador == Tipo_Relacional.MENOR_IGUAL:
            codigo += "if "+contador+"<="+contador2+" {goto "+evv+";}\ngoto "+eff+";\n"

        

        keep.addCodigo(codigo)

        return {"bool":valor1 == valor2,"etiquetas":[evv,eff]}





