from optimizacion.Reporte_optimizacion import Reporte


class General():

    codigo = ""
    funciones = []
    listaFuncion = {}
    reporte = []
    def __init__(self):
        self.codigo = ""
        self.funciones = []
    
    def addReporte(self,repo):
        self.reporte.append(repo)
        
    def getFunciones(self):
        return self.funciones
    
    def getCodigo(self):
        return self.codigo
    
    def addCodigo(self,codigo):
        self.codigo += codigo
    
    def addListaFuncion(self,nombre,codigo):
        self.listaFuncion[nombre]= codigo
    

    def htmlOptimizacion(self):

        cadena = "<table class=\"table\">\n"
        cadena += "<thead>"
        cadena +="<tr>"
        cadena +="<th scope=\"col\">Tipo de optmización</th>"
        cadena +="<th scope=\"col\">Regla aplicada</th>"
        cadena +="<th scope=\"col\">Expresión Original</th>"
        cadena +="<th scope=\"col\">Expresión Optimizada</th>"
        cadena +="<th scope=\"col\">Linea</th>"
        cadena +="</tr>"
        cadena +="</thead>"
        cadena +="<tbody>"
        
        for regla in self.reporte:
            if isinstance(regla,Reporte):
                cadena+="<tr>"
                cadena+="<td>"
                cadena+= regla.optimizacion
                cadena+="</td>"
                cadena+="<td>"
                cadena+= regla.regla
                cadena+="</td>"
                cadena+="<td>"
                cadena+= regla.original
                cadena+="</td>"
                cadena+="<td>"
                cadena+= regla.optimizada
                cadena+="</td>"
                cadena+="<td>"
                cadena+= str(regla.linea)
                cadena+="</td>"
                cadena+="</tr>"
        cadena+="</tbody>"
        cadena+="</table>"
        return cadena
        