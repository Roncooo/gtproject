# Primi Composti

## Game description
"Primi Composti" is a strategy card game that can be played by 2 to 6 people.
The game is presented in two possible versions (denoted as 1 and 2), both requiring the use of a deck of cards with numbers from 2 to 73, of which only the smallest $12\cdot \mathcal{N}$ will be used, where $\mathcal{N}$ is the number of players.
For the sake of simplicity, we will consider only the two-player case, meaning that only cards 2 to 25 will be played.
The game board hosts two (initially empty) stacks of cards for each player, one for cards corresponding to prime numbers and one for composite ones. Only the topmost cards of each stack are considered to be in active play.
The game starts after the appropriate number of cards has been shuffled and equally distributed among the players, at which point the first move is made by the player holding the $2$ card (from now on $player 1$ or $P1$).
The two versions of the game are played with similar but non-identical rules, which we will describe separately.
### Version 1
This version features a scoreboard for players to track the points they will accumulate during the course of the game.
Each move consists of a player placing a card $C$ from their hand onto their corresponding stack (prime or composite). This nets them $VALUE(C)$ points, where $VALUE(C)$ is either $1$ ($COMPOSITE\_SCORE$) or $2$ ($PRIME\_SCORE$) depending on whether $C$ is composite or prime. Additionally, if the played card is the result of a mathematical operation between two other cards $A$ and $B$ in active play (the operations being addition, multiplication, subtraction or division) the player will earn an additional reward equal to $VALUE(A) + VALUE(B)$. $C$ must strictly be the result, with $A$ and $B$ being the operands. The game ends when all players have played their entire hand, at which point the one with the most points is declared the winner.
### Version 2
This version is played without a scoreboard, as the stacks themselves keep track of the score. The players still play a card $C$ on the corresponding stack per turn, but when the current player spots a valid operation involving two other active cards $A$ and $B$ they must remove them from the stack they're on and place them on their own side of the board, after which they will place $C$. The game still ends when all cards are finished, the winner being the player that has the highest sum $VALUE$ of the cards on their stacks.

## Installation of dependencies
The code is written in python. To run it, make sure to have all the dependencies installed, for example using `conda`:

1. update the absolute path of your folder in the field `prefix` of the file `environment.yml`
2. run `conda env create --file=environments.yml` to create the conda environment
3. run `conda activate gt_project_env` to activate the environment

## About the code
We provide 6 different executable python files that you can run simply from you terminal:
* `human_vs_cpu_1.py` and `human_vs_cpu_2.py` to play a match of the game 1 and 2 against the computer. These programs ask you if you want to play as player 1 or 2 and then which policy you want the computer to play with. You can find the specifications of the policies in `utilities/policies.py`.
* `run_simulation_1.py` and `run_simulation_1.py` to run a number of matches with each combination of the policies specified.
* `run_aplhabeta_1.py` and `run_aplhabeta_2.py` to run the resolution of a game using the alphabeta pruning algorithm, you can specify the size of the steps you want to use in such a way they sum to 24.
