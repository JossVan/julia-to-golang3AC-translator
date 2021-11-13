from abc import ABC, abstractmethod

class Codigo(ABC):
    def __init__(self, fila, columna):
        self.fila=fila
        self.columna=columna
        super().__init__()
    @abstractmethod
    def optimizar(self, codigo):
        pass
    @abstractmethod
    def Concatenar(self, codigo):
        pass