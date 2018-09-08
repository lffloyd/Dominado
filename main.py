from classes.Mesa import *
import os

def limpaTela(sistema): os.system("cls" if (sistema == "nt") else "clear")

mesa = Mesa(28)
jogador1 = Jogador(1)
jogador2 = Jogador(2)
mesa.comecarJogo(jogador1, jogador2)

sistema = os.name

while ((not jogador1.jaGanhou()) and (not jogador2.jaGanhou())):
    #limpaTela(sistema)
    jogador1.jogar(mesa, jogador2)
    jogador2.jogar(mesa, jogador1)
    if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())): break

if ((not jogador1.jogouRodada()) and (not jogador2.jogouRodada())):
    jogador1.jaGanhou() if (jogador1.somatorioPecas() > jogador2.somatorioPecas()) else jogador2.jaGanhou()
if (jogador1.jaGanhou()): jogador1.somaPontos(jogador2.somatorioPecas())
elif (jogador2.jaGanhou()): jogador2.somaPontos(jogador1.somatorioPecas())

if jogador1.jaGanhou(): print("\n\n\nJogador 1 venceu: " + jogador1.pegaPontos() + "pts.")
else: print("\n\n\nJogador 2 venceu: " + jogador2.pegaPontos() + "pts.")