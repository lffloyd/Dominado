#Código principal de execução do jogo.

#Escrito por: Luiz Felipe, Vítor Costa

from classes_base.Mesa import *
from classes_base.Jogador import *
import os

#Limpa a tela de um prompt de comando. Usado para facilitar a visualização do jogo caso executado em um shell ou cmd.exe.
def limpaTela(sistema): os.system("cls" if (sistema == "nt") else "clear")

#Inicialização de objetos do jogo.
mesa = Mesa(28)
jogador1 = Jogador(1, Jogador.HUMANO)
jogador2 = Jogador(2, Jogador.HUMANO)
mesa.comecarJogo(jogador1, jogador2)

sistema = os.name

#Loop de jogo. É abortado caso um dos jogadores tenha vencido o jogo ou caso o jogo tenha "travado", i.e. caso ambos os
#jogadores não estejam conseguindo jogar no momento.
while ((not jogador1.jaGanhou()) and (not jogador2.jaGanhou())):
    limpaTela(sistema)
    jogador1.jogar(mesa, jogador2)
    jogador2.jogar(mesa, jogador1)
    if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break

#Atualização da pontuação do jogador vencedor.
if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())):
    jogador1.jaGanhou() if (jogador1.somatorioPecas() > jogador2.somatorioPecas()) else jogador2.jaGanhou()
if (jogador1.jaGanhou()): jogador1.somaPontos(jogador2.somatorioPecas())
elif (jogador2.jaGanhou()): jogador2.somaPontos(jogador1.somatorioPecas())

if jogador1.jaGanhou(): print("\n\n\nJogador 1 venceu: " + jogador1.pegaPontos() + "pts.")
else: print("\n\n\nJogador 2 venceu: " + jogador2.pegaPontos() + "pts.")