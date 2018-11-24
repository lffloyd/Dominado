# Dominado
I.A. utilizando estratégias de busca ("Expectiminimax" e "Monte-Carlo tree search") para jogar dominó com dois jogadores

## Procedimentos

Os procedimentos a seguir descrevem os passos necessários para execução do programa "Dominado", um jogo de dominó implementando algoritmos de busca para inteligência artificial.

### Pré-requisitos

O programa foi testado nos sistemas operacionais Windows e Ubuntu 16.04 sem diferenças de execução entre ambos.
Para executar o programa é necessário possuir uma versão do Python instalada. Recomendamos:

* [Python >= 3.5.2](https://www.python.org/downloads/) - O programa foi testado na versão [3.5.2](https://www.python.org/downloads/release/python-352/).

### Executando

O arquivo a ser executado para iniciar o programa encontra-se na raiz do projeto e chama-se 'main.py'.

Ao ser iniciado, o jogo exibirá o seguinte menu:

```
***************************Dominado v 0.01***************************
(J)ogar
(S)air
```

Para o qual deve-se digitar 'j' ou 'J' para iniciar uma partida e 's' ou 'S' para finalizar o programa. O menu abaixo será exibido em seguida caso escolha jogar:

```
0. Random vs. Random
1. Random vs. Expectiminimax
2. Random vs. MCTS
3. Humano vs. Expectiminimax
4. Humano vs. MCTS
5. MCTS vs. Expectiminimax
```
Nesse momento, deve-se escolher a forma de jogo. Todas as formas de jogo envolvem uma partida de dois jogadores, oponentes entre si. O dígito inicial em cada uma das linhas será o valor que deve ser digitado no teclado para que a opção referida seja escolhida.
Por exemplo, digitando-se 0 no teclado, uma partida de dois jogadores 'Random' será executada do início ao fim. Um jogador 'Random' escolhe aleatoriamente os movimentos a serem executados. Já os jogadores 'Expectiminimax' e 'MCTS' implementam as estratégias de busca de mesmo nome para decidirem suas jogadas, sendo ambos I.A.. O jogador 'Humano' disponibiliza a um usuário que jogue o jogo interativamente opondo-se a uma das duas implementações de inteligência artificial citadas.

Ainda, para facilitar a execução de testes, pode-se dizer quantas simulações do cenário escolhido serão feitas. Após a etapa anterior será exibida uma requisição por esse número de simulações:

```
Repetições do cenário:
```

Aqui deve-se digitar um valor inteiro indicando o número de simulações. Por exemplo, 1 executa apenas uma partida sob as circunstâncias definidas e exibe algumas estatísticas sobre essa simulação ao seu fim. Valores maiores executam mais simulações.

## Autores

* **Luiz Felipe de Melo** - *Implementação básica do jogo e métodos de busca/I.A.* - [lffloyd](https://github.com/lffloyd)
* **Vítor Costa** - *Implementação básica do jogo e métodos de busca/I.A.* - [vitorhardoim](https://github.com/vitorhardoim)
* **Renato Bastos** - *Implementação de métodos de busca/I.A.* - [RenatoBastos33](https://github.com/RenatoBastos33)

Veja a lista de [contribuidores](https://github.com/lffloyd/Dominado/contributors) participantes no projeto.

## Licença

Projeto licenciado sob a licença MIT - leia [LICENSE.md](https://github.com/lffloyd/Dominado/blob/rev0.1/LICENSE) para maiores detalhes.

