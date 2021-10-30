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
                etiquetas1 = resultado1["etiquetas"]
                if self.tipooperacion == Tipo_Logico.AND:
                    keep.addCodigo(etiquetas1[0]+":\n")
                    keep.etiquetaFalsa = etiquetas1[1]
                    keep.etiquetaVerdadera =""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        etiquetas2 = resultado2["etiquetas"]
                        return {"etiquetas":etiquetas2}
                    elif(resultado2,bool):
                        e1 = keep.getNuevaEtiqueta()
                        e2 = etiquetas1[1]
                        if resultado2:
                            keep.addCodigo("goto "+e1+";\n")
                            return {"etiquetas":[e1,e2]}
                        else:
                            keep.addCodigo("goto "+e2+";\n")
                            return {"etiquetas":[e1,e2]}                     
                elif self.tipooperacion == Tipo_Logico.OR:
                    keep.addCodigo(etiquetas1[1]+":\n")
                    keep.etiquetaVerdadera = etiquetas1[0]
                    keep.etiquetaFalsa = ""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        etiquetas2 = resultado2["etiquetas"]
                        return {"etiquetas":etiquetas2}
                    elif(resultado2,bool):
                        e1 = etiquetas1[1]
                        e2 = keep.getNuevaEtiqueta()
                        if resultado2:
                            keep.addCodigo("goto "+e1+";\n")
                            return {"etiquetas":[e1,e2]}
                        else:
                            keep.addCodigo("goto "+e2+";\n")
                            return {"etiquetas":[e1,e2]}


            elif isinstance(resultado1,bool):
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
                if self.tipooperacion == Tipo_Logico.AND:
                    codigo = "if 1 == "+str(int(resultado1))+"{goto "+ev+";}\ngoto "+ef+";\n"
                    keep.addCodigo(codigo)
                    keep.addCodigo(ev+":\n")
                    keep.etiquetaFalsa = ef
                    keep.etiquetaVerdadera = ""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        etiquetas2 = resultado2["etiquetas"]
                        return {"etiquetas":etiquetas2}
                    elif(resultado2,bool):
                        e11 = keep.getNuevaEtiqueta()
                        codigo = "if 1 == "+str(int(resultado2))+"{goto "+e11+";}\ngoto "+ef+";\n"
                        keep.addCodigo(codigo)
                        return {"etiquetas":[e11,ef]}
                    
                elif self.tipooperacion == Tipo_Logico.OR:
                    e1 = keep.getNuevaEtiqueta()
                    e2 = keep.getNuevaEtiqueta()
                    codigo = "if 1 == "+str(int(resultado1))+"{goto "+e1+";}\ngoto "+e2+";\n"
                    codigo += e2+":\n"
                    keep.addCodigo(codigo)
                    keep.etiquetaVerdadera = e1
                    #keep.etiquetaFalsa = ""
                    resultado2 = self.operador2.traducir(tree,table,keep)
                    if isinstance(resultado2,dict):
                        etiquetas2 = resultado2["etiquetas"]
                        return {"etiquetas":etiquetas2}
                    elif(resultado2,bool):
                        if keep.etiquetaFalsa == "":
                            e11 = keep.getNuevaEtiqueta()
                        else:
                            e11 = keep.etiquetaFalsa
                            keep.etiquetaFalsa =""
                        codigo = "if 1 == "+str(int(resultado2))+"{goto "+e1+";}\ngoto "+e11+";\n"
                        keep.addCodigo(codigo)
                        return {"etiquetas":[e1,e11]}
        if self.operador2== None and self.operador1 !=None:
            if isinstance(self.operador1,NodoAST):
                resultado1= self.operador1.traducir(tree,table,keep)
            else:
                resultado1 = self.operador1
            if isinstance(resultado1,dict):
                etiquetas1 = resultado1["etiquetas"]
                if self.tipooperacion == Tipo_Logico.DIFERENTE:
                    return {"etiquetas",[etiquetas1[1],etiquetas1[0]]}
                else:
                    print(self.tipooperacion)
            elif isinstance(resultado1,bool):
                if keep.etiquetaVerdadera!= "":
                    e1 = keep.etiquetaVerdadera
                else:
                    e1 = keep.getNuevaEtiqueta()
                if keep.etiquetaFalsa!= "":
                    e2 = keep.etiquetaFalsa
                else:
                    e2 = keep.getNuevaEtiqueta()
                codigo = "if 1 == "+str(int(resultado1))+"{goto "+e2+";}\ngoto "+e1+";\n"
                keep.addCodigo(codigo)
                return {"etiquetas":[e1,e2]}
            
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