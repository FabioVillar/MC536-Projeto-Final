# Lab08 - Modelo Lógico e Análise de Dados em Grafos
Estrutura de pastas:
```
├── README.md  <- arquivo apresentando a tarefa
│
└── images     <- arquivos de imagem usados na tarefa
```
# Equipe Akers - Akers
* Arthur Cemim Baia -  213259
* Fábio Santos Villar - 234135
* José Augusto Nascimento Afonso Marcos - 200025
## Modelo Lógico Combinado do Banco de Dados de Grafos

![](images/modelo_logico.png)

A partir do modelo combinado, podemos fazer uma operação de projeção entre 2 elementos: Jogadoras e Seleções. O intuito disso é montar um grafo cuja associação entre eles é determinada por uma variável chamada desempenho, ou seja, o desempenho do jogador perante à uma seleção. Cada desempenho é determinado por diversas características contra a seleção alvo, como número de minutos jogados, número de gols marcados, número de assistências, expulsões e cartões amarelos, ou seja, por uma função. A partir do desempenho, vamos calcular uma distância (float) entre a jogadora e a seleção dentro do grafo, normalizada por exemplo entre 0 e 1, onde 1 corresponde ao desempenho mínimo.

![](images/modelo_distancia.png)

## Perguntas de Pesquisa/Análise Combinadas e Respectivas Análises

### Pergunta/Análise 1
  * Quais jogadoras tem melhor desempenho contra a seleção X?
    * A partir de uma análise de centralidades podemos estabelecer vínculos entre cada seleção e as jogadoras mais próximas a elas.

### Pergunta/Análise 2
  * Quais são as jogadoras com melhor performance total?
    * Jogadoras que atraem várias seleções pra si, ou seja, que tem baixas distâncias contra várias formarão clusteres no grafo, onde podemos fazer análises de comunidades.

### Pergunta/Análise 3
  * Qual a relação entre as jogadoras baseada em sua posição no grafo?
    * Podemos estabelecer conexões entre jogadoras próximas. Por exemplo, podemos conferir se todas fazem parte de um mesmo país, se possuem uma posição em comum, se já foram campeãs do torneio, etc. Para isso, podemos fazer uma análise de comunidades.
