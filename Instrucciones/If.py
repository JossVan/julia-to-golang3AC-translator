from TablaSimbolos.Errores import Errores
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from Abstractas.NodoAST import NodoAST

class If(NodoAST):

    def __init__(self, condicion, instrucciones_if, instrucciones_elseif, instrucciones_else, fila, columna):
        self.condicion = condicion
        self.instrucciones_if = instrucciones_if
        self.instrucciones_elseif = instrucciones_elseif
        self.instrucciones_else = instrucciones_else 
        self.fila = fila
        self.columna = columna
    
    def ejecutar(self, tree, table):
        condicion = self.condicion.ejecutar(tree,table)
        if(bool(condicion) == True):
            nuevaTabla = TablaSimbolos("If",table)
            for instruccion in self.instrucciones_if:
                resp=instruccion.ejecutar(tree,nuevaTabla)
                if isinstance(resp, Continue):
                    return resp
                elif isinstance(resp,Break):
                    return resp
                elif isinstance(resp, Return):
                    return resp
                elif isinstance(resp, Errores):
                    return resp
        elif self.instrucciones_elseif != None :
            nuevaTabla = TablaSimbolos("elseif",table)
            resp = self.instrucciones_elseif.ejecutar(tree,nuevaTabla)
            if isinstance(resp, Continue):
                return resp
            elif isinstance(resp,Break):
                return resp
            elif isinstance(resp, Return):
                return resp
            elif isinstance(resp,Errores):
                return resp
        else:
            if(self.instrucciones_else!=None):
                nuevaTabla = TablaSimbolos("else",table)
                for instruccion in self.instrucciones_else:
                    resp= instruccion.ejecutar(tree,nuevaTabla)
                    if isinstance(resp, Continue):
                        return resp
                    elif isinstance(resp,Break):
                        return resp
                    elif isinstance(resp, Return):
                        return resp
                    elif isinstance(resp, Errores):
                        return resp
        
    def traducir(self, tree, table, keep):
        resultado = self.condicion.traducir(tree,table,keep)
        if isinstance(resultado,bool):
            if keep.etiquetaVerdadera == "":
                nuevaTabla = TablaSimbolos("If",table)
                if self.instrucciones_if != None:
                    for instruccion in self.instrucciones_if:
                        resp = instruccion.traducir(tree,nuevaTabla,keep)
            elif keep.etiquetaVerdadera != "":
                keep.addCodigo(keep.etiquetaVerdadera+":\n")
                keep.etiquetaVerdadera = ""
                nuevaTabla = TablaSimbolos("If",table)
                if self.instrucciones_if != None:
                    for instruccion in self.instrucciones_if:
                        resp = instruccion.traducir(tree,nuevaTabla,keep)
            if keep.etiquetaFalsa != "":
                keep.addCodigo(keep.etiquetaFalsa+":\n")
                keep.etiquetaFalsa = ""
                if self.instrucciones_elseif != None:
                    nuevaTabla = TablaSimbolos("elseif",table)
                    resp = self.instrucciones_elseif.traducir(tree,nuevaTabla,keep)
                if self.instrucciones_else != None:
                    nuevaTabla = TablaSimbolos("else",table)
                    for instruccion in self.instrucciones_else:
                        resp= instruccion.traducir(tree,nuevaTabla,keep)
            
        elif isinstance(resultado,dict):
            if "etiquetas" in resultado:
                salida = keep.getNuevaEtiqueta()

                etiquetaVerdadera = resultado["etiquetas"][0]
                etiquetaFalsa = resultado["etiquetas"][1]                
                keep.addCodigo(etiquetaVerdadera+":\n")
                nuevaTabla = TablaSimbolos("If",table)
                for instruccion in self.instrucciones_if:
                    resp = instruccion.traducir(tree,nuevaTabla,keep)
                    if isinstance(resp,dict):
                        if "break" in resp:
                            keep.addCodigo("//*******BREAK*******\n")
                            keep.addCodigo(resp["cad"])
                        elif "continue":
                            keep.addCodigo("//*******CONTINUE*******\n")
                            keep.addCodigo(resp["cad"])
                        
                    keep.etiquetaFalsa = ""
                    keep.etiquetaVerdadera = "" 
                keep.addCodigo("goto "+salida+";\n")
                keep.addCodigo(etiquetaFalsa+":\n")                
                if self.instrucciones_elseif != None:
                    nuevaTabla = TablaSimbolos("elseif",table)
                    resp = self.instrucciones_elseif.traducir(tree,nuevaTabla,keep)
                if self.instrucciones_else != None:
                    nuevaTabla = TablaSimbolos("else",table)
                    for instruccion in self.instrucciones_else:
                        resp= instruccion.traducir(tree,nuevaTabla,keep)
                        if isinstance(resp,dict):
                            if "break" in resp:
                                keep.addCodigo("//*******BREAK*******\n")
                                keep.addCodigo(resp["cad"])
                            elif "continue":
                                keep.addCodigo("//*******CONTINUE*******\n")
                                keep.addCodigo(resp["cad"])
                            if isinstance(resp, Return):
                                return resp
                        keep.etiquetaFalsa = ""
                        keep.etiquetaVerdadera = "" 
                keep.addCodigo(salida+":\n")       
                keep.etiquetaFalsa = ""
                keep.etiquetaVerdadera = ""   
                


    def getNodo(self):
        NodoPadre = NodoArbol("If")
        # Se crea un nodo para la condición y se le introduce el hijo que es la condición
        NodoCondicion = NodoArbol("Condicion")
        NodoCondicion.agregarHijoNodo(self.condicion.getNodo())
        # Se crea un nuevo nodo para las instrucciones del if
        NodoIf = NodoArbol("Instrucciones_if")
        NodoElse = NodoArbol("Instrucciones_elseif")
        if self.instrucciones_if != None:
            for instruccion_if in self.instrucciones_if:
                NodoIf.agregarHijoNodo(instruccion_if.getNodo())
        if self.instrucciones_else != None:
            for instruccion_else in self.instrucciones_else:
                NodoElse.agregarHijoNodo(instruccion_else.getNodo())
        NodoPadre.agregarHijoNodo(NodoCondicion)
        NodoPadre.agregarHijoNodo(NodoIf)
        if self.instrucciones_else != None:
            NodoPadre.agregarHijoNodo(NodoElse)
        if self.instrucciones_elseif!= None:
            NodoPadre.agregarHijoNodo(self.instrucciones_elseif.getNodo())
        NodoPadre.agregarHijo("end")
        NodoPadre.agregarHijo(";")
        return NodoPadre
        