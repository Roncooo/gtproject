| VER | POLICIES              | N_GAMES   | TEMPO  | CORES | RISULTATI                         |
| --- | --------------------- | --------- | ------ | ----- | --------------------------------- |
| 1   | greedy_asc, minimax4  | 8         | 11.4s  | 8     | inutili                           |
| 1   | greedy_asc, minimax45 | 8         | 171s   | 8     |                                   |
| 1   | greedy_asc, minimax45 | 16        | 341.7s | 8     |                                   |
| 1   | greedy all, minimax45 | 1000      | 7506s  | 16    | già nel paper (solo greedy rand)  |
| 1   | minimax56             | 1         | 297s   | 8     | inutili, solo per vedere il tempo |
| 1   | minimax56             | 8         | 1444s  | 8     |                                   |
| 1   | minimax456            | 16        | 3612s  | 8     | già nel paper ma sono poche       |
| 1   | simple_policies       | 200k      | 2575s  | 8     | già nel paper                     |
| 2   | simple_policies       | 200k      | 659s   | 16    | già nel paper                     |
| 2   | minimax456            | almeno 16 | -      | -     | TODO                              |
