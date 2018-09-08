from classes.Color import *

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
                    resp += " " + color.BLUE + color.UNDERLINE + str(mao.index(peca)+1) + color.END
                else:
                    resp += " " + str(mao.index(peca)+1)
        else:
            return
            #for peca in mao:
            #    if (peca.nEsq == mesa.extremoEsq() || peca.nEsq == mesa.extremoDir() || peca.nDir == mesa.extremoEsq() || peca.nDir == mesa.extremoDir()):
            #            resp += color.BLUE + " " + mao.index(peca) + color.END
            #    else:
            #        resp += " " + mao.index(peca)
        return resp

    def jogar(self, mesa):
        if self.vezAtual == False: return
        else:
            print("\nJogador "+str(self.__ind),self)
            print(self.pecasJogaveis(mesa, self.mao))
            #escolhida = input("Qual peça deseja jogar?")
            #addMesa(mesa, self.mao[escolhida-1])
            #del self.mao[escolhida-1]
