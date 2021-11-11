from optimizacion.Codigo import Codigo


class Encabezado(Codigo):

    def __init__(self, paquete,importaciones,heap,stack,declaraciones,funciones):
        self.paquete = paquete
        self.importaciones = importaciones
        self.heap = heap 
        self.stack = stack 
        self.declaraciones = declaraciones
        self.funciones = funciones 
    
    def optimizar(self, tree, table, keep):
        return super().optimizar(tree, table, keep)

    def Concatenar(self):
        return super().Concatenar()