#Código principal de execução do jogo.

#Escrito por: Luiz Felipe, Vítor Costa.

from classes_base.Mesa import *
from classes_base.Jogador import *
import os

#Limpa a tela de um prompt de comando. Usado para facilitar a visualização do jogo caso executado em um shell ou cmd.exe.
def limpaTela(sistema): os.system("cls" if (sistema == "nt") else "clear")

sistema = os.name

def gameLoop(mesa, jogador1, jogador2):
    n = int(input("Repetições do cenário: "))
    if (n <= 0): return
    for i in range(n):
        mesa.comecarJogo(jogador1, jogador2)
        #Loop de jogo. É abortado caso um dos jogadores tenha vencido o jogo ou caso o jogo tenha "travado", i.e. caso ambos os
        #jogadores não estejam conseguindo jogar no momento.
        while (True):
            # limpaTela(sistema)
            jogador1.jogar(mesa, jogador2)
            if len(jogador1.pecas()) == 0 : break
            if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break
            jogador2.jogar(mesa, jogador1)
            if len(jogador2.pecas()) == 0: break
            if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break
        #Atualização da pontuação do jogador vencedor.
        if jogador1.somatorioPecas()>jogador2.somatorioPecas():
            jogador1.somaPontos(jogador1.somatorioPecas())
            jogador1.vitorias=jogador1.vitorias +1
            print("\n\n\nJ1 venceu: " + str(jogador1.pegaPontos()) + "pts.")
        elif jogador1.somatorioPecas()<jogador2.somatorioPecas():
            jogador2.somaPontos(jogador2.somatorioPecas())
            jogador2.vitorias = jogador2.vitorias + 1
            print("\n\n\nJ2 venceu: " + str(jogador2.pegaPontos()) + "pts.")
        #else:
         #   jogador1.vitorias=jogador1.vitorias +1
          #  jogador2.vitorias = jogador2.vitorias + 1

    print("J1 venceu: " + str(jogador1.vitorias) + "/" + str(n) + ",\tPorcent.: " + str((jogador1.vitorias/n)*100) +
          "%,\tPts. totais: " + str(jogador1.pegaPontos()))
    print("J2 venceu: " + str(jogador2.vitorias) + "/" + str(n) + ",\tPorcent.: " + str((jogador2.vitorias/n)*100) +
          "%,\tPts. totais: " + str(jogador2.pegaPontos()))


#Menu inicial do jogo.
def menu():
    print("***************************Dominado v 0.01***************************")
    print("(J)ogar")
    print("(S)air")
    escolha = input()
    if (escolha == "J") or (escolha == "j"): escolherModoDeJogo()

# Seleção de modos de jogo.
def escolherModoDeJogo():
    print("\n\n\n\n\n")
    print("0. Random vs. Random")
    print("1. Random vs. Expectiminimax")
    print("2. Random vs. MCTS")
    print("3. Humano vs. Expectiminimax")
    print("4. Humano vs. MCTS")
    print("5. MCTS vs. Expectiminimax")
    escolha = int(input())
    jogador1 = None
    jogador2 = None
    # Inicialização de objetos do jogo.
    if (escolha <= 0) or (escolha > 5):
        jogador1 = Jogador(1, Jogador.RANDOM)
        jogador2 = Jogador(2, Jogador.RANDOM)
    if (escolha > 0) and (escolha < 3):
        jogador1 = Jogador(1, Jogador.RANDOM)
        jogador2 = (Jogador(2, Jogador.EXPECTMM) if (escolha == 1) else Jogador(2, Jogador.MCTS))
    if (escolha > 2) and (escolha < 5):
        jogador1 = Jogador(1, Jogador.HUMANO)
        jogador2 = (Jogador(2, Jogador.EXPECTMM) if (escolha == 3) else Jogador(2, Jogador.MCTS))
    if (escolha == 5):
        jogador1 = Jogador(1, Jogador.MCTS)
        jogador2 = Jogador(2, Jogador.EXPECTMM)
    print("\n")
    mesa = Mesa(28)
    gameLoop(mesa, jogador1, jogador2)
    escolha = input("Jogar novamente? S|N")
    if (escolha == "S") or (escolha == "s"): escolherModoDeJogo()
    else: return

menu()