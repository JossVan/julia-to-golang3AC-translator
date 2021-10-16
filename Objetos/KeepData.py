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
        self.codigo3d = None


    def getObject(self):
        return self.codigo3d
    
    def addOperacion(self,var,op1,op,op2):
        return  var+" = "+str(op1)+op+str(op2)+"\n"
    
    def addCodigo(self,codigo):
        self.codigo += codigo+"\n"
    
    def addIgual(self,arg1,arg2):
        return arg1 +" = "+str(arg2)+"\n"

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
        self.header = "package main\nimport \"fmt\"\n"
        self.header += "var HEAP[10000000]float64\n"
        self.header += "var STACK[10000000]float64\n"
        self.header += "var SP float64 = 0\n"
        self.header += "var HP float64 = 0\n"
    
    def addVariables(self):
        if len(self.listaTemporalesEnUso)>0:
            self.header += "var "
            index = 0
            for variable in self.listaTemporalesEnUso:
                self.header += variable
                if index < (len(self.listaTemporalesEnUso)-1):
                    self.header+=","
                index = index+1
            self.header+=" float64\n"
        return self.header

    def funcionMain(self):
         return "func main() {\n"
    
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
        return nombre+"()\n"

    def FuncionPrint(self):
        nombre = "\nfunc Native_PrintString() {\n"
        temp = self.getNuevoTemporal()
        nombre += self.addOperacion(temp,"SP","-","1")
        temp2 = self.getNuevoTemporal()
        nombre += self.addIgual(temp2,self.getValStack(temp))
        etiquetaVerdadera = self.getNuevaEtiqueta()
        etiquetaFalsa = self.getNuevaEtiqueta()
        temp3 = self.getNuevoTemporal()
        nombre += etiquetaVerdadera+":\n"
        nombre += self.addIgual(temp3,self.getValHeap(temp2))
        nombre += "if ("+ temp3+" != -1) {\n fmt.Printf(\"%c\",int("+temp3+"))\n"+self.addOperacion(temp2,temp2,"+","1")+"goto "+ etiquetaVerdadera+"\n}\n"
        nombre += "goto "+ etiquetaFalsa+"\n"
        nombre += etiquetaFalsa+":\n"
        nombre += "return\n"
        nombre += "}\n"
        return nombre
    def imprimir(self,valor,tipo):
        if tipo == "c":
            return "fmt.Printf(\"%"+tipo+"\","+str(valor)+")\n"
        elif tipo == "f":
            return "fmt.Printf(\"%.2f\","+str(valor)+")\n"
            
        return "fmt.Print("+str(valor)+")\n"
    
    def eliminarTemps(self):
            self.listaTemporalesEnUso=[]
            self.listaTemporalesLibres=[]
        
