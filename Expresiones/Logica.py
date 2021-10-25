from Expresiones.Relacional import Relacional
from TablaSimbolos.Errores import Errores
from Abstractas.NodoArbol import NodoArbol
from TablaSimbolos.Tipos import Tipo_Logico, Tipo_Relacional
from Abstractas.NodoAST import NodoAST

class Logica(NodoAST):

    
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
            if isinstance(self.operador1,NodoAST):
                resultado1= self.operador1.traducir(tree,table,keep)
            else:
                resultado1 = self.operador1
            if isinstance(resultado1,dict):
                result1 = resultado1["bool"] 
                etiquetas1 = resultado1["etiquetas"]
                if self.tipooperacion == Tipo_Logico.AND:
                    keep.addCodigo(etiquetas1[0]+":\n")
                    keep.etiquetaFalsa = etiquetas1[1]
                    keep.etiquetaVerdadera =""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        result2 = resultado2["bool"]
                        etiquetas2 = resultado2["etiquetas"]
                        keep.addCodigo(etiquetas2[0]+":\n")
                        keep.etiquetaFalsa = etiquetas2[1]
                        keep.etiquetaVerdadera = ""
                        return result1 and result2
                    elif isinstance(resultado2,bool):
                        
                        return result1 and resultado2
                        
                elif self.tipooperacion == Tipo_Logico.OR:
                    keep.addCodigo(etiquetas1[1]+":\n")
                    keep.etiquetaVerdadera = etiquetas1[0]
                    keep.etiquetaFalsa = ""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        result2 = resultado2["bool"]
                        etiquetas2 = resultado2["etiquetas"]
                        keep.addCodigo(etiquetas2[1]+":\n")
                        keep.etiquetaVerdadera = etiquetas2[0]
                        keep.etiquetaFalsa = ""
                        return result1 or result2
                    elif isinstance(resultado2,bool):
                        return result1 or resultado2

            elif isinstance(resultado1,bool):
                if self.tipooperacion == Tipo_Logico.AND:
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        result2 = resultado2["bool"]
                        etiquetas2 = resultado2["etiquetas"]
                        keep.addCodigo(etiquetas2[0]+":\n")
                        keep.etiquetaFalsa = etiquetas2[1]
                        keep.etiquetaVerdadera = ""
                        return resultado1 and result2
                    elif isinstance(resultado2,bool):
                        if keep.etiquetaVerdadera != "":
                            keep.addCodigo(keep.etiquetaVerdadera+":\n")
                            keep.etiquetaVerdadera =""
                        eSigue = keep.getNuevaEtiqueta()
                        ePara = keep.getNuevaEtiqueta()
                        if resultado1:
                            keep.addCodigo("goto "+eSigue+";\n")
                            keep.addCodigo(eSigue+":\n")
                        else:
                            keep.addCodigo("goto "+ePara+";\n")
                            keep.etiquetaFalsa = ePara
                            return resultado1 and resultado2

                        eSigue2 = keep.getNuevaEtiqueta()
                        if resultado2:
                            keep.addCodigo("goto "+eSigue2+";\n")
                            keep.addCodigo(eSigue2+":\n")
                        else:
                            keep.addCodigo("goto "+ePara+";\n")
                            keep.etiquetaFalsa = ePara
                        return resultado1 and resultado2
                elif self.tipooperacion == Tipo_Logico.OR:
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        result2 = resultado2["bool"]
                        etiquetas2 = resultado2["etiquetas"]
                        #keep.addCodigo(etiquetas2[1]+":\n")
                        keep.etiquetaVerdadera = etiquetas2[0]
                        keep.etiquetaFalsa = etiquetas2[1]
                        return resultado1 or result2
                    elif isinstance(resultado2,bool):
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
                        codigo = "if 1 == "+str(int(resultado1))+"{ goto "+ef+";}\ngoto "+ev+";\n"
                        codigo += ev+":\n"
                        nueva = keep.getNuevaEtiqueta()
                        codigo += "if 1 =="+str(int(resultado2))+"{ goto "+ef+";}\ngoto "+nueva+";\n"
                        codigo += nueva+":\n"
                        keep.etiquetaVerdadera = ef
                        keep.addCodigo(codigo)
                        return resultado1 or resultado2

        if self.operador2== None and self.operador1 !=None:
            if isinstance(self.operador1,NodoAST):
                resultado1= self.operador1.traducir(tree,table,keep)
            else:
                resultado1 = self.operador1
            if isinstance(resultado1,dict):
                result1 = resultado1["bool"] 
                etiquetas1 = resultado1["etiquetas"]
                if self.tipooperacion == Tipo_Logico.DIFERENTE:
                    keep.addCodigo(etiquetas1[1]+":\n")
                    keep.etiquetaFalsa = etiquetas1[0]
                    keep.etiquetaVerdadera =""
                    return not result1
                else:
                    print(self.tipooperacion)
            elif isinstance(resultado1,bool):
                if self.tipooperacion == Tipo_Logico.DIFERENTE:
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
                    codigo = "if 1 == "+str(int(resultado1))+"{ goto "+ev+";}\ngoto "+ef+";\n"
                    codigo += ev+":\n"
                    return not resultado1
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