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
    
    
    def getInstancia(self):
        if self.codigo3d == None:
            self.codigo3d = KeepData()
            return self.codigo3d
        else:
            return self.codigo3d

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
        self.header += "var HEAP[10000000]double\n"
        self.header += "var STACK[10000000]double\n"
        self.header += "var PS int = 0\n"
        self.header += "var PH int = 0\n"
    
    def addVariables(self):
        if len(self.listaTemporalesEnUso)>0:
            self.header += "var "
            index = 0
            for variable in self.listaTemporalesEnUso:
                self.header += variable
                if index < (len(self.listaTemporalesEnUso)-1):
                    self.header+=","
                index = index+1
            self.header+=" int\n"
            self.header += "func main() {\n"
        return self.header

    def getNuevaEtiqueta(self):
        etiqueta =  "L"+self.contadorEtiqueta
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
        return "STACK["+str(valor)+"]"

    def getValHeap(self,valor):
        return "HEAP["+str(valor)+"]"
    
    def endFuncion(self):
        return "}"
    
    
