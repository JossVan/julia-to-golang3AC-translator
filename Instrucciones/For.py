from Instrucciones.Return import Return
from Expresiones.Arreglos import Arreglos
from Abstractas.NodoArbol import NodoArbol
from Expresiones.Rango import Rango
from Instrucciones.Continue import Continue
from TablaSimbolos.Errores import Errores
from Abstractas.Objeto import TipoObjeto
from Objetos.Primitivos import Primitivo
from Expresiones.Constante import Constante
from TablaSimbolos.Tipos import Tipo_Acceso
from Instrucciones.Asignacion import Asignacion
from Instrucciones.Break import Break
from TablaSimbolos.TablaSimbolos import TablaSimbolos
from Abstractas.NodoAST import NodoAST

class For(NodoAST):

    def __init__(self, id, rango, instrucciones, fila, columna):
        self.id = id
        self.rango = rango
        self.instrucciones = instrucciones
        self.fila = fila 
        self.columna = columna
    
    def ejecutar(self, tree, table):
        nuevaTabla= TablaSimbolos("For",table)
        self.id.ejecutar(tree,nuevaTabla)
        id = self.id.id
        rango = self.rango.ejecutar(tree,nuevaTabla)
        if isinstance(rango,Rango):
            rango1 = rango.izquierdo
            rango2 = rango.derecho
            if isinstance(rango1,int) and isinstance(rango2,int):
                for i in range(rango1,rango2):
                    #if isinstance(rango1,int):                 
                    nuevaTabla.actualizarValor(id,i)
                    nuevaConstante = Constante(Primitivo(TipoObjeto.ENTERO, i), self.fila, self.columna)
                    '''elif isinstance(rango1,float):
                        nuevaConstante = Constante(Primitivo(TipoObjeto.DECIMAL, i), self.fila, self.columna)
                    else:
                        return Errores((str(rango1)+","+str(rango2)),"Semántico","Rango no aceptado", self.fila,self.columna)'''
                    nuevaAsignacion = Asignacion(Tipo_Acceso.NONE,id,nuevaConstante,None, self.fila,self.columna)
                    nuevaAsignacion.ejecutar(tree,nuevaTabla)
                    for instruccion in self.instrucciones:
                        resp= instruccion.ejecutar(tree,nuevaTabla)
                        if isinstance(resp,Break):
                            return None
                        elif isinstance(resp,Continue):
                            return None
                        elif isinstance(resp, Return):
                            return resp
            elif isinstance(rango1,float) and isinstance(rango2,float):
                total = int(rango2-rango1)+1
                if total >0:
                    for i in range(0,total):
                        nuevaTabla.actualizarValor(id,i)
                        variable = rango1
                        nuevaConstante = Constante(Primitivo(TipoObjeto.DECIMAL, variable), self.fila, self.columna)
                        rango1 = rango1+1
                        nuevaAsignacion = Asignacion(Tipo_Acceso.NONE,id,nuevaConstante,None, self.fila,self.columna)
                        nuevaAsignacion.ejecutar(tree,nuevaTabla)
                        for instruccion in self.instrucciones:
                            resp= instruccion.ejecutar(tree,nuevaTabla)
                            if isinstance(resp,Break):
                                return None
                            elif isinstance(resp,Continue):
                                return None
                            elif isinstance(resp, Return):
                                return resp
                            elif isinstance(resp, Errores):
                                return resp
        else:
            if isinstance(rango,int) or isinstance(rango,float):
                if isinstance(rango, int):
                    nuevaConstante = Constante(Primitivo(TipoObjeto.ENTERO, rango), self.fila, self.columna)
                else:
                    nuevaConstante = Constante(Primitivo(TipoObjeto.DECIMAL, rango), self.fila, self.columna)

                nuevaAsignacion = Asignacion(Tipo_Acceso.NONE,id,nuevaConstante,None,self.fila,self.columna)
                nuevaAsignacion.ejecutar(tree,nuevaTabla)
                if self.instrucciones != None:
                    for instruccion in self.instrucciones:
                        resp=instruccion.ejecutar(tree,nuevaTabla)
                        if isinstance(resp,Break):
                            return None
                        elif isinstance(resp,Continue):
                            return None
                        elif isinstance(resp, Return):
                            return resp
                        elif isinstance(resp,Errores):
                            return resp
            else:
                try:
                    for i in rango:
                        if isinstance(i, str):
                            nuevaConstante = Constante(Primitivo(TipoObjeto.CADENA, i), self.fila, self.columna)
                            nuevaAsignacion = Asignacion(Tipo_Acceso.NONE,id,nuevaConstante,None,self.fila,self.columna)
                            nuevaAsignacion.ejecutar(tree,nuevaTabla)
                        elif isinstance(i,int): 
                            nuevaConstante = Constante(Primitivo(TipoObjeto.ENTERO, i), self.fila, self.columna)
                            nuevaAsignacion = Asignacion(Tipo_Acceso.NONE,id,nuevaConstante,None,self.fila,self.columna)
                            nuevaAsignacion.ejecutar(tree,nuevaTabla)
                        elif isinstance(i, NodoAST):
                            #val = i.ejecutar(tree,nuevaTabla)
                            nuevaTabla.actualizarValor(id,i)
                        elif isinstance(i, list):
                            nuevaTabla.actualizarValor(id,i)
                        if self.instrucciones != None:
                            for instruccion in self.instrucciones:
                                resp=instruccion.ejecutar(tree,nuevaTabla)
                                if isinstance(resp,Break):
                                    return None
                                elif isinstance(resp, Continue):
                                    return None
                                elif isinstance(resp, Return):
                                    return resp
                                elif isinstance(resp, Errores):
                                    return resp
                except:
                    err = Errores("For","Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                    tree.insertError(err)
                    return err

    def traducir(self, tree, table, keep):
        nuevaTabla= TablaSimbolos("For",table)
        self.id.traducir(tree,nuevaTabla,keep)
        id = self.id.id
        rango = self.rango.traducir(tree,nuevaTabla,keep)
        if isinstance(rango,Rango):
            rango1 = rango.izquierdo
            rango2 = rango.derecho
            if isinstance(rango1,int) and isinstance(rango2,int):  
                nuevaTabla.actualizarTipo(id.lower(),"Int64")
                indice = keep.getNuevoTemporal()
                codigo = "//**********CICLO FOR**********\n"
                codigo +=keep.addIgual(indice,rango1)
                ei = keep.getNuevaEtiqueta()
                ev = keep.getNuevaEtiqueta()
                ef = keep.getNuevaEtiqueta()
                codigo += ei+":\n"
                codigo += "if "+indice+" <= "+str(rango2)+"{goto "+ev+";}\ngoto "+ef+";\n"
                codigo += ev+":\n"
                #EN ESTA SECCIÓN SE ACTUALIZA LA VARIABLE DEL FOR 
                id = id.lower()
                resultado = nuevaTabla.BuscarIdentificador(id)
                if resultado == None:
                    print("F")
                    tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                    return
                apuntador = resultado.getApuntador()
                #tipo = resultado.getTipo()
                codigo += keep.addIgual(keep.getValStack(apuntador),indice)
                keep.addCodigo(codigo)
                for instruccion in self.instrucciones:
                    resp= instruccion.traducir(tree,nuevaTabla,keep)
                    if isinstance(resp,Break):
                        return None
                    elif isinstance(resp,Continue):
                        return None
                    elif isinstance(resp, Return):
                        return resp
                codigo = keep.addOperacion(indice,indice,"+","1")
                codigo += "goto "+ei+";\n"
                codigo += ef+":\n"
                keep.addCodigo(codigo)
            elif isinstance(rango1,float) and isinstance(rango2,float):
                total = int(rango2-rango1)+1
                if total >0:
                    nuevaTabla.actualizarTipo(id.lower(),"Int64")
                    inferior = keep.getNuevoTemporal()
                    superior = keep.getNuevoTemporal()
                    codigo = "//**********CICLO FOR**********\n"
                    codigo +=keep.addIgual(inferior,"0")
                    codigo += keep.addIgual(superior,total)
                    ei = keep.getNuevaEtiqueta()
                    ev = keep.getNuevaEtiqueta()
                    ef = keep.getNuevaEtiqueta()
                    codigo += ei+":\n"
                    codigo += "if "+inferior+" <= "+superior+"{goto "+ev+";}\ngoto "+ef+";\n"
                    codigo += ev+":\n"
                    #EN ESTA SECCIÓN SE ACTUALIZA LA VARIABLE DEL FOR 
                    id = id.lower()
                    resultado = nuevaTabla.BuscarIdentificador(id)
                    if resultado == None:
                        print("F")
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador = resultado.getApuntador()
                    #tipo = resultado.getTipo()
                    codigo += keep.addIgual(keep.getValStack(apuntador),inferior)
                    keep.addCodigo(codigo)
                    for instruccion in self.instrucciones:
                        resp= instruccion.traducir(tree,nuevaTabla,keep)
                        if isinstance(resp,Break):
                            return None
                        elif isinstance(resp,Continue):
                            return None
                        elif isinstance(resp, Return):
                            return resp
                    codigo = keep.addOperacion(inferior,inferior,"+","1")
                    codigo += "goto "+ei+";\n"
                    codigo += ef+":\n"
                    keep.addCodigo(codigo)
        else:
            if isinstance(rango,dict):
                if "izquierdo" in rango and "derecho" in rango:
                    izquierdo = rango["izquierdo"]
                    derecho = rango["derecho"]
                    if isinstance(izquierdo,dict):
                        if "temp" in izquierdo:
                            temp = izquierdo["temp"]
                            tipo = izquierdo["tipo"]
                        elif "apuntador" in izquierdo:
                            apuntador = izquierdo["apuntador"]
                            tipo = izquierdo["tipo"]
                            temp = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp,keep.getValStack(apuntador))
                            keep.addCodigo(codigo)
                        else:
                            print ("ERROR")
                    else:
                        temp = keep.getNuevoTemporal()
                        codigo  = keep.addIgual(temp,izquierdo)
                        keep.addCodigo(codigo)
                    if isinstance(derecho,dict):
                        if "temp" in derecho:
                            temp2 = derecho["temp"]
                            tipo2 = derecho["tipo"]
                        elif "apuntador" in derecho:
                            apuntador2 = derecho["apuntador"]
                            tipo2 = derecho["tipo"]
                            temp2 = keep.getNuevoTemporal()
                            codigo = keep.addIgual(temp2,keep.getValStack(apuntador2))
                            keep.addCodigo(codigo)
                        else:
                            print ("ERROR")
                    else:
                        temp2 = keep.getNuevoTemporal()
                        codigo  = keep.addIgual(temp,derecho)
                        keep.addCodigo(codigo)
                    # EMPIEZA LA CODIFICACIÓN EN 3D
                    nuevaTabla.actualizarTipo(id.lower(),"Int64")
                    inferior = keep.getNuevoTemporal()
                    superior = keep.getNuevoTemporal()
                    codigo = "//**********CICLO FOR**********\n"
                    codigo +=keep.addIgual(inferior,temp)
                    codigo += keep.addIgual(superior,temp2)
                    ei = keep.getNuevaEtiqueta()
                    ev = keep.getNuevaEtiqueta()
                    ef = keep.getNuevaEtiqueta()
                    codigo += ei+":\n"
                    codigo += "if "+inferior+" <= "+superior+"{goto "+ev+";}\ngoto "+ef+";\n"
                    codigo += ev+":\n"
                    #EN ESTA SECCIÓN SE ACTUALIZA LA VARIABLE DEL FOR 
                    id = id.lower()
                    resultado = nuevaTabla.BuscarIdentificador(id)
                    if resultado == None:
                        print("F")
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador = resultado.getApuntador()
                    #tipo = resultado.getTipo()
                    codigo += keep.addIgual(keep.getValStack(apuntador),inferior)
                    keep.addCodigo(codigo)
                    for instruccion in self.instrucciones:
                        resp= instruccion.traducir(tree,nuevaTabla,keep)
                        if isinstance(resp,Break):
                            return None
                        elif isinstance(resp,Continue):
                            return None
                        elif isinstance(resp, Return):
                            return resp
                    codigo = keep.addOperacion(inferior,inferior,"+","1")
                    codigo += "goto "+ei+";\n"
                    codigo += ef+":\n"
                    keep.addCodigo(codigo)
                elif "apuntador" in rango:
                    nuevaTabla.actualizarTipo(id.lower(),"String")

                    puntero = rango["apuntador"]
                    ei = keep.getNuevaEtiqueta()
                    ev = keep.getNuevaEtiqueta()
                    ef = keep.getNuevaEtiqueta()
                    temp = keep.getNuevoTemporal()
                    temp2 = keep.getNuevoTemporal()
                    temp3 = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(temp,"SP","+",puntero)
                    codigo += keep.addIgual(temp2, keep.getValStack(temp))
                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                    codigo += "//*****INICIO DEL FOR CON CADENA*****\n"
                    codigo += ei+":\n"
                    codigo += "if "+ temp3 +"!= -1"+"{goto "+ev+";}\ngoto "+ef+";\n"
                    codigo += ev+":\n"
                    #BUSCO LA VARIABLE INDICE EN LA TABLA DE SIMBOLOS
                    id = id.lower()
                    resultado = nuevaTabla.BuscarIdentificador(id)
                    if resultado == None:
                        print("F")
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador = resultado.getApuntador()
                    temp4 = keep.getNuevoTemporal()
                    codigo += "//ASIGNO EL VALOR DEL HEAP A LA VARIABLE INDICE\n"
                    codigo += keep.addOperacion(temp4,"SP","+",apuntador)
                    temp5 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp5,"HP")
                    codigo += keep.addIgual(keep.getValHeap("HP"),temp3)
                    codigo += keep.addOperacion("HP","HP","+","1")
                    codigo += keep.addIgual(keep.getValHeap("HP"),"-1")
                    codigo += keep.addOperacion("HP","HP","+","1")
                    codigo += keep.addIgual(keep.getValStack(temp4),temp5)
                    codigo += "//*********************************************\n"
                    keep.addCodigo(codigo)
                    if self.instrucciones != None:
                        for instruccion in self.instrucciones:
                            resp=instruccion.traducir(tree,nuevaTabla,keep)
                            if isinstance(resp,Break):
                                return None
                            elif isinstance(resp, Continue):
                                return None
                            elif isinstance(resp, Return):
                                return resp
                            elif isinstance(resp, Errores):
                                return resp
                    codigo = keep.addOperacion(temp2,temp2,"+","1")
                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                    codigo += "goto "+ei+";\n"
                    codigo += ef+":\n"
                    keep.addCodigo(codigo)
                    keep.liberarTemporales(temp)
                    keep.liberarTemporales(temp2)
                    keep.liberarTemporales(temp3)
                    keep.liberarTemporales(temp4)
                    keep.liberarTemporales(temp5)
            else:
                if isinstance(rango, str):
                    nuevaTabla.actualizarTipo(id.lower(),"String")
                    puntero = keep.getStack()-1
                    ei = keep.getNuevaEtiqueta()
                    ev = keep.getNuevaEtiqueta()
                    ef = keep.getNuevaEtiqueta()
                    temp = keep.getNuevoTemporal()
                    temp2 = keep.getNuevoTemporal()
                    temp3 = keep.getNuevoTemporal()
                    codigo = keep.addOperacion(temp,"SP","+",puntero)
                    codigo += keep.addIgual(temp2, keep.getValStack(temp))
                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                    codigo += "//*****INICIO DEL FOR CON CADENA*****\n"
                    codigo += ei+":\n"
                    codigo += "if "+ temp3 +"!= -1"+"{goto "+ev+";}\ngoto "+ef+";\n"
                    codigo += ev+":\n"
                    #BUSCO LA VARIABLE INDICE EN LA TABLA DE SIMBOLOS
                    id = id.lower()
                    resultado = nuevaTabla.BuscarIdentificador(id)
                    if resultado == None:
                        print("F")
                        tree.insertError(Errores(id,"Semántico","Variable no definida", self.fila,self.columna))
                        return
                    apuntador = resultado.getApuntador()
                    temp4 = keep.getNuevoTemporal()
                    codigo += "//ASIGNO EL VALOR DEL HEAP A LA VARIABLE INDICE\n"
                    codigo += keep.addOperacion(temp4,"SP","+",apuntador)
                    temp5 = keep.getNuevoTemporal()
                    codigo += keep.addIgual(temp5,"HP")
                    codigo += keep.addIgual(keep.getValHeap("HP"),temp3)
                    codigo += keep.addOperacion("HP","HP","+","1")
                    codigo += keep.addIgual(keep.getValHeap("HP"),"-1")
                    codigo += keep.addOperacion("HP","HP","+","1")
                    codigo += keep.addIgual(keep.getValStack(temp4),temp5)
                    codigo += "//*********************************************\n"
                    keep.addCodigo(codigo)
                    if self.instrucciones != None:
                        for instruccion in self.instrucciones:
                            resp=instruccion.traducir(tree,nuevaTabla,keep)
                            if isinstance(resp,Break):
                                return None
                            elif isinstance(resp, Continue):
                                return None
                            elif isinstance(resp, Return):
                                return resp
                            elif isinstance(resp, Errores):
                                return resp
                    codigo = keep.addOperacion(temp2,temp2,"+","1")
                    codigo += keep.addIgual(temp3,keep.getValHeap(temp2))
                    codigo += "goto "+ei+";\n"
                    codigo += ef+":\n"
                    keep.addCodigo(codigo)    
                    keep.liberarTemporales(temp)
                    keep.liberarTemporales(temp2)
                    keep.liberarTemporales(temp3)
                    keep.liberarTemporales(temp4)
                    keep.liberarTemporales(temp5)  
                '''except:
                    err = Errores("For","Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                    tree.insertError(err)
                    return err   ''' 
    
    def getNodo(self):
        
        NodoNuevo = NodoArbol("For")
        NodoNuevo.agregarHijoNodo(self.id.getNodo())
        NodoNuevo.agregarHijoNodo(self.rango.getNodo())
        NodoInst = NodoArbol("Instrucciones")
        for instruccion in self.instrucciones:
            NodoInst.agregarHijoNodo(instruccion.getNodo())
        NodoNuevo.agregarHijoNodo(NodoInst)
        NodoNuevo.agregarHijo("end")
        NodoNuevo.agregarHijo(";")
        return NodoNuevo

        