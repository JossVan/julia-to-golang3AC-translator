from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from Abstractas.NodoAST import NodoAST
from Instrucciones.Break import Break
class While(NodoAST):

    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion= condicion
        self.instrucciones = instrucciones
        self.fila = fila 
        self.columna = columna

    def ejecutar(self, tree, table):
        
        while True:
            nuevaTabla = TablaSimbolos("While",table)
            condicion = self.condicion.ejecutar(tree,nuevaTabla)
            if (condicion):
                for instruccion in self.instrucciones:
                    resp = instruccion.ejecutar(tree,nuevaTabla)
                    if isinstance(resp, Break):
                        return None
                    if isinstance(resp, Continue):
                        break
                    if isinstance(resp, Return):
                        return resp
            else:
                break
    def traducir(self, tree, table, keep):
        nuevaTabla = TablaSimbolos("While",table)
        ev = keep.getNuevaEtiqueta()
        #ef = keep.getNuevaEtiqueta()
        keep.etiquetaContinue = ev
        keep.addCodigo("//********** SENTENCIA WHILE **********\n")
        keep.addCodigo(ev+":\n")
        condicion = self.condicion.traducir(tree,nuevaTabla,keep)
        keep.etiquetaBreak = condicion["etiquetas"][1]
        if isinstance(condicion,dict):
            keep.addCodigo(condicion["etiquetas"][0]+":\n")
            for instruccion in self.instrucciones:
                etiqueta = keep.etiquetaContinue
                etiqueta2 = keep.etiquetaBreak
                resp = instruccion.traducir(tree,nuevaTabla,keep)
                if isinstance(resp,dict):
                    if "break" in resp:
                        keep.addCodigo("//*******BREAK*******\n")
                        keep.addCodigo(resp["cad"])
                    elif "continue":
                        keep.addCodigo("//*******CONTINUE*******\n")
                        keep.addCodigo(resp["cad"])
                    if isinstance(resp, Return):
                        return resp
                keep.etiquetaContinue = etiqueta
                keep.etiquetaBreak = etiqueta2
            keep.addCodigo("goto "+ev+";\n")
            keep.addCodigo(condicion["etiquetas"][1]+":\n")
        keep.etiquetaContinue = ""
        keep.etiquetaBreak = ""
    def getNodo(self):
        NodoNuevo = NodoArbol("While")
        NodoNuevo.agregarHijoNodo(self.condicion.getNodo())
        inst = NodoArbol("Instrucciones")
        for instruccion in self.instrucciones:
            inst.agregarHijoNodo(instruccion.getNodo())
        NodoNuevo.agregarHijoNodo(inst)
        NodoNuevo.agregarHijo("end")
        NodoNuevo.agregarHijo(";")
        return NodoNuevo