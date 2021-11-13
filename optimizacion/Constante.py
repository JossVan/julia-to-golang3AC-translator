from Abstractas.Objeto import TipoObjeto
from TablaSimbolos.Tipos import Tipo_Dato
from optimizacion.Codigo import Codigo
class Constante(Codigo):

    def __init__(self, valor, linea, columna):
        self.valor = valor 
        self.linea = linea 
        self.columna = columna
    
    def Concatenar(self, codigo):
        
        if self.valor.getTipo() == Tipo_Dato.DECIMAL:
            return str(self.valor.getValor())
        elif self.valor.getTipo() == Tipo_Dato.ENTERO:
            return str(self.valor.getValor())
        
            
    def optimizar(self, codigo):
        return super().optimizar(codigo)