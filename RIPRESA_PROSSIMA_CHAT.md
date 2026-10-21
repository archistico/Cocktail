# Ripresa — Cocktail Mood 3.6

**Versione di riferimento:** `cocktail-mood-3.6-essenziale.zip`.

530 ricette, 518 verificate, 6 parziali e 6 non verificate; 433 ingredienti base, 474 chip unici.

1. Leggere `METODO_VERIFICA.md` e `STATO_VERIFICA.md`.
2. Usare `data/cocktails.json` come fonte canonica; le verifiche aperte sono in `data/audit_ricette.csv`.
3. Proseguire le 12 ricette aperte senza attribuire dosi arbitrarie, poi audit globale di sinonimi di ingredienti/guarnizioni.
4. Nel selettore un solo chip `Brandy alla pesca`, cercabile anche come `Peach brandy`; evitare la fusione con Liquore alla pesca e Schnapps alla pesca.
5. `Caffè di Rüdesheim` e `Rüdesheimer Kaffee` sono una sola scheda; mantenere i due nomi e il redirect dell'ID precedente.
6. Aggiornare `data/catalog.js`, il CSV del catalogo e il CSV delle verifiche dopo modifiche alle ricette; eseguire i quattro controlli descritti in `METODO_VERIFICA.md`.
7. Nei pacchetti e nella Libreria mantenere una sola versione operativa, più il backup di rollback se necessario. Niente ZIP e audit cumulativi di versioni superate.
