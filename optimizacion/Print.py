from optimizacion.Codigo import Codigo


class Print(Codigo):

    def __init__(self, tipo, valor, int, linea, columna):
        self.tipo = tipo 
        self.valor = valor
        self.int = int 
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        cod = "fmt.Printf(\""+self.tipo+"\","
        
        if isinstance(self.valor,Codigo):
            val = self.valor.Concatenar(codigo)
        
        if self.int == None:
            cod += val+");\n"
        else:
            cod += "int("+val+"));\n"

        return {"print":"\t"+cod}

    def optimizar(self, codigo):
        return super().optimizar(codigo)
