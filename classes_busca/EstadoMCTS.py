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


#Define a classe EstadoMCTS, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com o algoritmo de busca 'Monte-Carlo tree search'. Observar que a classe tem diferenças em
#relação a classe 'Estado'.

#Escrito por: Vítor Costa, Renato Bastos.

import copy

class EstadoMCTS():
    #Construtor de classe. Define atributos associados ao estado global de uma partida.
    def __init__(self, jogador, oponente, mesa):
        self.jogador = jogador
        self.oponente = oponente
        self.mesa = mesa
        self.qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.qtdPecasOponente = len(self.oponente.pecas())
        self.probabilidade = 0
        self.ultimaPecaJogada = None
        self.onde=None

    def __str__(self):
        resp=""
        resp+=str(self.jogador)+ "\n"
        resp += str(self.oponente)+ "\n"
        resp += str(self.mesa)+ "\n"
        return resp

    #funcao que compara se dois estados são iguais, ou seja, possui as mesmas peças em ambos jogadores e na mesa
    def comparar(self,estado2):
        for peca in self.jogador.pecas():
            achou=False
            for peca2 in estado2.jogador.pecas():
                if peca==peca2:
                    achou=True
                    break
            if achou==False: return False
        for peca in self.oponente.pecas():
            igual=False
            for peca2 in estado2.oponente.pecas():
                if peca==peca2:
                    igual=True
                    break
            if igual==False: return False
        onde=0
        for pecaTab in self.mesa.pegaTabuleiro():
            pecaTab2=estado2.mesa.pegaTabuleiro()[onde]
            if not pecaTab==pecaTab2: return False
            onde+=1
        return True

    #Indica se um estado terminal foi atingido
    def ehEstadoFinal(self):
        #print("----Teste no ehEstadoFinal()")
        #print(self)
        #print("Jogador:" + str(self.jogador.jogouRodada()))
        #print("Oponente:" + str(self.oponente.jogouRodada()))
        #print("--------Fim do teste -------\n")
        if (not self.jogador.jogouRodada() and not self.oponente.jogouRodada() and len(self.mesa.pegaPecasAComprar())==0) \
                or (len(self.jogador.pecas())==0 or len(self.oponente.pecas())==0) :
            return True
        return False
