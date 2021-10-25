from TablaSimbolos.Errores import Errores
from TablaSimbolos.Tipos import Tipo_FuncionAritmetica
from Abstractas.NodoArbol import NodoArbol
from Abstractas.NodoAST import NodoAST
import math

class Funciones_matematicas(NodoAST):

    def __init__(self, funcion, valor1, valor2, fila, columna):
        self.funcion = funcion
        self.valor1 = valor1
        self.valor2 = valor2
        self.fila = fila 
        self.columna = columna
    
    def ejecutar(self, tree, table):
        
        if self.valor2 == None and self.valor1 != None:
            valor1 = self.valor1.ejecutar(tree,table)

            if self.funcion == Tipo_FuncionAritmetica.lowercase:
                if isinstance(valor1,str):
                    return valor1.lower()
                err = Errores(valor1,"Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                tree.insertError(err)
                return err
            elif self.funcion == Tipo_FuncionAritmetica.uppercase:
                if isinstance(valor1,str):
                    return valor1.upper()
                err = Errores(valor1,"Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                tree.insertError(err)
                return err
            elif self.funcion == Tipo_FuncionAritmetica.log10:
                try:
                    return round(math.log(valor1,10))
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.seno:
                try:
                    return math.sin(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.coseno:
                try:
                    return math.cos(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.tangente:
                try:
                    return math.tan(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.sqrt:
                try:
                    return math.sqrt(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
        elif self.valor2!=None and self.valor1 !=None:
            valor1 = self.valor1.ejecutar(tree,table)
            valor2 = self.valor2.ejecutar(tree,table)
            if self.funcion == Tipo_FuncionAritmetica.log:
                return math.log(valor2,valor1)
   
    def traducir(self, tree, table, keep):
        if self.valor2 == None and self.valor1 != None:
            valor1 = self.valor1.traducir(tree,table,keep)
            apuntador = None
            tipo = None
            valor = None
            if isinstance(valor1,dict):
                if "apuntador" in valor1:
                    apuntador = valor1["apuntador"]
                    tipo = valor1["tipo"]
                    valor = valor1["valor"]
                else:
                    print("ERROR")
            elif isinstance(valor1,str):
                tipo = "String"
                valor = valor1
                apuntador = keep.getStack()-1
            else:
                print("TIPO NO PERMITIDO")
            if self.funcion == Tipo_FuncionAritmetica.lowercase:
                if tipo == "String":
                    self.lower(keep,apuntador)
                    return valor1.lower()
                err = Errores(valor1,"Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                tree.insertError(err)
                return err
            elif self.funcion == Tipo_FuncionAritmetica.uppercase:
                if tipo == "String":
                    self.upper(keep,apuntador)
                    return valor1.upper()
                err = Errores(valor1,"Semántico","Valor no permitido, debe ser una cadena", self.fila,self.columna)
                tree.insertError(err)
                return err
            elif self.funcion == Tipo_FuncionAritmetica.log10:
                try:
                    return round(math.log(valor1,10))
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.seno:
                try:
                    return math.sin(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.coseno:
                try:
                    return math.cos(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.tangente:
                try:
                    return math.tan(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
            elif self.funcion == Tipo_FuncionAritmetica.sqrt:
                try:
                    return math.sqrt(valor1)
                except:
                    err = Errores(valor1,"Semántico","Valor no permitido, debe ser un número", self.fila,self.columna)
                    tree.insertError(err)
                    return err
        elif self.valor2!=None and self.valor1 !=None:
            valor1 = self.valor1.ejecutar(tree,table)
            valor2 = self.valor2.ejecutar(tree,table)
            if self.funcion == Tipo_FuncionAritmetica.log:
                return math.log(valor2,valor1)
    
    def upper(self,keep,apuntador):

        #saco el primer valor del heap
        temp = keep.getNuevoTemporal()
        temp2 = keep.getNuevoTemporal()
        codigo = "//*****FUNCIÓN UPPERCASE*****\n"
        codigo += keep.addIgual(temp,keep.getValStack(apuntador))
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        eentrada = keep.getNuevaEtiqueta()
        e1 = keep.getNuevaEtiqueta()
        e2 = keep.getNuevaEtiqueta()
        temp3 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp3,"HP")
        codigo += eentrada+":\n"
        codigo += "if "+temp2+" >= 97"+" {goto "+e1+";}\ngoto "+e2+";\n"
        codigo += e1+":\n"
        e3 = keep.getNuevaEtiqueta()
        es = keep.getNuevaEtiqueta()
        codigo += "if "+temp2+"<= 122 {goto "+ e3 +";}\ngoto "+e2+";\n"
        codigo += e3+":\n"
        codigo += keep.addOperacion(temp2,temp2,"-","32")
        codigo += keep.addIgual(keep.getValHeap(temp),temp2)
        #codigo += keep.addOperacion("HP","HP","+","1")
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        codigo += "if "+temp2+" != -1 {goto "+eentrada+";}\ngoto "+es+";\n"
        codigo += e2+":\n"
        codigo += keep.addIgual(keep.getValHeap(temp),temp2)
        #codigo += keep.addOperacion("HP","HP","+","1")
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        codigo += "if "+temp2+" != -1 {goto "+eentrada+";}\ngoto "+es+";\n"
        codigo += es+":\n"
        codigo += keep.addOperacion("SP","SP","+","1")
        codigo += keep.addIgual(keep.getValStack("SP"),temp3)
        keep.incrementarStack()
        keep.addCodigo(codigo)

    def lower(self,keep,apuntador):

        #saco el primer valor del heap
        temp = keep.getNuevoTemporal()
        temp2 = keep.getNuevoTemporal()
        codigo = "//*****FUNCIÓN UPPERCASE*****\n"
        codigo += keep.addIgual(temp,keep.getValStack(apuntador))
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        eentrada = keep.getNuevaEtiqueta()
        e1 = keep.getNuevaEtiqueta()
        e2 = keep.getNuevaEtiqueta()
        temp3 = keep.getNuevoTemporal()
        codigo += keep.addIgual(temp3,"HP")
        codigo += eentrada+":\n"
        codigo += "if "+temp2+" >= 65"+" {goto "+e1+";}\ngoto "+e2+";\n"
        codigo += e1+":\n"
        e3 = keep.getNuevaEtiqueta()
        es = keep.getNuevaEtiqueta()
        codigo += "if "+temp2+"<= 90 {goto "+ e3 +";}\ngoto "+e2+";\n"
        codigo += e3+":\n"
        codigo += keep.addOperacion(temp2,temp2,"+","32")
        codigo += keep.addIgual(keep.getValHeap(temp),temp2)
        #codigo += keep.addOperacion("HP","HP","+","1")
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        codigo += "if "+temp2+" != -1 {goto "+eentrada+";}\ngoto "+es+";\n"
        codigo += e2+":\n"
        codigo += keep.addIgual(keep.getValHeap(temp),temp2)
        #codigo += keep.addOperacion("HP","HP","+","1")
        codigo += keep.addOperacion(temp,temp,"+","1")
        codigo += keep.addIgual(temp2,keep.getValHeap(temp))
        codigo += "if "+temp2+" != -1 {goto "+eentrada+";}\ngoto "+es+";\n"
        codigo += es+":\n"
        codigo += keep.addOperacion("SP","SP","+","1")
        codigo += keep.addIgual(keep.getValStack("SP"),temp3)
        keep.incrementarStack()
        keep.addCodigo(codigo)
        
    
    def getNodo(self):
        NuevoNodo = NodoArbol("Funciones")
        if self.funcion == Tipo_FuncionAritmetica.lowercase:
            NuevoNodo.agregarHijo("Lowercase")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.uppercase:
            NuevoNodo.agregarHijo("Uppercase")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.seno:
            NuevoNodo.agregarHijo("Sin")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.coseno:
            NuevoNodo.agregarHijo("Cos")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.tangente:
            NuevoNodo.agregarHijo("Tan")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.sqrt:
            NuevoNodo.agregarHijo("Sqrt")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.log10:
            NuevoNodo.agregarHijo("Log10")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(")")
        elif self.funcion == Tipo_FuncionAritmetica.log:
            NuevoNodo.agregarHijo("Log")
            NuevoNodo.agregarHijo("(")
            NuevoNodo.agregarHijoNodo(self.valor1.getNodo())
            NuevoNodo.agregarHijo(",")
            NuevoNodo.agregarHijoNodo(self.valor2.getNodo())
            NuevoNodo.agregarHijo(")")
        
        return NuevoNodo