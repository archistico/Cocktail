# Cocktail Mood 3.6 — Audit consolidato e pulizia

**Data:** 22 ottobre 2026. Baseline v3.5, senza nuove ricette né promozioni di stato.

## Deduplicazione ingredienti

L'IBA prescrive **15 ml di Peach Brandy** nel *Missionary’s Downfall*. La variante Tipsy con **15 ml di Brandy alla pesca** fa riferimento alla stessa denominazione di ingrediente nel contesto di queste due formule. Abbiamo adottato il chip italiano **Brandy alla pesca**, salvando `peach brandy` tra gli alias. Le dosi restano **15 ml** in entrambe, e le due ricette rimangono distinte per differenze di miele, ananas e presentazione.

Nota merceologica: il termine storico *peach brandy* può indicare un distillato di pesche e anche un brandy aromatizzato. **Non** implica equivalenza generalizzata con *Liquore alla pesca*, *Schnapps alla pesca* o *Vodka alla pesca*. Evitare sostituzioni automatiche di bottiglie. <https://iba-world.com/iba-cocktail/missionarys-downfall/>; <https://www.spiritsanddistilling.com/dictionary/acref-9780199311132-e-1054>; <https://onestigroup.com/prodotti/peach-brandy-liqueur/>.

## Deduplicazione ricette già consolidata (v3.5)

*Caffè di Rüdesheim* e *Rüdesheimer Kaffee* sono una sola formula: nome canonico italiano, nomi tedeschi in `nomiAlternativi`, ID precedente `tipsy3-rudesheimer-kaffee` mappato su `tipsy-caffe-di-rudesheim` tramite `aliasIdRicette`. Nessuna scheda distinta eliminata in questo ciclo.

## Pulizia dati e file

- Rimossi i nomi di chip duplicati, un alias orfano e le etichette composite che puntavano a due ingredienti diversi. Non cancellate le guarnizioni alternative dalle ricette.
- Eliminati contatori di lotti storici non più operativi da `meta`; mantenute metriche attuali.
- Ridenominati `audit_531_ricette.csv/.json` in `audit_ricette.csv/.json`, indipendenti dal numero di ricette.
- Rimossi `AUDIT_EDITORIALE_V35.md` e `PULIZIA_2026-10-21.md` dal pacchetto corrente: sostituiti da questo rapporto consolidato. Le regressioni storiche restano attive in `tests/test_regressioni.py`.
- Conservati catalogo JSON, JS offline, CSV, audit, alias, esportazioni regionali e test.

## Risultati

530 ricette (102 IBA, 428 Extra); 518 complete, 6 parziali, 6 non verificate. **433 ingredienti base**, **474 voci selezionabili**.
