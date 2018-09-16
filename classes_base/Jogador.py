#Define a classe Jogador e seus atributos associados.

#Escrito por: Vítor Costa, Luiz Felipe

from classes_base.Cor import *
from classes_busca.Expectiminimax import *

class Jogador():
    #Construtor define atributos como a "mão" do jogador (i.e. suas peças), as peças jogáveis num dado momento (i.e. aque-
    #las que ele pode efetivamente encaixar no tabuleiro), qtd. de pontos acumulada e outros parãmetros de controle.
    def __init__(self, ind=None, ehIa=True):
        self.__ind = ind
        self.__mao = []
        self.__maoJogaveis = []
        self.__pontos = None
        self.__vezAtual = False
        self.__jogouDaUltimaVez = False
        self.__ganhou = False
        self.__pontos = 0

        self.__ehIa = ehIa

    def __str__(self):
        resp = "Jogador " + str(self.__ind) + " -"
        resp += "\tMão: "
        for peca in self.__mao: resp += str(peca)
        resp += "\tVez atual: "
        resp += ("Sim" if(self.__vezAtual) else "Não")
        return resp

    #Adiciona uma peça à mão do jogador.
    def adicionaPeca(self, peca):
        self.__mao.append(peca)

    #Retorna as peças do jogador.
    def pecas(self): return self.__mao

    #Usada para indicar se o jogador está ativo no momento corrente.
    def ehSuaVez(self): return self.__vezAtual

    #Modifica o estado de atividade do jogador.
    def setaVez(self, seuTurno): self.__vezAtual = seuTurno

    #Retorna o índice do jogador. O índice é um número usado para distinguir os diferentes jogadores.
    def pegaIndice(self): return self.__ind

    #Modifica o estado da última tentativa de jogada realizada pelo jogador (i.e. ele pode ter conseguido jogar ou não).
    def setaJogou(self, jogou): self.__jogouDaUltimaVez = jogou

    #Retorna se o jogador participou efetivamente da última rodada do jogo (usado para verificar se o jogador está "travado",
    #ou seja, se não pode mais jogar por não ter peças para encaixar nem peças para comprar).
    def jogouRodada(self): return self.__jogouDaUltimaVez

    # Indica as peças que o jogador pode encaixar num dado momento no tabuleiro, avaliando se esta é a primeira jogada do jogo
    # ou se ele precisa encaixar uma peça numa das duas pontas da mesa. Para indicar quais peças o jogador pode encaixar,
    # cores são utilizadas.
    def pecasJogaveis(self, mesa, mao):
        resp = "                    "
        if len(mesa.pegaTabuleiro()) == 0:
            for peca in mao:
                maiorPeca, nada = mesa.procuraMaiorPeca(self)
                if peca == maiorPeca:
                    aux = mao.index(peca)
            for peca in mao:
                if mao.index(peca) == aux:
                    resp += Cor.BLUE + Cor.UNDERLINE + str(mao.index(peca)+1) + Cor.END + "    "
                    self.__maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        else:
            extremoEsq, extremoDir = mesa.extremos()
            for peca in mao:
                if ((peca.esq() == extremoEsq or (peca.esq() == extremoDir) or
                         (peca.dir() == extremoEsq) or (peca.dir() == extremoDir))):
                    resp += Cor.BLUE + Cor.UNDERLINE + str(mao.index(peca)+1) + Cor.END + "    "
                    self.__maoJogaveis.append(peca)
                else:
                    resp += str(mao.index(peca)+1) + "    "
        return resp

    def pegaPecasJogaveis(self): return self.__maoJogaveis

    #Elimina todas as cartas de um jogador.
    def limparMao(self):
        self.__mao = []
        self.__maoJogaveis = []

    #Verifica se um jogador ganhou, ou seja, se a variável de controle do mesmo indica sua vitória.
    def jaGanhou(self): return self.__ganhou

    #Retorna o somatório de valores de todas as peças do jogador. Ambos os lados de uma peça são somados.
    def somatorioPecas(self):
        soma = 0
        for peca in self.__mao: soma += (peca.esq() + peca.dir())
        return soma

    #Incrementa a pontuação de um jogador.
    def somaPontos(self, soma): self.__pontos += soma

    #Retorna a qtd. de pontos acumulada até o momento do jogador.
    def pegaPontos(self): return self.__pontos

    #Método que coordena cada uma das jogadas do jogador. Até o momento, necessita da interação de um humano para realizar
    # uma jogada. Aguarda até que o jogador escolha uma peça válida para encaixar ou até que não possua nenhuma peça válida
    #para jogar, passando a vez a seu oponente.
    def jogar(self, mesa, oponente):
        if (self.__ehIa): return self.jogarIA(mesa, oponente)
        else: return self.jogarHumano(mesa, oponente)

    def jogarHumano(self, mesa, oponente):
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
            if (len(self.__mao) == 0): self.__ganhou = True
            return

    def jogarIA(self, mesa, oponente): return