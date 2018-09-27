# MIT License
#
# Copyright (c) 2018 Luiz Felipe de Melo (lffloyd), Vítor Costa (vitorhardoim), Renato Bastos (RenatoBastos33)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################################################


#Define a Mesa de jogo, que representa onde as peças do dominó serão dispostas e onde estarão
#disponíveis peças para compra pelos jogadores.

#Escitor por: Vítor Costa, Luiz Felipe.

from classes_base.Peca import *
from classes_base.Cor import *
import random

class Mesa():
    #Construtor define os conjuntos de peças que estarão disponíveis para compra e aquelas que estão encaixadas no dominó.
    def __init__(self, totalPecas=None):
        self.__pecasAComprar = []
        self.__tabuleiro = []
        self.totalPecas = totalPecas
        self.fechada = False

    def __str__(self):
        resp = "Compra: "
        resp += " (" + str(len(self.__pecasAComprar)) + " peça(s))" + ", \tTabuleiro: "
        for peca in self.__tabuleiro:
            if (peca.pegaOrdem() == len(self.__tabuleiro)): resp += Cor.RED + str(peca) + Cor.END
            else: resp += str(peca)
        resp += " (" + str(len(self.__tabuleiro)) + " peça(s))"
        return resp

    #Cria as instâncias de Peça do jogo.
    def gerarPecas(self):
        pecas = [] * self.totalPecas
        for i in range(0, 7):
            for j in range(i, 7): pecas.append(Peca(i, j))
        return pecas

    #Método usado para compra de peças pelo jogador. Retorna uma peça dentre as disponíveis para compra, selecionada
    #aleatoriamente.
    def comprarPeca(self):
        pos = random.randint(0, len(self.__pecasAComprar)-1)
        peca = self.__pecasAComprar.pop(pos)
        return peca

    #Método que configura as mãos dos jogadores da partida além do estado inicial do tabuleiro.
    #Distribui peças a cada um dos jogadores e determina qual deles irá iniciar a partida baseando-se em suas peças.
    def comecarJogo(self, jogador1, jogador2):
        self.__tabuleiro = []
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

    #Método usado para buscar a maior peça de um jogador. Utilizado para definir o jogador iniciante numa partida.
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

    #Retorna as peças disponíveis para compra.
    def pegaPecasAComprar(self): return self.__pecasAComprar

    #Retorna o estado atual do tabuleiro de jogo, i.e. as peças que foram encaixadas até agora e seu posicionamento.
    def pegaTabuleiro(self): return self.__tabuleiro

    #Retorna os valores mais extremos (na esquerda e na direita) do tabuleiro, i.e. os valores disponíveis para encaixe.
    def extremos(self):
        return self.__tabuleiro[0].esq(), self.__tabuleiro[len(self.__tabuleiro)-1].dir()

    #Método usado para posicionar no tabuleiro uma peça escolhida pelo jogodar. Avalia se a inserção no local escolhido
    #pode ocorrer, virando a peça caso necessário.
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

    # Conta a ocorrência de um dado valor (como uma das faces de uma peça) entre as peças da mesa (no caso, as peças já
    #  encaixadas no tabuleiro).
    def contarValor(self, valor):
        cont = 0
        for peca in self.__tabuleiro:
            if (peca.esq() == valor) or (peca.dir() == valor): cont += 1
        return cont
