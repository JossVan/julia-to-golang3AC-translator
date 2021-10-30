class KeepData:

    header = ""
    codigo = ""
    contador = 0
    PH = 0
    PS = 0
    punteroActual = 0
    contadorEtiqueta = 0
    listaTemporalesEnUso = []
    listaTemporalesLibres = []
    etiquetas = []


    codigo3d = None

    def __init__(self) -> None:
        
        self.contador = 0
        self.contadorEtiqueta = 0
        self.header = ""
        self.codigo = ""
        self.header = ""
        self.codigo = ""
        self.contador = 0
        self.PH = 0
        self.PS = 0
        self.punteroActual = 0
        self.contadorEtiqueta = 0
        self.listaTemporalesEnUso = []
        self.listaTemporalesLibres = []
        self.etiquetas = []
        self.etiquetaFalsa = ""
        self.etiquetaVerdadera = ""
        self.codigo3d = None
        self.codigoFuncion = ""
        self.listaFuncion =  {}
        

    def getObject(self):
        return self.codigo3d
    
    def addOperacion(self,var,op1,op,op2):
        return  var+" = "+str(op1)+op+str(op2)+";\n"
    
    def addCodigo(self,codigo):
        self.codigo += codigo
    
    def addIgual(self,arg1,arg2):
        return arg1 +" = "+str(arg2)+";\n"

    def getNuevoTemporal(self):
        if len(self.listaTemporalesLibres) == 0:
            temporal = "T" + str(self.contador)
            self.listaTemporalesEnUso.append(temporal)
            self.contador = self.contador+1
            return temporal
        else:
            return self.listaTemporalesLibres.pop()
    
    def liberarTemporales(self, temporal):
        self.listaTemporalesLibres.append(temporal)

    def init(self):
        self.header = "//**********IMPORTACIÓN DE LIBRERÍAS Y DECLARACIÓN DE VARIABLES**********\n"
        self.header += "package main;\nimport (\"fmt\";\"math\");\n"
        self.header += "var HEAP[10000000]float64;\n"
        self.header += "var STACK[10000000]float64;\n"
        self.header += "var SP,HP float64;\n"
       
    
    def addVariables(self):
        if len(self.listaTemporalesEnUso)>0:
            self.header += "var "
            index = 0
            for variable in self.listaTemporalesEnUso:
                self.header += variable
                if index < (len(self.listaTemporalesEnUso)-1):
                    self.header+=","
                index = index+1
            self.header+=" float64;\n"
        return self.header

    def funcionMain(self):
         return "//***************INICIANDO FUNCIÓN MAIN***************\nfunc main() {\nSP = 0;\nHP = 0;\n"
    
    def getNuevaEtiqueta(self):
        etiqueta =  "L"+ str(self.contadorEtiqueta)
        self.contadorEtiqueta = self.contadorEtiqueta+1
        return etiqueta
    
    def incrementarHeap(self):
        self.PH = self.PH +1
    
    def incrementarStack(self):
        self.PS = self.PS +1
    
    def getHeap(self):
        return self.PH
    
    def getStack(self):
        return self.PS

    def getValStack(self, valor):
        return "STACK[int("+str(valor)+")]"

    def getValHeap(self,valor):
        return "HEAP[int("+str(valor)+")]"
    
    def endFuncion(self):
        return "}"
    
    def llamada(self,nombre):
        return nombre+"();\n"

    def FuncionPrint(self):
        nombre = "//***************FUNCIÓN IMPRIMIR***************\n"
        nombre += "\nfunc Native_PrintString() {\n"
        temp = self.getNuevoTemporal()
        nombre += self.addOperacion(temp,"SP","+","0")
        temp2 = self.getNuevoTemporal()
        nombre += self.addIgual(temp2,self.getValStack(temp))
        etiquetaVerdadera = self.getNuevaEtiqueta()
        etiquetaFalsa = self.getNuevaEtiqueta()
        etiqueta = self.getNuevaEtiqueta()
        temp3 = self.getNuevoTemporal()
        nombre += etiquetaVerdadera+":\n"
        nombre += self.addIgual(temp3,self.getValHeap(temp2))
        nombre += "if "+ temp3+" != -1 {\ngoto "+etiqueta+";\n}\n"
        nombre += "goto "+ etiquetaFalsa+";\n"
        nombre += etiqueta+":\n"
        nombre += "fmt.Printf(\"%c\",int("+temp3+"));\n"+self.addOperacion(temp2,temp2,"+","1")
        nombre += "goto "+etiquetaVerdadera+";\n"
        nombre += etiquetaFalsa+":\n"
        #nombre += "return\n"
        nombre += "}\n"
        return nombre
    def imprimir(self,valor,tipo):
        if tipo == "c":
            return "fmt.Printf(\"%"+tipo+"\","+str(valor)+");\n"
        if tipo == "f":
            return "fmt.Printf(\"%.2f\","+str(valor)+");\n"
        else:
            return "fmt.Printf(\"%d\",int("+str(valor)+"));\n"
    
    def generarC3D_Cadenas(self,cadena):
        temp = self.getNuevoTemporal()
        codigo = "//***************ALMACENANDO CADENAS***************\n"
        
        codigo += self.addIgual(temp,"HP")
        for caracter in cadena:
            codigoascii = ord(caracter)
            valor = self.addIgual(self.getValHeap("HP"),codigoascii)
            valor += self.addOperacion("HP","HP","+","1")
            codigo+=valor
            self.incrementarHeap()

        codigo += self.addIgual(self.getValHeap("HP"),"-1")
        self.incrementarHeap()
        codigo += self.addOperacion("HP","HP","+","1")
        temporal = self.getNuevoTemporal()
        codigo += self.addOperacion(temporal,"SP","+",self.getStack())
        codigo += self.addIgual(self.getValStack(temporal),temp)
        #codigo += self.addOperacion("SP","SP","+","1")
        self.incrementarStack()
        self.addCodigo(codigo)
        self.liberarTemporales(temp)
        
    def booleanos(self,valor):
        codigo = "//*****IMPRIMIENDO UN BOOLEANO*****\n"
        if valor:
            cad = "true"
        else:
            cad = "false"
        for i in cad :
            caracter = ord(i)
            codigo +=self.imprimir(caracter,"c")
        self.addCodigo(codigo)
        
    def comparar(self,temp):

        codigo="//***** IMPRIMIENDO VARIABLE BOOLEANA*****\n"
        ev = self.getNuevaEtiqueta()
        ef = self.getNuevaEtiqueta()
        es = self.getNuevaEtiqueta()
        codigo += "if "+temp +"== 1 {\n\tgoto "+ev+";\n}\n"
        codigo += "goto "+ef+";\n"
        codigo += ev+":\n"
        cad = "true"
        for i in cad :
            caracter = ord(i)
            codigo +=self.imprimir(caracter,"c")
        codigo += "goto "+es+";\n"
        codigo += ef+":\n"
        cad = "false"
        for i in cad :
            caracter = ord(i)
            codigo +=self.imprimir(caracter,"c")
        codigo += es+":\n"
        self.addCodigo(codigo)
    
    def Parse(self,tipo):
        codigo = "\nfunc Parse(){\n"
        codigo += "// *****MÉTODO PARSER*****\n"
        temp = self.getNuevoTemporal()
        codigo += "// Variable que almacena el apuntador del stack\n"
        codigo += self.addOperacion(temp,"SP","+","0")
        temp2 = self.getNuevoTemporal()
        temp3 = self.getNuevoTemporal()
        codigo += "// Variable que almacena el valor del stack\n"
        codigo += self.addIgual(temp2,self.getValStack(temp))
        codigo += "// Variable que almacena el valor del heap\n"
        codigo += self.addIgual(temp3,self.getValHeap(temp2))
        ei = self.getNuevaEtiqueta()
        ef = self.getNuevaEtiqueta()
        contador = self.getNuevoTemporal()
        unidades = self.getNuevoTemporal()
        totales = self.getNuevoTemporal()
        temporal = self.getNuevoTemporal()
        codigo += self.addIgual(totales,"0")
        codigo += self.addIgual(contador,"0")
        codigo += self.addIgual(unidades,"1")
        codigo += ei+":\n"
        codigo += "if "+temp3+" == "+tipo+"{goto "+ef+";}\n"
        codigo += self.addOperacion(contador,contador,"+","1")
        codigo += "// Aumento la posición del heap\n"
        codigo += self.addOperacion(temp2,temp2,"+","1")
        codigo += "// Variable que almacena el valor del heap\n"
        codigo += self.addIgual(temp3,self.getValHeap(temp2))
        codigo += "goto "+ei+";\n"
        codigo += ef+":\n"
        codigo += "//Posición del heap del últmo valor de la cadena\n"
        codigo += self.addOperacion(contador,contador,"-","1")
        codigo += "// Variable que almacena el valor del stack\n"
        codigo += self.addIgual(temp2,self.getValStack(temp))
        codigo += "// Variable que almacena el valor del heap\n"
        codigo += self.addOperacion(temporal,contador,"+",temp2)
        codigo += self.addIgual(temp3,self.getValHeap(temporal))
        et = self.getNuevaEtiqueta()
        temp4 = self.getNuevoTemporal()
        #codigo += et+":\n"
        codigo += self.addOperacion(temp4,temp3,"-","48")
        codigo += self.addOperacion(temp4,temp4,"*", unidades)
        codigo += self.addOperacion(totales,totales,"+",temp4)
        codigo += self.addOperacion(unidades,unidades,"*",10)
        codigo += "if "+contador+"== 0 {goto "+et+";}\n"
        codigo += "goto "+ef+";\n"
        codigo += et+":\n"
        codigo += self.addIgual(self.getValStack(temp), totales)
        self.liberarTemporales(temp)
        self.liberarTemporales(temp2)
        self.liberarTemporales(temp3)
        self.liberarTemporales(temp4)
        self.liberarTemporales(contador)
        self.liberarTemporales(totales)
        codigo += "\n}\n"
        self.codigoFuncion= codigo
        return totales