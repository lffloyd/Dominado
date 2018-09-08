class Peca():
    def __init__(self, nEsq=None, nDir=None):
        self.__nEsq = nEsq
        self.__nDir = nDir

    def __str__(self): return "(" + str(self.__nEsq) +"|"+ str(self.__nDir) + ")"

    def __cmp__(self, other):
        return self.__eq__(other)

    # Método de comparação de equivalência da classe. Compara apenas os números do dominó.
    def __eq__(self, other):
        # Checa se "other" é instância de Peca.
        if isinstance(other, self.__class__):
            return ((self.__nEsq == other.__nEsq) and (self.__nDir == other.__nDir)) \
                   or ((self.__nEsq == other.__nDir) and (self.__nDir == other.__nEsq))

    def esq(self): return self.__nEsq

    def dir(self): return self.__nDir

    def somatorio(self): return self.__nEsq + self.__nDir

    def viraPeca(self):
        aux = self.__nEsq
        self.__nEsq = self.__nDir
        self.__nDir = aux