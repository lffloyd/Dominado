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


#Define uma Peça de dominó e operações básicas associadas.

#Escrito por: Luiz Felipe, Vítor Costa

class Peca():
    #Construtor de classe define os valores para cada um dos lados da Peça.
    def __init__(self, nEsq=None, nDir=None):
        self.__nEsq = nEsq
        self.__nDir = nDir
        self.__ordem = -1

    def __str__(self): return "(" + str(self.__nEsq) +"|"+ str(self.__nDir) + ")"

    #Método de comparação entre Peças. Retorna se duas peças equivalem entre si de acordo com o método abaixo.
    def __cmp__(self, other): return self.__eq__(other)

    # Método de verificação de equivalência de Peças. Compara apenas se os números de duas Peças são iguais.
    def __eq__(self, other):
        # Checa se "other" é instância de Peça.
        if isinstance(other, self.__class__):
            if (self.__nEsq == other.esq()) and (self.__nDir == other.dir()): return True
            if (self.__nEsq == other.dir()) and (self.__nDir == other.esq()): return True
        return False

    #Getter para val. esquerdo da Peça.
    def esq(self): return self.__nEsq

    # Getter para val. direito da Peça.
    def dir(self): return self.__nDir

    def pegaOrdem(self): return self.__ordem

    def ordem(self, ordem): self.__ordem = ordem

    #Retorna a soma dos valores dos dois lados da Peça.
    def somatorio(self): return self.__nEsq + self.__nDir

    #Vira a Peça, trocando os valores dos lados. Usada para posicionar a instância de forma diferente no tabuleiro/mesa.
    def viraPeca(self):
        aux = self.__nEsq
        self.__nEsq = self.__nDir
        self.__nDir = aux
        return self

    #Verifica se a instância de Peça pode ser encaixada numa dada posição de um modo ou outro (virando-a).
    def ehJogavel(self, pos): return (self.__nEsq == pos) or (self.__nDir == pos)
