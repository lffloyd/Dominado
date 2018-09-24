#Define a classe Jogador e seus atributos associados.

#Escrito por: Vítor Costa, Luiz Felipe

import random
from classes_base.Cor import *
from classes_base.Peca import *
from classes_busca.Expectiminimax import *
from classes_busca.Estado import *
from classes_busca.EstadoMCTS import *
from classes_busca.MonteCarloNo import *

class Jogador():
    #Constantes para identificação do tipo de jogador.
    RANDOM = 3
    MCTS = 2
    EXPECTMM = 1
    HUMANO = 0

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
        elif (self.tipo == self.EXPECTMM): self.tipoStr = "MCTS"
        else: self.tipoStr = "RANDOM"

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
            indice = self.__mao.index(peca)
            self.__mao.pop(indice)
            self.atualizaPecasJogaveis(mesa)

    def removePeca2(self, mesa, peca):
        #print("Caralho: " + str(peca))
        resp = ""
        for p in self.__mao: resp += str(p)
        #print("removePeca2(): " + resp)
        if (len(self.__mao) != 0):
            self.__mao.remove(peca)
            self.atualizaPecasJogaveis(mesa)
            resp = ""
            for p in self.__mao: resp += str(p)
            #print("removePeca2(): " + resp)

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
    #Nenhum cálculo mais elaborado é executado ainda para a probabilidade.
    def possibilidadesJogaveis(self, mesa):
        possibilidades = []
        probabilidade = 0
        self.atualizaPecasJogaveis(mesa)
        if (len(mesa.pegaTabuleiro()) == 0):
            for peca in self.__maoJogaveis: possibilidades.append([peca, 0, probabilidade])
        else:
            esq, dir = mesa.extremos()
            for peca in self.__maoJogaveis:
                if peca.ehJogavel(esq) and peca.ehJogavel(dir):
                    possibilidades.append([peca, 0, probabilidade])
                    possibilidades.append([peca.viraPeca(), 1, probabilidade])
                else: possibilidades.append([peca, (0 if (peca.ehJogavel(esq)) else 1), probabilidade])
            #Distribui uma probabilidade equivalente para cada uma das possíveis escolhas a serem feitas.
            probabilidade = 1 / len(possibilidades)
            for jogada in possibilidades: jogada[2] = probabilidade
        return possibilidades

    def compraDaMesa(self, mesa):
        self.atualizaPecasJogaveis(mesa)
        #i = 0
        while (len(self.pegaPecasJogaveis()) == 0):
            if (len(mesa.pegaPecasAComprar()) != 0):
                peca = mesa.comprarPeca()
                self.adicionaPeca(peca)
                self.atualizaPecasJogaveis(mesa)
                #i += 1
            else: break
        #if (i != 0): print("J" + str(self.__ind) + " comprou " + str(i) + " peça(s).")
        return

    def compraDaMesa2(self, mesa):
        self.atualizaPecasJogaveis(mesa)
        #i = 0
        while (len(self.pegaPecasJogaveis()) == 0):
            if (len(mesa.pegaPecasAComprar()) != 0):
                peca = mesa.comprarPeca()
                self.adicionaPeca(peca)
                self.atualizaPecasJogaveis(mesa)
                #i += 1
            else: break
        #if (i != 0): print("J" + str(self.__ind) + " comprou " + str(i) + " peça(s).")
        return

    #Elimina todas as cartas de um jogador.
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

    #Incrementa a pontuação de um jogador.
    def somaPontos(self, soma): self.__pontos += soma

    #Retorna a qtd. de pontos acumulada até o momento do jogador.
    def pegaPontos(self): return self.__pontos

    #Método que coordena cada uma das jogadas do jogador. Até o momento, necessita da interação de um humano para realizar
    # uma jogada. Aguarda até que o jogador escolha uma peça válida para encaixar ou até que não possua nenhuma peça válida
    #para jogar, passando a vez a seu oponente.
    def jogar(self, mesa, oponente):
        #if (not (self.tipo == self.HUMANO)): print(self)
        if (self.tipo == self.HUMANO): return self.jogarHumano(mesa, oponente)
        elif (self.tipo == self.EXPECTMM): return self.jogarIA(mesa, oponente)
        elif (self.tipo == self.MCTS): return self.jogarMCTS(mesa, oponente)
        else: return self.jogarRandom(mesa, oponente)

    #Define a função 'jogar' para um jogador humano. Possibilita a escolha da peça a ser jogada e sua posição por um
    #jogador humano, que interage pelo console da aplicação.
    def jogarHumano(self, mesa, oponente):
        if self.__vezAtual == False: return
        self.atualizaPecasJogaveis(mesa)
        # Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa(mesa)
        print("\n" + str(mesa))
        print("\n" + self.pecasJogaveis(mesa, self.__mao))
        print(self)
        if (len(self.pegaPecasJogaveis()) == 0):
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

    #Defina o método 'jogar' para um jogador controlado por inteligência artificial (Expectiminimax ou
    #Monte-Carlo tree search).
    def jogarIA(self, mesa, oponente):
        if (self.__vezAtual == False): return
        #Atualiza as peças jogáveis por este jogador no estado atual do jogo.
        self.atualizaPecasJogaveis(mesa)
        #Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa2(mesa)
        print("\n" + str(mesa))
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
                #if (peca in self.__mao): print(str(peca)+" está na mão")
                self.removePeca2(mesa, Peca(peca.esq(), peca.dir()))
                #resp = ""
                #for peca in self.__mao: resp += str(peca)
                #print(".remove(): " + resp)
                #self.__mao.remove(peca)
                #self.atualizaPecasJogaveis(mesa)
                #resp = ""
                #for peca in self.__mao: resp += str(peca)
                #print(".remove(): " + resp)
                self.setaJogou(True)
                peca.ordem(len(mesa.pegaTabuleiro()))
            # Caso contrário, não executa qualquer jogada neste turno da aprtida.
            else:
                self.setaJogou(False)
                print("J" + str(self.__ind) + " passou a vez.")
        # Seta as variáveis para controle de quem é o jogador ativo atualmente no jogo.
        self.setaVez(False)
        oponente.setaVez(True)
        return

    def jogarRandom(self, mesa, oponente):
        if self.__vezAtual == False: return
        self.atualizaPecasJogaveis(mesa)
        # Caso não existam peças jogáveis em sua mão, executa a compra de peças enquanto for possível.
        if (len(self.pegaPecasJogaveis()) == 0): self.compraDaMesa2(mesa)
        print("\n" + str(mesa))
        print("\n" + self.pecasJogaveis(mesa, self.__mao))
        print(self)
        if (len(self.pegaPecasJogaveis()) == 0):
            self.setaJogou(False)
            print("J" + str(self.__ind) + " passou a vez.")
        else:
            possibilidades = self.possibilidadesJogaveis(mesa)
            escolhida = random.randint(0, len(possibilidades) - 1)
            peca = possibilidades[escolhida][0]
            pos = possibilidades[escolhida][1]
            self.__maoJogaveis.remove(peca)
            self.__mao.remove(peca)
            adicionou = mesa.adicionarNaMesa(peca, pos)
            self.setaJogou(True)
            self.__maoJogaveis = []
            peca.ordem(len(mesa.pegaTabuleiro()))
        self.setaVez(False)
        oponente.setaVez(True)
        return

    def jogarMCTS(self, mesa, oponente):
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
                estadoAtual = EstadoMCTS(self, oponente, mesa)
                noTeste = MonteCarloNo(estadoAtual)
                noTeste.expandir()
                print(noTeste)
                escolhida = int(input("Qual peça deseja jogar? "))
                if (len(mesa.pegaTabuleiro()) != 0): pos = int(input("Em que posição?(0 p/ esquerda, 1 p/ direita) "))
                else: pos = 0
                peca = self.__mao.pop(escolhida - 1)
                adicionou = mesa.adicionarNaMesa(peca, pos)
                if (not adicionou):  self.__mao.append(peca)
                else: self.setaJogou(True)
                self.__maoJogaveis = []
                peca.ordem(len(mesa.pegaTabuleiro()))
            self.setaVez(False)
            oponente.setaVez(True)
            return

    def contarValor(self, valor):
        cont = 0
        for peca in self.__mao:
            if (peca.esq() == valor) or (peca.dir() == valor): cont += 1
        return cont