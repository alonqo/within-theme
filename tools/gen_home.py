# Builds sections/within-home.liquid (homepage-only blocks, new structure) + templates/index.json
import json, os, re
SP=os.path.dirname(os.path.abspath(__file__))
ns={}; exec(open(os.path.join(SP,'gen.py')).read(), ns)
scss, js, scope = ns['scss'], ns['js'], ns['scope']
T,TA,IMG,CB,PADS,img,I = [ns[k] for k in 'T TA IMG CB PADS img I'.split()]
def U(i,l): return {"type":"url","id":i,"label":l}
def R(i,l,mn,mx,st,d,unit=None):
    r={"type":"range","id":i,"label":l,"min":mn,"max":mx,"step":st,"default":d}
    if unit: r["unit"]=unit
    return r
PAD=' style="--pt:{{ block.settings.padding_top }}px;--pb:{{ block.settings.padding_bottom }}px;"'
EB='{% if block.settings.eyebrow != blank %}<p class="wa-eyebrow">{{ block.settings.eyebrow }}</p>{% endif %}'
BTN='{% if block.settings.cta_label != blank %}<a class="wa-btn" href="{{ block.settings.cta_url | default: \'#\' }}">{{ block.settings.cta_label }}</a>{% endif %}'
LNK='{% if block.settings.link_label != blank %}<a class="wa-link" href="{{ block.settings.link_url | default: \'#\' }}">{{ block.settings.link_label }}</a>{% endif %}'
def IM(pick,url,cls='',w=1600,alt=''):
    return ('{%% if block.settings.%s != blank %%}<img class="%s" src="{{ block.settings.%s | image_url: width: %d }}" alt="{{ block.settings.%s.alt | escape }}" loading="lazy">'
            '{%% elsif block.settings.%s != blank %%}<img class="%s" src="{{ block.settings.%s }}" alt="%s" loading="lazy">{%% endif %%}')%(pick,cls,pick,w,pick,url,cls,url,alt)
def DIM(p,u,cls='',w=1200):
    return ('{%% if %s != blank %%}<img class="%s" src="{{ %s | image_url: width: %d }}" alt="{{ %s.alt | escape }}" loading="lazy">'
            '{%% elsif %s != blank %%}<img class="%s" src="{{ %s }}" alt="" loading="lazy">{%% endif %%}')%(p,cls,p,w,p,u,cls,u)

