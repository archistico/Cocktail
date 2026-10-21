# Cocktail Mood 3.6 — archivio operativo pulito

**Data:** 22 ottobre 2026. Versione di riferimento unica.

- **530** ricette distinte: 102 IBA, 428 Extra; **518 verificate**, 6 parziali e 6 non verificate.
- **433** ingredienti base; **474** chip unici includendo guarnizioni e alternative.
- Ricerca `Peach brandy` → **Brandy alla pesca** (senza fondere liquore/schnapps alla pesca). Ricetta IBA del *Missionary's Downfall* aggiornata, dose 15 ml conservata.
- **Caffè di Rüdesheim** e **Rüdesheimer Kaffee** condividono una scheda; alias nominali e ID storico mantenuti.
- Audit e export senza nomi versione obsoleti: `data/audit_ricette.csv`, `data/audit_ricette.json`.

## Avvio

Aprire `index.html` anche offline. La fonte canonica è `data/cocktails.json`; `data/catalog.js` è la copia per l'app. Non modificare l'una senza sincronizzare l'altra.

## File

- `index.html`, `css/stile.css`, `js/app.js`: interfaccia.
- `data/cocktails.json`, `catalog.js`: catalogo.
- `data/alias_ingredienti.json`, `alias_id_ricette.json`: sinonimi e ID precedenti.
- `data/ingredienti.json`, `regioni.json`: elenchi di supporto.
- `data/cocktails.csv`, `cocktail_regionali.csv`, `audit_ricette.csv`, `audit_ricette.json`: esportazioni correnti.
- `METODO_VERIFICA.md`, `STATO_VERIFICA.md`, `AUDIT_CONSOLIDATO.md`, `RIPRESA_PROSSIMA_CHAT.md`: documentazione corrente.
- `tests/*`: regressioni automatiche.

## Test

```sh
python tests/verifica_catalogo.py
python tests/test_regressioni.py
python tests/test_sinonimi.py
node tests/test_ui.js
```
