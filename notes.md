# Primi Composti

## Robe da fare/discutere

- discutere il vantaggio di essere giocatore 1 o 2
  - e di conseguenza se sarebbe il caso di aggiustare i punteggi (tipo 1 per composite e 3 per prime o simili)
- discutere il vantaggio relativo a quanti primi ti capitano
- vedere come variano le prestazioni delle policy al variare delle profondità
- una roba che secondo me è interessante ma non so se possa entrare nel paper è che le persone comuni quando provano a giocare fanno praticamente una policy greedy

## Possibile quantificazione del materiale per il paper

Molto abbozzato, solo per farci un'idea

| N. Colonne | Argomento                                                                   |
| :--------: | --------------------------------------------------------------------------- |
|    0.75    | Titolo e abstract                                                           |
|    1.25    | Regole dei giochi                                                           |
|    1.5     | Albero grosso -> alphabeta pruning -> ancora infattibile quindi più livelli |
|     2      | Statistiche + commento risultati                                            |
|     1      | Ha senso vederlo come static game tra le diverse policies?                  |
|    0.5     | bibliografia                                                                |

> Così siamo a 7, dobbiamo arrivare almeno a 8 colonne, meglio 9 o 10.

## Spiegazione del codice

(Magari da mettere nel readme)

- `human_vs_cpu_1` e `human_vs_cpu_2` permettono all'utente umano di fare una partita (al gioco 1 o 2) contro una qualsiasi policy (se Murrone vuole fare un'app si può vendere questa come un'AI che gioca con diversi livelli di difficoltà)

- `run_alphabeta_1` e `run_alphabeta_2` eseguono la risoluzione dei giochi 1 e 2 attraverso minimax e alpha-beta pruning: il senso è quello di fare backward induction in modo efficiente sull'albero totale del gioco per trovare il NE, ma essendo troppo grande lo suddividiamo in livelli (e.g. [4,4,5,5,6]). Così non troviamo precisamente il NE ma credo che sia la cosa più vicina a cui possiamo arrivare in un tempo ragionevole

- `run_simulation_1` e `run_simulation_2` eseguono la simulazione di un certo numero di partite con tutte le combinazioni di policy che vogliamo (vedi `results.txt` e `tempi.md`). Il senso è quello di vedere se in qualche modo una strategia è statisticamente più forte di un'altra (e da qui poi il possibile ragionamento sulla trasformazione in static game del tipo "scelgo la strategia")

- `utilities`

  - `Node`: nodo dell'albero
  - `Stack`: perché non ho trovato uno stack che mi comodasse già implementato
  - `policies`: solo per contenere le costanti con i nomi delle policies
  - `simulations`: logica molto semplice per fare le simulazioni
  - `solve_tree`: quello che serve per risolvere un albero cioè `minimax` e `solve` (che chiama minimax con le varie depths)
  - `utils`: un po' di funzioni che vengono usate dappertutto

- `play_primi_composti` 1 e 2 fanno le simulazioni rispettive
