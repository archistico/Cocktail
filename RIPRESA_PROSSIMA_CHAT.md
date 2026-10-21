# Ripresa — Cocktail Mood 3.6

**Versione di riferimento:** `cocktail-mood-3.6-pulito.zip`.

530 ricette, 518 verificate, 6 parziali e 6 non verificate; 433 ingredienti base, 474 chip unici.

1. Leggere `README.md`, `METODO_VERIFICA.md`, `STATO_VERIFICA.md` e `AUDIT_CONSOLIDATO.md`.
2. Usare `data/cocktails.json` come fonte canonica; le verifiche aperte sono in `data/audit_ricette.csv`.
3. Proseguire le 12 ricette aperte senza attribuire dosi arbitrarie, poi audit globale di sinonimi di ingredienti/guarnizioni.
4. Nel selettore un solo chip `Brandy alla pesca`, cercabile anche come `Peach brandy`; evitare la fusione con Liquore alla pesca e Schnapps alla pesca.
5. `Caffè di Rüdesheim` e `Rüdesheimer Kaffee` sono una sola scheda; mantenere i due nomi e il redirect dell'ID precedente.
6. Rigenerare sempre `data/catalog.js`, CSV ed audit dopo modifiche al JSON e lanciare i quattro test di `README.md`.
7. Nei pacchetti e nella Libreria mantenere una sola versione operativa, più il backup di rollback se necessario. Niente ZIP e audit cumulativi di versioni superate.
