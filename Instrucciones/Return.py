from Abstractas.NodoArbol import NodoArbol
from Abstractas.NodoAST import NodoAST


class Return(NodoAST):

    def __init__(self, valor, fila, columna):
        self.valor = valor
        self.fila = fila 
        self.columna = columna
    
    def ejecutar(self, tree, table):
        if isinstance(self.valor, NodoAST):
            valor =  self.valor.ejecutar(tree,table)
            return Return(valor,self.fila,self.columna)
        else:
            return self
    def traducir(self, tree, table, keep):
        if isinstance(self.valor, NodoAST):
            valor = self.valor.traducir(tree,table,keep)
            if isinstance(valor,dict):
                if "llamada" in valor:
                    self.AsignandoReturn(keep,valor["apuntador"])
                    keep.stackreturn = valor
                    keep.HayReturn =True
                elif "apuntador" in valor:
                    self.AsignandoReturn(keep,valor["apuntador"])
                    #simbolo = Simbolo("return-"+keep.nombrefuncion,"return",table.nombre,self.fila,self.columna,valor["tipo"],keep.getStack())
                    #table.actualizarSimboloGlobal(simbolo)
                    #tree.agregarTS("return-"+keep.nombrefuncion,simbolo)
                    keep.stackreturn = valor
                    keep.HayReturn =True
                elif "temp" in valor:
                    keep.stackreturn = self.AsignandoReturn2(keep,valor["temp"],valor["tipo"])
                    #simbolo = Simbolo("return-"+keep.nombrefuncion,"return",table.nombre,self.fila,self.columna,keep.stackreturn["tipo"],keep.getStack())
                    #table.actualizarSimboloGlobal(simbolo)
                    #tree.agregarTS("return-"+keep.nombrefuncion,simbolo)
                    keep.HayReturn =True
            else:
                if isinstance(valor,int):
                    tipo = "Int64"
                elif isinstance(valor,float):
                    tipo = "Float64"
                elif isinstance(valor,str):
                    tipo = "String"
                
                keep.stackreturn = self.AsignandoReturn2(keep,valor,tipo)
                #simbolo = Simbolo("return-"+keep.nombrefuncion,"return",table.nombre,self.fila,self.columna,keep.stackreturn["tipo"],keep.getStack())
                #table.actualizarSimboloGlobal(simbolo)
                #tree.agregarTS("return-"+keep.nombrefuncion,simbolo)
                keep.HayReturn =True
        else:
            return self
    def getNodo(self):
        NodoNuevo = NodoArbol("RETURN")
        NodoNuevo.agregarHijo("return")
        if self.valor != None:
            NodoNuevo.agregarHijoNodo(self.valor.getNodo())
        NodoNuevo.agregarHijo(";")
        return NodoNuevo
    
    def AsignandoReturn(self,keep,apuntador):
        T1 = keep.getNuevoTemporal()
        T2 = keep.getNuevoTemporal()
        #T3 = keep.getNuevoTemporal()
        codigo ="//*****Asignando el valor al return*****\n"
        codigo += keep.addOperacion(T1,"SP","+",apuntador)
        codigo += keep.addIgual(T2,keep.getValStack(T1))
        #codigo += keep.addOperacion(T3,"SP","+",0)
        codigo += keep.addIgual(keep.getValStack("SP"),T2)
        keep.addCodigo(codigo)
        keep.addCodigo("return;\n")
        #keep.liberarTemporales(T1)
        #keep.liberarTemporales(T2)
        #keep.liberarTemporales(T3)
        

    def AsignandoReturn2(self,keep,valor,tipo):
        
        codigo ="//*****Asignando el valor al return*****\n"
        codigo += keep.addIgual(keep.getValStack("SP"),valor)
        keep.addCodigo(codigo)
        keep.addCodigo("return;\n")
        #keep.liberarTemporales(T1)
        return {"apuntador": 0, "tipo":tipo,"valor":valor}
    