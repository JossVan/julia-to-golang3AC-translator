from optimizacion.Codigo import Codigo


class If(Codigo):

    def __init__(self, condicion, salto, linea, columna):
        self.condicion = condicion 
        self.salto = salto
        self.linea = linea
        self.columna = columna
    

    def Concatenar(self, codigo):
        if isinstance(self.condicion,Codigo):
            condicion = self.condicion.Concatenar(codigo)
        else: 
            condicion = self.condicion
        
        cod = "if "+ condicion+" {"

        if isinstance(self.salto,Codigo):
            salto = self.salto.Concatenar(codigo)
            if isinstance(salto,dict):
                if "goto" in salto:
                    salt = "goto " +salto["goto"]+";\n"
                    cod += salt+"}"
        return {"if": "\t"+cod}
    
    def optimizar(self, codigo):
        return super().optimizar(codigo)

    