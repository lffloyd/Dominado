class Jogador:
    def __init__(self):
        self.mao = []
        self.pontos = None

    def __str__(self):
        resp = "Mão: "
        for i in self.mao:
            resp += str(i)
        return resp

    def addPeca(self, peca):
        self.mao.append(peca)