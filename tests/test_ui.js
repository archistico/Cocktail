/* Test funzionali minimi dell'app offline senza browser / dipendenze. */
'use strict';
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.join(__dirname,'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'data/cocktails.json'),'utf8'));
class Element {
 constructor(tag='div') {this.tag=tag;this.children=[];this.listeners={};this.value='';this.textContent='';this.className='';this.disabled=false;this.checked=false;this.attributes={}; this._classes=new Set(); this.classList={toggle:(key,force)=>{const has=force===undefined?!this._classes.has(key):!!force;if(has)this._classes.add(key);else this._classes.delete(key);return has;}};}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=[...nodes];}
 addEventListener(type,fn){(this.listeners[type]??=[]).push(fn);}
 setAttribute(name,value){this.attributes[name]=value;}
 trigger(type,evt={}){for(const fn of this.listeners[type]??[])fn(evt);}
}
const elements=new Map();
const document={getElementById:(id)=>{if(!elements.has(id))elements.set(id,new Element('id:'+id));return elements.get(id);},createElement:(tag)=>new Element(tag)};
const window={COCKTAIL_CATALOG:data};
vm.runInNewContext(fs.readFileSync(path.join(root,'js/app.js'),'utf8'),{window,document,console});
const get=id=>document.getElementById(id), assert=(yes,msg)=>{if(!yes)throw new Error(msg)};
function contains(node,word){return node.children.filter(n=>n.textContent===word)}
function hasCard(name){
  for(let page=0;page<30;page++){
    if(get('cards').children.some(card=>card.children.some(node=>node.textContent===name))) return true;
    if(get('loadMore')._classes.has('hidden')) return false;
    get('loadMore').trigger('click');
  }
  return false;
}
function emitSearch(q){get('ingredientSearch').value=q;get('ingredientSearch').trigger('input',{target:{value:q}})}
function emitFilter(id,q){get(id).value=q;get(id).trigger('change',{target:{value:q}})}
// Test di regressione dei chip normalizzati e dei dettagli per-ricetta.
assert(get('totalCocktails').textContent===530,'530 cocktail');
assert(window.COCKTAIL_RESOLVE_ID('tipsy3-rudesheimer-kaffee')?.id==='tipsy-caffe-di-rudesheim','ID storico reindirizzato al caffè canonico');
assert(window.COCKTAIL_RESOLVE_ID('tipsy-caffe-di-rudesheim')?.nome==='Caffè di Rüdesheim','ID canonico risolto');
assert(get('totalIngredients').textContent===433,'433 ingredienti base');
assert(get('ingredientList').children.filter(n=>n.textContent==='Fernet').length===1,'Fernet unico');
assert(!get('ingredientList').children.some(n=>n.textContent==='fernet'),'fernet minuscolo assente');
function searchAndPick(term,expected){
  get('clear').trigger('click');emitSearch(term);
  const entries=get('ingredientList').children.filter(n=>n.textContent===expected);
  assert(entries.length===1,term+' restituisce solo '+expected+': '+entries.length);
  entries[0].trigger('click');
  assert(get('ingredientSearch').value==='','casella ricerca svuotata dopo selezione');
  assert(get('selected').children.some(n=>n.textContent===expected+' ×'),'selezione canonica');
}
for(const term of ['ciliegia al maraschino','ciliegie maraschino','ciliegina al maraschino (facoltativa)','2-3 ciliegine al maraschino']){
 searchAndPick(term,'Ciliegina al maraschino');
 assert(hasCard('Shirley Temple'),'Shirley Temple con ciliegine');
}
searchAndPick('Peach brandy','Brandy alla pesca');
assert(hasCard("Missionary's Downfall"),'Missionary’s Downfall IBA ricercabile da Peach brandy');
assert(get('ingredientList').children.every(n=>n.textContent!=='Peach brandy'),'nessun chip Peach brandy duplicato');
searchAndPick('3 chicchi di caffè','Chicchi di caffè');
assert(hasCard('Espresso Martini'),'espresso martini guarnizione');
searchAndPick('mora','More');
searchAndPick('tuorlo d’uovo',"Tuorlo d'uovo");
searchAndPick('jarabe de goma','Sciroppo di gomma');
searchAndPick('fernet','Fernet');
assert(hasCard('Hanky Panky'),'Hanky Panky trovato');
searchAndPick('Stroh 80','Stroh 80');
searchAndPick('Campari Soda','Campari Soda');
searchAndPick('Bitter rosso','Bitter rosso');
searchAndPick('Cocchi Americano Rosa','Cocchi Rosa');
searchAndPick('ciliegie al brandy','Ciliegina al brandy');
assert(hasCard('Rose (cocktail francese)'),'Rose con guarnizione brandy');
searchAndPick('oliva verde','Oliva');
assert(hasCard('Dry Martini'),'Dry Martini trovato tramite oliva');
get('clear').trigger('click');
get('nameSearch').value='Shirley Temple';get('nameSearch').trigger('input',{target:{value:'Shirley Temple'}});
const shirley=get('cards').children.find(card=>card.children.some(node=>node.textContent==='Shirley Temple'));
assert(shirley,'Shirley Temple card');
assert(shirley.children.some(node=>node.textContent.includes('2-3 ciliegine al maraschino')),'quantità visibile solo sulla card ricetta');
get('clear').trigger('click');
get('nameSearch').value='Espresso Martini';get('nameSearch').trigger('input',{target:{value:'Espresso Martini'}});
const espresso=get('cards').children.find(card=>card.children.some(node=>node.textContent==='Espresso Martini'));
assert(espresso.children.some(node=>node.textContent.includes('3 chicchi di caffè')),'3 chicchi mostrati sulla ricetta');
get('clear').trigger('click');
get('modeDispensa').trigger('click');
// una guarnizione non deve rendere una ricetta preparabile
emitSearch('Ciliegina al maraschino');const chip=get('ingredientList').children.find(n=>n.textContent==='Ciliegina al maraschino');chip.trigger('click');
assert(Number(get('count').textContent)===0,'la guarnizione non è ingrediente obbligatorio in dispensa');
get('clear').trigger('click');
for(const id of ['onlyIba','onlyAlcoholFree','onlyVerified','onlyLocal','onlyTraditional']){get(id).checked=true;get(id).trigger('change',{target:{checked:true}})}
emitFilter('regionFilter','Piemonte');emitSearch('fernet');
get('clear').trigger('click');
assert(get('ingredientSearch').value==='','reset search');
assert(Number(get('count').textContent)===530,'reset all results (530)');
for(const id of ['onlyIba','onlyAlcoholFree','onlyVerified','onlyLocal','onlyTraditional'])assert(get(id).checked===false,'reset checkbox '+id);
console.log('OK UI v3.6: unificazione chip, sinonimi, quantità guarnizioni sulla ricetta, ricerca, dispensa e reset totale');
