# Primi Composti

## Game description
"Primi Composti" is a strategy card game that can be played by 2 to 6 people.
The game is presented in two possible versions (denoted as 1 and 2), both requiring the use of a deck of cards with numbers from 2 to 73, of which only the smallest $12\cdot \mathcal{N}$ will be used, where $\mathcal{N}$ is the number of players. For the sake of simplicity, we will consider only the two-player case, meaning that only cards 2 to 25 will be played. 

The game board hosts two (initially empty) stacks of cards for each player, one for cards corresponding to prime numbers and one for composite ones. Only the topmost cards of each stack are considered to be in active play.
The game starts after the appropriate number of cards has been shuffled and equally distributed among the players, at which point the first move is made by the player holding the $2$ card (from now on $player 1$ or $P1$).
The two versions of the game are played with similar but non-identical rules, which we will describe separately.

### Version 1
This version features a scoreboard on which players track the points they will accumulate during the course of the game with some markers.
Each card is worth a certain amount of points $VALUE(Card)$ that is either $1$ ($COMPOSITE\_SCORE$) or $2$ ($PRIME\_SCORE$) depending on whether the card is composite or prime. 

Each move consists of a player choosing a card $C$ from their hand. If $C$ is the result of a mathematical operation between exactly two cards  $A$ and $B$ among the visible ones (that can be at most four) the player will earn $VALUE(A) + VALUE(B) + VALUE(C)$ points. $C$ must strictly be the result, with $A$ and $B$ being the operands and the valid operations are addition, multiplication, subtraction and division.
If $C$ is not the result of a valid operation, then the player only gets $VALUE(C)$ points. 

After having computed the points earned (and moved their marker on the scoreboard accordingly), the player places $C$ on the corresponding stack (the one of their primes or of their composites).
The game ends when all players have played their entire hand, at which point the one with the most points is declared the winner.

Of course the physical scoreboard with the markers is just a marketing ploy to make the tabletop version more visually competitive but in reality we can represent the exact same thing with two numerical values, one for the score of each player. Another useful and analogous representation of the score can be to compute (and update each time) the difference of the scores between the two players. This is particularly close to what the _minimax_ algorithm does. 

### Version 2
This version is played without a scoreboard, as the stacks themselves keep track of the score. 

As for version 1, each move consists of a player choosing a card $C$ and searching for a valid operation that has as operands exactly two visible cards $A$ and $B$ and result $C$ but now when they spot this operation they have to remove $A$ and $B$ from the stack they're on and place them on their own side of the board, after which they will place $C$. Of course if $A$ or $B$ are already on the current player's decks, they just need to place $C$ but if they are not then the player is possibly "stealing" some cards from the opponent's stacks. 

The game still ends when all cards are finished, the winner being the player that has the highest sum $VALUE$ of the cards on their stacks.

## Installation of dependencies
The code is written in python. To run it, make sure to have all the dependencies installed, for example using `conda`:

1. update the absolute path of your folder in the field `prefix` of the file `environment.yml`
2. run `conda env create --file=environments.yml` to create the conda environment
3. run `conda activate gt_project_env` to activate the environment

## About the code
We provide 6 different executable python files that you can run simply from you terminal:
* `human_vs_cpu_1.py` and `human_vs_cpu_2.py` to play a match of the game 1 and 2 against the computer. These programs ask you if you want to play as player 1 or 2 and then which policy you want the computer to play with. You can find the specifications of the policies in `utilities/policies.py`. When playing against `minimax_6` you may need to wait few seconds for the first moves played by the computer. According to the policy you choose for the computer, you may face different levels of difficulty:
    * very easy mode: simple policies (`asc`, `rand`, `desc`)
    * easy mode: greedy policies (`greedy_asc`, `greedy_rand`, `greedy_desc`) and lower minimax (`minimax_2`, `minimax_3`)
    * normal mode: `minimax_4`
    * hard mode: `minimax_5`
    * impossible mode: `minimax_6`
* `run_simulation_1.py` and `run_simulation_1.py` to run a number of matches with each combination of the policies specified.
* `run_aplhabeta_1.py` and `run_aplhabeta_2.py` to run the resolution of a game where each player has 6 cards using the alphabeta pruning algorithm to find the SPE.
