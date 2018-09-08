from classes.Color import *

class Jogador():
    def __init__(self, ind=None):
        self.__ind = ind
        self.__mao = []
        self.__maoJogaveis = []
        self.__pontos = None
        self.__vezAtual = False
        self.__jogouDaUltimaVez = False
        self.__ganhou = False
        self.__pontos = 0

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

    def setaJogou(self, jogou): self.__jogouDaUltimaVez = jogou

    def jogouRodada(self): return self.__jogouDaUltimaVez

    def pecasJogaveis(self, mesa, mao):
        resp = "                    "
        if len(mesa.pegaTabuleiro()) == 0:
            for peca in mao:
                maiorPeca, nada = mesa.procuraMaiorPeca(self)
                if peca == maiorPeca:
                    aux = mao.index(peca)
            for peca in mao:
                if mao.index(peca) == aux:
                    resp += Color.BLUE + Color.UNDERLINE + str(mao.index(peca)+1) + Color.END + "    "
                    self.__maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        else:
            extremoEsq, extremoDir = mesa.extremos()
            for peca in mao:
                if ((peca.esq() == extremoEsq or (peca.esq() == extremoDir) or
                         (peca.dir() == extremoEsq) or (peca.dir() == extremoDir))):
                    resp += Color.BLUE + Color.UNDERLINE + str(mao.index(peca)+1) + Color.END + "    "
                    self.__maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        return resp

    def limparMao(self):
        self.__mao = []
        self.__maoJogaveis = []

    def jaGanhou(self): return self.__ganhou

    def somatorioPecas(self):
        soma = 0
        for peca in self.__mao: soma += (peca.esq() + peca.dir())
        return soma

    def somaPontos(self, soma): self.__pontos += soma

    def pegaPontos(self): return self.__pontos

    def jogar(self, mesa, oponente):
        if self.__vezAtual == False: return
        else:
            adicionou = False
            while not adicionou:
                print("\n" + self.pecasJogaveis(mesa, self.__mao))
                print(self)
                print("\n" + str(mesa))
                while (len(self.__maoJogaveis) == 0):
                    if (len(mesa.pegaPecasAComprar()) != 0):
                        self.adicionaPeca(mesa.comprarPeca())
                        self.__maoJogaveis = []
                        print("\n" + self.pecasJogaveis(mesa, self.__mao))
                        print(self)
                    else:
                        self.setaJogou(False)
                        self.setaVez(False)
                        oponente.setaVez(True)
                        return
                escolhida = int(input("Qual peça deseja jogar? "))
                if (len(mesa.pegaTabuleiro()) != 0): pos = int(input("Em que posição? "))
                else: pos = 0
                peca = self.__mao.pop(escolhida-1)
                adicionou = mesa.adicionarNaMesa(peca, pos)
                if (not adicionou): self.__mao.append(peca)
                else: self.setaJogou(True)
                self.__maoJogaveis = []
            self.setaVez(False)
            oponente.setaVez(True)