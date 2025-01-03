## Tempi per la prima mossa poi vanno a calare

| Versione gioco | minimax_4   | minimax_5  | minimax_6   |
| -------------- | ----------- | ---------- | ----------- |
| 1              | 1 s (medio) | 3 s (diff) | 30 s (diff) |
| 2              | 1 s         | 15 s       | 93 s        |

## Tempi alpha beta

in funzione delle depths

- run_alphabeta_1.py with [6,6,12]:
  - Done 6 levels in 40.67 s
  - Done 6 levels in 5.96 s
  - Done 12 levels in 42.95 s
- run_alphabeta_2.py with [3]\*8: instant
- run_alphabeta_2.py with [4,5,7,8]:
  - Done 4 levels in 0.99 s
  - Done 5 levels in 5.14 s
  - Done 7 levels in 29.99 s
  - Done 8 levels in 0.16 s
- run_alphabeta_2.py with [5,5,5,9]:
  - Done 5 levels in 9.34 s
  - Done 5 levels in 4.13 s
  - Done 5 levels in 0.86 s
  - Done 9 levels in 1.17 s

## Tempi simulazioni

Tempi per fare una simulazione di minimax_n vs minimax_n (per le altre policy è quasi istantaneo, si possono runnare anche migliaia di simulazioni, vedi results.txt):

| Versione gioco | maximin_4 | maximin_5 | maximin_6 |
| -------------- | --------- | --------- | --------- |
| 1              | 2 s       | 15 s      | 145 s     |
| 2              | 9 s       | 64 s      | 640 s     |
