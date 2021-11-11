from abc import ABC, abstractmethod

class Codigo(ABC):
    def __init__(self, fila, columna):
        self.fila=fila
        self.columna=columna
        super().__init__()
    @abstractmethod
    def optimizar(self,tree,table, keep):
        pass
    @abstractmethod
    def Concatenar(self):
        pass