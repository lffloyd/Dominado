#Define a classe Expectiminimax, responsável por realizar uma busca por possibilidades de ações para o jogador IA.

#Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos

from classes_busca.Estado import *
from classes_base.Mesa import *
import copy

#Essa classe deveria ser estática, mas isso não deve existir em Pyhton. :-|
class Expectiminimax():
    def __init__(self):
        return

    #Retorna o resultado da execução de uma dada ação (i.e. inserção de peça) num dado estado (i.e. mesa/tabuleiro). Ou
    # seja, retorna o estado resultado da ação/jogada tomada.
    def resultado(estado, acao):
        novaMesa = copy.deepcopy(estado.mesa)
        novaMesa.adicionarNaMesa(acao.peca, acao.pos)
        return Estado(estado.jogador, estado.oponente, novaMesa)

    #Inicia o procedimento de busca Expectiminax.
    def decisaoMinimax(jogador, mesa, oponente): return

    def max(self): return

    def min(self): return