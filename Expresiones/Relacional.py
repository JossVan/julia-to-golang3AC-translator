from TablaSimbolos.Errores import Errores
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Relacional
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
            resultado2 = self.operador2.traducir(tree,table,keep)
            tipo = ""
            apuntador = 0
            tipo2 = ""
            apuntador2 = 0
            valor = ""
            valor2 = ""
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
                    valor = op1
                elif "error" in resultado1:
                    return resultado1
            if isinstance(resultado2,dict):
                if "apuntador" in resultado2:
                    apuntador2 = int(resultado2["apuntador"])
                    tipo2 =  resultado2["tipo"]
                    valor2 = resultado2["valor"]
                    
                    tip2 = True
                elif "temp" in resultado2:
                    op2 = resultado2['temp']
                    valor2 = op2
                    tipo2 = "Float64"
                elif "error" in resultado2:
                    return resultado2
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
                    elif "error" in op1:
                        return op1
                elif isinstance(op1,str):
                    tipo = "String"
                    apuntador = keep.getStack()-1
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
                elif issubclass(op1,bool):
                    valor = op1
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
                    elif "error" in op2:
                        return op2       
                elif isinstance(op2,str):
                    tipo2 = "String"
                    apuntador2 = keep.getStack()-1
                    valor2 = op2
                elif isinstance(op2,int):
                    apuntador2= op2
                    if valor2 == "":
                        valor2 = op2
                    tipo2 = "Int64"
                elif isinstance(op2,bool):
                    valor2 = op2 
                elif isinstance(op2,float):
                    apuntador2= op2
                    if valor2 == "":
                        valor2 = op2
                    tipo2 = "Float64"
            if isinstance(resultado1,Errores) or isinstance(resultado2,Errores):
                return False
            if self.tipooperacion == Tipo_Relacional.MAYOR:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,">",valor2,valor,tip,tip2)
                if valor>valor2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MENOR:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"<",valor2,valor,tip,tip2)
                if valor<valor2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MENOR_IGUAL:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"<=",valor2,valor,tip,tip2)
                if valor<= valor2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.MAYOR_IGUAL:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,">=",valor2,valor,tip,tip2)
                if valor>= valor2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.IGUAL:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"==",valor2,valor,tip,tip2)
                if valor == valor2:
                    return True
                return False
            elif self.tipooperacion == Tipo_Relacional.DIFERENTE:
                self.revisar(keep,apuntador,tipo,apuntador2,tipo2,"!=",valor2,valor,tip,tip2)
                if valor != valor2:
                    return True
                return False
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
    
    def revisar(self,keep,puntero,tipo,puntero2,tipo2, operador,valor2,valor,tip,tip2):
        ev = keep.getNuevaEtiqueta()
        #ef = keep.getNuevaEtiqueta()
        #keep.etiquetas.append(ef)
        keep.etiquetas.append(ev)
        if tip and tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,keep.getValStack(puntero))
            codigo += keep.addIgual(temp2,keep.getValStack(puntero2))
            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {\n\tgoto "+ev +";\n}\n"
                keep.addCodigo(codigo)
            else:
                print("paso por una cadena")
        elif tip and not tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,keep.getValStack(puntero))
            codigo += keep.addIgual(temp2,valor2)

            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {\n\tgoto "+ev +";\n}\n"
                keep.addCodigo(codigo)
            else:
                print("paso por una cadena")
        elif not tip and tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,valor)
            codigo += keep.addIgual(temp2,keep.getValStack(puntero2))

            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {\n\tgoto "+ev +";\n}\n"
                keep.addCodigo(codigo)
            else:
                print("paso por una cadena")
        elif not tip and not tip2:
            codigo = "//OPERACIÓN RELACIONAL\n"
            temp = keep.getNuevoTemporal()
            temp2 = keep.getNuevoTemporal()
            codigo += keep.addIgual(temp,valor)
            codigo += keep.addIgual(temp2,valor2)
            if (tipo == "Int64" or tipo == "Float64") and (tipo2 == "Int64" or tipo2=="Float64"):
                codigo += "if "+temp+operador+temp2+" {\n\tgoto "+ev +";\n}\n"
                keep.addCodigo(codigo)
            else:
                print("paso por una cadena")
        