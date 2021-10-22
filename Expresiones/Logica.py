from Expresiones.Relacional import Relacional
from TablaSimbolos.Errores import Errores
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Logico, Tipo_Relacional
from Abstractas.NodoAST import NodoAST

class Logica(NodoAST):
    tipo = None
    apuntador = None
    valor = None
    
    def __init__(self, operador1, operador2, tipooperacion, fila, columna):
        self.operador1=operador1
        self.operador2 = operador2
        self.tipooperacion = tipooperacion
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):
        
        if self.operador1!=None and self.operador2!=None:
            resultado1= self.operador1.ejecutar(tree,table)
            resultado2= self.operador2.ejecutar(tree,table)
            if isinstance(resultado2,Errores) or isinstance(resultado1,Errores):
                return Errores("Operación no permitida", "Semántico", "F", self.fila,self.columna)
            if self.tipooperacion == Tipo_Logico.AND:
                if resultado1 and resultado2:
                    return True
                return False
            if self.tipooperacion == Tipo_Logico.OR:
                if resultado1 or resultado2:
                    return True
                return False
        if self.operador2== None and self.operador1 !=None:
            resultado1= self.operador1.ejecutar(tree,table)

            if self.tipooperacion == Tipo_Logico.DIFERENTE:
                if not resultado1:
                    return True
                return False

    def traducir(self, tree, table, keep):
        if self.operador1!=None and self.operador2!=None:
            # AQUI REALIZO LA PRIMERA CONDICIÓN DEL OPERADOR
            resultado1= self.operador1.traducir(tree,table,keep)
            self.verificar(resultado1,tree,table,keep)
            # ASIGNO LAS VARIABLES RESULTANTES A LOCALES
            valor = self.valor 
            tipo = self.tipo 
            apuntador = self.apuntador
            if self.tipooperacion == Tipo_Logico.AND:               
                if len(keep.etiquetas) == 0:
                    # LIMPIO LAS VARIABLES GLOBALES
                    self.valor = None
                    self.tipo = None 
                    self.apuntador = None 
                    # REALIZO LA SEGUNDA CONDICIÓN DEL OPERADOR 2
                    resultado2= self.operador2.traducir(tree,table,keep)
                    self.verificar(resultado2,tree,table,keep)
                    # ASIGNO LAS VARIABLES RESULTANTES A LAS LOCALES
                    valor2 = self.valor
                    apuntador2 = self.apuntador
                    tipo2 = self.tipo
                    if len(keep.etiquetas) == 0:
                        codigo = "//**********EMPEZANDO IF LÓGICOS**********\n"
                        if tipo == "Int64" or tipo == "Float64" or tipo2 == "Int64" or tipo2 == "Float64":
                            print("La condición debe ser booleana we")
                            return
                        elif tipo == "Bool":
                            if apuntador == None:
                                ev = keep.getNuevaEtiqueta()
                                ef = keep.getNuevaEtiqueta()
                                temp = keep.getNuevoTemporal()
                                val1 = ""
                                val2 =""
                                if valor:
                                    val1 = "1"
                                else:
                                    val1 = "0"
                                codigo += keep.addIgual(temp,val1)
                                if apuntador2 == None:
                                    if valor2:
                                        val2 = "1"
                                    else:
                                        val2 = "0"
                                    
                                    codigo += "if "+temp+" == "+val2 +"{\n\t goto "+ev+";\n}\n"
                                    codigo += "goto "+ef+";\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetas.append(ef)
                                    keep.etiquetas.append(ev)
                                    return valor and valor2
                                else:
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,keep.getValStack(apuntador2))
                                    codigo += "//*****CONDICIÓN LÓGICA AND*****\n"
                                    codigo += "if "+val1+" == "+temp +"{\n\t goto "+ev+";\n}\n"
                                    codigo += "goto "+ef+";\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetas.append(ef)
                                    keep.etiquetas.append(ev)
                                    return valor and valor2
                            else:
                                ev = keep.getNuevaEtiqueta()
                                ef = keep.getNuevaEtiqueta()
                                temp = keep.getNuevoTemporal()
                                codigo = "//*****CONDICIÓN LÓGICA AND******\n"
                                val2 =""                                
                                codigo += keep.addIgual(temp,keep.getValStack(apuntador))
                                if apuntador2 == None:
                                    if valor2:
                                        val2 = "1"
                                    else:
                                        val2 = "0"
                                    
                                    codigo += "if "+temp+" == "+val2 +"{\n\t goto "+ev+";\n}\n"
                                    codigo += "goto "+ef+";\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetas.append(ef)
                                    keep.etiquetas.append(ev)
                                    return valor and valor2
                                else:
                                    temp1 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,keep.getValStack(apuntador2))
                                    codigo += "//*****CONDICIÓN LÓGICA AND*****\n"
                                    codigo += "if "+temp+" == "+temp1 +"{\n\t goto "+ev+";\n}\n"
                                    codigo += "goto "+ef+";\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetas.append(ef)
                                    keep.etiquetas.append(ev)
                                    return valor and valor2
                elif len (keep.etiquetas)== 1:
                    codigo = "//**********EMPEZANDO IF LÓGICOS**********\n"
                    #ETIQUETAS PARA EL OPERADOR 1
                    etiquetaSalida = keep.getNuevaEtiqueta()
                    keep.addCodigo("goto "+etiquetaSalida+";\n")
                    ev = keep.etiquetas.pop()
                    keep.addCodigo(ev+":\n")
                    # LIMPIO LAS VARIABLES GLOBALES
                    self.valor = None
                    self.tipo = None 
                    self.apuntador = None 
                    # REALIZO LA SEGUNDA CONDICIÓN DEL OPERADOR 2
                    resultado2= self.operador2.traducir(tree,table,keep)
                    self.verificar(resultado2,tree,table,keep)
                    # ASIGNO LAS VARIABLES RESULTANTES A LAS LOCALES
                    valor2 = self.valor
                    apuntador2 = self.apuntador
                    tipo2 = self.tipo
                    if apuntador2 == None:
                        if len(keep.etiquetas) == 1:
                            keep.addCodigo("goto "+etiquetaSalida+";\n")
                            evv = keep.etiquetas.pop()
                            keep.addCodigo(evv+":\n")
                            keep.etiquetas.append(etiquetaSalida)
                            return valor and valor2
                        elif len(keep.etiquetas) == 0:
                            evv = keep.getNuevaEtiqueta()
                            if not valor2:
                                cod = "if 1 == "+str(int(valor2))+" {goto "+evv+";}\ngoto "+etiquetaSalida+";\n"
                                keep.addCodigo(cod)
                                keep.addCodigo(evv+":\n")
                            else:
                                keep.addCodigo("goto "+etiquetaSalida+";\n")
                                keep.addCodigo(evv+":\n")
                    keep.etiquetas.append(etiquetaSalida)
                    return valor and valor2 
                    #keep.addCodigo(ef+":\n")
                    
                elif len(keep.etiquetas):
                    codigo = "//**********EMPEZANDO IF LÓGICOS**********\n"


            if self.tipooperacion == Tipo_Logico.OR:
                print("OR")
        if self.operador2== None and self.operador1 !=None:
            resultado1= self.operador1.ejecutar(tree,table)

            if self.tipooperacion == Tipo_Logico.DIFERENTE:
                if not resultado1:
                    return True
                return False

    def getNodo(self):
        NuevoNodo = NodoArbol("Lógicas")
        if self.tipooperacion == Tipo_Logico.AND:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("AND")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Logico.OR:
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())
            NuevoNodo.agregarHijo("OR")
            NuevoNodo.agregarHijoNodo(self.operador2.getNodo())
        elif self.tipooperacion == Tipo_Logico.DIFERENTE:
            NuevoNodo.agregarHijo("!")
            NuevoNodo.agregarHijoNodo(self.operador1.getNodo())

        return NuevoNodo


    def verificar(self,resultado,tree,table,keep):     
            if isinstance(resultado,dict):
                if "apuntador" in resultado:
                    self.apuntador = int(resultado["apuntador"])
                    self.tipo = resultado["tipo"]
                    self.valor = resultado["valor"]
                elif "temp" in resultado:
                    op1 = resultado['temp']
                    self.valor = op1 
                elif "error" in resultado:
                    return resultado
            if not isinstance(resultado,dict):
                if isinstance(resultado,NodoAST):
                    op1 = resultado.traducir(tree,table,keep)
                else:
                    op1 = resultado 
                # si es un diccionario quiere decir que es ID
                if isinstance(op1,dict):
                    if "apuntador" in op1:
                        self.apuntador = int(op1["apuntador"])
                        self.tipo = op1["tipo"]
                        self.valor = op1["valor"]
                    elif "temp" in op1:
                        self.valor = int(op1['valor'])
                        op1= op1['temp']                       
                    elif "error" in op1:
                        return op1
                elif isinstance(op1,str):
                    self.tipo = "String"
                    self.apuntador = keep.getStack()-1
                    self.valor = op1
                    self.cadena = True
                elif isinstance(op1,bool):
                    self.valor = op1
                    self.tipo = "Bool"
                elif isinstance(op1,int):
                    self.tipo = "Int64"
                    if self.valor == "":
                        self.valor = op1 
                elif isinstance(op1,float):
                    self.tipo = "Float64"
                    if self.valor == "":
                        self.valor = op1 
                
            if isinstance(resultado,Errores):
                return Errores("Operación no permitida", "Semántico", "F", self.fila,self.columna)