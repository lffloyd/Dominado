from classes.Peca import *
from classes.Jogador import *
import random

class Mesa():
    def __init__(self, totalPecas=None):
        self.__pecasAComprar = []
        self.__tabuleiro = []
        self.totalPecas = totalPecas

    def __str__(self):
        resp = "Compra: "
        resp += " (" + str(len(self.__pecasAComprar)) + " peça(s))" + "\nTabuleiro: "
        for peca in self.__tabuleiro: resp += str(peca)
        resp += " (" + str(len(self.__tabuleiro)) + " peça(s))"
        return resp

    def gerarPecas(self):
        pecas = [] * self.totalPecas
        for i in range(0, 7):
            for j in range(i, 7): pecas.append(Peca(i, j))
        return pecas

    def comprarPeca(self):
        pos = random.randint(0, len(self.__pecasAComprar)-1)
        peca = self.__pecasAComprar.pop(pos)
        return peca

    def comecarJogo(self, jogador1, jogador2):
        self.__pecasAComprar = []
        self.__pecasAComprar = self.gerarPecas()
        jogador1.limparMao()
        jogador2.limparMao()
        for i in range(0, 7):
            jogador1.adicionaPeca(self.comprarPeca())
            jogador2.adicionaPeca(self.comprarPeca())
        maior1, somar1 = self.procuraMaiorPeca(jogador1)
        maior2, somar2 = self.procuraMaiorPeca(jogador2)
        if ((somar1 == True) and (somar2 == True)) or ((somar1 == False) and (somar2 == False)):
            jogador1.setaVez(True) if (maior1.somatorio() > maior2.somatorio()) else jogador2.setaVez(True)
        else:
            jogador1.setaVez(True) if ((somar1 == False) and (somar2 == True)) else jogador2.setaVez(True)
        print("Maior peça de jog. 1: " + str(maior1) + "\tSomar? " + str(somar1))
        print("Maior peça de jog. 2: " + str(maior2) + "\tSomar? " + str(somar2))
        return

    def procuraMaiorPeca(self, jogador):
        maior = None
        somar = True
        for i in range(6, 0, -1):
            if ((maior == None) and (somar == True)) and (Peca(i, i) in jogador.pecas()):
                maior = Peca(i, i)
                somar = False
                break
        if (maior == None) and (somar == True):
            maior = jogador.pecas()[0]
            for i in range(1, len(jogador.pecas())):
                if ((jogador.pecas()[i]).somatorio() > maior.somatorio()): maior = jogador.pecas()[i]
        return maior, somar

    def pegaPecasAComprar(self): return self.__pecasAComprar

    def pegaTabuleiro(self): return self.__tabuleiro

    def extremos(self):
        return self.__tabuleiro[0].esq(), self.__tabuleiro[len(self.__tabuleiro)-1].dir()

    def adicionarNaMesa(self, peca, pos):
        if (len(self.__tabuleiro) == 0):
            self.__tabuleiro.insert(0, peca)
            return True
        else:
            esq, dir = self.extremos()
            esqIgual = False
            dirIgual = False
            if (pos == 0):
                if (esq == peca.esq()): esqIgual = True
                if (esq == peca.dir()): dirIgual = True
                if ((not esqIgual) and (not dirIgual)): return False
                else:
                    if (esqIgual and not dirIgual): peca.viraPeca()
                    self.__tabuleiro.insert(0, peca)
                    return True
            if (pos == 1):
                if (dir == peca.esq()): esqIgual = True
                if (dir == peca.dir()): dirIgual = True
                if ((not esqIgual) and (not dirIgual)): return False
                else:
                    if (dirIgual and not esqIgual): peca.viraPeca()
                    self.__tabuleiro.append(peca)
                    return True