body='''
<div class="wa-root wh">
{%- for block in section.blocks -%}
{%- case block.type -%}

{%- when 'home_hero' -%}
<section class="wh-hero{% if block.settings.align_right %} wh-right{% endif %}" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wh-hero-media" style="--fx:{{ block.settings.focus_x }}%">'''+IM('image','image_url','wh-cover',2400)+'''</div>
  <div class="wh-hero-shade"></div>
  <div class="wh-hero-in"><div class="wh-hero-copy wa-reveal">'''+EB+'''
    <h1 class="wh-hero-t">{{ block.settings.heading }}</h1>
    {% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}
    <div class="wa-hero-btns">'''+BTN+LNK+'''</div>
  </div></div>
</section>

{%- when 'marquee' -%}
{%- assign mq = block.settings.items | newline_to_br | split: '<br />' -%}
<div class="wh-mq{% if block.settings.accent %} wh-mq-accent{% endif %}" {{ block.shopify_attributes }} style="--mq:{{ block.settings.speed }}s">
  <div class="wh-mq-track">{%- for r in (1..2) -%}{%- for it in mq -%}{%- assign t = it | strip -%}{%- if t != blank -%}<span>{{ t }}</span><i aria-hidden="true"></i>{%- endif -%}{%- endfor -%}{%- endfor -%}</div>
</div>

{%- when 'scroll_text' -%}
<section class="wa-sect wh-st" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">'''+EB+'''<p class="wh-st-p" data-st>{{ block.settings.text }}</p></div>
</section>

{%- when 'bento' -%}
<section class="wa-sect wh-bento-s" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-center wa-reveal" style="margin-bottom:44px">'''+EB+'''{% if block.settings.heading != blank %}<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% endif %}</div>
    <div class="wh-bento">
    {%- for i in (1..6) -%}
      {%- assign bk = 't' | append: i | append: '_big' -%}{%- assign tk = 't' | append: i | append: '_title' -%}{%- assign xk = 't' | append: i | append: '_text' -%}
      {%- assign pk = 't' | append: i | append: '_image' -%}{%- assign uk = 't' | append: i | append: '_image_url' -%}
      {%- assign p = block.settings[pk] -%}{%- assign u = block.settings[uk] -%}
      <div class="wh-tile wh-t{{ i }}{% if p != blank or u != blank %} wh-has-img{% endif %} wa-reveal" style="--d:{{ forloop.index0 | times: 0.06 }}s">
        '''+DIM('p','u','wh-tile-img',1200)+'''
        <div class="wh-tile-c">
          {%- if block.settings[bk] != blank -%}<p class="wh-big">{{ block.settings[bk] }}</p>{%- endif -%}
          {%- if block.settings[tk] != blank -%}<h3>{{ block.settings[tk] }}</h3>{%- endif -%}
          {%- if block.settings[xk] != blank -%}<p class="wh-tile-x">{{ block.settings[xk] }}</p>{%- endif -%}
        </div>
      </div>
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'ritual' -%}
<section class="wa-sect wh-rit-s{% if block.settings.tinted %} wa-tint{% endif %}" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wh-head wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub wa-left">{{ block.settings.sub }}</p>{% endif %}</div>
    <div class="wh-rit">
    {%- for i in (1..3) -%}
      {%- assign tk = 'c' | append: i | append: '_title' -%}{%- assign xk = 'c' | append: i | append: '_text' -%}{%- assign lk = 'c' | append: i | append: '_label' -%}
      {%- assign pk = 'c' | append: i | append: '_image' -%}{%- assign uk = 'c' | append: i | append: '_image_url' -%}
      {%- assign p = block.settings[pk] -%}{%- assign u = block.settings[uk] -%}
      {%- if block.settings[tk] != blank -%}
      <article class="wh-rit-c wa-reveal" style="--d:{{ forloop.index0 | times: 0.1 }}s">
        <div class="wh-rit-img">'''+DIM('p','u','',900)+'''{%- if block.settings[lk] != blank -%}<span class="wh-chip">{{ block.settings[lk] }}</span>{%- endif -%}</div>
        <h3>{{ block.settings[tk] }}</h3><p>{{ block.settings[xk] }}</p>
      </article>
      {%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'compare' -%}
<section class="wa-sect" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wa-center wa-reveal" style="margin-bottom:44px">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}</div>
    <div class="wh-cmp wa-reveal" role="table">
      <div class="wh-cmp-r wh-cmp-h" role="row"><span role="columnheader"></span><span class="wh-cmp-w" role="columnheader">{{ block.settings.col_a }}</span><span role="columnheader">{{ block.settings.col_b }}</span><span role="columnheader">{{ block.settings.col_c }}</span></div>
      {%- for i in (1..7) -%}
        {%- assign lk = 'r' | append: i | append: '_label' -%}
        {%- if block.settings[lk] != blank -%}
        {%- assign ak = 'r' | append: i | append: '_a' -%}{%- assign bk = 'r' | append: i | append: '_b' -%}{%- assign ck = 'r' | append: i | append: '_c' -%}
        <div class="wh-cmp-r{% if forloop.last %} wh-cmp-last{% endif %}" role="row"><span class="wh-cmp-l" role="rowheader">{{ block.settings[lk] }}</span><span class="wh-cmp-w" role="cell">{{ block.settings[ak] }}</span><span role="cell">{{ block.settings[bk] }}</span><span role="cell">{{ block.settings[ck] }}</span></div>
        {%- endif -%}
      {%- endfor -%}
    </div>
    {% if block.settings.cta_label != blank %}<div class="wa-btn-row wa-reveal">'''+BTN+'''</div>{% endif %}
  </div>
</section>

{%- when 'banner' -%}
<section class="wa-sect" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wh-ban wa-reveal">
      '''+IM('image','image_url','wh-cover',2000)+'''
      <div class="wh-ban-c">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.text != blank %}<p class="wa-sub wa-left">{{ block.settings.text }}</p>{% endif %}<div class="wa-hero-btns">'''+BTN+LNK+'''</div></div>
    </div>
  </div>
</section>

{%- when 'newsletter' -%}
{%- assign nf = 'wh-nl-' | append: block.id -%}
<section class="wa-sect" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wh-nl wa-reveal">'''+EB+'''
      <h2 class="wa-h2">{{ block.settings.heading }}</h2>
      {% if block.settings.text != blank %}<p class="wa-sub">{{ block.settings.text }}</p>{% endif %}
      {%- form 'customer', id: nf -%}
        <input type="hidden" name="contact[tags]" value="newsletter">
        {%- if form.posted_successfully? -%}<p class="wh-nl-ok" role="status">{{ block.settings.success }}</p>{%- else -%}
        <div class="wh-nl-f"><label class="wh-sr" for="{{ nf }}-email">Email</label><input id="{{ nf }}-email" type="email" name="contact[email]" placeholder="La tua email" autocomplete="email" required><button class="wa-btn" type="submit">{{ block.settings.button_label }}</button></div>
        {%- if form.errors -%}<p class="wh-nl-err" role="alert">{{ form.errors | default_errors }}</p>{%- endif -%}
        {%- endif -%}
      {%- endform -%}
      {% if block.settings.note != blank %}<p class="wh-nl-note">{{ block.settings.note }}</p>{% endif %}
    </div>
  </div>
</section>

{%- endcase -%}
{%- endfor -%}
</div>
'''

