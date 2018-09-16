from classes_busca.Estado import *
from classes_base.Mesa import *
import copy

class Expectiminimax():
    def __init__(self):
        return

    def resultado(estado, acao):
        novaMesa = copy.deepcopy(estado.mesa)
        novaMesa.adicionarNaMesa(acao.peca, acao.pos)
        return Estado(estado.jogador, estado.oponente, novaMesa)

    def decisaoMinimax(self): return

    def max(self): return

    def min(self): return