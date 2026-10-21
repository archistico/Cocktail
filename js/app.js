'use strict';
(()=>{
 const root=window.COCKTAIL_CATALOG;
 const $=id=>document.getElementById(id);
 if(!root||!Array.isArray(root.cocktails)){$('status').textContent='Impossibile leggere il catalogo.';return;}
 const recipes=root.cocktails;
 // Alias ID di schede editoriali consolidate: mantengono compatibili i riferimenti precedenti.
 const recipeIdMap=new Map(recipes.map(recipe=>[recipe.id,recipe]));
 window.COCKTAIL_RESOLVE_ID=id=>recipeIdMap.get(root.aliasIdRicette?.[id]||id)||null;
 const aliases=root.aliasIngredienti||{};
 const STROH_ANY='Stroh (qualsiasi gradazione)';
 const isStrohGrade=x=>/^Stroh (40|60|80)$/.test(x);
 const drinkIngredients=[...new Set(recipes.flatMap(r=>[...r.ingredienti,...r.facoltativi,...(r.variantiStroh||[])]))];
 const garnishes=new Set(recipes.flatMap(r=>r.guarnizione||[]));
 const baseIngredients=new Set(drinkIngredients);
 const alternativeNames=recipes.flatMap(r=>Object.values(r.alternativeConsentite||{}).flat());
 // Guarnizioni e alternative sono selezionabili per scoperta ma non conteggiate
 // come ingredienti di base obbligatori nella statistica di catalogo.
 const ingredients=[...new Set([...drinkIngredients,...alternativeNames,...garnishes,STROH_ANY])].sort((a,b)=>a.localeCompare(b,'it'));
 const state={selected:new Set(),mode:'desidero',ingQuery:'',ingCategory:'tutti',nameQuery:'',onlyIBA:false,onlyNA:false,onlyVerified:false,onlyLocal:false,onlyTraditional:false,region:'tutte',country:'tutti',collection:'tutte',maxMissing:0,visible:21};
 $('totalCocktails').textContent=recipes.length;$('totalIba').textContent=recipes.filter(r=>r.tipo==='IBA').length;$('totalIngredients').textContent=drinkIngredients.length; // guarnizioni indicizzate separatamente
 $('totalRegional').textContent=recipes.filter(r=>r.regioni?.length || (r.tipicita && r.luogoEstero)).length;
 const regions=[...new Set(recipes.flatMap(r=>r.regioni||[]))].sort((a,b)=>a.localeCompare(b,'it'));for(const reg of regions){const opt=document.createElement('option');opt.value=reg;opt.textContent=reg;$('regionFilter').append(opt);}
 const countries=[...new Set(recipes.map(r=>r.paese).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'it'));for(const country of countries){const opt=document.createElement('option');opt.value=country;opt.textContent=country;$('countryFilter').append(opt);}
 const collectionCounts=new Map();for(const r of recipes)for(const c of r.collezioni||[])collectionCounts.set(c,(collectionCounts.get(c)||0)+1);const collections=[...collectionCounts.keys()].sort((a,b)=>a.localeCompare(b,'it'));for(const collection of collections){const opt=document.createElement('option');opt.value=collection;opt.textContent=`${collection} (${collectionCounts.get(collection)})`;$('collectionFilter').append(opt);}
 const accent=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[’ʼ‘]/g,"'").toLowerCase();
 // Ricerca per nome italiano e sinonimi originali: la selezione resta sull'ingrediente canonico.
 function matchesIngredient(name,query){return accent(name).includes(query)||(aliases[name]||[]).some(a=>accent(a).includes(query));}
 const categories={
  distillati:/rum|whisk|whiskey|gin|vodka|cognac|brandy|tequila|mezcal|cachaça|pisco|grappa|prosecco|champagne|spumante|vino|sherry|porto|calvados|aguardiente|aguardente|singani|shochu|soju|tsikoudia|zivania|scotch|STROH/i,
  mixers:/soda|tonica|ginger ale|ginger beer|cola|lemon soda|limonata|acqua frizzante|gassosa|energy drink|acqua$|chinotto|bergamottata/i,
  succhi:/succo|purea|fragol|pompelmo|arancia$|lime$|limone$|ananas$|melagrana|mandarino|passion fruit$|pompelmo$|mora|lampon|sorbetto|percoche/i,
  sciroppi:/sciroppo|miele|zucchero|granatina|cordiale|falernum/i,
  liquori:/liquore|crema di |crème de |cointreau|campari|aperol|cynar|select|p31|fernet|amaro|vermouth|vermut|chartreuse|maraschino|curaçao|triple sec|frangelico|grand marnier|amaretto|lillet|baileys|bénédictine|drambuie|malibu|midori|martini|pernod|assenzio|bitter bianco|suze|rum.*liqueur|apricot brandy|brandy alla pesca|peach brandy|cherry brandy|liquore al pimento|genepì|ratafia|nocino|mirto|punt e mes|mezzoemezzo|rosolio/i
 };
 function classify(x){for(const id of ['mixers','succhi','sciroppi','liquori','distillati'])if(categories[id].test(x))return id;return 'altro';}
 function allIngredients(r){
  const extra=r.variantiStroh||[];
  // Le alternative esplicitamente documentate possono essere cercate senza diventare
  // ingredienti contemporaneamente obbligatori (es. champagne O prosecco in Old Cuban).
  const substitutions=Object.values(r.alternativeConsentite||{}).flat();
  return [...new Set([...r.ingredienti,...r.facoltativi,...(r.guarnizione||[]),...extra,...substitutions,...(extra.length?[STROH_ANY]:[])])];
 }
 function inRecipe(r,x){return allIngredients(r).includes(x);}
 function hasSpecificIngredient(r,required){
  if(state.selected.has(required))return true;
  if(isStrohGrade(required))return (r.variantiStroh||[]).some(x=>state.selected.has(x));
  return (r.alternativeConsentite?.[required]||[]).some(x=>state.selected.has(x));
 }
 function missingIngredients(r){return r.ingredienti.filter(x=>!hasSpecificIngredient(r,x));}
 function selectedRequiredCount(r){return r.ingredienti.length-missingIngredients(r).length;}
 function baseResult(){return recipes.filter(r=>(!state.onlyIBA||r.tipo==='IBA')&&(!state.onlyNA||r.analcolico)&&(!state.onlyVerified||r.verificaRicetta?.esito==='confrontata_con_ricetta_originale')&&(!state.onlyLocal||(r.regioni?.length || (r.tipicita && r.luogoEstero)))&&(!state.onlyTraditional||['tradizione_locale','creato_in_loco','variante_locale'].includes(r.tipicita))&&(state.region==='tutte'||(r.regioni||[]).includes(state.region))&&(state.country==='tutti'||r.paese===state.country)&&(state.collection==='tutte'||(r.collezioni||[]).includes(state.collection))&&(!state.nameQuery||[r.nome,...(r.nomiAlternativi||[])].some(n=>accent(n).includes(accent(state.nameQuery)))));}
 function matching(r){
  const s=state.selected;
  if(state.mode==='desidero')return [...s].every(x=>inRecipe(r,x));
  if(!s.size)return false;
  const missing=missingIngredients(r);
  return selectedRequiredCount(r)>0 && missing.length<=state.maxMissing;
 }
 function sortedResults(){return baseResult().filter(matching).sort((a,b)=>{
  if(state.mode==='dispensa'){
   const ma=missingIngredients(a).length,mb=missingIngredients(b).length;
   if(ma!==mb)return ma-mb;
   const aa=selectedRequiredCount(a),bb=selectedRequiredCount(b);
   if(aa!==bb)return bb-aa;
  }
  if(state.selected.size){
   const locality=x=>!(x.regioni?.length || (x.tipicita && x.luogoEstero))?0:(x.ingredientiLocali||[]).some(i=>state.selected.has(i))?2:1;
   if(locality(a)!==locality(b))return locality(b)-locality(a);
  }
  return Number(b.inEvidenza)-Number(a.inEvidenza)||a.nome.localeCompare(b.nome,'it');
 });}
 function el(tag,text,klass){let node=document.createElement(tag);if(text!==null&&text!==undefined)node.textContent=text;if(klass)node.className=klass;return node;}
 function button(text,klass,fn){const b=el('button',text,klass);b.type='button';b.addEventListener('click',fn);return b;}
 function clearIngredientSearch(){
  state.ingQuery='';
  $('ingredientSearch').value='';
 }
 function toggle(name){
  if(name===STROH_ANY && state.mode==='dispensa')return;
  if(name===STROH_ANY){for(const v of ['Stroh 40','Stroh 60','Stroh 80'])state.selected.delete(v);}
  else if(isStrohGrade(name))state.selected.delete(STROH_ANY);
  state.selected.has(name)?state.selected.delete(name):state.selected.add(name);
  clearIngredientSearch();
  state.visible=21;
  render();
 }
 function ingredientsUI(){
  const sel=$('selected');sel.replaceChildren();
  if(!state.selected.size)sel.append(el('span','Nessun ingrediente selezionato','muted'));
  else for(let name of [...state.selected].sort((a,b)=>a.localeCompare(b,'it')))sel.append(button(name+' ×','',()=>toggle(name)));
  const container=$('ingredientList');container.replaceChildren();
  const query=accent(state.ingQuery);const eligible=ingredients.filter(i=>(!query||matchesIngredient(i,query))&&(state.ingCategory==='tutti'||classify(i)===state.ingCategory));
  const baseline=baseResult().filter(matching);
  const viable=new Set(baseline.flatMap(allIngredients));
  // Esamina l'intero catalogo: se non è compatibile con la selezione corrente, non rendere un chip cliccabile.
  for(let i of eligible){
   const active=state.selected.has(i),isGarnish=garnishes.has(i)&&!baseIngredients.has(i),chip=button(i,`chip${active?' selected-chip':''}${isGarnish?' garnish-chip':''}`,()=>toggle(i));
   chip.setAttribute('aria-pressed',String(active));
   if(isGarnish)chip.setAttribute('title','Usato come guarnizione; non obbligatorio nella modalità dispensa');
   else if(aliases[i]?.length)chip.setAttribute('title','Altri nomi: '+aliases[i].join(', '));
   if((state.mode==='dispensa'&&i===STROH_ANY)||(state.mode==='desidero'&&!active&&state.selected.size>0&&!viable.has(i)))chip.disabled=true;
   container.append(chip);
  }
  if(!eligible.length)container.append(el('span','Nessun ingrediente in questa categoria.','muted'));
 }
 function card(r){
  const wrapper=el('article',null,'cocktail-card');
  const top=el('div',null,'card-upper');const badges=el('div',null,'badge-line');
  badges.append(el('span',r.tipo==='IBA'?'IBA · '+r.categoria:'Fuori lista IBA','tag'+(r.tipo==='IBA'?'':' extra')));
  if(r.analcolico)badges.append(el('span','Analcolico','tag free'));
  if(r.verificaRicetta?.esito==='confrontata_con_ricetta_originale')badges.append(el('span','Ricetta ricontrollata','tag verified'));
  if(r.regioni?.length)badges.append(el('span','📍 '+r.regioni.join(' · '),'tag territory'));
  else if(r.paese)badges.append(el('span','🌍 '+r.paese,'tag territory'));
  if((r.collezioni||[]).includes('Proibizionismo'))badges.append(el('span','Proibizionismo','tag era'));
  if(r.gruppoFonte)badges.append(el('span',r.gruppoFonte,'tag source'));
  if(Number.isFinite(r.valutazioneTipsy))badges.append(el('span',`★ ${r.valutazioneTipsy.toFixed(1)}/5 · ${r.numeroValutazioniTipsy} su Tipsy`,'tag rating')); 
  if(r.tipoBevanda==='bevanda_tradizionale')badges.append(el('span','Bevanda locale','tag regional-drink'));
  top.append(badges);wrapper.append(top);wrapper.append(el('h3',r.nome,'card-name'));
  const missing=missingIngredients(r);
  if(state.mode==='dispensa'&&missing.length)wrapper.append(el('span',`Mancano ${missing.length}: ${missing.join(', ')}`,'tag missing'));
  wrapper.append(el('div','Ingredienti della ricetta','card-label'));
  const ingredientsList=el('div',null,'ingredients');
  for(const name of r.ingredienti){ingredientsList.append(el('span',name,'ing'+((hasSpecificIngredient(r,name)||(state.mode==='desidero'&&isStrohGrade(name)&&state.selected.has(STROH_ANY)))?' have':state.mode==='dispensa'?' need':'')));}
  wrapper.append(ingredientsList);
  if(r.facoltativi?.length){
   wrapper.append(el('div','Facoltativi','card-label'));
   const optional=el('div',null,'ingredients');
   for(const name of r.facoltativi)optional.append(el('span',name,'ing optional-ing'));
   wrapper.append(optional);
  }
  if(r.guarnizione?.length){
   wrapper.append(el('div',r.guarnizioniAlternative?'Guarnizione — scegli una delle alternative':'Guarnizione','card-label'));
   const garn=el('div',null,'ingredients');
   for(const name of r.guarnizione){
    const chip=el('span',name,'ing garnish-ing'+(state.selected.has(name)?' have':''));
    const detail=r.dettagliGuarnizione?.[name];
    const optional=(r.guarnizioniFacoltative||[]).includes(name);
    if(detail||optional){chip.title=[detail||name,optional?'Facoltativa nella versione documentata':''].filter(Boolean).join(' · ');}
    garn.append(chip);
   }
   wrapper.append(garn);
   // Quantità e modalità della guarnizione appartengono alla ricetta, mai ai chip di selezione.
   if(r.dettagliGuarnizione && Object.keys(r.dettagliGuarnizione).length){
    const lines=[];
    for(const name of r.guarnizione){
     const how=r.dettagliGuarnizione?.[name];
     const optional=(r.guarnizioniFacoltative||[]).includes(name);
     if(how||optional) lines.push(name+': '+(how||name)+(optional?' (facoltativa)':''));
    }
    if(lines.length)wrapper.append(el('p','Presentazione: '+lines.join(' · '),'mini-help'));
   }
   if(r.gruppiAlternativiGuarnizione?.length){
    wrapper.append(el('p','Alternative nella stessa ricetta: '+r.gruppiAlternativiGuarnizione.map(g=>g.join(' oppure ')).join('; '),'mini-help'));
   }
  }
  const details=el('div',null,'card-bottom'),item=el('details');item.append(el('summary','Dosi, note e fonte'));
  if(r.storiaLocale){item.append(el('p',(r.citta?r.citta+' · ':'')+r.storiaLocale));}
  if(r.collezioni?.length)item.append(el('p','Collezioni: '+r.collezioni.join(' · ')));
  if(r.paese)item.append(el('p','Paese nella classificazione editoriale: '+r.paese));
  if(r.nomiAlternativi?.length)item.append(el('p','Nomi precedenti cercabili: '+r.nomiAlternativi.join(' · ')));
  if(Number.isFinite(r.valutazioneTipsy))item.append(el('p',`Valutazione della versione Tipsy: ${r.valutazioneTipsy.toFixed(1)}/5, da ${r.numeroValutazioniTipsy} recensioni (rilevata il ${r.dataValutazioneTipsy}). Non è una valutazione indipendente della versione IBA.`));
  if(r.notaValutazioneTipsy)item.append(el('p','Nota sulla valutazione Tipsy: '+r.notaValutazioneTipsy));
  if(r.notaRicetta)item.append(el('p','Nota sulla ricetta: '+r.notaRicetta));
  if(r.preparazioneSintetica)item.append(el('p','Preparazione: '+r.preparazioneSintetica));
  if(r.verificaRicetta?.esito==='confrontata_con_ricetta_originale')item.append(el('p','Verifica puntuale effettuata il '+r.verificaRicetta.data+'. Controlla le fonti indicate per la versione selezionata.'));
  else if(r.verificaRicetta?.esito==='confrontata_parzialmente')item.append(el('p','Verifica parziale: gli ingredienti sono stati confrontati con la fonte, ma le dosi sono assenti o incongruenti. Non usare quantità presunte.'));
  else item.append(el('p','Verifica esterna indipendente non ancora completata in questa revisione. Controlla la fonte prima di preparare o pubblicare la ricetta.'));
  if(r.alternativeConsentite)item.append(el('p','Sostituzioni previste dalla fonte: '+Object.entries(r.alternativeConsentite).map(([k,v])=>k+' → '+v.join(' oppure ')).join('; ')));
  if(r.porzioniFonte)item.append(el('p','Quantità della fonte: '+r.porzioniFonte));
  if(r.statoDosi==='non_specificate')item.append(el('p','Dosi non indicate dalla fonte: ingredienti documentati, proporzioni da verificare prima della preparazione.'));
  else if(r.statoDosi==='parziali')item.append(el('p','Dosi parziali: non sono specificate tutte le quantità.')); 
  if((r.variantiStroh||[]).length)item.append(el('p','Gradazioni Stroh ammesse dalla fonte: '+r.variantiStroh.join(' / ')+'. Controlla nelle note le dosi alternative.'));
  if(r.tipicita){const kinds={tradizione_locale:'Tradizione locale documentata',creato_in_loco:'Creato nel territorio',variante_locale:'Variante locale',reinterpretazione:'Interpretazione contemporanea',ispirazione_territoriale:'Ispirato al territorio, non nato lì'};item.append(el('p','Legame territoriale: '+(kinds[r.tipicita]||r.tipicita)));}
  if(r.facoltativi.length)item.append(el('p','Facoltativi: '+r.facoltativi.join(', ')));
  if(r.dettagliIngredienti&&Object.keys(r.dettagliIngredienti).length)item.append(el('p','Forma degli ingredienti nella ricetta: '+Object.entries(r.dettagliIngredienti).map(([k,v])=>k+' → '+v).join(' · ')));
  if(r.guarnizione.length)item.append(el('p','Guarnizione (ricercabile ma facoltativa nella dispensa): '+r.guarnizione.join(r.guarnizioniAlternative?' OPPURE ':', ')));
  const amounts=Object.entries(r.dosi);
  if(amounts.length)item.append(el('p','Dosi della versione documentata: '+amounts.map(([k,v])=>`${v} ${k}`).join(' · ')));
  if(r.nome==='Zombie')item.append(el('p',"La ricetta IBA usa Donn's Mix: 2 parti di succo di pompelmo giallo e una parte di sciroppo di cannella. È un preparato composto, non due ulteriori dosi separate."));
  if(r.nome==='Porn Star Martini')item.append(el('p','Lo champagne si serve a parte, non si miscela direttamente nel cocktail.'));
  if(r.statoFonte==='raccolta_quantita_documentate')item.append(el('p','Ingredienti e dosi verificati nella raccolta della fonte; la scheda individuale non è stata consultabile. Controllare la ricetta originale prima della preparazione.'));
  if(!['scheda_verificata','ricetta_dosi_documentate','ingredienti_documentati_dosi_incomplete','raccolta_quantita_documentate'].includes(r.statoFonte))item.append(el('p',r.tipo==='IBA'?'Ingredienti trascritti per il catalogo: verificare quantità e varianti nella scheda IBA.':r.statoFonte==='fonte_collezione'?'Ricetta ricavata dalla raccolta della fonte: ingredienti e varianti da ricontrollare sulla pagina specifica prima della pubblicazione.':'Integrazione editoriale: ricetta/variante da confrontare con una fonte specifica prima della pubblicazione.'));
  if(r.fonte){const link=el('a','Apri la ricetta ↗');link.href=r.fonte;link.target='_blank';link.rel='noopener noreferrer';item.append(link);}
  if(r.fonteValutazioneTipsy && r.fonteValutazioneTipsy!==r.fonte){const link=el('a','Vedi versione e valutazione Tipsy ↗');link.href=r.fonteValutazioneTipsy;link.target='_blank';link.rel='noopener noreferrer';item.append(link);}
  if(r.fonteTerritoriale && r.fonteTerritoriale!==r.fonte){const link=el('a','Fonte turistica ↗');link.href=r.fonteTerritoriale;link.target='_blank';link.rel='noopener noreferrer';item.append(link);}
  if(r.fonteDosi && ![r.fonte,r.fonteTerritoriale].includes(r.fonteDosi)){const link=el('a','Dosi ufficiali ↗');link.href=r.fonteDosi;link.target='_blank';link.rel='noopener noreferrer';item.append(link);}
  details.append(item);wrapper.append(details);return wrapper;
 }
 function resultsUI(){
  const results=sortedResults();$('count').textContent=results.length;
  $('status').textContent=state.mode==='dispensa'&&!state.selected.size?'Seleziona almeno un ingrediente che hai in casa.':state.mode==='desidero'&&!state.selected.size?'Scopri i classici e le specialità locali d’Italia e del mondo, oppure scegli uno o più ingredienti.':results.length?'Risultati compatibili: le specialità del territorio associate agli ingredienti scelti sono mostrate per prime.':'Nessun risultato: prova a togliere un ingrediente o ad allargare i filtri territoriali.';
  const box=$('cards');box.replaceChildren();
  for(let r of results.slice(0,state.visible))box.append(card(r));
  if(results.length===0)box.append(el('div','Nessuna corrispondenza. Prova una combinazione diversa.','no-results'));
  $('loadMore').classList.toggle('hidden',results.length<=state.visible);
  $('loadMore').textContent=`Mostra altri cocktail (${results.length-state.visible}) ↓`;
 }
 function render(){ingredientsUI();resultsUI();$('missingLabel').classList.toggle('hidden',state.mode!=='dispensa');
  $('modeDesidero').classList.toggle('active',state.mode==='desidero');$('modeDispensa').classList.toggle('active',state.mode==='dispensa');
  $('modeDesidero').setAttribute('aria-pressed',String(state.mode==='desidero'));$('modeDispensa').setAttribute('aria-pressed',String(state.mode==='dispensa'));
  $('modeHelp').textContent=state.mode==='desidero'?'Puoi scegliere anche le guarnizioni: i cocktail compatibili le mostreranno. Gli ingredienti scelti devono comparire nella ricetta o nelle guarnizioni.':'Solo gli ingredienti obbligatori sono necessari; guarnizioni escluse. Per Stroh seleziona la gradazione effettiva (40, 60 o 80): non sono intercambiabili se la fonte non lo indica. Mostriamo cocktail con al massimo 1–2 ingredienti mancanti.';
 }
 $('modeDesidero').addEventListener('click',()=>{state.mode='desidero';state.visible=21;render()});
 $('modeDispensa').addEventListener('click',()=>{state.mode='dispensa';state.selected.delete(STROH_ANY);state.visible=21;render()});
 function resetAllFilters(){
  // Ripristina l'intero stato dell'app, non solo i chip degli ingredienti.
  state.selected.clear();
  state.mode='desidero';
  state.ingQuery='';state.ingCategory='tutti';state.nameQuery='';
  state.onlyIBA=false;state.onlyNA=false;state.onlyVerified=false;state.onlyLocal=false;state.onlyTraditional=false;
  state.region='tutte';state.country='tutti';state.collection='tutte';
  state.maxMissing=0;state.visible=21;
  $('ingredientSearch').value='';$('ingredientCategory').value='tutti';
  $('nameSearch').value='';
  $('onlyIba').checked=false;$('onlyAlcoholFree').checked=false;$('onlyVerified').checked=false;
  $('onlyLocal').checked=false;$('onlyTraditional').checked=false;
  $('regionFilter').value='tutte';$('countryFilter').value='tutti';
  $('collectionFilter').value='tutte';$('missingLimit').value='0';
  render();
 }
 $('clear').addEventListener('click',resetAllFilters);
 $('ingredientSearch').addEventListener('input',e=>{state.ingQuery=e.target.value;ingredientsUI()});
 $('ingredientCategory').addEventListener('change',e=>{state.ingCategory=e.target.value;ingredientsUI()});
 $('nameSearch').addEventListener('input',e=>{state.nameQuery=e.target.value;state.visible=21;render()});
 $('onlyIba').addEventListener('change',e=>{state.onlyIBA=e.target.checked;state.visible=21;render()});
 $('onlyAlcoholFree').addEventListener('change',e=>{state.onlyNA=e.target.checked;state.visible=21;render()});
 $('onlyVerified').addEventListener('change',e=>{state.onlyVerified=e.target.checked;state.visible=21;render()});
 $('onlyLocal').addEventListener('change',e=>{state.onlyLocal=e.target.checked;state.visible=21;render()});
 $('onlyTraditional').addEventListener('change',e=>{state.onlyTraditional=e.target.checked;state.visible=21;render()});
 $('regionFilter').addEventListener('change',e=>{state.region=e.target.value;state.visible=21;render()});
 $('countryFilter').addEventListener('change',e=>{state.country=e.target.value;state.visible=21;render()});
 $('collectionFilter').addEventListener('change',e=>{state.collection=e.target.value;state.visible=21;render()});
 $('missingLimit').addEventListener('change',e=>{state.maxMissing=Number(e.target.value);state.visible=21;render()});
 $('loadMore').addEventListener('click',()=>{state.visible+=21;resultsUI()});
 render();
})();
