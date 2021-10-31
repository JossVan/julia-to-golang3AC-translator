from Expresiones.Arreglos import Arreglos
from Abstractas.NodoArbol import NodoArbol
from Instrucciones.Return import Return
from TablaSimbolos.Simbolo import Simbolo
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from TablaSimbolos.Errores import Errores
from Abstractas.NodoAST import NodoAST

class Llamadas(NodoAST):

    def __init__(self, id, parametros, fila, columna):
        self.id = id 
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
        
    def ejecutar(self, tree, table):
        funcion = tree.getFuncion(self.id)
        struct = tree.getStruct(self.id)
        if funcion == None and struct == None:
            err = Errores(self.id, "Semántico", "Instruccion no reconocida", self.fila, self.columna)
            tree.insertError(err)
            return
        elif funcion != None and struct == None:
            NuevaTabla = TablaSimbolos(self.id,table)
            if self.parametros != None:
                if len(funcion.parametros) == len(self.parametros):
                    contador = 0
                    for parametro in self.parametros:
                        valor = parametro.ejecutar(tree,table)
                        variable = funcion.parametros[contador].id
                        simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,"No definido")
                        NuevaTabla.addSimboloLocal(simbolo)
                        tree.agregarTS(self.id,simbolo)
                        contador = contador+1

                    resultado = funcion.ejecutar(tree,NuevaTabla)
                    if isinstance(resultado,Return):
                        return resultado.valor
                    elif isinstance(resultado, Errores):
                        return resultado
                else :
                    err = Errores(self.id, "Semántico", "No coinciden los parámetros de llamada", self.fila,self.columna)
                    tree.insertError(err)
            else:
                resultado = funcion.ejecutar(tree,NuevaTabla)
                if isinstance(resultado,Return):
                    return resultado.valor
        elif struct != None:
            #HAY UNA ASIGNACION DE TIPO STRUCT
            elementos = struct.ejecutar(tree,table)
            if len(elementos) == len(self.parametros):
                contador = 0
                tablita = TablaSimbolos(self.id)
                for par in  self.parametros:
                    verificar = elementos[contador].verificarTipo(tree, table, par)
                    if  verificar:
                        if isinstance(par,NodoAST):
                            par = par.ejecutar(tree,table)
                        tablita.tabla[elementos[contador].id] = par
                    elif isinstance(verificar,Errores):
                        return verificar
                    contador = contador +1
                return tablita

    def traducir(self, tree, table, keep):
        funcion = tree.getFuncion(self.id)
        struct = tree.getStruct(self.id)
        if funcion == None and struct == None:
            err = Errores(self.id, "Semántico", "Instruccion no reconocida", self.fila, self.columna)
            tree.insertError(err)
            return
        elif funcion != None and struct == None:
            NuevaTabla = TablaSimbolos(self.id,table)
            if self.parametros != None:
                if len(funcion.parametros) == len(self.parametros):
                    contador = 0
                    cont2 = 0
                    T0 = keep.getNuevoTemporal()
                    keep.addCodigo(keep.addIgual(T0,keep.getStack()))
                    stack = keep.getStack()
                    for parametro in self.parametros:
                        # VERIFICO QUE TIPO DE PARÁMETRO PUEDA SER 
                        valor = parametro.traducir(tree,table,keep)
                        # SI ES UN PRIMITIVO 
                        if isinstance(valor,str):
                            # VALOR DEL ULTIMO PUNTERO LIBRE 
                            #punteroSiguiente = keep.getStack()
                            #puntero = keep.getStack()-1
                            variable = funcion.parametros[contador].id
                            simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,"String",cont2)
                            NuevaTabla.addSimboloLocal(simbolo)
                            tree.agregarTS(self.id,simbolo)
                        elif isinstance(valor,int) or isinstance(valor,float):
                            puntero = keep.getStack()
                            #T1 = keep.getNuevoTemporal()
                            T2 = keep.getNuevoTemporal()
                            cod = "//******INGRESO DE PARÁMETROS AL NUEVO ENTORNO*******\n"
                            # ALMACENO EL VALOR DEL STACK EN UNA VARIABLE TEMPORAL 
                            cod += keep.addOperacion(T2,"SP","+" ,puntero)
                            cod += keep.addIgual(keep.getValStack(T2),valor)
                            variable = funcion.parametros[contador].id
                            if isinstance(valor,float):
                                tipo = "Float64"
                            else:
                                tipo = "Int64"
                            simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,tipo,cont2)
                            NuevaTabla.addSimboloLocal(simbolo)
                            tree.agregarTS(self.id,simbolo)
                            keep.incrementarStack()
                            keep.addCodigo(cod)
                        elif isinstance(valor,dict):
                            if "apuntador" in valor:
                                puntero = valor["apuntador"]
                                if valor["tipo"] == "String":
                                    # VALOR DEL ULTIMO PUNTERO LIBRE 
                                    #punteroSiguiente = keep.getStack()
                                    T1 = keep.getNuevoTemporal()
                                    T2 = keep.getNuevoTemporal()
                                    T3 = keep.getNuevoTemporal()
                                    T4 = keep.getNuevoTemporal()
                                    T5 = keep.getNuevoTemporal()
                                    L1 = keep.getNuevaEtiqueta()
                                    L2 = keep.getNuevaEtiqueta()
                                    cod = "//******INGRESO DE PARÁMETROS AL NUEVO ENTORNO*******\n"
                                    # ALMACENO EL VALOR DE LA PRIMERA POSICIÓN DE LA CADENA EN EL HEAP 
                                    cod += keep.addOperacion(T1,"SP","+",puntero)
                                    cod += keep.addIgual(T2,keep.getValStack(T1))
                                    cod += "//Guardo la posición libre del heap\n"
                                    cod += keep.addIgual(T3,"HP")
                                    cod += L1+":\n"
                                    cod += keep.addIgual(T4,keep.getValHeap(T2))
                                    cod += "if "+T4+" == -1 {goto " + L2+";}\n"
                                    cod += keep.addIgual(keep.getValHeap("HP"), T4)
                                    cod += keep.addOperacion("HP","HP","+","1")
                                    cod += keep.addOperacion(T2,T2,"+","1")
                                    cod += "goto "+L1+";\n"
                                    cod += L2+":\n"
                                    cod += keep.addIgual(keep.getValHeap("HP"), "-1")
                                    cod += keep.addOperacion("HP","HP","+","1")
                                    cod += keep.addOperacion(T5,"SP","+",keep.getStack())
                                    cod += keep.addIgual(keep.getValStack(T5),T3)
                                    keep.addCodigo(cod)
                                    keep.incrementarStack()
                                    keep.liberarTemporales(T1)
                                    keep.liberarTemporales(T2)
                                    keep.liberarTemporales(T3)
                                    keep.liberarTemporales(T4)
                                    keep.liberarTemporales(T5)
                                    variable = funcion.parametros[contador].id
                                    simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,"String",cont2)
                                elif valor["tipo"] == "Int64" or valor["tipo"] == "Float64":
                                    T1 = keep.getNuevoTemporal()
                                    T2 = keep.getNuevoTemporal()
                                    T3 = keep.getNuevoTemporal()
                                    cod = "//*****ENVIANDO PARÁMETROS AL ENTORNO*****\n"
                                    cod += keep.addOperacion(T1,"SP","+",puntero)
                                    cod += keep.addIgual(T2, keep.getValStack(T1))
                                    cod += keep.addOperacion(T3,"SP","+",keep.getStack())
                                    cod += keep.addIgual(keep.getValStack(T3),T2)
                                    keep.addCodigo(cod)
                                    keep.liberarTemporales(T1)
                                    keep.liberarTemporales(T2)
                                    keep.liberarTemporales(T3)
                                    keep.incrementarStack()
                                    variable = funcion.parametros[contador].id
                                    simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,valor["tipo"],cont2)
                                NuevaTabla.addSimboloLocal(simbolo)
                                tree.agregarTS(self.id,simbolo)
                            elif "temp" in valor:
                                if valor["tipo"] == "Int64" or valor["tipo"] == "Float64":
                                    T3 = keep.getNuevoTemporal()
                                    cod = "//*****ENVIANDO PARÁMETROS AL ENTORNO*****\n"
                                    cod += keep.addOperacion(T3,"SP","+",keep.getStack())
                                    cod += keep.addIgual(keep.getValStack(T3),valor["temp"])
                                    keep.addCodigo(cod)
                                    keep.liberarTemporales(T3)
                                    keep.incrementarStack()
                                    variable = funcion.parametros[contador].id
                                simbolo = Simbolo(variable,valor,self.id,self.fila,self.columna,valor["tipo"],cont2)
                                NuevaTabla.addSimboloLocal(simbolo)
                                tree.agregarTS(self.id,simbolo)
                        contador = contador+1
                        cont2 = cont2+1
                    keep.addCodigo(keep.addOperacion("SP","SP","+",T0))
                    keep.addCodigo(self.id+"();\n")
                    keep.addCodigo(keep.addOperacion("SP","SP","-",T0))
                    keep.PS = cont2
                    resultado = funcion.traducir(tree,NuevaTabla,keep)
                    keep.PS = stack
                    if isinstance(resultado,Return):
                        if isinstance(resultado.valor,dict):
                            if "apuntador" in resultado.valor:
                                simbolo = Simbolo("return",valor,self.id,self.fila,self.columna,resultado.valor["tipo"],T0)
                                table.addSimboloLocal(simbolo)
                                tree.agregarTS(self.id,simbolo)
                                return {"apuntador":T0, "tipo":resultado.valor["tipo"],"valor":None}
                            elif "temp" in resultado.valor:
                                return {"apuntador":T0, "tipo":resultado.valor["tipo"],"valor":None}
                        return resultado.valor
                    elif isinstance(resultado, Errores):
                        return resultado
                    else:
                        return resultado
                else :
                    err = Errores(self.id, "Semántico", "No coinciden los parámetros de llamada", self.fila,self.columna)
                    tree.insertError(err)
            else:
                resultado = funcion.ejecutar(tree,NuevaTabla)
                if isinstance(resultado,Return):
                    return resultado.valor
        elif struct != None:
            #HAY UNA ASIGNACION DE TIPO STRUCT
            elementos = struct.ejecutar(tree,table)
            if len(elementos) == len(self.parametros):
                contador = 0
                tablita = TablaSimbolos(self.id)
                for par in  self.parametros:
                    verificar = elementos[contador].verificarTipo(tree, table, par)
                    if  verificar:
                        if isinstance(par,NodoAST):
                            par = par.ejecutar(tree,table)
                        tablita.tabla[elementos[contador].id] = par
                    elif isinstance(verificar,Errores):
                        return verificar
                    contador = contador +1
                return tablita
    def getNodo(self):
        
        NodoPadre = NodoArbol("Llamada")
        Nodoid = NodoArbol("Identificador")
        Nodopar = NodoArbol("Parámetros")
        Nodoid.agregarHijo(self.id)
        NodoPadre.agregarHijoNodo(Nodoid)
        NodoPadre.agregarHijo("(")
        cont = 1
        if self.parametros != None:
            for parametro in self.parametros:
                Nodopar.agregarHijoNodo(parametro.getNodo())
                if cont < len(self.parametros):
                    Nodopar.agregarHijo(",")
                    cont= cont+1
            NodoPadre.agregarHijoNodo(Nodopar)
        NodoPadre.agregarHijo(")")
        return NodoPadre