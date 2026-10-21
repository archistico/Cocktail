# Metodo di verifica — Cocktail Mood 3.6

**Stato al 22 ottobre 2026:** 518/530 ricette verificate; 6 parziali e 6 non verificate. L'elenco esatto è in `STATO_VERIFICA.md`.

## Criteri per confermare una ricetta

1. Identificare una formula precisa nella fonte (produttore, autore, guida professionale, fonte locale competente). Preferire ricette singole rispetto a riassunti e pagine di raccolta.
2. Controllare ingredienti obbligatori/facoltativi, dosi, numero di porzioni, tecnica, bicchiere quando documentato e guarnizioni.
3. Conservare nelle dosi le unità della fonte. Una soda «a completare» non deve diventare un volume fittizio. Non trasformare automaticamente quantità per quattro persone in quantità per un bicchiere senza dichiararlo.
4. Tenere separati i nomi usati per formule differenti. Non mescolare il metodo di una variante con dosi di un'altra senza indicarlo.
5. Se gli ingredienti risultano confermati ma dosi o tecnica mancano, segnare `confronto_parziale`. Se la pagina è soltanto descrittiva e non verifica la preparazione, non promuovere la scheda a completa.
6. Salvare fonte, data, note su varianti e limitazioni nel campo `verificaRicetta`.

## Ingredienti e guarnizioni

- Un chip canonico ha una sola denominazione con iniziale maiuscola.
- Niente quantità, plurali descrittivi e «facoltativo» nei nomi dei chip; registrare quantità e optional soltanto nella singola ricetta.
- Non fondere prodotti diversi soltanto perché la traduzione può essere simile. Verificare le equivalenze `Peach brandy` / `Brandy alla pesca`: per le due schede Missionary’s Downfall il chip è **Brandy alla pesca**, con alias inglese. Non equiparare automaticamente prodotti con caratteristiche diverse (distillato di pesche, liquore alla pesca, schnapps).
- Le guarnizioni alternative restano distinte e sono selezionabili, ma non diventano ingredienti obbligatori per la modalità dispensa.

## Consolidamento dei duplicati

Una scheda si elimina solo se rappresenta **la medesima formula** per ingredienti, dosi, preparazione e fonte. Mantenere tutti i nomi di ricerca in `nomiAlternativi`; preservare l'ID eliminato in `aliasIdRicette` e `data/alias_id_ricette.json`. L'interfaccia fornisce `window.COCKTAIL_RESOLVE_ID(id)` per la compatibilità con riferimenti storici.

## Passaggi tecnici obbligatori

1. Modificare `data/cocktails.json`.
2. Rigenerare `data/catalog.js`, CSV del catalogo, audit JSON/CSV, export regionale e `data/ingredienti.json` quando necessario.
3. Verificare ID univoci, assenza di duplicati case/accenti, coerenza di `dosi`/ingredienti e compatibilità degli alias.
4. Eseguire tutti i test:

```bash
python tests/verifica_catalogo.py
python tests/test_regressioni.py
python tests/test_sinonimi.py
node tests/test_ui.js
```

5. Preparare ZIP dei soli file operativi, con audit e istruzioni per proseguire.

**Nota:** la versione 3.6 conferma il Baxeichito genovese usando fonti locali e una tecnica praticabile ricostruita dall'articolo sul Mojito. Non pretende di conoscere una procedura interna non pubblicata dal locale.