CSS='''
.wh .wa-sect{padding:var(--pt,120px) 22px var(--pb,120px)}
.wh-hero{position:relative;display:flex;align-items:flex-end;min-height:min(92vh,880px);overflow:hidden;background:var(--dark);color:#fff;padding:var(--pt,0px) 0 0}
.wh-hero-media{position:absolute;inset:0}
.wh-cover{position:absolute;inset:0;width:100%;height:100%!important;object-fit:cover}
.wh-hero-media .wh-cover{object-position:var(--fx,70%) 50%}
.wh-hero-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,22,20,.74) 0%,rgba(14,22,20,.38) 46%,rgba(14,22,20,0) 72%),linear-gradient(0deg,rgba(14,22,20,.5) 0%,rgba(14,22,20,0) 42%)}
.wh-right .wh-hero-shade{background:linear-gradient(270deg,rgba(14,22,20,.74) 0%,rgba(14,22,20,.38) 46%,rgba(14,22,20,0) 72%),linear-gradient(0deg,rgba(14,22,20,.5) 0%,rgba(14,22,20,0) 42%)}
.wh-hero-in{position:relative;z-index:2;width:100%;max-width:var(--wide);margin:0 auto;padding:0 22px var(--pb,88px)}
.wh-right .wh-hero-in{display:flex;justify-content:flex-end}
.wh-hero-copy{max-width:580px}
.wh-hero-t{font-size:clamp(2.8rem,6.6vw,5.4rem);font-weight:650;line-height:1;letter-spacing:-.035em;margin:0 0 20px;color:#fff}
.wh-hero .wa-eyebrow{color:var(--accent-hi)}
.wh-hero .wa-sub{color:rgba(255,255,255,.88);margin:0;max-width:34ch}
.wh-hero .wa-hero-btns{justify-content:flex-start}
.wh-hero .wa-link{color:#fff}
.wa-hero-btns{display:flex;gap:26px;align-items:center;flex-wrap:wrap;margin-top:32px}
.wh-mq{overflow:hidden;background:var(--dark);color:var(--on-dark);padding:20px 0;white-space:nowrap}
.wh-mq-accent{background:var(--accent);color:#fff}
.wh-mq-track{display:inline-flex;align-items:center;gap:28px;padding-left:28px;animation:wh-mq var(--mq,40s) linear infinite}
.wh-mq span{font-size:1.02rem;font-weight:550;letter-spacing:.01em}
.wh-mq i{width:6px;height:6px;border-radius:50%;background:var(--accent-hi);flex:0 0 auto}
.wh-mq-accent i{background:#fff}
@keyframes wh-mq{to{transform:translateX(-50%)}}
.wh-st-p{font-size:clamp(2rem,4.6vw,3.7rem);font-weight:650;line-height:1.12;letter-spacing:-.03em;margin:0;color:var(--ink)}
.wh-st-p .w{transition:opacity .25s linear}
.wh-bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:270px;gap:16px}
.wh-tile{position:relative;overflow:hidden;border-radius:var(--r-lg);background:var(--bg-2);padding:30px;display:flex;flex-direction:column;justify-content:flex-start}
.wh-tile-img{position:absolute;inset:0;width:100%;height:100%!important;object-fit:cover;transition:transform .8s cubic-bezier(.16,.8,.26,1)}
.wh-tile:hover .wh-tile-img{transform:scale(1.04)}
.wh-tile-c{position:relative;z-index:2;max-width:30ch}
.wh-tile h3{margin:0 0 6px;font-size:1.3rem;font-weight:600;letter-spacing:-.015em;color:var(--ink)}
.wh-tile-x{margin:0;color:var(--muted);font-size:1rem;line-height:1.4}
.wh-big{margin:0 0 8px;font-size:clamp(2.4rem,3.6vw,3.4rem);font-weight:650;letter-spacing:-.04em;line-height:1;color:var(--accent)}
.wh-t1{grid-column:span 2;grid-row:span 2}
.wh-t4{grid-column:span 2}
.wh-t5{grid-column:span 2;background:var(--dark)}
.wh-t5 h3{color:#fff}.wh-t5 .wh-tile-x{color:var(--on-dark-mut)}.wh-t5 .wh-big{color:var(--accent-hi)}
.wh-t6{grid-column:span 2;background:var(--accent)}
.wh-t6 h3,.wh-t6 .wh-big{color:#fff}.wh-t6 .wh-tile-x{color:rgba(255,255,255,.86)}
.wh-t5,.wh-t6{justify-content:flex-end}
.wh-head{display:grid;grid-template-columns:1fr 1fr;gap:24px 56px;align-items:end;margin-bottom:48px}
.wh-head .wa-h2{margin:0}
.wh-head .wa-eyebrow{grid-column:1/-1;margin:0}
.wh-rit{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.wh-rit-img{position:relative;border-radius:var(--r-lg);overflow:hidden;aspect-ratio:4/5;background:var(--bg-2);margin-bottom:18px}
.wh-rit-img img{width:100%;height:100%!important;object-fit:cover;transition:transform .8s cubic-bezier(.16,.8,.26,1)}
.wh-rit-c:hover .wh-rit-img img{transform:scale(1.04)}
.wh-chip{position:absolute;left:14px;top:14px;padding:7px 12px;border-radius:var(--r-pill);background:rgba(255,255,255,.82);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);font-size:.78rem;font-weight:650;color:var(--ink)}
.wh-rit-c h3{margin:0 0 6px;font-size:1.3rem;font-weight:600;letter-spacing:-.015em}
.wh-rit-c p{margin:0;color:var(--muted);font-size:1.02rem}
.wh-cmp{border-radius:var(--r-lg);border:1px solid var(--line);overflow:hidden;background:var(--bg)}
.wh-cmp-r{display:grid;grid-template-columns:minmax(0,1.15fr) repeat(3,minmax(0,1fr));border-bottom:1px solid var(--line-soft)}
.wh-cmp-r span{min-width:0;overflow-wrap:break-word;hyphens:auto;line-height:1.35}
.wh-cmp-last{border-bottom:0}
.wh-cmp-r span{padding:18px 20px;font-size:1rem;color:var(--muted);display:flex;align-items:center}
.wh-cmp-h span{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);padding-top:22px;padding-bottom:22px}
.wh-cmp-l{color:var(--ink)!important;font-weight:600}
.wh-cmp-r .wh-cmp-w{background:rgba(168,67,46,.07);color:var(--ink);font-weight:600}
.wh-cmp-h .wh-cmp-w{background:var(--accent);color:#fff}
.wh-ban{position:relative;min-height:540px;border-radius:var(--r-lg);overflow:hidden;background:var(--dark);display:flex;align-items:flex-end}
.wh-ban::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(14,22,20,.78) 0%,rgba(14,22,20,.2) 55%,rgba(14,22,20,0) 75%)}
.wh-ban-c{position:relative;z-index:2;padding:clamp(28px,5vw,64px);max-width:640px;color:#fff}
.wh-ban-c .wa-h2{color:#fff}.wh-ban-c .wa-sub{color:rgba(255,255,255,.86)}.wh-ban-c .wa-eyebrow{color:var(--accent-hi)}.wh-ban-c .wa-link{color:#fff}
.wh-nl{text-align:center;background:var(--bg-2);border-radius:var(--r-lg);padding:clamp(36px,6vw,72px) clamp(22px,5vw,64px)}
.wh-nl form{margin-top:30px}
.wh-nl-f{display:flex;gap:10px;max-width:520px;margin:0 auto;background:var(--bg);border:1px solid var(--line);border-radius:var(--r-pill);padding:6px}
.wh-nl-f input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:1rem;padding:0 18px;color:var(--ink)}
.wh-nl-f input:focus{outline:none}
.wh-nl-f .wa-btn{min-height:46px;padding:0 24px}
.wh-nl-ok{margin:0;font-weight:600;color:#1f6b47}
.wh-nl-err{color:var(--accent);margin:12px 0 0}
.wh-nl-note{margin:16px 0 0;font-size:.8rem;color:var(--muted)}
.wh-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (prefers-reduced-motion:reduce){.wh-mq-track{animation:none}}
@media (max-width:860px){
.wh .wa-sect{padding:min(var(--pt,120px),80px) 20px min(var(--pb,120px),80px)}
.wh-hero{min-height:88vh}
.wh-hero-shade,.wh-right .wh-hero-shade{background:linear-gradient(0deg,rgba(14,22,20,.86) 0%,rgba(14,22,20,.5) 45%,rgba(14,22,20,.05) 75%)}
.wh-hero-in{padding:0 20px 56px}.wh-right .wh-hero-in{justify-content:flex-start}
.wh-bento{grid-template-columns:1fr 1fr;grid-auto-rows:210px;gap:12px}
.wh-tile{padding:20px}
.wh-t1{grid-column:span 2;grid-row:span 2}.wh-t4{grid-column:span 2}.wh-t5,.wh-t6{grid-column:span 1}
.wh-big{font-size:2.2rem}.wh-tile h3{font-size:1.05rem}.wh-tile-x{font-size:.86rem}
.wh-head{grid-template-columns:1fr;gap:12px}
.wh-rit{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin:0 -20px;padding:0 20px;scrollbar-width:none}
.wh-rit::-webkit-scrollbar{display:none}
.wh-rit-c{flex:0 0 78%;scroll-snap-align:start}
.wh-cmp-r{grid-template-columns:repeat(3,minmax(0,1fr))}.wh-cmp-h span:first-child{display:none}.wh-cmp-h span{padding:14px 12px;font-size:.64rem;letter-spacing:.05em;line-height:1.25}.wh-cmp-r span{padding:4px 12px 16px;font-size:.88rem;align-items:flex-start}.wh-cmp-r .wh-cmp-l{grid-column:1/-1;padding:14px 12px 6px;font-size:.68rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--accent)!important;background:transparent}
.wh-ban{min-height:480px}
.wh-nl-f{flex-direction:column;border-radius:20px;padding:8px}
.wh-nl-f input{padding:12px}
}
'''
scss2=scss+'\n'+scope(CSS)

