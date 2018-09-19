#Código principal de execução do jogo.

#Escrito por: Luiz Felipe, Vítor Costa

from classes_base.Mesa import *
from classes_base.Jogador import *
import os

#Limpa a tela de um prompt de comando. Usado para facilitar a visualização do jogo caso executado em um shell ou cmd.exe.
def limpaTela(sistema): os.system("cls" if (sistema == "nt") else "clear")

sistema = os.name

def gameLoop(mesa, jogador1, jogador2):
    mesa.comecarJogo(jogador1, jogador2)
    #Loop de jogo. É abortado caso um dos jogadores tenha vencido o jogo ou caso o jogo tenha "travado", i.e. caso ambos os
    #jogadores não estejam conseguindo jogar no momento.
    while ((not jogador1.jaGanhou()) and (not jogador2.jaGanhou())):
        #limpaTela(sistema)
        jogador1.jogar(mesa, jogador2)
        jogador2.jogar(mesa, jogador1)
        if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break
    #Atualização da pontuação do jogador vencedor.
    if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())):
        jogador1.jaGanhou() if (jogador1.somatorioPecas() > jogador2.somatorioPecas()) else jogador2.jaGanhou()
    if (jogador1.jaGanhou()): jogador1.somaPontos(jogador2.somatorioPecas())
    elif (jogador2.jaGanhou()): jogador2.somaPontos(jogador1.somatorioPecas())
    if jogador1.jaGanhou(): print("\n\n\nJogador 1 venceu: " + str(jogador1.pegaPontos()) + "pts.")
    else: print("\n\n\nJogador 2 venceu: " + str(jogador2.pegaPontos()) + "pts.")


#Menu inicial do jogo.
def menu():
    print("\n***************************Dominado v 0.01***************************")
    print("(J)ogar")
    print("(S)air")
    escolha = input()
    if (escolha == "J") or (escolha == "j"):
        # Escolha de modos de jogo.
        print("0. Random vs. Random")
        print("1. Humano vs. Expectiminimax")
        print("2. Humano vs. MCTS")
        print("3. MCTS vs. Expectiminimax")
        escolha = int(input())
        jogador1 = None
        jogador2 = None
        # Inicialização de objetos do jogo.
        if (escolha == 0):
            jogador1 = Jogador(1, Jogador.RANDOM)
            jogador2 = Jogador(2, Jogador.RANDOM)
        if (escolha > 0) and (escolha < 3):
            jogador1 = Jogador(1, Jogador.HUMANO)
            jogador2 = (Jogador(2, Jogador.EXPECTMM) if (escolha == 1) else Jogador(2, Jogador.MCTS))
        if (escolha == 3):
            jogador1 = Jogador(1, Jogador.MCTS)
            jogador2 = Jogador(2, Jogador.EXPECTMM)
        print("\n")
        mesa = Mesa(28)
        gameLoop(mesa, jogador1, jogador2)
        escolha = input("Jogar novamente? S|N")
        if (escolha == "S") or (escolha == "s"): menu()

menu()
