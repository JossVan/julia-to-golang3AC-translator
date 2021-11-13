from Abstractas.Objeto import TipoObjeto
from TablaSimbolos.Tipos import Tipo_Dato
from optimizacion.Codigo import Codigo
from Abstractas.Objeto import TipoObjeto
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
        elif self.valor.getTipo() == TipoObjeto.NEGATIVO:
            valor = self.valor.getValor().valor.getValor()
            return "-"+str(valor)
        
            
    def optimizar(self, codigo):
        return super().optimizar(codigo)