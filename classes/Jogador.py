class Jogador:
    def __init__(self, ind=None):
        self.__ind = ind
        self.mao = []
        self.pontos = None
        self.vezAtual = False

    def __str__(self):
        resp = "Mão: "
        for peca in self.mao: resp += str(peca)
        resp += "\tVez atual: "
        resp += ("Sim" if(self.vezAtual) else "Não")
        return resp

    def adicionaPeca(self, peca):
        self.mao.append(peca)

    def pecas(self): return self.mao

    def ehSuaVez(self): return self.vezAtual

    def setaVez(self, seuTurno): self.vezAtual = seuTurno

    def pegaIndice(self): return self.__ind