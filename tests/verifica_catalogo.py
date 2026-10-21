"""Controlli correnti per Cocktail Mood 3.6. Eseguire: python tests/verifica_catalogo.py"""
from pathlib import Path
import json,csv,re,unicodedata
p=Path(__file__).resolve().parents[1]
d=json.loads((p/'data/cocktails.json').read_text('utf8'));a=d['cocktails']
assert len(a)==530 and sum(x['tipo']=='IBA' for x in a)==102
assert len({r['id'] for r in a})==len(a)
def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('’',"'")) if not unicodedata.combining(c))
base=set(v for r in a for field in ('ingredienti','facoltativi') for v in r[field]);sel=base|{v for r in a for v in r['guarnizione']}|{v for r in a for vs in r.get('alternativeConsentite',{}).values() for v in vs}
assert len(base)==433,(len(base),433)
assert len(sel)==474,(len(sel),474)
assert len({norm(v) for v in sel})==len(sel),'duplicati case/accent'
assert all(v[0].isupper() or v[0].isdigit() for v in sel)
assert not any('facoltativ' in norm(v) or re.search(r'^\d+[- /]\d*\s+(?:ciliegin|fett|chicch|stecc)',v,re.I) for v in sel)
for r in a:
 assert r['ingredienti'] and set(r['facoltativi']).isdisjoint(set(r['ingredienti'])),r['nome']
 assert set(r['dosi'])<=set(r['ingredienti']+r['facoltativi']),r['nome']
 assert set(r['ingredientiLocali'])<=set(r['ingredienti']),r['nome']
 assert all(len(r[f])==len(set(r[f])) for f in ('ingredienti','facoltativi','guarnizione')),r['nome']
 assert set(r.get('dettagliGuarnizione',{}))<=set(r['guarnizione']),r['nome']
 assert set(r.get('guarnizioniFacoltative',[]))<=set(r['guarnizione']),r['nome']
 assert set(y for vs in r.get('gruppiAlternativiGuarnizione',[]) for y in vs)<=set(r['guarnizione'])
assert set(json.loads((p/'data/ingredienti.json').read_text('utf8')))==base
assert d['meta']['ingredienti']==433
assert len(json.loads((p/'data/audit_ricette.json').read_text('utf8')))==530
with (p/'data/cocktails.csv').open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f,delimiter=';')))==530
with (p/'data/audit_ricette.csv').open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f,delimiter=';')))==530
assert len({r['nome'] for r in a})==len(a)
assert len([r for r in a if r['regioni']])==57
assert len({z for r in a for z in r['regioni']})==20
assert 'Fernet' in base and 'fernet' not in sel
assert 'Ciliegina al brandy' in sel and 'Ciliegine al brandy' not in sel and 'Ciliegia al brandy' not in sel
assert 'Ciliegina al maraschino' in sel and not any('ciliegie maraschino'==norm(v) for v in sel)
shirley=next(r for r in a if r['nome']=='Shirley Temple')
assert shirley['guarnizione']==['Ciliegina al maraschino'] and shirley['dettagliGuarnizione']['Ciliegina al maraschino']=='2-3 ciliegine al maraschino'
aviation=next(r for r in a if r['nome']=='Aviation')
assert 'Ciliegina al maraschino' in aviation['guarnizioniFacoltative']
espresso=next(r for r in a if r['nome']=='Espresso Martini')
assert espresso['dettagliGuarnizione']['Chicchi di caffè']=='3 chicchi di caffè'
dry=next(r for r in a if r['nome']=='Dry Martini')
assert dry['guarnizioniAlternative'] and set(dry['guarnizione'])=={'Oliva','Scorza di limone'} and dry['dettagliGuarnizione']['Oliva']=='oliva verde'
old=next(r for r in a if r['nome']=='Old Fashioned')
assert ['Arancia',"Scorza d'arancia"] in old['gruppiAlternativiGuarnizione']
assert {'Stroh 40','Stroh 60','Stroh 80'}<=set(sel)
assert {'Fernet','Fernet-Branca'}<=set(sel)
assert 'Menta' in sel and 'More' in sel
print('OK v3.6: 530 ricette, 433 ingredienti base, 474 selezionabili, niente duplicati maiuscolo/quantità/facoltativo e dettagli originali conservati')
