"""Regressione cumulativa Cocktail Mood 2.8: ricette, fonti, dosi, audit ed export."""
from pathlib import Path
import json,csv
r=Path(__file__).resolve().parents[1];d=json.loads((r/'data/cocktails.json').read_text('utf-8'));recipes=d['cocktails'];by={c['id']:c for c in recipes};byname={c['nome']:c for c in recipes}
verified={c['id'] for c in recipes if c.get('verificaRicetta',{}).get('esito')=='confrontata_con_ricetta_originale'}
partial={c['id'] for c in recipes if c.get('verificaRicetta',{}).get('esito')=='confronto_parziale'}
new=['tintoretto','maidens-prayer','leap-year-cocktail','hugo-originale-alla-melissa','moretta-fanese','americano-bianco','gin-tonic-al-pompelmo','spritzer-austriaco']
assert len(recipes)==530 and sum(c['tipo']=='IBA' for c in recipes)==102
assert len(verified)==518 and len(partial)==6
assert set(new)<=verified
assert d['meta']['versione']=='3.6-sinonimi-e-pulizia'
assert d['meta']['ingredienti']==433 and d['meta']['ingredientiSelezionabili']==474
for id in new:
 c=by[id]
 assert c['dosi'] and c['fonteDosi'] and c['preparazioneSintetica'] and c['notaRicetta']
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi'])
 assert c['verificaRicetta']['fonti'][0]==c['fonteDosi']
