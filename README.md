# Primi Composti

Primi Composti is a game ideated and invented by eng. Luciano Murrone. 

"Our rules" a little bit more formalized

In this work we will consider the version of the game with just two players. In this version the deck is composed by all the cards from 2 to 25 (so 24 in total). The deck is shuffled and each player gets 12 cards.

At each round, one player at the time has to choose one of his cards and place it on the gameboard which is initially empty. Each player has two places in the gameboard where he can put the chosen card: one dedicated to prime cards and the other to composite cards. This way we can see that the gameboard is composed by 4 stacks, but we are only interested in the topmost card of each stack. The player who begins the game is the one with 2 in his deck (let's call him pA). We use this notation for the gameboard: [primes pA, composites pA, primes pB, composites pB].

At each round, if the card placed by the player is C, the score obtained card_s(C)+operation_s(C) where: 
* card_s(C) is equal to 1 if card is a composite number and 2 if card is prime. 
* operation_s(C) is equal to max{0, card_s(A)+card_s(B) where A#B=C, C!=A!=B!=C,  both A and B are visible cards in the gameboard, # is an operation in {+,-,x,/} }. 
In other words, the operation (if it exists) must involve 3 different cards (A#B=C) where C is the card that the player wants to place.

So for example if the gameboard is [2,-,3,-] and player A has the card 5 then by playing it he gets 6 points and then the gameboard will be [5,-,3-,-]. We do not allow for a#x=x since the operation does not involve 3 different cards so in the case [9,-,-,-], player B can play 3 but he only gets 2 points (and not 5).

Things we have deduced from the rules even though they are not 100% clear:
* "risultato di un’operazione aritmetica (+, -, x, /) tra __altre__ due CARD...": this implies that we cannot have a#x=x: all operations must involve 3 different cards (two operands and one result)
* the rules allow the case P=P#P: this implies that chosen a card to play: you first evaluate the score and then place it on the gameboard, so the operands can be chosen among the 4 visible cards before placing the new one

For our analysis it's useful to visualize: \
all the cards (24): [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]\
primes (9):         [2,3,5,7,11,13,17,19,23]\
composites (15):    [4,6,8,9,10,12,14,15,16,18,20,21,22,24,25]


## Installation of dependencies
The code is written in python. To run it, make sure to have all the dependencies installed, for example using ```conda```:
1. update the absolute path of your folder in the field  ```prefix``` of the file ```environment.yml```
2. run ```conda env create --file=environments.yml``` to create the conda environment
3. run ```conda activate gt_project_env``` to activate the environment



## Idee

* Generare l'albero e fare backward induction
    * Pro: troverei il NE
    * Contro: troppo grande l'albero
        * si può pensare ad un 'pruning' cioè non generare alcuni nodi se so già che non andranno a buon fine ma sembra non bastare (ad esempio se arrivo ad un punto dove la differenza di punteggio è maggiore del massimo di punti che può fare da quel momento in avanti un determinato player, allora so già chi vincerà e posso non espandere tutto)

* Rinunciare ad espandere tutto l'albero ma usare una qualche euristica per espandere pochi nodi ad ogni livello, ad esempio se il massimo punteggio che posso fare in quel turno è p, espando tutti i nodi che rappresentano le possibili giocate di carte che mi darebbero quel punteggio p (in generale saranno poche per turno). Non sono sicuro che abbia senso questa cosa perché non credo si arrivi ad avere un NE e non abbiamo nemmeno garanzia sull'ottimalità della partita. 

* Vedere se per case la soluzione greedy è un NE (secondo me in generale no).

* Fare un simulatore di una sola partita con delle carte da test

* Generare d livelli, risolvere con minmax e alfa beta pruning, riprendere il nodo finale e ricominciare. In questo modo non troviamo il NE (a meno che d=24, ma noi usiamo d piccolo) però è il modo che si usa per gli alberi enormi (scacchi).

# TODO

* greedy random policy on the simulation (and then run the cross policy simulation for a bit)

* understand if evaluate is needed or not in minimax
