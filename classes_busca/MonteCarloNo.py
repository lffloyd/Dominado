#Define a classe MonteCarloNo, responsável por descrever o um nó no algoritmo de busca 'Monte-Carlo tree search'.

#Escrito por: Vítor Costa.

import copy

class MonteCarloNo:
    def __init__(self, estado, pai = None):
        self.estado = estado
        self.pai = pai
        self.filhos = []

    def __str__(self):
        x = 0
        for i in self.filhos:
            print("\n\nFilho" + str(x))
            print(i.estado.mesa)
            x+=1
        return "\nQtd de Filhos:" + str(len(self.filhos))

    def expandir(self):
        print("AQUIII" + str(len(self.estado.jogador.pegaPecasJogaveis())))
        for peca in self.estado.jogador.pegaPecasJogaveis():
            for i in range(0,2):
                novoEstado = copy.deepcopy(self.estado)
                adicionou = novoEstado.mesa.adicionarNaMesa(peca, i)
                novoNo = MonteCarloNo(novoEstado, self)
                novoEstado.jogador.setaVez(False)
                if(adicionou):
                    self.filhos.append(novoNo)

    def melhorFilho(self):
        for i in self.filhos:
            return

    def foiTotalmenteExpandido(self):
        if(self.estado.jogador.ehSuaVez() == True):
            return len(self.filhos) == len(self.estado.jogador.pegaPecasJogaveis())
        else:
            return len(self.filhos) == len(self.estado.oponente.pegaPecasJogaveis())

    #TEM QUE FAZER ESSA FUNÇÃO DO ESTADO TERMINAL
    def simular(self, no):
        while(no.estado.ehEstadoTerminal() != True):
            no.expandir()