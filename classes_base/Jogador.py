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


#Define a classe Jogador e seus atributos associados. A classe pode comportar-se como um jogador aleatório, humano ou
# de inteligência artificial.

#Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos.

import random
from classes_base.Cor import *
from classes_base.Peca import *
from classes_busca.Expectiminimax import *
from classes_busca.Estado import *
from classes_busca.EstadoMCTS import *
from classes_busca.MonteCarloNo import *

class Jogador():
    #Constantes para identificação do tipo de jogador.
    RANDOM = 3 #Jogador 'Random'. Executa qualquer das ações que tiver como disponíveis em qualquer momento do jogo.
    MCTS = 2 #I.A. que emprega Monte Carlo tree search na determinação do melhor mov. a ser executado.
    EXPECTMM = 1 #I.A. que emprega Expectiminimax para determinar a melhor jogada a ser feita.
    HUMANO = 0 #Representa um jogador humano, que interage com o jogo escolhendo as jogadas que deseja realizar por
               # linha de comando.

    #Construtor define atributos como a "mão" do jogador (i.e. suas peças), as peças jogáveis num dado momento (i.e. aque-
    #las que ele pode efetivamente encaixar no tabuleiro), qtd. de pontos acumulada e outros parãmetros de controle.
    def __init__(self, ind=None, tipo=HUMANO):
        self.__ind = ind
        self.__mao = []
        self.__maoJogaveis = []
        self.__vezAtual = False
        self.__jogouDaUltimaVez = False
        self.__pontos = 0
        self.vitorias = 0
        self.tipo = tipo
        self.tipoStr = None
        if (self.tipo == self.HUMANO): self.tipoStr = "HUMANO"
        elif (self.tipo == self.EXPECTMM): self.tipoStr = "EXPMM"
        elif (self.tipo == self.MCTS): self.tipoStr = "MCTS"
        else: self.tipoStr = "RANDOM"

    #Rerpesentação textual da instância de Jogador.
    def __str__(self):
        resp = "J" + str(self.__ind) + " ("+ self.tipoStr + ") -"
        resp += "\tMão: "
        for peca in self.__mao: resp += str(peca)
        resp += ",\tVez atual: "
        resp += ("Sim" if(self.__vezAtual) else "Não")
        resp += ",\tPossui "+str(len(self.__mao))+" peça(s)"
        return resp

    #Adiciona uma peça à mão do jogador.
    def adicionaPeca(self, peca): self.__mao.append(peca)

    #Remove uma dada instância de Peça da mão do jogador, caso ela exista. Necessita receber uma instância de Mesa
    #para manter a consistência da variável que armazena as peças jogáveis num dado momento pelo jogador.
    def removePeca(self, mesa, peca):
        if (len(self.__mao) != 0):
            self.__mao.remove(peca)
            self.atualizaPecasJogaveis(mesa)

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
        resp = "                        "
        if len(mesa.pegaTabuleiro()) == 0:
            aux = None
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
                else: resp += str(mao.index(peca)+1) + "    "
        return resp

    #Atualiza as peças jogáveis no tabuleiro de jogo no dado momento da partida.
    def atualizaPecasJogaveis(self, mesa):
        self.__maoJogaveis = []
        if (len(mesa.pegaTabuleiro()) == 0):
            aux = None
            for peca in self.__mao:
                maiorPeca, nada = mesa.procuraMaiorPeca(self)
                if (peca == maiorPeca): aux = self.__mao.index(peca)
            for peca in self.__mao:
                if self.__mao.index(peca) == aux: self.__maoJogaveis.append(peca)
        else:
            esq, dir = mesa.extremos()
            for peca in self.__mao:
                if ((peca.esq() == esq or (peca.esq() == dir) or
                         (peca.dir() == esq) or (peca.dir() == dir))):
                    self.__maoJogaveis.append(peca)

    #Retorna as peças jogáveis num dado momento da partida.
    def pegaPecasJogaveis(self): return self.__maoJogaveis

    #Retorna todas as possibilidades de jogadas disponíveis no dado momento a esta instância de Jogador.
    #O retorno é composto de uma matriz contendo pares [Peça, Posição de jogada, Probabilidade da jogada].
    def possibilidadesJogaveis(self, mesa):
        possibilidades = []
        probabilidade = 1//7
        self.atualizaPecasJogaveis(mesa)
        if (len(mesa.pegaTabuleiro()) == 0):
            for peca in self.__maoJogaveis: possibilidades.append([peca, 0, probabilidade])
        else:
            esq, dir = mesa.extremos()
            for peca in self.__maoJogaveis:
                if (peca.ehJogavel(esq) and peca.ehJogavel(dir)):
                    possibilidades.append([peca, 0, self.probabilidadeJogada(peca, esq, mesa)])
                    possibilidades.append([peca.viraPeca(), 1, self.probabilidadeJogada(peca, dir, mesa)])
                else: possibilidades.append([peca, (0 if (peca.ehJogavel(esq)) else 1),
                                             (self.probabilidadeJogada(peca, esq, mesa) if (peca.ehJogavel(esq)) else
                                              self.probabilidadeJogada(peca, dir, mesa))])
        return possibilidades

    #Calcula a probabilidade de uma dada peça ser encaixada numa dada posição do tabuleiro/mesa baseando-se no total
    # de ocorrência dos valores das faces da peça no tabuleiro.
    def probabilidadeJogada(self, peca, pos, mesa):
        contagemMax = 7
        contagem = 1
        probMax = 1
        if (peca.esq() == pos): contagem += mesa.contarValor(peca.dir())
        elif (peca.dir() == pos): contagem += mesa.contarValor(peca.esq())
        probabilidade = (probMax*contagem) / contagemMax
        return probabilidade

    #Compra peças da mesa enquanto existirem peças disponíveis para compra na mesma e/ou enquanto o jogador não
    #tiver nenhuma peça jogável em mãos. Invólucro para o métod de compra de peças disponibilizado pela classe Mesa
    # (mesa.comprarPeca()).
    def compraDaMesa(self, mesa):
        self.atualizaPecasJogaveis(mesa)
        while (len(self.pegaPecasJogaveis()) == 0):
            if (len(mesa.pegaPecasAComprar()) != 0):
                peca = mesa.comprarPeca()
                self.adicionaPeca(peca)
                self.atualizaPecasJogaveis(mesa)
            else: break
        return

    #Elimina todas as peças da mão de um jogador.
    def limparMao(self):
        self.__mao = []
        self.__maoJogaveis = []

    #Indica se um jogador ganhou, ou seja, se a variável de controle do mesmo indica sua vitória ou não.
    def jaGanhou(self): return len(self.__mao) == 0

    #'Seta' se o jogador ganhou ou não a partida.
    def setaGanhou(self, bool):
        if (bool): self.__mao = []

    #Retorna o somatório de valores de todas as peças do jogador. Ambos os lados de uma peça são somados.
    def somatorioPecas(self):
        soma = 0
        for peca in self.__mao: soma += (peca.esq() + peca.dir())
        return soma

    #Incrementa a pontuação de um jogador de um valor passado por parâmetro.
    def somaPontos(self, soma): self.__pontos += soma

    #Retorna a qtd. de pontos acumulada até o momento do jogador.
    def pegaPontos(self): return self.__pontos

    #Método que coordena qual o tipo de método de jogar será chamado. Há diferentes métodos para cada um dos diferentes tipos
    # de jogadores existentes.
    def jogar(self, mesa, oponente):
        if (self.tipo == self.HUMANO): return self.jogarHumano(mesa, oponente)
        elif (self.tipo == self.EXPECTMM): return self.jogarExpectMM(mesa, oponente)
        elif (self.tipo == self.MCTS): return self.jogarMCTS(mesa, oponente)
        else: return self.jogarRandom(mesa, oponente)

    #Define a função 'jogar' para um jogador humano. Possibilita a escolha da peça a ser jogada e sua posição por um
    #jogador humano, que interage pelo console da aplicação.
    def jogarHumano(self, mesa, oponente):
        if self.__vezAtual == False: return
        self.atualizaPecasJogaveis(mesa)
        # Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa(mesa)
        #print("\n" + str(mesa))
        print("\n" + self.pecasJogaveis(mesa, self.__mao))
        print(self)
        if (len(self.pegaPecasJogaveis()) == 0):
            mesa.fechada = True
            self.setaJogou(False)
            print("J" + str(self.__ind) + " passou a vez.")
        else:
            escolhida = int(input("Qual peça deseja jogar? "))
            if (len(mesa.pegaTabuleiro()) != 0): pos = int(input("Em que posição? (0 p/ esquerda, 1 p/ direita) "))
            else: pos = 0
            peca = self.__mao.pop(escolhida - 1)
            adicionou = mesa.adicionarNaMesa(peca, pos)
            if (not adicionou):
                self.__mao.append(peca)
                self.jogarHumano(mesa, oponente)
            else: self.setaJogou(True)
            self.__maoJogaveis = []
            peca.ordem(len(mesa.pegaTabuleiro()))
        self.setaVez(False)
        oponente.setaVez(True)
        return

    #Define o método 'jogar' para um jogador controlado por inteligência artificial (Expectiminimax).
    def jogarExpectMM(self, mesa, oponente):
        if (self.__vezAtual == False): return
        #Atualiza as peças jogáveis por este jogador no estado atual do jogo.
        self.atualizaPecasJogaveis(mesa)
        #Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa(mesa)
        #print("\n" + str(mesa))
        print("\n" + self.pecasJogaveis(mesa, self.__mao))
        print(self)
        # Caso mesmo assim não seja possível conseguir uma peça jogável, pula esta rodada sem executar movimento.
        if (len(self.pegaPecasJogaveis()) == 0):
            self.setaJogou(False)
            print("J" + str(self.__ind) + " passou a vez.")
        else:
            #Escolhe a melhor jogada a ser feita dado o estado atual.
            estadoAtual = Estado(self, oponente, mesa, Estado.MAX)
            jogada = None
            # Se o tabuleiro está vazio, joga a peça possível.
            if (len(mesa.pegaTabuleiro()) == 0): jogada = [self.__maoJogaveis[0], 0]
            else: jogada = escolheJogada(estadoAtual)
            # Se uma jogada possível foi encontrada:
            if (jogada != None):
                # Executa a jogada.
                peca = jogada[0]
                pos = jogada[1]
                mesa.adicionarNaMesa(peca, pos)
                self.removePeca(mesa, peca)
                self.setaJogou(True)
                peca.ordem(len(mesa.pegaTabuleiro()))
            # Caso contrário, não executa qualquer jogada neste turno da aprtida.
            else:
                #mesa.fechada = True
                self.setaJogou(False)
                print("J" + str(self.__ind) + " passou a vez.")
        # Seta as variáveis para controle de quem é o jogador ativo atualmente no jogo.
        self.setaVez(False)
        oponente.setaVez(True)
        return

    # Define o método 'jogar' para um jogador controlado por inteligência artificial (Monte Carlo tree search).
    def jogarMCTS(self, mesa, oponente):
        if self.__vezAtual == False: return
        else:
            print("\n" + self.pecasJogaveis(mesa, self.__mao))
            print(self)
            #print("\n" + str(mesa))
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
                    print("J" + str(self.__ind) + " passou a vez.")
                    return
            estadoAtual = EstadoMCTS(self, oponente, mesa)
            noTeste = MonteCarloNo(estadoAtual)
            noTeste.expandir()
            if len(noTeste.filhos)>1:
                for i in range(100):
                    melhorfilho=noTeste.melhorFilho()
                    noTeste.gerarJogo(melhorfilho,False)
            melhorfilho=noTeste.melhorFilho()
            print(str(melhorfilho.UCT))
            self.removePeca(mesa,melhorfilho.estado.ultimaPecaJogada)
            mesa.adicionarNaMesa(melhorfilho.estado.ultimaPecaJogada, melhorfilho.estado.onde)
            self.setaJogou(True)
            self.__maoJogaveis = []
            melhorfilho.estado.ultimaPecaJogada.ordem(len(mesa.pegaTabuleiro()))
            #print("MCTS jogou a peça:"+ str(melhorfilho.estado.ultimaPecaJogada)+"na posição :"+ str(melhorfilho.estado.onde)+"\n" )
        self.setaVez(False)
        oponente.setaVez(True)
        return

    # Define o método 'jogar' para um jogador 'random'. Usado para testes. Realiza escolhas de jogadas sem obedecer nenhum
    # padrão específico de jogo, escolhendo apenas qualquer das possibilidades existentes para ele num dado momento.
    def jogarRandom(self, mesa, oponente):
        if self.__vezAtual == False: return
        self.atualizaPecasJogaveis(mesa)
        # Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa(mesa)
        #print("\n" + str(mesa))
        #print("\n" + self.pecasJogaveis(mesa, self.__mao))
        #print(self)
        if (len(self.pegaPecasJogaveis()) == 0): self.setaJogou(False)
            #print("J" + str(self.__ind) + " passou a vez.")
        else:
            possibilidades = self.possibilidadesJogaveis(mesa)
            escolhida = random.randint(0, len(possibilidades) - 1)
            peca = possibilidades[escolhida][0]
            pos = possibilidades[escolhida][1]
            self.removePeca(mesa, peca)
            mesa.adicionarNaMesa(peca, pos)
            self.setaJogou(True)
            peca.ordem(len(mesa.pegaTabuleiro()))
        self.setaVez(False)
        oponente.setaVez(True)
        return

    #Conta a ocorrência de um dado valor entre as peças do jogador corrente.
    def contarValor(self, valor):
        cont = 0
        for peca in self.__mao:
            if (peca.esq() == valor) or (peca.dir() == valor): cont += 1
        return cont
