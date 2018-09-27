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


#Código principal de execução do jogo.

#Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos.

from classes_base.Mesa import *
from classes_base.Jogador import *
import os

#Limpa a tela de um prompt de comando. Usado para facilitar a visualização do jogo caso executado em um shell ou cmd.exe.
def limpaTela(sistema): os.system("cls" if (sistema == "nt") else "clear")

sistema = os.name

def gameLoop(mesa, jogador1, jogador2):
    empatou = 0
    #Inteiro que indicará o total de repetições do jogo obedecendo as configurações definidas no menu inicial que será feito.
    n = int(input("Repetições do cenário: "))
    if (n <= 0): return
    for i in range(n):
        #Inicializa mesa e jogadores (no que se refere às peças).
        mesa.comecarJogo(jogador1, jogador2)
        # Loop de jogo. É abortado caso um dos jogadores tenha vencido o jogo ou caso o jogo tenha "travado", i.e.
        # caso ambos os jogadores não estejam conseguindo jogar no momento.
        while ((not jogador1.jaGanhou()) and (not jogador2.jaGanhou())):
            # limpaTela(sistema)
            print(mesa)
            aleatorio = random.randint(0,1)
            if(aleatorio == 0):
                jogador1.jogar(mesa, jogador2)
                if len(jogador1.pecas()) == 0: break
                print(mesa)
                jogador2.jogar(mesa, jogador1)
                if len(jogador2.pecas()) == 0: break
            else:
                jogador2.jogar(mesa, jogador1)
                if len(jogador2.pecas()) == 0: break
                print(mesa)
                jogador1.jogar(mesa, jogador2)
                if len(jogador1.pecas()) == 0: break
            if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break
        # Atualização da pontuação do jogador vencedor após a finalização de uma partida.
        if jogador1.somatorioPecas() > jogador2.somatorioPecas():
            jogador2.somaPontos(jogador1.somatorioPecas())
            jogador2.vitorias = jogador2.vitorias + 1
            print("\n\n\nJ2 venceu: " + str(jogador2.pegaPontos()) + "pts.")
        elif jogador1.somatorioPecas() < jogador2.somatorioPecas():
            jogador1.somaPontos(jogador2.somatorioPecas())
            jogador1.vitorias = jogador1.vitorias + 1
            print("\n\n\nJ1 venceu: " + str(jogador1.pegaPontos()) + "pts.")
        elif jogador1.somatorioPecas() == jogador2.somatorioPecas():
            empatou += 1
    #Ao fim do laço de repetição de cenário, mostra algumas estatísticas básicas obtidas pelas simulações, como porcentagem
    # de vitórias para cada jogador.
    print("J1 venceu: " + str(jogador1.vitorias) + "/" + str(n) + ",\tPorcent.: " + str((jogador1.vitorias / n) * 100) +
          "%,\tPts. totais: " + str(jogador1.pegaPontos()))
    print("J2 venceu: " + str(jogador2.vitorias) + "/" + str(n) + ",\tPorcent.: " + str((jogador2.vitorias / n) * 100) +
          "%,\tPts. totais: " + str(jogador2.pegaPontos()))
    print("J1 e J2 empataram: " + str(empatou) + " vezes" + ",\tPorcent.: " + str((empatou / (jogador1.vitorias+jogador2.vitorias))
                                                                                  * 100) + "%")

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
    #Usuário deve digitar o inteiro correspondente ao início de uma das strings a seguir para escolher a referida opção
    # de jogo/simulação.
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
