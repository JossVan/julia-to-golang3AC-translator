from Expresiones.Acceso import Acceso
from Objetos.KeepData import KeepData
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from Abstractas.NodoArbol import NodoArbol
from Expresiones.Array import Array
from Expresiones.Identificador import Identificador
from Expresiones.Arreglos import Arreglos
from TablaSimbolos.Tipos import Tipo_Acceso, Tipo_Dato
from TablaSimbolos.Errores import Errores
from TablaSimbolos.Simbolo import Simbolo
from Abstractas.NodoAST import NodoAST

class Asignacion(NodoAST):

    def __init__(self, acceso, id, valor, tipo, fila, columna):
        self.acceso = acceso
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.fila = fila 
        self.columna = columna

    def ejecutar(self, tree, table):
        id =""
        if isinstance(self.id,Identificador):
            id = self.id.id
        elif isinstance(self.id, Array):
            self.id.actualizar(self.valor,tree,table)
            return
        elif isinstance(self.id, str):
            id = self.id
        elif isinstance(self.id, Acceso):
            id = self.id.verificar(tree,table,self.valor)
            return
        if self.tipo == None:
            if self.valor == None:
                simbolo = table.BuscarIdentificador(id)
                if simbolo != None:
                    if self.acceso == Tipo_Acceso.GLOBAL:
                        table.actualizarSimboloGlobal(simbolo)
                    else:
                        table.actualizarSimbolo(simbolo)
                    tree.agregarTS(id,simbolo)
                else:   
                    simbolo = Simbolo(id, None, self.acceso,self.fila,self.columna, "Ninguno")
                    if self.acceso == Tipo_Acceso.GLOBAL:
                        table.actualizarSimboloGlobal(simbolo)
                    else:
                        table.actualizarSimbolo(simbolo)
                    tree.agregarTS(id,simbolo)
            else:
                if isinstance(self.valor,list):
                    for val in self.valor :
                        if isinstance(val, Arreglos):
                            valor = val.ejecutar(tree,table)
                            if isinstance(valor,Errores):
                                return valor
                            simbolo = Simbolo(id, valor, self.acceso,self.fila,self.columna,"Arreglo")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            print("ERROR")
                else:
                    valor = self.valor.ejecutar(tree,table)
                    if isinstance(valor,Errores):
                        return valor
                    elif isinstance(valor, TablaSimbolos):
                        simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "STRUCT")
                    else:
                        simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Primitivo")
                    if self.acceso == Tipo_Acceso.GLOBAL:           
                        table.actualizarSimboloGlobal(simbolo)
                    else:
                        table.actualizarSimbolo(simbolo)
                    tree.agregarTS(id,simbolo)
        else:
            
            if self.valor != None:
                if self.tipo == Tipo_Dato.CADENA:
                    if isinstance(self.valor,NodoAST):
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor, str):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "String")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                            tree.insertError(err)
                            return err
                    elif isinstance(self.valor, list):
                        for val in self.valor :
                            if isinstance(val, Arreglos):
                                print("ES UN ARREGLO")
                    else:
                        error = Errores(self.valor,"Semántico","La variable declarada debe ser una cadena",self.fila,self.columna)
                        tree.insertError(error)
                elif self.tipo == Tipo_Dato.BOOLEANO:
                    if isinstance(self.valor,NodoAST):
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor, bool):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna,"Bool")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                            tree.insertError(err)
                            return err
                    elif isinstance(self.valor, list):
                        for val in self.valor :
                            if isinstance(val, Arreglos):
                                print("ES UN ARREGLO")
                    else: 
                        error = Errores(self.valor,"Semántico","El valor de la variable debe ser tipo booleano",self.fila,self.columna)
                        tree.insertError(error)
                elif self.tipo == Tipo_Dato.CARACTER:
                     if isinstance(self.valor,NodoAST):
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor, chr):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna,"Char")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                            tree.insertError(err)
                            return err
                     elif isinstance(self.valor, list):
                        for val in self.valor :
                            if isinstance(val, Arreglos):
                                print("ES UN ARREGLO")  
                     else: 
                        error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo caracter",self.fila,self.columna)
                        tree.insertError(error)
                elif self.tipo == Tipo_Dato.DECIMAL:
                    if isinstance(self.valor,NodoAST):
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor, float):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Float64")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                            tree.insertError(err)
                            return err
                    elif isinstance(self.valor, list):
                        for val in self.valor :
                            if isinstance(val, Arreglos):
                                print("ES UN ARREGLO")
                    else: 
                        error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Float64",self.fila,self.columna)
                        tree.insertError(error)
                elif self.tipo == Tipo_Dato.ENTERO:
                    if isinstance(self.valor,NodoAST):
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor, int):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Int64")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                            tree.insertError(err)
                            return err
                    elif isinstance(self.valor, list):
                        for val in self.valor :
                            if isinstance(val, Arreglos):
                                print("ES UN ARREGLO")
                    else: 
                        error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Int64",self.fila,self.columna)
                        tree.insertError(error)
                        return error
                else :
                    result = tree.getStruct(self.tipo)
                    if result == None:
                        error = Errores(self.valor,"Semántico","El tipo de la variable no existe",self.fila,self.columna)
                        tree.insertError(error)
                        return error
                    else:
                        valor = self.valor.ejecutar(tree,table)
                        if isinstance(valor,Errores):
                            return valor
                        if isinstance(valor, TablaSimbolos):
                            simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "STRUCT")
                        if self.acceso == Tipo_Acceso.GLOBAL:           
                            table.actualizarSimboloGlobal(simbolo)
                        else:
                            table.actualizarSimbolo(simbolo)
                        tree.agregarTS(id,simbolo)

    def traducir(self, tree, table,keep):
        id = ""
        if isinstance(self.id,Identificador):
            id = self.id.id
        else:
            id = self.id 
        
        if self.tipo == None:
            if self.valor == None:
                simbolo = table.BuscarIdentificador(id)
                if simbolo != None:
                    if self.acceso == Tipo_Acceso.GLOBAL:
                        table.actualizarSimboloGlobal(simbolo)
                    else:
                        table.actualizarSimbolo(simbolo)
                    tree.agregarTS(id,simbolo)
                else:   

                    simbolo = Simbolo(id, "nothing", table.nombre,self.fila,self.columna, "nothing",keep.getStack())
                    codigo = "//ASIGNACIÓN DE ESPACIO PARA LA VARIABLE\n"
                    temp = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(temp,"SP","+",keep.getStack())
                    codigo += keep.addIgual(keep.getValStack(temp),"-1")
                    #codigo += keep.addOperacion("SP","SP","+","1")
                    keep.incrementarStack()
                    keep.addCodigo(codigo)
                    if self.acceso == Tipo_Acceso.GLOBAL:
                        table.actualizarSimboloGlobal(simbolo)
                    else:
                        table.actualizarSimbolo(simbolo)
                    tree.agregarTS(id,simbolo)
            else:
                simbolo = table.BuscarIdentificador(id)
                existe = False
                if simbolo != None:
                    #SIGNIFICA QUE LA VARIABLE YA HA SIDO DECLARADA ANTERIORMENTE 
                    existe = True
                if isinstance(self.valor,list):
                    for val in self.valor :
                        if isinstance(val, Arreglos):
                            valor = val.ejecutar(tree,table)
                            if isinstance(valor,Errores):
                                return valor
                            simbolo = Simbolo(id, valor, self.acceso,self.fila,self.columna,"Arreglo")
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            print("ERROR")
                else:           
                    valor = self.valor.traducir(tree,table,keep)
                    if isinstance(valor,Errores):
                        return valor
                    elif isinstance(valor, TablaSimbolos):
                        simbolo = Simbolo(id,"",self.acceso,self.fila,self.columna, "STRUCT")
                    else:
                        if existe:
                            if isinstance(valor,str):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"String",simbolo.apuntador)
                            elif isinstance(valor,bool):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Bool",simbolo.apuntador)
                                if keep.etiquetaFalsa != "":
                                    keep.addCodigo(keep.etiquetaFalsa+":\n")
                                    keep.etiquetaFalsa = ""
                                if keep.etiquetaVerdadera != "":
                                    keep.addCodigo(keep.etiquetaVerdadera+":\n")
                                    keep.etiquetaVerdadera = ""
                                if valor: 
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    #keep.incrementarStack()
                                else:
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"0")
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    #keep.incrementarStack()                           
                            elif isinstance(valor,float):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Float64",simbolo.apuntador)
                                keep.liberarTemporales(temp)
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.addCodigo(codigo)
                            elif isinstance(valor,int):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Int64",simbolo.apuntador)
                                keep.liberarTemporales(temp)
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.addCodigo(codigo)                      
                            elif isinstance(valor,dict):
                                if "temp" in valor:
                                    val = valor["valor"]
                                    tipo = valor["tipo"]
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,valor["temp"])
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                
                                    simbolo = Simbolo(id,val,table.nombre,self.fila,self.columna,tipo,simbolo.apuntador)
                                    keep.liberarTemporales(temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                elif "etiquetas" in valor:
                                    simbolo = Simbolo(id,None,table.nombre,self.fila,self.columna,"Bool",simbolo.apuntador)
                                    ev = valor["etiquetas"][0]
                                    ef = valor["etiquetas"][1]
                                    nueva = keep.getNuevaEtiqueta()
                                    keep.addCodigo(ev+":\n")
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    codigo += "goto "+nueva+";\n"
                                    keep.addCodigo(codigo)
                                    keep.addCodigo(ef+":\n")
                                    codigo = keep.addIgual(temp,"0")
                                    temp3 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp3,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp3),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    codigo += nueva+":\n"
                                    keep.addCodigo(codigo)
                                    keep.liberarTemporales(temp3)
                                    keep.liberarTemporales(temp)
                                    keep.etiquetaFalsa = ""
                                    keep.etiquetaVerdadera=""
                                elif "apuntador" in valor:
                                    simbolo = Simbolo(id,valor["valor"],table.nombre,self.fila,self.columna,valor["tipo"],valor["apuntador"])
                                    if self.acceso == Tipo_Acceso.GLOBAL:           
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                    return 
                            if self.acceso == Tipo_Acceso.GLOBAL:
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                        else:
                            if isinstance(valor,str):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"String",keep.getStack()-1)
                            elif isinstance(valor,bool):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Bool",keep.getStack())
                                if keep.etiquetaFalsa != "":
                                    keep.addCodigo(keep.etiquetaFalsa+":\n")
                                    keep.etiquetaFalsa = ""
                                if keep.etiquetaVerdadera != "":
                                    keep.addCodigo(keep.etiquetaVerdadera+":\n")
                                    keep.etiquetaVerdadera = ""
                                if valor: 
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    keep.incrementarStack()
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                else:
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"0")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    keep.incrementarStack()  
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)                   
                            elif isinstance(valor,float):
                                temp = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                temp2 = keep.getNuevoTemporal()
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Float64",keep.getStack())
                                keep.liberarTemporales(temp)
                                keep.liberarTemporales(temp2)
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.addCodigo(codigo)
                            elif isinstance(valor,int):
                                temp = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                temp2 = keep.getNuevoTemporal()
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Int64",keep.getStack())
                                keep.liberarTemporales(temp)
                                keep.liberarTemporales(temp2)
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.addCodigo(codigo)                      
                            elif isinstance(valor,dict):
                                if "temp" in valor:
                                    val = valor["valor"]
                                    tipo = valor["tipo"]
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,valor["temp"])
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    simbolo = Simbolo(id,val,table.nombre,self.fila,self.columna,tipo,keep.getStack())
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                elif "etiquetas" in valor:
                                    simbolo = Simbolo(id,None,table.nombre,self.fila,self.columna,"Bool",keep.getStack())
                                    ev = valor["etiquetas"][0]
                                    ef = valor["etiquetas"][1]
                                    nueva = keep.getNuevaEtiqueta()
                                    keep.addCodigo(ev+":\n")
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    keep.incrementarStack()
                                    codigo += "goto "+nueva+";\n"
                                    keep.addCodigo(codigo)
                                    keep.addCodigo(ef+":\n")
                                    codigo = keep.addIgual(temp,"0")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    codigo += nueva+":\n"
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    keep.incrementarStack()
                                    keep.addCodigo(codigo)
                                    keep.etiquetaFalsa = ""
                                    keep.etiquetaVerdadera=""
                                    if self.acceso == Tipo_Acceso.GLOBAL:           
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                    return 
                                elif "apuntador" in valor:
                                    simbolo = Simbolo(id,valor["valor"],table.nombre,self.fila,self.columna,valor["tipo"],valor["apuntador"])
                                    if self.acceso == Tipo_Acceso.GLOBAL:           
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                    return 
                            if not isinstance(valor,str) and not isinstance(valor,bool):
                                keep.incrementarStack()
                            if self.acceso == Tipo_Acceso.GLOBAL:           
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
        else:
            simbolo = table.BuscarIdentificador(id)
            existe = False
            if simbolo != None:
                #SIGNIFICA QUE LA VARIABLE YA HA SIDO DECLARADA ANTERIORMENTE 
                existe = True
            if self.valor != None:
                if existe:
                    if self.tipo == Tipo_Dato.CADENA:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, str):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna, "String", simbolo.apuntador)
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else:
                            error = Errores(self.valor,"Semántico","La variable declarada debe ser una cadena",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.BOOLEANO:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, bool):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Bool",simbolo.apuntador)
                                if keep.etiquetaVerdadera!="":
                                    keep.addCodigo(keep.etiquetaVerdadera+":\n") 
                                if keep.etiquetaFalsa!="":
                                    keep.addCodigo(keep.etiquetaFalsa+":\n")
                                    
                                if valor: 
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    codigo += keep.addIgual(keep.getValStack(simbolo.apuntador),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    #keep.incrementarStack()
                                else:
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"0")
                                    codigo += keep.addIgual(keep.getValStack(simbolo.apuntador),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    #keep.incrementarStack()
                                
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            elif isinstance(valor,dict):
                                if "etiquetas" in valor:
                                    simbolo = Simbolo(id,None,table.nombre,self.fila,self.columna,"Bool",simbolo.apuntador)
                                    ev = valor["etiquetas"][0]
                                    ef = valor["etiquetas"][1]
                                    nueva = keep.getNuevaEtiqueta()
                                    keep.addCodigo(ev+":\n")
                                    temp = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    keep.addCodigo(codigo)
                                    keep.addCodigo(ef+":\n")
                                    codigo = keep.addIgual(temp,"0")
                                    temp2 = keep.getNuevoTemporal()
                                    codigo += keep.addOperacion(temp2,"SP","+",simbolo.apuntador)
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    codigo += nueva+":\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetaFalsa = ""
                                    keep.etiquetaVerdadera=""
                                    if self.acceso == Tipo_Acceso.GLOBAL:
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                elif "apuntador" in valor:
                                    simbolo = Simbolo(id,valor["valor"],table.nombre,self.fila,self.columna,valor["tipo"],valor["apuntador"])
                                    if self.acceso == Tipo_Acceso.GLOBAL:           
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                    return  
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser tipo booleano",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.CARACTER:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, chr):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Char",keep.getStack()-1)
                                #keep.incrementarStack()
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")  
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo caracter",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.DECIMAL:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, float):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Float64",keep.getStack())
                                keep.liberarTemporales(temp) 
                                keep.liberarTemporales(temp2)    
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.incrementarStack()
                                keep.addCodigo(codigo)
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Float64",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.ENTERO:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table, keep)
                            if isinstance(valor, int):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Int64",keep.getStack())
                                keep.liberarTemporales(temp)    
                                keep.liberarTemporales(temp2)    
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.incrementarStack()
                                keep.addCodigo(codigo)
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Int64",self.fila,self.columna)
                            tree.insertError(error)
                            return error
                    else :
                        result = tree.getStruct(self.tipo)
                        if result == None:
                            error = Errores(self.valor,"Semántico","El tipo de la variable no existe",self.fila,self.columna)
                            tree.insertError(error)
                            return error
                        else:
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor,Errores):
                                return valor
                            if isinstance(valor, TablaSimbolos):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna, "struct",keep.getStack())
                                keep.incrementarStack()
                            if self.acceso == Tipo_Acceso.GLOBAL:           
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
                else:
                    #LA VARIABLE ES NUEVA 
                    if self.tipo == Tipo_Dato.CADENA:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, str):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna, "String", keep.getStack()-1)
                                #keep.incrementarStack()
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else:
                            error = Errores(self.valor,"Semántico","La variable declarada debe ser una cadena",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.BOOLEANO:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, bool):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Bool",keep.getStack())
                                if keep.etiquetaVerdadera!="":
                                    keep.addCodigo(keep.etiquetaVerdadera+":\n") 
                                if keep.etiquetaFalsa!="":
                                    keep.addCodigo(keep.etiquetaFalsa+":\n")
                                    
                                if valor: 
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    keep.incrementarStack()
                                else:
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"0")
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    keep.addCodigo(codigo)
                                    keep.incrementarStack()
                                

                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            elif isinstance(valor,dict):
                                if "etiquetas" in valor:
                                    simbolo = Simbolo(id,None,table.nombre,self.fila,self.columna,"Bool",keep.getStack())
                                    ev = valor["etiquetas"][0]
                                    ef = valor["etiquetas"][1]
                                    nueva = keep.getNuevaEtiqueta()
                                    keep.addCodigo(ev+":\n")
                                    temp = keep.getNuevoTemporal()
                                    temp2 = keep.getNuevoTemporal()
                                    codigo = keep.addIgual(temp,"1")
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    keep.liberarTemporales(temp)
                                    keep.liberarTemporales(temp2)
                                    #codigo += keep.addIgual(keep.getValStack("SP"),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    keep.addCodigo(codigo)
                                    keep.addCodigo(ef+":\n")
                                    codigo = keep.addIgual(temp,"0")
                                    codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                    codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                    #codigo += keep.addIgual(keep.getValStack("SP"),temp)
                                    #codigo += keep.addOperacion("SP","SP","+","1")
                                    codigo += "goto "+nueva+";\n"
                                    codigo += nueva+":\n"
                                    keep.addCodigo(codigo)
                                    keep.etiquetaFalsa = ""
                                    keep.etiquetaVerdadera=""
                                    if self.acceso == Tipo_Acceso.GLOBAL:
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                elif "apuntador" in valor:
                                    simbolo = Simbolo(id,valor["valor"],table.nombre,self.fila,self.columna,valor["tipo"],valor["apuntador"])
                                    if self.acceso == Tipo_Acceso.GLOBAL:           
                                        table.actualizarSimboloGlobal(simbolo)
                                    else:
                                        table.actualizarSimbolo(simbolo)
                                    tree.agregarTS(id,simbolo)
                                    return  
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser tipo booleano",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.CARACTER:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, chr):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna,"Char",keep.getStack()-1)
                                #keep.incrementarStack()
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")  
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo caracter",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.DECIMAL:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor, float):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Float64",keep.getStack())
                                keep.liberarTemporales(temp)    
                                keep.liberarTemporales(temp2)    
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.incrementarStack()
                                keep.addCodigo(codigo)
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Float64",self.fila,self.columna)
                            tree.insertError(error)
                    elif self.tipo == Tipo_Dato.ENTERO:
                        if isinstance(self.valor,NodoAST):
                            valor = self.valor.traducir(tree,table, keep)
                            if isinstance(valor, int):
                                temp = keep.getNuevoTemporal()
                                temp2 = keep.getNuevoTemporal()
                                codigo = keep.addIgual(temp,valor)
                                codigo += keep.addOperacion(temp2,"SP","+",keep.getStack())
                                codigo += keep.addIgual(keep.getValStack(temp2),temp)
                                simbolo = Simbolo(id,valor,self.acceso,self.fila,self.columna, "Int64",keep.getStack())
                                keep.liberarTemporales(temp)    
                                keep.liberarTemporales(temp2)
                                #codigo += keep.addOperacion("SP","SP","+","1")
                                keep.incrementarStack()
                                keep.addCodigo(codigo)
                                if self.acceso == Tipo_Acceso.GLOBAL:
                                    table.actualizarSimboloGlobal(simbolo)
                                else:
                                    table.actualizarSimbolo(simbolo)
                                tree.agregarTS(id,simbolo)
                            else:
                                err = Errores(str(valor),"Semántico","Los tipos no coinciden", self.fila,self.columna)
                                tree.insertError(err)
                                return err
                        elif isinstance(self.valor, list):
                            for val in self.valor :
                                if isinstance(val, Arreglos):
                                    print("ES UN ARREGLO")
                        else: 
                            error = Errores(self.valor,"Semántico","El valor de la variable debe ser de tipo Int64",self.fila,self.columna)
                            tree.insertError(error)
                            return error
                    else :
                        result = tree.getStruct(self.tipo)
                        if result == None:
                            error = Errores(self.valor,"Semántico","El tipo de la variable no existe",self.fila,self.columna)
                            tree.insertError(error)
                            return error
                        else:
                            valor = self.valor.traducir(tree,table,keep)
                            if isinstance(valor,Errores):
                                return valor
                            if isinstance(valor, TablaSimbolos):
                                simbolo = Simbolo(id,valor,table.nombre,self.fila,self.columna, "struct",keep.getStack())
                                keep.incrementarStack()
                            if self.acceso == Tipo_Acceso.GLOBAL:           
                                table.actualizarSimboloGlobal(simbolo)
                            else:
                                table.actualizarSimbolo(simbolo)
                            tree.agregarTS(id,simbolo)
    def getNodo(self):
        NodoNuevo = NodoArbol("Asignación")
        if self.tipo == Tipo_Acceso.GLOBAL:
            NodoNuevo.agregarHijo("Global")
        elif self.tipo == Tipo_Acceso.LOCAL:
            NodoNuevo.agregarHijo("Local")

        if isinstance(self.id,NodoAST):
            NodoNuevo.agregarHijoNodo(self.id.getNodo())
        elif isinstance(self.id,str):
            NodoNuevo.agregarHijo(self.id)
        if isinstance(self.valor, NodoAST):
            NodoNuevo.agregarHijoNodo(self.valor.getNodo())
        elif isinstance(self.valor, list):
            for inst in self.valor:
                NodoNuevo.agregarHijoNodo(inst.getNodo())
        if self.tipo == Tipo_Dato.BOOLEANO:
            NodoNuevo.agregarHijo("::")
            NodoNuevo.agregarHijo("Bool")
        elif self.tipo == Tipo_Dato.CADENA:
            NodoNuevo.agregarHijo("::")
            NodoNuevo.agregarHijo("String")
        elif self.tipo == Tipo_Dato.ENTERO:
            NodoNuevo.agregarHijo("::")
            NodoNuevo.agregarHijo("Int64")
        elif self.tipo == Tipo_Dato.DECIMAL:
            NodoNuevo.agregarHijo("::")
            NodoNuevo.agregarHijo("Float64")
        elif self.tipo == Tipo_Dato.CARACTER:
            NodoNuevo.agregarHijo("::")
            NodoNuevo.agregarHijo("Char")
        
        NodoNuevo.agregarHijo(";")
        return NodoNuevo