ST_JS=r'''
var sts=[].slice.call(R.querySelectorAll('[data-st]'));
sts.forEach(function(p){p.innerHTML=p.textContent.trim().split(/\s+/).map(function(w){return '<span class="w">'+w.replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})+'</span>'}).join(' ');});
if(sts.length&&!reduce){var stk=false;function stu(){stk=false;sts.forEach(function(p){var r=p.getBoundingClientRect(),vh=innerHeight,pr=(vh*0.85-r.top)/(r.height+vh*0.35);pr=Math.max(0,Math.min(1,pr));var ws=p.querySelectorAll('.w'),n=ws.length;for(var i=0;i<n;i++){ws[i].style.opacity=(i/n<pr)?1:.16;}});}
addEventListener('scroll',function(){if(!stk){requestAnimationFrame(stu);stk=true;}},{passive:true});addEventListener('resize',stu);stu();}
'''
js2=js.replace("var GAP=12,EDGE=20;", ST_JS+"\nvar GAP=12,EDGE=20;",1)
assert ST_JS in js2

PR=lambda: PADS()
schema={"name":"Within · Home","tag":"section","class":"wa-section","max_blocks":30,
"settings":[s for s in ns['schema']['settings']],
"blocks":[
 {"type":"home_hero","name":"Hero a tutto schermo","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo","La pelle che avevi. Di nuovo tua."),TA("sub","Sottotitolo","x"),T("cta_label","Pulsante","Scopri Within"),U("cta_url","Link pulsante"),T("link_label","Link secondario",""),U("link_url","Link secondario · URL"),IMG("image","Immagine"),T("image_url","Immagine (link, usato se non carichi un file)",""),R("focus_x","Punto focale orizzontale",0,100,5,70,"%"),CB("align_right","Testo a destra",False),R("padding_top","Spazio sopra",0,200,4,0,"px"),R("padding_bottom","Spazio sotto il testo",0,200,4,88,"px")]},
 {"type":"marquee","name":"Nastro scorrevole","settings":[TA("items","Frasi (una per riga)","x"),R("speed","Velocità (secondi per giro)",10,90,5,40,"s"),CB("accent","Colore accento",False)]},
 {"type":"scroll_text","name":"Testo che si illumina","settings":[T("eyebrow","Sopra-titolo",""),TA("text","Testo","x")]+PR()},
 {"type":"bento","name":"Griglia bento","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo","")]+sum([[{"type":"header","content":"Riquadro %d%s"%(i,{1:" (grande, con immagine)",4:" (largo, con immagine)",5:" (scuro)",6:" (colore accento)"}.get(i,""))},T("t%d_big"%i,"Numero grande (opz.)",""),T("t%d_title"%i,"Titolo",""),TA("t%d_text"%i,"Testo","x"),IMG("t%d_image"%i,"Immagine (opz.)"),T("t%d_image_url"%i,"Immagine (link, opz.)","")] for i in range(1,7)],[])+PR()},
 {"type":"ritual","name":"Rituale (3 schede)","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),TA("sub","Sottotitolo","x")]+sum([[T("c%d_label"%i,"%d · etichetta"%i,""),T("c%d_title"%i,"%d · titolo"%i,""),TA("c%d_text"%i,"%d · testo"%i,"x"),IMG("c%d_image"%i,"%d · immagine"%i),T("c%d_image_url"%i,"%d · immagine (link)"%i,"")] for i in range(1,4)],[])+[CB("tinted","Sfondo tinta",False)]+PR()},
 {"type":"compare","name":"Confronto","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),TA("sub","Sottotitolo","x"),T("col_a","Colonna evidenziata","Within"),T("col_b","Colonna 2",""),T("col_c","Colonna 3","")]+sum([[T("r%d_label"%i,"Riga %d · voce"%i,""),T("r%d_a"%i,"Riga %d · colonna evidenziata"%i,""),T("r%d_b"%i,"Riga %d · colonna 2"%i,""),T("r%d_c"%i,"Riga %d · colonna 3"%i,"")] for i in range(1,8)],[])+[T("cta_label","Pulsante (opz.)",""),U("cta_url","Link pulsante")]+PR()},
 {"type":"banner","name":"Banner con immagine","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),TA("text","Testo","x"),T("cta_label","Pulsante",""),U("cta_url","Link pulsante"),T("link_label","Link secondario",""),U("link_url","Link secondario · URL"),IMG("image","Immagine"),T("image_url","Immagine (link)","")]+PR()},
 {"type":"newsletter","name":"Iscrizione newsletter","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),TA("text","Testo","x"),T("button_label","Pulsante","Iscriviti"),T("success","Messaggio di conferma","Grazie! Controlla la tua email."),T("note","Nota sotto il modulo","")]+PR()},
],
"presets":[{"name":"Within · Home","blocks":[{"type":"home_hero"}]}]}
for b in schema['blocks']:
    assert len(b['name'])<=25,b['name']
    for s in b['settings']:
        if s.get('default') in ("","x"): s.pop('default',None)
        if s.get('type')=='range': assert (s['default']-s['min'])%s['step']==0,(b['type'],s)

out='''{% comment %}
  Within · Home — sezione a blocchi per la homepage (struttura dedicata, diversa dalla product page).
{% endcomment %}
{% style %}
'''+scss2+'''
{% endstyle %}
'''+body+'''
<script>'''+js2+'''</script>

{% schema %}
'''+json.dumps(schema,ensure_ascii=False,indent=2)+'''
{% endschema %}
'''
REPO='/home/claude/within-theme'
open(REPO+'/sections/within-home.liquid','w').write(out); print('within-home',len(out))

# ---------- content
B="https://d8j0ntlcm91z4.cloudfront.net/user_3CoHflE6XwKC5XeJge3JDzQw5PH/hf_"
M=json.load(open(os.path.join(SP,'home_media.json')))
P='/products/within-collagene-marino'
blocks=[
 ("home_hero",{"eyebrow":"Within · Collagene marino da bere","heading":"La pelle che avevi. Di nuovo tua.","sub":"Un sachet al giorno per una pelle più compatta, idratata e luminosa. Dall'interno, dove la bellezza comincia.","cta_label":"Scopri Within","cta_url":P,"link_label":"Prossimi eventi →","link_url":"/pages/eventi","image_url":M['hero'],"focus_x":70}),
 ("marquee",{"items":"Collagene marino tripeptide\n5.000 mg in ogni sachet\n1 miliardo di fermenti lattici\nGusto mango e passion fruit\nZero retrogusto di pesce\nSoddisfatta o rimborsata 90 giorni"}),
 ("scroll_text",{"eyebrow":"Il nostro punto di vista","text":"Non vogliamo farti sembrare un'altra. Vogliamo che ti guardi allo specchio e ti riconosca. Più luminosa, più compatta, più tu."}),
 ("bento",{"eyebrow":"Dentro ogni sachet","heading":"Piccolo gesto. Grande differenza.",
   "t1_title":"Tutto quello che serve. In 25 ml.","t1_text":"Già liquido, già pronto. Lo apri, lo bevi, e la tua giornata comincia meglio.","t1_image_url":M['still'],
   "t2_big":"5.000 mg","t2_title":"Collagene marino","t2_text":"In ogni dose, dichiarato al milligrammo.",
   "t3_big":"3×","t3_title":"Più piccolo","t3_text":"Molecole sotto i 3.000 Dalton: tre volte più piccole del collagene generico.",
   "t4_title":"Sa di mango e passion fruit.","t4_text":"Un piacere, non un dovere.","t4_image_url":M['pour'],
   "t5_big":"1 mld","t5_title":"Fermenti lattici","t5_text":"Per una bellezza che parte dall'intestino.",
   "t6_big":"90 giorni","t6_title":"Per vedere la differenza","t6_text":"Se la tua pelle non cambia, ti rimborsiamo."}),
 ("ritual",{"eyebrow":"Il rituale","heading":"Si adatta alla tua giornata. Non il contrario.","sub":"Niente polveri, niente misurini, niente orari fissi. Solo 25 secondi per te, quando vuoi.",
   "c1_label":"Al mattino","c1_title":"Prima del caffè","c1_text":"Mentre la casa è ancora silenziosa. Il primo gesto gentile della giornata.","c1_image_url":M['r1'],
   "c2_label":"Fuori casa","c2_title":"In borsa, sempre","c2_text":"Ufficio, viaggio, pranzo con le amiche. Non serve acqua, non serve niente.","c2_image_url":M['r2'],
   "c3_label":"Il tuo momento","c3_title":"Dopo lo yoga","c3_text":"Una passeggiata, una lezione, una pausa. Venticinque secondi che sono solo tuoi.","c3_image_url":M['r3'],"tinted":True}),
 ("compare",{"eyebrow":"Fai il confronto","heading":"Perché Within è diverso.","sub":"Non tutti i collageni sono uguali. E una crema non arriva dove arriva Within.","col_a":"Within","col_b":"Collagene generico","col_c":"Creme anti-age",
   "r1_label":"Dove agisce","r1_a":"Dall'interno","r1_b":"Dall'interno","r1_c":"In superficie",
   "r2_label":"Dimensione molecole","r2_a":"Sotto i 3.000 Da","r2_b":"Spesso oltre 10.000 Da","r2_c":"—",
   "r3_label":"Fermenti lattici","r3_a":"1 miliardo","r3_b":"No","r3_c":"No",
   "r4_label":"Dosaggi dichiarati","r4_a":"Sì, al milligrammo","r4_b":"Non sempre","r4_c":"—",
   "r5_label":"Gusto","r5_a":"Mango e passion fruit","r5_b":"Spesso neutro o di pesce","r5_c":"—",
   "r6_label":"Formato","r6_a":"Sachet liquido pronto","r6_b":"Polvere o capsule","r6_c":"Vasetto",
   "r7_label":"Garanzia","r7_a":"90 giorni","r7_b":"Raramente","r7_c":"Raramente",
   "cta_label":"Provalo per 90 giorni","cta_url":P}),
 ("banner",{"eyebrow":"Dal vivo","heading":"Assaggialo con noi.","text":"Degustazioni e consulenze nelle farmacie e nei negozi partner. Trova la data più vicina e salvala nel tuo calendario.","cta_label":"Vedi gli eventi","cta_url":"/pages/eventi","image_url":B+"20261028_232314_16b8c81f-dc92-4970-afb7-b80afdfea592.png","padding_top":40,"padding_bottom":40}),
 ("newsletter",{"eyebrow":"La cerchia Within","heading":"Consigli per la tua pelle, una volta al mese.","text":"Novità, inviti agli eventi e offerte riservate alle iscritte.","button_label":"Iscriviti","success":"Grazie! Sei nella cerchia Within.","note":"Niente spam. Ti cancelli quando vuoi con un clic.","padding_top":80,"padding_bottom":120}),
 ("home_hero",{"eyebrow":"Inizia oggi","heading":"Il tuo primo sachet ti aspetta.","sub":"Provalo per 90 giorni. Se la tua pelle non cambia, ti restituiamo i soldi.","cta_label":"Scopri Within","cta_url":P,"link_label":"Leggi la nostra storia →","link_url":"/pages/chi-siamo","image_url":M['final'],"focus_x":75,"padding_bottom":96}),
]
defs={b['type']:{s['id']:s['default'] for s in b['settings'] if 'default' in s} for b in schema['blocks']}
bl={};order=[]
for n,(t,st) in enumerate(blocks,1):
    k='%s_%d'%(t,n); s=dict(defs[t]); s.update(st); bl[k]={'type':t,'settings':s}; order.append(k)
tpl={'sections':{'home':{'type':'within-home','blocks':bl,'block_order':order,'settings':{}}},'order':['home']}
open(REPO+'/templates/index.json','w').write('/*\n * Homepage Within — generato da tools/gen_home.py\n */\n'+json.dumps(tpl,ensure_ascii=False,indent=2))
print('index.json',len(order))
