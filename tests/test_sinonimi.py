from pathlib import Path
import json,csv
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/cocktails.json').read_text('utf8'));r=d['cocktails'];ids={x['id']:x for x in r}
assert len(r)==530 and len(ids)==530 and sum(x['tipo']=='IBA' for x in r)==102
assert d['aliasIdRicette']=={'tipsy3-rudesheimer-kaffee':'tipsy-caffe-di-rudesheim'}
assert 'tipsy3-rudesheimer-kaffee' not in ids
assert 'Rüdesheimer Kaffee' in ids['tipsy-caffe-di-rudesheim']['nomiAlternativi']
assert ids['baxeichito-genovese']['dosi']['Rum bianco']=='50 ml'
assert ids['baxeichito-genovese']['dosi']['Zucchero di canna']=='2 cucchiaini'
assert ids['baxeichito-genovese']['verificaRicetta']['esito']=='confrontata_con_ricetta_originale'
assert len([x for x in r if x.get('verificaRicetta',{}).get('esito')=='confrontata_con_ricetta_originale'])==518
assert len([x for x in r if x.get('verificaRicetta',{}).get('esito')=='confronto_parziale'])==6
assert len([x for x in r if x.get('verificaRicetta',{}).get('esito') not in ['confrontata_con_ricetta_originale','confronto_parziale']])==6
assert json.loads((p/'data/alias_id_ricette.json').read_text('utf8'))==d['aliasIdRicette']
assert json.loads((p/'data/catalog.js').read_text('utf8').removeprefix('window.COCKTAIL_CATALOG = ').rstrip('\n;'))==d
with (p/'data/cocktails.csv').open(encoding='utf-8-sig',newline='') as f: assert len(list(csv.DictReader(f,delimiter=';')))==530
with (p/'data/audit_ricette.csv').open(encoding='utf-8-sig',newline='') as f: assert len(list(csv.DictReader(f,delimiter=';')))==530
print('OK v3.6: ID alias, unificazione ricetta, Baxeichito, esportazioni, 518/530 verificate')

# Nessun duplicato nel selettore e traduzione Peach brandy su un solo chip.
base=set(x for rec in r for field in ['ingredienti','facoltativi'] for x in rec[field]);selectable=base|{x for rec in r for x in rec.get('guarnizione',[])}|{x for rec in r for g in rec.get('alternativeConsentite',{}).values() for x in g}
assert 'Peach brandy' not in selectable
assert 'Brandy alla pesca' in selectable
assert ids['missionary-s-downfall']['dosi']['Brandy alla pesca']=='15 ml'
assert 'Peach brandy' not in ids['missionary-s-downfall']['dosi']
assert 'Peach brandy' not in d['aliasIngredienti']
assert 'peach brandy' in d['aliasIngredienti']['Brandy alla pesca']
for separate in ('Liquore alla pesca','Schnapps alla pesca','Vodka alla pesca'):
 assert separate in selectable and separate != 'Brandy alla pesca'
from collections import defaultdict
from unicodedata import normalize as normal
rev=defaultdict(set)
for canonical,variants in d['aliasIngredienti'].items():
 for v in variants:rev[normal('NFKC',v.casefold())].add(canonical)
assert not any(len(names)>1 for names in rev.values()),[i for i in rev.items() if len(i[1])>1]
assert len(base)==433 and len(selectable)==474
assert json.loads((p/'data/audit_ricette.json').read_text('utf8'))==list(csv.DictReader((p/'data/audit_ricette.csv').open(encoding='utf-8-sig',newline=''),delimiter=';'))
assert 'Rüdesheimer Kaffee' in ids['tipsy-caffe-di-rudesheim']['nomiAlternativi']
print('OK sinonimi v3.6: brandy pesca, alias unico, caffè di Rüdesheim, CSV e JSON audit')
