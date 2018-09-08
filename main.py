from classes.Peca import *
from classes.Jogador import *
from classes.Mesa import *
from classes.Color import *

mesa = Mesa()
listaPecas, jogador1, jogador2 = mesa.comecarJogo()

print(jogador1)
print(jogador2)

jogador1.jogar(mesa)
jogador2.jogar(mesa)

print(mesa)
print(jogador1)