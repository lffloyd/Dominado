from classes.Color import *

class Jogador():
    def __init__(self, ind=None):
        self.__ind = ind
        self.__mao = []
        self.__pontos = None
        self.__vezAtual = False

    def __str__(self):
        resp = "Jogador " + str(self.__ind) + " -"
        resp += "\tMão: "
        for peca in self.__mao: resp += str(peca)
        resp += "\tVez atual: "
        resp += ("Sim" if(self.__vezAtual) else "Não")
        return resp

    def adicionaPeca(self, peca):
        self.__mao.append(peca)

    def pecas(self): return self.__mao

    def ehSuaVez(self): return self.__vezAtual

    def setaVez(self, seuTurno): self.__vezAtual = seuTurno

    def pegaIndice(self): return self.__ind


    # TESTEEEE
    def pecasJogaveis(self, mesa, mao):
        resp = ""
        if len(mesa.pegaTabuleiro()) == 0:
            for peca in mao:
                maiorPeca, nada = mesa.procuraMaiorPeca(self)
                if peca == maiorPeca:
                    aux = mao.index(peca)
            for peca in mao:
                if mao.index(peca) == aux:
                    resp += " " + Color.BLUE + Color.UNDERLINE + str(mao.index(peca) + 1) + Color.END
                else:
                    resp += " " + str(mao.index(peca) + 1)
        else:
            extremoEsq, extremoDir = mesa.extremos()
            for peca in mao:
                if ((peca.nEsq == extremoEsq or (peca.nEsq == extremoDir) or (peca.nDir == extremoEsq) or (
                    peca.nDir == extremoDir))):
                    resp += " " + Color.BLUE + Color.UNDERLINE + str(mao.index(peca) + 1) + Color.END
                else:
                    resp += " " + str(mao.index(peca) + 1)
        return resp

    def jogar(self, mesa):
        if self.__vezAtual == False: return
        else:
            print(self)
            print(self.pecasJogaveis(mesa, self.__mao))
            #escolhida = input("Qual peça deseja jogar?")
            #mesa.adicionarNaMesa(self.mao[escolhida-1], pos)
            #del self.mao[escolhida-1]