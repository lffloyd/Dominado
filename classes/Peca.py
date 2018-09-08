class Peca():
    def __init__(self, nEsq=None, nDir=None):
        self.nEsq = nEsq
        self.nDir = nDir

    def __str__(self): return "(" + str(self.nEsq) +"|"+ str(self.nDir) + ")"

    def __cmp__(self, other):
        return self.__eq__(other)

    # Método de comparação de equivalência da classe. Compara apenas os números do dominó.
    def __eq__(self, other):
        # Checa se "other" é instância de Peca.
        if isinstance(other, self.__class__):
            return ((self.nEsq == other.nEsq) and (self.nDir == other.nDir)) \
                   or ((self.nEsq == other.nDir) and (self.nDir == other.nEsq))

    def somatorio(self): return self.nEsq + self.nDir

    def viraPeca(self):
        aux = self.__nEsq
        self.__nEsq = self.__nDir
        self.__nDir = aux