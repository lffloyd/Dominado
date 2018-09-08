from classes.Color import *

class Jogador:
    def __init__(self, ind=None):
        self.__ind = ind
        self.mao = []
        self.maoJogaveis = []
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


# TESTEEEE
    def pecasJogaveis(self, mesa, mao):
        resp = "                "
        if len(mesa.pegaTabuleiro()) == 0:
            for peca in mao:
                maiorPeca, nada = mesa.procuraMaiorPeca(self)
                if peca == maiorPeca:
                    aux = mao.index(peca)
            for peca in mao:
                if mao.index(peca) == aux:
                    resp += Color.BLUE + Color.UNDERLINE + str(mao.index(peca)+1) + Color.END + "    "
                    self.maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        else:
            extremoEsq, extremoDir = mesa.extremos()
            for peca in mao:
                if ((peca.nEsq == extremoEsq or (peca.nEsq == extremoDir) or (peca.nDir == extremoEsq) or (peca.nDir == extremoDir))):
                    resp += Color.BLUE + Color.UNDERLINE + str(mao.index(peca)+1) + Color.END + "    "
                    self.maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        return resp

    def jogar(self, mesa):
        if self.vezAtual == False: return
        else:
            print("\n" + self.pecasJogaveis(mesa, self.mao))
            print("Jogador "+str(self.__ind),self)
            print("\n" + str(mesa))
            while (len(self.maoJogaveis) == 0):
                self.adicionaPeca(mesa.comprarPeca())
                self.maoJogaveis = []
                print("\n" + self.pecasJogaveis(mesa, self.mao))
                print("Jogador " + str(self.__ind), self)

            escolhida = int(input("Qual peça deseja jogar?"))
            if (len(mesa.pegaTabuleiro())) != 0: pos = int(input("Em que posição?"))
            else: pos = 0
            mesa.adicionarNaMesa(self.mao[escolhida-1], pos)
            del self.mao[escolhida-1]