assert by['tintoretto']['dosi']=={'Prosecco':'120 ml','Succo di melagrana':'50 ml'}
assert by['maidens-prayer']['guarnizione']==['Arancia']
assert by['maidens-prayer']['dosi']['Succo di limone']=='5 ml'
assert by['leap-year-cocktail']['dosi']['Succo di limone']=='1 dash'
assert by['hugo-originale-alla-melissa']['dosi']['Sciroppo di melissa']=='20 ml'
assert by['hugo-originale-alla-melissa']['guarnizione']==['Limone']
assert by['moretta-fanese']['porzioniFonte']=='4 bicchierini'
assert 'Scorza di limone' in by['moretta-fanese']['ingredienti'] and not by['moretta-fanese']['guarnizione']
assert by['americano-bianco']['ingredienti']==['Bitter bianco','Vermouth dry','Soda']
assert by['gin-tonic-al-pompelmo']['ingredienti']==['Gin','Acqua tonica'] and by['gin-tonic-al-pompelmo']['guarnizione']==['Pompelmo']
assert by['spritzer-austriaco']['dosi']=={'Vino bianco fermo':'1 parte (50%)','Soda':'1 parte (50%)'}
assert {'bicerin-torinese','spritz-bianco','amarcord-di-moasca','spritz-euganeo'}<=partial
# Regressioni storiche rappresentative, mantenute dai lotti precedenti.
assert byname['Old Pal']['dosi']['Rye whiskey']=='45 ml'
assert byname['Tinto de Verano']['dosi']['Vino rosso']=='150 ml'
assert byname['Rossini']['dosi']=={'Prosecco':'100 ml','Purea di fragole':'50 ml'}
assert byname['Campari Soda']['guarnizione']==[]
assert byname['Dirty Martini']['dettagliGuarnizione']['Oliva']=='3 olive verdi'
assert byname['Gin Tonic al cetriolo']['ingredienti']==['Gin','Acqua tonica']
assert byname['Gin Tonic al cetriolo']['guarnizione']==['Cetriolo']
assert byname['Gin Soda']['guarnizione']==['Limone']
assert byname['Green Spritz']['dosi']['P31 Aperitivo Green']=='3 parti'
assert by['vodka-martini']['guarnizioniAlternative'] is True
assert by['vodka-martini']['guarnizione']==['Scorza di limone','Oliva']
assert by['x-y-z']['ingredienti']==['Rum bianco','Cointreau','Succo di limone']
assert by['bucks-fizz']['dosi']['Champagne']=='4 oz'
assert by['caffe-alla-valdostana']['porzioniFonte']=='6 porzioni'
assert by['malibu-e-ananas']['dosi']=={'Malibu':'50 ml','Succo di ananas':'100 ml'}
assert by['viaggio-umeshu-soda']['dosi']=={'Umeshu':'1 parte','Soda':'2 parti'}
assert by['bellini-analcolico']['dosi']=={'Purea di pesca':'50 ml','Spumante analcolico':'100 ml'}
assert by['virgin-margarita']['guarnizioniFacoltative']==['Sale']
assert by['viaggio-japanese-whisky-highball']['gruppiAlternativiGuarnizione']==[['Scorza di limone','Pompelmo']]
assert json.loads((r/'data/catalog.js').read_text('utf-8').removeprefix('window.COCKTAIL_CATALOG = ').rstrip('\n;'))==d
with (r/'data/audit_ricette.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f,delimiter=';'))
assert len(rows)==530
assert sum(x['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale' for x in rows)==518
assert sum(x['stato_verifica_2026_10_21']=='confronto_parziale' for x in rows)==6
assert sum(x['stato_verifica_2026_10_21']=='non_verificata' for x in rows)==6
assert sum(x['priorita']=='ALTA' and x['stato_verifica_2026_10_21']!='confrontata_con_fonte_originale' for x in rows)==10
assert {x['id'] for x in rows if x['stato_verifica_2026_10_21']=='confronto_parziale'}<=partial
assert json.loads((r/'data/audit_ricette.json').read_text('utf-8'))==[{k:r[k] for k in rows[0]} for r in rows]
with (r/'data/cocktails.csv').open(encoding='utf-8-sig',newline='') as f: cr=list(csv.DictReader(f,delimiter=';'))
assert len(cr)==530
for id in new:
 a=next(x for x in cr if x['id']==id)
 assert json.loads(a['dosi'])==by[id]['dosi'],id
 assert a['preparazioneSintetica']==by[id]['preparazioneSintetica'],id
new25=['puccini','aperol-sour','rose-cocktail-francese','french-75-analcolico','manhattan-alla-castagna','spritz-normanno','monaco-birra','peach-blush-spritz']
assert set(new25)<=verified
for id in new25:
 x=by[id]
 assert set(x['dosi'])==set(x['ingredienti']+x['facoltativi'])
 assert x['fonteDosi'] and x['preparazioneSintetica'] and x['verificaRicetta']['fonti'][0]==x['fonteDosi']
assert by['puccini']['dosi']=={'Prosecco':'100 ml','Succo di mandarino':'50 ml'}
assert by['aperol-sour']['dosi']['Albume']=='15 ml (facoltativo)'
assert by['rose-cocktail-francese']['guarnizione']==['Ciliegina al brandy']
assert by['rose-cocktail-francese']['dettagliGuarnizione']['Ciliegina al brandy']=='3 ciliegie al brandy'
assert by['french-75-analcolico']['dosi']['Spumante analcolico']=='90 ml'
assert by['manhattan-alla-castagna']['dosi']['Angostura']=='2 dash'
assert by['spritz-normanno']['dosi']['Perry (sidro di pere)']=='3⅓ oz (circa 100 ml)'
assert by['monaco-birra']['guarnizione']==[]
assert by['peach-blush-spritz']['dosi']['Limonata'].startswith('a completare')
for id in ['tipsy3-left-hand','tipsy-rated-amaretto-sour','tipsy-rated-boothby']:
 assert 'Ciliegina al brandy' in by[id]['guarnizione']
assert d['aliasIngredienti']['Ciliegina al brandy'] and 'Ciliegine al brandy' not in d['aliasIngredienti']
assert json.loads((r/'data/alias_ingredienti.json').read_text('utf-8'))==d['aliasIngredienti']

new26=['gin-tonic-alla-viola','vino-rosso-con-le-percoche','viaggio-somaek-coreano','viaggio-berliner-weisse-al-lampone','viaggio-berliner-weisse-allasperula','viaggio-poncha-a-pescador','viaggio-poncha-al-maracuja','viaggio-teh-tarik-di-singapore','viaggio-milo-dinosaur-di-singapore']
assert set(new26)<=verified
for id in new26:
 c=by[id]
 assert c['verificaRicetta']['fonti'][0]==c['fonteDosi']
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi'])
 assert c['preparazioneSintetica'] and c['porzioniFonte'] and c['notaRicetta']
 assert c['fonteDosi'].startswith('https://')
assert by['gin-tonic-alla-viola']['dosi']=={'Gin':'50 ml','Acqua tonica':'100 ml','Sciroppo alla violetta':'10 ml'}
assert by['gin-tonic-alla-viola']['guarnizione']==['Scorza di limone']
assert by['vino-rosso-con-le-percoche']['dosi']=={'Vino rosso':'1 litro','Percoche':'1 kg'}
assert by['viaggio-somaek-coreano']['dosi']=={'Soju':'3 parti (30%)','Birra chiara':'7 parti (70%)'}
assert by['viaggio-poncha-a-pescador']['alternativeConsentite']=={'Zucchero':['Miele']}
assert 'Scorza di limone' in by['viaggio-poncha-a-pescador']['ingredienti']
assert by['viaggio-teh-tarik-di-singapore']['dosi']['Acqua calda']=='250 ml'
assert by['viaggio-milo-dinosaur-di-singapore']['dettagliGuarnizione']['Milo in polvere'].startswith('2 cucchiai')
assert 'love-in-portofino' in partial and 'baxeichito-genovese' in verified
for id in new26:
 row=next(x for x in rows if x['id']==id)
 assert row['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 assert row['fonti_verifica_diretta']==by[id]['fonteDosi']
for id in new26:
 crrow=next(x for x in cr if x['id']==id)
 assert json.loads(crrow['dosi'])==by[id]['dosi']
 assert crrow['preparazioneSintetica']==by[id]['preparazioneSintetica']

new27=['viaggio-terremoto-cileno','viaggio-rakomelo-cretese','viaggio-coctel-de-algarrobina','viaggio-nikita-di-madeira','viaggio-cola-de-mono-cilena','viaggio-lonkero-finlandese','strawberry-shortcake-mimosa','viaggio-chu-hi-al-limone']
assert set(new27)<=verified
for id in new27:
 c=by[id]
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),id
 assert c['fonteDosi']==c['verificaRicetta']['fonti'][0],id
 assert c['preparazioneSintetica'] and c['porzioniFonte'] and c['notaRicetta'],id
 row=next(x for x in rows if x['id']==id)
 assert row['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 assert row['fonti_verifica_diretta']==c['fonteDosi']
 crrow=next(x for x in cr if x['id']==id)
 assert json.loads(crrow['dosi'])==c['dosi']
assert by['viaggio-terremoto-cileno']['porzioniFonte']=='4 persone'
assert by['viaggio-rakomelo-cretese']['dosi']['Miele']=='20 g'
assert by['viaggio-coctel-de-algarrobina']['dosi']["Tuorlo d'uovo"]=='1 tuorlo'
assert 'Sciroppo di gomma' in by['viaggio-coctel-de-algarrobina']['ingredienti'] and 'Sciroppo di zucchero' not in by['viaggio-coctel-de-algarrobina']['ingredienti']
assert by['viaggio-nikita-di-madeira']['dosi']['Birra chiara']=='250 g'
assert "Scorza d'arancia" in by['viaggio-cola-de-mono-cilena']['ingredienti']
assert 'Rosmarino' in by['viaggio-lonkero-finlandese']['guarnizione']
assert 'Fragole' in by['strawberry-shortcake-mimosa']['guarnizione']
assert by['viaggio-chu-hi-al-limone']['dosi']['Shochu']=='50 ml'

print('OK regressioni storiche v2.x: ricette, dosi, audit/export coerenti')

# Lotto 2.8: ricette ad alta priorità identificate per variante specifica.
new28=['invisible','quattro-bianchi','japanese-iced-tea','amici-miei-cocchi-rosa','vodka-pesca-lemon','bianchin-sprussa']
assert set(new28)<=verified
for id in new28:
 c=by[id]; assert c['verificaRicetta']['fonti'][0]==c['fonteDosi']
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),id
 assert c['preparazioneSintetica'] and c['porzioniFonte'] and c['notaRicetta'],id
 assert next(row for row in rows if row['id']==id)['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 assert json.loads(next(row for row in cr if row['id']==id)['dosi'])==c['dosi']
assert by['invisible']['dosi']['Succo di limone']=='30 ml'
assert 'Cointreau' in by['invisible']['ingredienti']
assert 'Triple sec' not in by['quattro-bianchi']['ingredienti']
assert 'Midori' in by['japanese-iced-tea']['ingredienti'] and 'Triple sec' not in by['japanese-iced-tea']['ingredienti']
assert by['amici-miei-cocchi-rosa']['dosi']['Bibita al pompelmo rosa']=='90 ml'
assert by['vodka-pesca-lemon']['dosi']['Angostura']=='3 gocce'
assert 'Campari Soda' in by['bianchin-sprussa']['ingredienti'] and 'Campari' not in by['bianchin-sprussa']['ingredienti']
assert 'Bitter rosso' in by['amici-miei-cocchi-rosa']['ingredienti']
assert len(set(r['id'] for r in recipes))==530
print('OK regressione v2.8: sei verifiche su fonti distinte, senza fusione di formule')

# Lotto 2.9: preservazione delle 30 ricette del lotto precedente.
new29={c['id'] for c in recipes if c.get('lotto')=='2.9'}
assert len(new29)==30 and new29<=verified
for id in new29:
 c=by[id]
 assert c['fonteDosi']==c['verificaRicetta']['fonti'][0],id
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),id
 assert c['preparazioneSintetica'] and c['porzioniFonte'] and c['notaRicetta'],id
 row=next(x for x in rows if x['id']==id)
 assert row['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 crrow=next(x for x in cr if x['id']==id)
 assert json.loads(crrow['dosi'])==c['dosi']
assert byname['Pimm’s Cup']['dosi']=={"Pimm's No. 1":"50 ml",'Limonata frizzante':'150 ml'}
assert 'Ciliegina al maraschino' in byname['Alcohol-Free Piña Colada']['guarnizione']
assert 'Cointreau' in byname['Breakfast Martini']['ingredienti']
assert byname['Painkiller']['dosi']['Succo di ananas']=='4 oz (120 ml)'
assert byname['Saturn']['dosi']['Gin']=='1¼ oz (37,5 ml)'
assert byname['Hotel Nacional']['dosi']['Rum invecchiato']=='1½ oz (45 ml)'
assert byname['Rum Punch delle Barbados']['dosi']['Acqua']=='4 parti'
assert len(new29)==30 and all(next(row for row in rows if row['id']==i)['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale' for i in new29)
assert len(json.loads((r/'data/ingredienti.json').read_text('utf8')))==433
assert len({*json.loads((r/'data/ingredienti.json').read_text('utf8')),*[i for c in recipes for i in c['guarnizione']],*[j for c in recipes for vs in c.get('alternativeConsentite',{}).values() for j in vs]})==474
print('OK regressione v2.9: 30 formule storiche preservate')

# Lotto 3.1 — 60 verifiche complete e modifiche sostanziali.
new30=['Malibu Bay Breeze', 'Kentucky Buck', 'Cinnamon Daiquiri', 'Strawberry Mojito', 'White Christmas Margarita', 'Whiskey Smash', 'Missionary’s Downfall (Tipsy version)', 'Bourbon Sweet Tea', 'Lazy Red Cheeks', 'Fitzgerald', 'Frozen Pornstar Martini', 'Raspberry Mojito', 'Caipirão', 'Rum Punch', 'Charlie Chaplin', 'Blue Hawaii', 'Tom Collins', 'Vodka Cranberry', 'Jack and Coke', 'Appletini', 'Fruit Tingle', 'Lychee Martini', 'Sweet Poison Cocktail', 'Ward Eight', 'Ranch Water', 'Red Sangria', 'Sunflower', 'Kentucky Mule', 'Spicy Margarita', 'Gold Rush', 'Bay Breeze', 'Lynchburg Lemonade', 'Gin Rickey', 'Mango Margarita', 'Purple Rain', 'Elderflower Spritz', 'Dirty Vodka Martini', 'Gin Lemonade', 'Buttery Nipple', 'Mexican Firing Squad', 'White Sangria', 'Limoncello Martini', 'Passion Fruit Mojito', 'Watermelon Margarita', 'Pineapple Upside-Down Cake', 'Cape Codder', 'Gin Daisy', 'Electric Lemonade', 'Elderflower Gimlet', 'Pink Gin and Tonic', 'Gin Sour', 'Pineapple Margarita', 'Vodka Sour', 'Coconut Margarita', 'Disaronno Coke', 'Screaming Orgasm', '7 & 7', 'Army & Navy', 'London Mule', 'Spicy Bloody Mary']
assert len(new30)==60 and len(set(new30))==60
for name in new30:
 c=byname[name]
 assert c['verificaRicetta']['esito']=='confrontata_con_ricetta_originale',name
 assert c['fonteDosi']==c['verificaRicetta']['fonti'][0] and c['preparazioneSintetica'],name
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),name
assert byname['Gin Rickey']['ingredienti']==['Gin','Succo di lime','Soda']
assert 'Sciroppo di zucchero' not in byname['Gin Rickey']['ingredienti']
assert byname['Malibu Bay Breeze']['dosi']['Succo di ananas']=='30 ml'
assert byname['Strawberry Mojito']['dosi']['Fragole']=='3 fragole'
assert byname['7 & 7']['ingredienti']==['Whiskey','7 Up']
assert byname['Fitzgerald']['dosi']['Sciroppo di zucchero']=='1 oz'
assert byname['Tom Collins']['guarnizione']==['Arancia','Ciliegina al brandy']
assert byname['Ward Eight']['guarnizione']==['Arancia','Ciliegina al brandy']
print('OK regressione lotto 3.0: 60 ricette preservate')

# Lotto 3.1 — 60 ricette, e verifiche dei dettagli editoriali.
new31=['Spagett', 'Black Velvet', 'Snakebite', 'Red Eye', 'Shandygaff', 'Ginger Beer Shandy', 'Carajillo', 'Espresso Tonic', 'Maria Theresia', 'Revolver', 'Ginger Espresso', 'Karsk', 'Pumpkin Spice Espresso Martini', 'Latte Martini', 'Coconut Espresso Martini', 'Tequila Espresso Martini', 'Riesling Spritz', 'Strawberry Margarita', 'Frozen Margarita', 'Miami Vice', 'Frozen Bellini', 'Frozen Grasshopper', 'Frozen Blue Hawaiian', 'Virgin Strawberry Daiquiri', 'Amarula Dom Pedro', 'Frozen Mango Daiquiri', 'Amaretto Sour', 'Lemon Drop Shot', 'Lemon Drop', 'Dirty Shirley', 'Mudslide', 'Frozen Strawberry Daiquiri', 'Maple Old Fashioned', 'Green Tea Shot', 'Dill Pickle Shot', 'Chocolate Martini', 'Irish Old Fashioned', 'Amaretto Sicily', 'Boothby', 'Balalaika', 'Eastern Standard', 'Elk’s Own', 'Parisian', 'Creole Cocktail', 'Lavender Lemon Drop', 'Mulled Wine', 'Baby Guinness', 'Bijou', 'Blackthorn', 'Bloody Maria', 'Bobby Burns Cocktail', 'Brandy Cobbler', 'Brandy Flip', 'Espresso Rumtini', 'Elderflower Caipirinha', 'Lemon Elderflower Spritzer', 'Lunch Box', 'Banana Daiquiri', 'Lassi - Mango', "Quaker's Cocktail"]
assert len(new31)==60 and len(set(new31))==60
for name in new31:
 c=byname[name]
 assert c['verificaRicetta']['esito']=='confrontata_con_ricetta_originale',name
 assert c['verificaRicetta']['fonti'][0]==c['fonteDosi'],name
 assert c['preparazioneSintetica'] and c['statoDosi']=='complete',name
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),name
assert byname['Amarula Dom Pedro']['dosi']=={'Gelato alla vaniglia':'150 ml','Panna fresca':'25 ml','Liquore alla crema Amarula':'40 ml'}
assert byname['Spagett']['guarnizione']==[]
assert byname['Spagett']['dosi']['Birra Miller High Life']=='9 oz'
assert byname['Strawberry Margarita']['dosi']['Fragole']=='5 fragole'
assert byname['Lassi - Mango']['porzioniFonte']!='1 porzione'
assert byname['Baby Guinness']['guarnizione']==[]
assert byname['Brandy Flip']['guarnizione']==['Noce moscata']
assert byname['Amaretto Sour']['guarnizione']==['Arancia','Ciliegina al brandy']
print('OK regressione lotto 3.1: 60 ricette preservate')

# Lotto 3.2
new32=['Agua de Valencia', 'Sangria di Sidro', 'Mule al Jägermeister', 'Weissbier Spritz', 'Caesar', 'Mojito al litchi', 'Vampiro', 'Virgin Paloma', 'Horchata messicana', 'Michelada', 'Mojito all’anguria', 'Regina Mary', 'Vancouver', 'Bahama Mama', 'Hurricane', 'East 8 Hold Up', 'Paloma piccante all’ananas', 'Agua fresca al cetriolo e lime', 'Agua fresca al mango', 'Treacle', 'Snowball', '20th Century', 'Left Bank Martini', 'Rum Runner', 'Fog Cutter', 'Test Pilot', 'Swimming Pool', 'Glühwein', 'Agua fresca all’anguria', 'Fallen Leaves', 'El Presidente', 'Comte de Sureau', 'Jägermeister e cola', 'Tropical Itch', 'Right Hand', 'Golden Cadillac', 'Chocolate Old Fashioned', 'Easy Speak', 'Chuflay boliviano', 'Sky Diving', 'Lemon Lime & Bitters', 'Blood Orange Radler', 'Pear Shandy', 'Beer Mule', 'Beer and Loathing', 'Black and Tan (lager)', 'Wet Pussy Shot', 'Black & Tan (pale ale)', 'Cherry Flip', 'Champagne Flip', 'Brandy Egg Nog Vintage', 'Batida Paulista', 'Scorpion', 'Aruba Ariba originale', 'Bandung di Singapore', 'Capitán peruviano', 'Machu Picchu Cocktail', 'Chilcano peruviano', 'Perú Libre', 'Chelada']
assert len(new32)==60 and len(set(new32))==60
for name in new32:
 c=byname[name]
 assert c['verificaRicetta']['esito']=='confrontata_con_ricetta_originale',name
 assert c['fonteDosi']==c['verificaRicetta']['fonti'][0],name
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),name
 assert c['preparazioneSintetica'],name
assert byname['Black and Tan (lager)']['ingredienti']==['Birra lager','Birra Guinness Draught']
assert byname['Black & Tan (pale ale)']['ingredienti']==['Birra pale ale','Birra stout Guinness']
assert byname['Capitán peruviano']['dosi']=={'Pisco':'1 oz','Vermouth rosso':'1 oz'}
assert byname['Bandung di Singapore']['dosi']['Sciroppo di rosa']=='75 ml'
print('OK regressione lotto 3.2: 60 ricette e Black and Tan distinti')

# Lotto 3.3: 37 ricette con identificazione puntuale della formula.
latest={c['id'] for c in recipes if c.get('lotto')=='3.3'}
assert len(latest)==36 and latest<=verified  # una delle 37 schede 3.3 era un duplicato, ora fuso con alias
for id in latest:
 c=by[id]
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),id
 assert c['fonteDosi']==c['verificaRicetta']['fonti'][0]
 assert c['preparazioneSintetica']
 assert next(x for x in rows if x['id']==id)['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 assert json.loads(next(x for x in cr if x['id']==id)['dosi'])==c['dosi']
assert byname['Toblerone Cocktail']['dosi']['Panna fresca']=='1 oz (circa 30 ml)'
assert byname['Ratafia Collins']['dosi']['Soda']=='a completare'
assert byname['Spritz al mirto']['dosi']['Soda']=='a completare'
assert byname['Diesel (birra e cola)']['dosi']['Cola']=='4 oz (circa 120 ml)'
print('OK lotto 3.3: 37 schede verificate, export, fonti e dosaggi')

# Lotto 3.4 — verifica dei nuovi 7 casi completi, del caso parziale e della lista residua.
new34=['ponce-livornese-mezzo-e-mezzo','nocino-sour-modenese','mezza-carolina','tipsy-leche-de-pantera','tipsy-cua-cua','fonti-3-moet-margarita','viaggio-appleton-ting']
assert len(new34)==7 and set(new34)<=verified
for id in new34:
 c=by[id]
 assert c['lotto']=='3.4' and c['verificaRicetta']['fonti'][0]==c['fonteDosi'],id
 assert set(c['dosi'])==set(c['ingredienti']+c['facoltativi']),id
 assert c['preparazioneSintetica'] and c['porzioniFonte'] and c['notaRicetta'],id
 assert next(x for x in rows if x['id']==id)['stato_verifica_2026_10_21']=='confrontata_con_fonte_originale'
 assert json.loads(next(x for x in cr if x['id']==id)['dosi'])==c['dosi']
assert by['fonti-3-cafe-blanco']['verificaRicetta']['esito']=='confronto_parziale'
assert by['fonti-3-moet-margarita']['guarnizione']==['Sale','Lime']
assert 'Sale' not in by['fonti-3-moet-margarita']['ingredienti']
assert by['viaggio-appleton-ting']['ingredienti']==['Rum giamaicano Appleton','Succo di lime','Nettare di agave','Ting al pompelmo']
assert by['tipsy-leche-de-pantera']['dosi']=={'Gin':'45 ml','Latte condensato zuccherato':'90 ml','Acqua':'30 ml'}
assert d['aliasIdRicette']['tipsy3-rudesheimer-kaffee']=='tipsy-caffe-di-rudesheim'
assert len(verified)==518 and len(partial)==6
assert len([x for x in rows if x['stato_verifica_2026_10_21']=='non_verificata'])==6
assert sum(x['priorita']=='ALTA' and x['stato_verifica_2026_10_21']!='confrontata_con_fonte_originale' for x in rows)==10
assert d['meta']['versione']=='3.6-sinonimi-e-pulizia'
print('OK lotto v3.6: 7 confermate, 1 parziale nuova, duplicati segnalati, integrazione audit/CSV corretta')
