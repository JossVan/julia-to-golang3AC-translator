class General():

    codigo = ""
    funciones = []
    listaFuncion = {}
    def __init__(self):
        self.codigo = ""
        self.funciones = []
    

    def getFunciones(self):
        return self.funciones
    
    def getCodigo(self):
        return self.codigo
    
    def addCodigo(self,codigo):
        self.codigo += codigo
    
    def addListaFuncion(self,nombre,codigo):
        self.listaFuncion[nombre]= codigo
        