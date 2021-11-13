from optimizacion.Codigo import Codigo
from optimizacion.Etiqueta import Etiqueta
from optimizacion.Reporte_optimizacion import Reporte


class Funcion(Codigo):

    def __init__(self, nombre, instrucciones, linea, columna) -> None:
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        cod = "func "+self.nombre+"(){\n"
        codigo.addCodigo(cod)
        inalcanzable = False
        contador = 0
        tam = len(self.instrucciones)
        while contador < tam:
            if isinstance(self.instrucciones[contador],Codigo):
                if not inalcanzable:
                    resultado = self.instrucciones[contador].Concatenar(codigo)
                    if isinstance(resultado,dict):
                        if "id" in resultado:
                            if (contador+1) < tam:
                                contador = contador +1
                                resultado2 = self.instrucciones[contador].Concatenar(codigo)
                                if isinstance(resultado2,dict):
                                    if "id" in resultado2:
                                        if resultado["id"] == resultado2["exp"]:
                                            if resultado2["id"] == resultado["exp"]:
                                                cod = resultado["id"]+" = "+resultado["exp"]+";\n"
                                                
                                                # SE GUARDA EN EL REPORTE
                                                original = resultado["id"]+" = "+resultado["exp"]+"\n"+ resultado2["id"]+ " = "+resultado2["exp"]                       
                                                codigo.addCodigo("\t"+cod)
                                                regla = Reporte("Optimización por mirilla","Regla 1",original,cod,self.linea)
                                                codigo.addReporte(regla)
                                                
                                        else:
                                            cod = "\t" +resultado["id"]+" = "+resultado["exp"]+";\n"
                                            cod += "\t" +resultado2["id"]+" = "+resultado2["exp"]+";\n"
                                            codigo.addCodigo(cod)
                                    elif "optimizada" in resultado2:
                                        cod = "\t" +resultado["id"]+" = "+resultado["exp"]+";\n"
                                        cod += resultado2["optimizada"]
                                        codigo.addCodigo(cod)
                                    elif "goto" in resultado2:
                                        cod = "\t" +resultado["id"]+" = "+resultado["exp"]+";\n"
                                        codigo.addCodigo(cod)
                                        codigo.addCodigo("\tgoto "+resultado2["goto"]+";\n")
                                        if (contador+1)< tam:
                                            contador = contador +1
                                            resultado3 = self.instrucciones[contador].Concatenar(codigo)
                                            if isinstance(resultado3,dict):
                                                if "etiqueta" in resultado3:
                                                    codigo.addCodigo(resultado3["etiqueta"]+":\n")
                                                else:
                                                    inalcanzable = True
                                    elif "etiqueta" in resultado2:
                                        cod = "\t" +resultado["id"]+" = "+resultado["exp"]+";\n"
                                        codigo.addCodigo(resultado2["etiqueta"]+":\n")
                                    elif "print" in resultado2:
                                        cod = "\t" +resultado["id"]+" = "+resultado["exp"]+";\n"
                                        codigo.addCodigo(cod)
                                        codigo.addCodigo(resultado2["print"])
                                elif resultado2 == None:
                                    cod = resultado["id"]+" = "+resultado["exp"]+";\n"
                                    codigo.addCodigo(cod)
                            else:
                                cod = resultado["id"]+" = "+resultado["exp"]+";\n"
                                codigo.addCodigo("\t"+cod)
                        elif "optimizada" in resultado:
                            codigo.addCodigo(resultado["optimizada"])
                        elif "goto" in resultado:
                            codigo.addCodigo("\tgoto"+resultado["goto"]+";\n")
                            if (contador+1)< tam:
                                contador = contador +1
                                resultado2 = self.instrucciones[contador].Concatenar(codigo)
                                if isinstance(resultado2,dict):
                                    if "etiqueta" in resultado2:
                                        codigo.addCodigo(resultado2["etiqueta"]+":\n")
                                    else:
                                        inalcanzable = True
                        elif "etiqueta" in resultado:
                            codigo.addCodigo(resultado["etiqueta"]+":\n")
                        elif "print" in resultado:
                            codigo.addCodigo(resultado["print"])
                else:
                    
                    if isinstance(self.instrucciones[contador],Etiqueta):
                        inalcanzable = False
                        resultado = self.instrucciones[contador].Concatenar(codigo)
                        if isinstance(resultado,dict):
                            if "etiqueta" in resultado:
                                codigo.addCodigo(resultado["etiqueta"]+":\n")
            contador = contador +1
        codigo.addCodigo("}")

    def optimizar(self, codigo):
        return super().optimizar(codigo)
    