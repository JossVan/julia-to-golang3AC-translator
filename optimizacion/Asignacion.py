from TablaSimbolos.Tipos import Tipo_Aritmetico
from optimizacion.Aritmetica import Aritmetica
from optimizacion.Arreglo import Arreglo
from optimizacion.Codigo import Codigo
from optimizacion.Constante import Constante
from optimizacion.Reporte_optimizacion import Reporte
from optimizacion.Variable import Variable


class Asignacion(Codigo):

    def __init__(self, id, expresion, linea, columna):
        self.id = id
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
        
    
    def Concatenar(self, codigo):
        
        if isinstance(self.id, str):
            id  = self.id
        elif isinstance(self.id,Arreglo):
            id = self.id.Concatenar(codigo)

        if isinstance(self.expresion,Aritmetica):
            expresion = self.expresion.Concatenar(codigo)
            if isinstance(expresion,dict):
                if "expresion1" in expresion:
                    if id == expresion["expresion1"] and (expresion["operador"] == Tipo_Aritmetico.SUMA or expresion["operador"] == Tipo_Aritmetico.RESTA):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                                if expresion["operador"] == Tipo_Aritmetico.SUMA:
                                    op = "+"
                                elif expresion["operador"] == Tipo_Aritmetico.RESTA:
                                    op = "-"
                        if expresion["expresion2"] == "0":
                            original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                            regla = Reporte("Optimización por mirilla","Regla 6",original,"Eliminada",self.linea)
                            codigo.addReporte(regla)
                        else:
                            original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                            return {"optimizada": "\t"+original+"\n"}
                    elif id == expresion["expresion1"] and (expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION or expresion["operador"] == Tipo_Aritmetico.DIVISION):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                                if expresion["operador"] == Tipo_Aritmetico.DIVISION:
                                    op = "/"
                                elif expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                                    op = "*"
                        if expresion["expresion2"] == "1":
                            original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                            regla = Reporte("Optimización por mirilla","Regla 6",original,"Eliminada",self.linea)
                            codigo.addReporte(regla)
                        else:
                            original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                            return {"optimizada": "\t"+original+"\n"}
                    elif expresion["expresion2"] == "0" and (expresion["operador"] == Tipo_Aritmetico.SUMA or expresion["operador"] == Tipo_Aritmetico.RESTA):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                            if expresion["operador"] == Tipo_Aritmetico.SUMA:
                                op = "+"
                            elif expresion["operador"] == Tipo_Aritmetico.RESTA:
                                op = "-"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion1"]
                        regla = Reporte("Optimización por mirilla","Regla 7",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion1"] == "0" and (expresion["operador"] == Tipo_Aritmetico.SUMA or expresion["operador"] == Tipo_Aritmetico.RESTA):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                            if expresion["operador"] == Tipo_Aritmetico.SUMA:
                                op = "+"
                            elif expresion["operador"] == Tipo_Aritmetico.RESTA:
                                op = "-"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion2"]
                        
                        regla = Reporte("Optimización por mirilla","Regla 7",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion2"] == "1" and (expresion["operador"] == Tipo_Aritmetico.DIVISION or expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                            if expresion["operador"] == Tipo_Aritmetico.DIVISION:
                                op = "/"
                            elif expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                                op = "*"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion1"]
                    
                        regla = Reporte("Optimización por mirilla","Regla 7",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion1"] == "1" and (expresion["operador"] == Tipo_Aritmetico.DIVISION or expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION):
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                            if expresion["operador"] == Tipo_Aritmetico.DIVISION:
                                op = "/"
                            elif expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                                op = "*"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion2"]
                        
                        regla = Reporte("Optimización por mirilla","Regla 7",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion2"] == "2" and expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                        op = "*"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion1"]+"+"+expresion["expresion1"]
                        
                        regla = Reporte("Optimización por mirilla","Regla 8",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion1"] == "2" and expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                        op = "*"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ expresion["expresion2"]+"+"+expresion["expresion2"]
                        
                        regla = Reporte("Optimización por mirilla","Regla 8",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion1"] == "0" or expresion["expresion2"] == "0" and expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                        op = "*"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ "0"
                        
                        regla = Reporte("Optimización por mirilla","Regla 8",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    elif expresion["expresion1"] == "0" and expresion["operador"] == Tipo_Aritmetico.DIVISION:
                        op = "/"
                        original = id+" = "+expresion["expresion1"]+op+expresion["expresion2"]
                        optimizada = id+ " = "+ "0"
                        
                        regla = Reporte("Optimización por mirilla","Regla 8",original,optimizada,self.linea)
                        codigo.addReporte(regla)
                        return {"optimizada": "\t"+optimizada+";\n"}
                    else:
                        if isinstance(expresion["operador"],Tipo_Aritmetico):
                            if expresion["operador"] == Tipo_Aritmetico.SUMA:
                                op = "+"
                            elif expresion["operador"] == Tipo_Aritmetico.RESTA:
                                op = "-"
                            elif expresion["operador"] == Tipo_Aritmetico.MULTIPLICACION:
                                op = "*"
                            elif expresion["operador"] == Tipo_Aritmetico.DIVISION:
                                op ="/"
                            elif expresion["operador"] == Tipo_Aritmetico.MODAL:
                                cod = "\t"+id +" = math.Mod("+expresion["expresion1"]+","+expresion["expresion2"]+");\n"
                                codigo.addCodigo(cod)
                                return
                            cod = "\t"+id+" = "+expresion["expresion1"]+op+ expresion["expresion2"]+";\n"
                            return {"optimizada": cod}
        elif isinstance(self.expresion,Arreglo):
            exp = self.expresion.Concatenar(codigo)
            cod = "\t"+ id+" = "+exp 
            #codigo.addCodigo(cod)
            return {"id":id,"exp":exp}
        elif isinstance(self.expresion,Variable):
            exp = self.expresion.Concatenar(codigo)
            cod ="\t"+ id+" = "+ exp+";\n"
            #codigo.addCodigo(cod)
            return {"id":id,"exp":exp}
        elif isinstance(self.expresion,Constante):
            exp = self.expresion.Concatenar(codigo)
            cod = "\t"+ id+" = "+ str(exp)+";\n"
            #codigo.addCodigo(cod)
            return {"id":id,"exp":exp}
        

    def optimizar(self, codigo):
        return super().optimizar(codigo)