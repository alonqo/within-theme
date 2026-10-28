# Builds sections/within-site.liquid (generic Within blocks for home/pages) + page templates
import json, copy, re, os
SP=os.path.dirname(os.path.abspath(__file__))
ns={}
exec(open(os.path.join(SP,'gen.py')).read(), ns)   # also regenerates product section/template (idempotent)
scss, body, js, schema0 = ns['scss'], ns['body'], ns['js'], ns['schema']
T,TA,IMG,URL,CB,PADS,img,dimg,PAD,TINT,EB,I,V = [ns[k] for k in 'T TA IMG URL CB PADS img dimg PAD TINT EB I V'.split()]
def U(i,l): return {"type":"url","id":i,"label":l}
PROD='/products/within-collagene-marino'

# ---------- CTA links: optional url (empty = scroll to top like the product page)
body=body.replace('<a class="wa-btn wa-top" href="#">{{ block.settings.cta_label }}</a>',
 '<a class="wa-btn{% if block.settings.cta_url == blank %} wa-top{% endif %}" href="{% if block.settings.cta_url != blank %}{{ block.settings.cta_url }}{% else %}#{% endif %}">{{ block.settings.cta_label }}</a>')
body=body.replace('<a class="wa-link wa-top" href="#">{{ block.settings.link_label }}</a>',
 '<a class="wa-link{% if block.settings.link_url == blank %} wa-top{% endif %}" href="{% if block.settings.link_url != blank %}{{ block.settings.link_url }}{% else %}#{% endif %}">{{ block.settings.link_label }}</a>')
assert body.count('block.settings.cta_url')>=6 and 'link_url' in body

NEW=r"""
{%- when 'hero' -%}
<section class="wa-hero{% if block.settings.dark %} wa-dark{% endif %}" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner wa-center wa-reveal">'''+EB+'''
    <h1 class="wa-display wa-hero-t">{{ block.settings.heading }}</h1>
    {% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}
    {%- if block.settings.cta_label != blank or block.settings.link_label != blank -%}
    <div class="wa-hero-btns">
      {% if block.settings.cta_label != blank %}<a class="wa-btn" href="{{ block.settings.cta_url | default: '#' }}">{{ block.settings.cta_label }}</a>{% endif %}
      {% if block.settings.link_label != blank %}<a class="wa-link" href="{{ block.settings.link_url | default: '#' }}">{{ block.settings.link_label }}</a>{% endif %}
    </div>
    {%- endif -%}
  </div>
  {%- if block.settings.image != blank or block.settings.image_url != blank -%}
  <div class="wa-hero-media wa-reveal wa-blur">'''+img('image','image_url',w=2000)+'''</div>
  {%- endif -%}
</section>

{%- when 'statement' -%}
<section class="wa-sect wa-center{{ '' }}'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner wa-reveal">'''+EB+'''
    <p class="wa-big">{{ block.settings.statement }}</p>
    {% if block.settings.text != blank %}<div class="wa-stmt-text">{{ block.settings.text }}</div>{% endif %}
  </div>
  {%- if block.settings.image != blank or block.settings.image_url != blank -%}
  <div class="wa-wide"><div class="wa-hero-media wa-reveal">'''+img('image','image_url',w=1800)+'''</div></div>
  {%- endif -%}
</section>

{%- when 'product_spot' -%}
{%- assign sp = block.settings.product -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-feat{% if block.settings.reversed %} wa-rev{% endif %}">
      <div class="wa-feat-copy wa-reveal">
        '''+EB+'''
        <h2 class="wa-h2">{% if block.settings.heading != blank %}{{ block.settings.heading }}{% elsif sp != blank %}{{ sp.title }}{% endif %}</h2>
        {% if block.settings.text != blank %}<p class="wa-sub wa-left wa-narrow">{{ block.settings.text }}</p>{% endif %}
        {%- if block.settings.show_price and sp != blank and sp.price > 0 -%}<p class="wa-price">{{ sp.price | money }}</p>{%- endif -%}
        {%- if block.settings.points != blank -%}<ul class="wa-checks">{%- assign pts = block.settings.points | newline_to_br | split: '<br />' -%}{%- for p in pts -%}{%- assign pt = p | strip -%}{%- if pt != blank -%}<li>{{ pt }}</li>{%- endif -%}{%- endfor -%}</ul>{%- endif -%}
        {%- if block.settings.cta_label != blank -%}<div class="wa-btn-row wa-left-row"><a class="wa-btn" href="{% if block.settings.cta_url != blank %}{{ block.settings.cta_url }}{% elsif sp != blank %}{{ sp.url }}{% else %}#{% endif %}">{{ block.settings.cta_label }}</a></div>{%- endif -%}
      </div>
      <div class="wa-feat-media wa-reveal">{%- if block.settings.image != blank -%}<img src="{{ block.settings.image | image_url: width: 1400 }}" alt="{{ block.settings.image.alt | escape }}" loading="lazy">{%- elsif block.settings.image_url != blank -%}<img src="{{ block.settings.image_url }}" alt="" loading="lazy">{%- elsif sp != blank and sp.featured_image != blank -%}<img src="{{ sp.featured_image | image_url: width: 1400 }}" alt="{{ sp.title | escape }}" loading="lazy">{%- else -%}<div class="wa-ph">Immagine</div>{%- endif -%}</div>
    </div>
  </div>
</section>

{%- when 'contact' -%}
{%- assign cf_id = 'wa-cf-' | append: block.id -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-ct">
      <div class="wa-ct-info wa-reveal">
        '''+EB+'''
        <h2 class="wa-h2">{{ block.settings.heading }}</h2>
        {% if block.settings.text != blank %}<p class="wa-sub wa-left">{{ block.settings.text }}</p>{% endif %}
        <dl class="wa-ct-list">
          {% if block.settings.email != blank %}<div><dt>Email</dt><dd><a href="mailto:{{ block.settings.email }}">{{ block.settings.email }}</a></dd></div>{% endif %}
          {% if block.settings.phone != blank %}<div><dt>Telefono</dt><dd><a href="tel:{{ block.settings.phone | remove: ' ' }}">{{ block.settings.phone }}</a></dd></div>{% endif %}
          {% if block.settings.address != blank %}<div><dt>Sede</dt><dd>{{ block.settings.address | newline_to_br }}</dd></div>{% endif %}
          {% if block.settings.hours != blank %}<div><dt>Orari</dt><dd>{{ block.settings.hours | newline_to_br }}</dd></div>{% endif %}
          {% if block.settings.note != blank %}<div><dt>Risposta</dt><dd>{{ block.settings.note }}</dd></div>{% endif %}
        </dl>
      </div>
      <div class="wa-ct-form wa-reveal">
        {%- form 'contact', id: cf_id -%}
          {%- if form.posted_successfully? -%}<p class="wa-cf-ok" role="status">{{ block.settings.success }}</p>{%- endif -%}
          {%- if form.errors -%}<div class="wa-cf-err" role="alert">{{ form.errors | default_errors }}</div>{%- endif -%}
          {% if block.settings.form_title != blank %}<h3 class="wa-cf-t">{{ block.settings.form_title }}</h3>{% endif %}
          <div class="wa-cf-row">
            <label>Nome<input type="text" name="contact[name]" autocomplete="name" required></label>
            <label>Email<input type="email" name="contact[email]" autocomplete="email" required></label>
          </div>
          <label>Telefono (facoltativo)<input type="tel" name="contact[phone]" autocomplete="tel"></label>
          <label>Messaggio<textarea name="contact[body]" rows="5" required></textarea></label>
          <label class="wa-cf-check"><input type="checkbox" required> <span>{{ block.settings.privacy_label }}</span></label>
          <button class="wa-btn" type="submit">{{ block.settings.button_label }}</button>
        {%- endform -%}
      </div>
    </div>
  </div>
</section>

{%- when 'events' -%}
{%- assign evs = section.blocks | where: 'type', 'event' -%}
<section class="wa-sect wa-ev'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-center wa-reveal" style="margin-bottom:48px">'''+EB+'''{% if block.settings.heading != blank %}<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% endif %}{% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}</div>
    <div class="wa-ev-grid">
      <div class="wa-cal wa-reveal">
        <div class="wa-cal-head"><button type="button" class="wa-cal-nav" data-prev aria-label="Mese precedente">&#8249;</button><b data-month></b><button type="button" class="wa-cal-nav" data-next aria-label="Mese successivo">&#8250;</button></div>
        <div class="wa-cal-dow"><span>Lun</span><span>Mar</span><span>Mer</span><span>Gio</span><span>Ven</span><span>Sab</span><span>Dom</span></div>
        <div class="wa-cal-days" data-days></div>
        <p class="wa-cal-leg"><i></i>Giorni con un evento</p>
        <button type="button" class="wa-btn wa-cal-dl" data-ics-all>{{ block.settings.download_label }}</button>
        <p class="wa-cal-note">{{ block.settings.download_note }}</p>
      </div>
      <div class="wa-ev-list" data-list><p class="wa-ev-empty" hidden>{{ block.settings.empty_text }}</p></div>
    </div>
    <script type="application/json" data-events>[{%- for e in evs -%}{"id":{{ e.id | json }},"title":{{ e.settings.title | default: '' | json }},"date":{{ e.settings.date | default: '' | strip | json }},"start":{{ e.settings.start | default: '' | strip | json }},"end":{{ e.settings.end | default: '' | strip | json }},"place":{{ e.settings.place | default: '' | json }},"address":{{ e.settings.address | default: '' | json }},"city":{{ e.settings.city | default: '' | json }},"desc":{{ e.settings.desc | default: '' | json }},"url":{{ e.settings.link | default: '' | json }},"cta":{{ e.settings.link_label | default: '' | json }}}{%- unless forloop.last -%},{%- endunless -%}{%- endfor -%}]</script>
  </div>
</section>

{%- when 'event' -%}
"""
body=body.replace("{%- when 'faq' -%}", NEW+"\n{%- when 'faq' -%}",1)
body=eval("'''"+body.replace("\\","\\\\")+"'''") if False else body  # (no-op, kept for clarity)
# the NEW string contains '''+X+''' fragments meant for python concatenation -> resolve them
body=re.sub(r"'''\+(\w+(?:\([^)]*\))?)\+'''", lambda m: str(eval(m.group(1), dict(ns, img=img, PAD=PAD, TINT=TINT, EB=EB))), body)
assert "'''" not in body, body[body.find("'''")-200:body.find("'''")+50]

CSS_ADD = '''
.wa-hero{padding:var(--pt,96px) 22px var(--pb,56px);background:var(--bg-2)}
.wa-hero.wa-dark{background:var(--dark)}
.wa-hero-t{max-width:16ch;margin:0 auto 18px}
.wa-hero-btns{display:flex;gap:26px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:32px}
.wa-hero-media{max-width:var(--wide);margin:52px auto 0;border-radius:var(--r-lg);overflow:hidden}
.wa-hero-media img{width:100%}
.wa-big{font-size:clamp(1.7rem,3.8vw,2.7rem);font-weight:600;line-height:1.18;letter-spacing:-.022em;max-width:24ch;margin:0 auto}
.wa-stmt-text{max-width:58ch;margin:26px auto 0;color:var(--muted);font-size:1.12rem;line-height:1.6}
.wa-stmt-text p{margin:0 0 14px}
.wa-price{font-size:1.6rem;font-weight:650;margin:18px 0 0;color:var(--ink)}
.wa-checks{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:10px}
.wa-checks li{position:relative;padding-left:28px;font-size:1.03rem}
.wa-checks li::before{content:"";position:absolute;left:0;top:.2em;width:18px;height:18px;border-radius:50%;background:var(--accent)}
.wa-checks li::after{content:"";position:absolute;left:6.5px;top:.42em;width:4px;height:8px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.wa-left-row{justify-content:flex-start;margin-top:28px}
.wa-ct{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:start}
.wa-ct-list{margin:34px 0 0;display:grid;gap:0;border-top:1px solid var(--line)}
.wa-ct-list div{display:grid;grid-template-columns:110px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--line)}
.wa-ct-list dt{font-size:.74rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);padding-top:3px}
.wa-ct-list dd{margin:0;font-size:1.04rem;color:var(--ink)}
.wa-ct-list a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.wa-ct-form form{background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:clamp(26px,4vw,44px);box-shadow:0 18px 50px rgba(28,43,40,.07);display:grid;gap:16px}
.wa-cf-t{margin:0 0 4px;font-size:1.3rem;font-weight:600;letter-spacing:-.01em}
.wa-cf-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.wa-ct-form label{display:grid;gap:7px;font-size:.86rem;font-weight:600;color:var(--ink)}
.wa-ct-form label span{font-weight:400;color:var(--muted)}
.wa-ct-form input,.wa-ct-form textarea{font:inherit;font-size:1rem;color:var(--ink);background:var(--bg-2);border:1px solid var(--line);border-radius:12px;padding:13px 14px;width:100%;transition:border-color .2s,background .2s}
.wa-ct-form input:focus,.wa-ct-form textarea:focus{outline:none;border-color:var(--accent);background:#fff}
.wa-ct-form .wa-cf-check{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:.84rem;color:var(--muted)}
.wa-ct-form .wa-cf-check input{width:18px;height:18px;margin:1px 0 0;flex:0 0 auto;accent-color:var(--accent)}
.wa-ct-form .wa-btn{justify-self:start}
.wa-cf-ok{margin:0;padding:14px 16px;border-radius:12px;background:#e8f5ee;color:#1f6b47;font-weight:600}
.wa-cf-err{padding:14px 16px;border-radius:12px;background:#fbeceA;color:var(--accent)}
.wa-ev-grid{display:grid;grid-template-columns:minmax(300px,.8fr) 1.2fr;gap:40px;align-items:start}
.wa-cal{position:sticky;top:96px;background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:26px;box-shadow:0 18px 50px rgba(28,43,40,.07)}
.wa-cal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.wa-cal-head b{font-size:1.15rem;font-weight:650;letter-spacing:-.01em}
.wa-cal-nav{width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:var(--bg);font-size:1.3rem;line-height:1;cursor:pointer;color:var(--ink)}
.wa-cal-nav:hover{border-color:var(--accent);color:var(--accent)}
.wa-cal-dow,.wa-cal-days{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}
.wa-cal-dow span{font-size:.7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:6px 0}
.wa-cal-d{display:flex;align-items:center;justify-content:center;aspect-ratio:1;border-radius:50%;font-size:.92rem;color:var(--ink);border:0;background:none;font-family:inherit;padding:0}
.wa-cal-x{visibility:hidden}
.wa-cal-t{box-shadow:inset 0 0 0 1px var(--line)}
.wa-cal-on{background:var(--accent);color:#fff;font-weight:650;cursor:pointer;transition:transform .2s}
.wa-cal-on:hover{transform:scale(1.08)}
.wa-cal-leg{display:flex;align-items:center;gap:8px;margin:16px 0 0;font-size:.8rem;color:var(--muted)}
.wa-cal-leg i{width:10px;height:10px;border-radius:50%;background:var(--accent)}
.wa-cal-dl{width:100%;margin-top:20px}
.wa-cal-note{margin:10px 0 0;font-size:.76rem;color:var(--muted);text-align:center}
.wa-ev-list{display:grid;gap:16px}
.wa-ev-card{display:grid;grid-template-columns:78px 1fr;gap:22px;background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:24px;transition:box-shadow .3s,border-color .3s;scroll-margin-top:110px}
.wa-ev-card.wa-ev-hl{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.wa-ev-date{display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--bg-2);border-radius:16px;height:84px}
.wa-ev-date b{font-size:2rem;font-weight:650;line-height:1;letter-spacing:-.03em;color:var(--ink)}
.wa-ev-date span{font-size:.72rem;font-weight:700;letter-spacing:.12em;color:var(--accent);margin-top:4px}
.wa-ev-meta{margin:0 0 4px;font-size:.8rem;font-weight:600;letter-spacing:.02em;color:var(--accent);text-transform:capitalize}
.wa-ev-body h3{margin:0 0 6px;font-size:1.3rem;font-weight:600;letter-spacing:-.01em;color:var(--ink)}
.wa-ev-place{margin:0;font-weight:600;color:var(--ink)}
.wa-ev-addr{display:inline-block;margin-top:2px;font-size:.95rem;color:var(--muted);text-decoration:none}
.wa-ev-addr:hover{color:var(--accent)}
.wa-ev-desc{margin:12px 0 0;color:var(--muted);font-size:1rem}
.wa-ev-acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.wa-ev-btn{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:var(--r-pill);border:0;background:var(--btn);color:#fff!important;font:inherit;font-size:.9rem;font-weight:600;cursor:pointer;text-decoration:none}
.wa-ev-btn:hover{background:var(--btn-hi)}
.wa-ev-ghost{background:transparent;color:var(--ink)!important;box-shadow:inset 0 0 0 1px var(--line)}
.wa-ev-ghost:hover{background:var(--bg-2)}
.wa-ev-past{opacity:.55}
.wa-ev-empty{padding:40px;text-align:center;color:var(--muted);background:var(--bg);border:1px dashed var(--line);border-radius:var(--r-lg)}
@media (max-width:860px){
.wa-hero{padding:var(--pt,64px) 20px var(--pb,40px)}
.wa-hero-media{margin-top:36px;border-radius:var(--r)}
.wa-ct{grid-template-columns:1fr;gap:36px}
.wa-cf-row{grid-template-columns:1fr}
.wa-ev-grid{grid-template-columns:1fr;gap:28px}
.wa-cal{position:static}
.wa-ev-card{grid-template-columns:62px 1fr;gap:16px;padding:18px}
.wa-ev-date{height:70px}.wa-ev-date b{font-size:1.6rem}
}
'''
def scope_more(css):
    return ns['scope'](css)
scss2 = scss + '\n' + scope_more(CSS_ADD)
scss2 = scss2.replace('{padding:var(--pt,96px) 22px var(--pb,56px)}','{padding:var(--pt,96px) 22px var(--pb,56px)}')

EV_JS = r'''
S.querySelectorAll('.wa-ev').forEach(function(sec){
 var data=[];try{data=JSON.parse(sec.querySelector('[data-events]').textContent)}catch(e){}
 data=data.filter(function(e){return e.title&&/^\d{4}-\d{2}-\d{2}$/.test(e.date)});
 var MESI=['Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio','Agosto','Settembre','Ottobre','Novembre','Dicembre'],MS=['GEN','FEB','MAR','APR','MAG','GIU','LUG','AGO','SET','OTT','NOV','DIC'],GG=['domenica','lunedì','martedì','mercoledì','giovedì','venerdì','sabato'];
 var today=new Date();today.setHours(0,0,0,0);
 function dt(e){var p=e.date.split('-');return new Date(+p[0],p[1]-1,+p[2]);}
 data.sort(function(a,b){return (a.date+(a.start||''))<(b.date+(b.start||''))?-1:1});
 var up=data.filter(function(e){return dt(e)>=today}),past=data.filter(function(e){return dt(e)<today}).reverse();
 var cur=up.length?dt(up[0]):(past.length?dt(past[0]):today);cur=new Date(cur.getFullYear(),cur.getMonth(),1);
 var list=sec.querySelector('[data-list]'),days=sec.querySelector('[data-days]'),mlab=sec.querySelector('[data-month]');
 function pad(n){return (n<10?'0':'')+n}
 function tm(t,f){return /^\d{1,2}[:.]\d{2}$/.test(t||'')?t.replace('.',':').padStart(5,'0'):f}
 function st(e,t){return e.date.replace(/-/g,'')+'T'+t.replace(':','')+'00'}
 function s0(e){return tm(e.start,'10:00')} function s1(e){var a=s0(e),b=tm(e.end,'');if(b&&b>a)return b;var h=+a.slice(0,2)+1;return pad(Math.min(h,23))+a.slice(2)}
 function esc(s){return String(s||'').replace(/\\/g,'\\\\').replace(/([,;])/g,'\\$1').replace(/\r?\n/g,'\\n')}
 function loc(e){return [e.place,e.address,e.city].filter(Boolean).join(', ')}
 function ve(e){return ['BEGIN:VEVENT','UID:'+e.id+'-'+e.date+'@within','DTSTAMP:'+new Date().toISOString().replace(/[-:]/g,'').split('.')[0]+'Z','DTSTART;TZID=Europe/Rome:'+st(e,s0(e)),'DTEND;TZID=Europe/Rome:'+st(e,s1(e)),'SUMMARY:'+esc(e.title),'LOCATION:'+esc(loc(e)),'DESCRIPTION:'+esc((e.desc||'')+(e.url?'\n'+e.url:'')),'END:VEVENT'].join('\r\n')}
 var TZ='BEGIN:VTIMEZONE\r\nTZID:Europe/Rome\r\nBEGIN:STANDARD\r\nDTSTART:19701025T030000\r\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU\r\nTZOFFSETFROM:+0200\r\nTZOFFSETTO:+0100\r\nTZNAME:CET\r\nEND:STANDARD\r\nBEGIN:DAYLIGHT\r\nDTSTART:19700329T020000\r\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU\r\nTZOFFSETFROM:+0100\r\nTZOFFSETTO:+0200\r\nTZNAME:CEST\r\nEND:DAYLIGHT\r\nEND:VTIMEZONE';
 function ics(a){return ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Within//Eventi//IT','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Eventi Within','X-WR-TIMEZONE:Europe/Rome',TZ].concat(a.map(ve)).concat('END:VCALENDAR').join('\r\n')}
 function dl(n,t){var b=new Blob([t],{type:'text/calendar;charset=utf-8'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download=n;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(u);a.remove()},800)}
 function gc(e){return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(e.title)+'&dates='+st(e,s0(e))+'/'+st(e,s1(e))+'&ctz=Europe/Rome&location='+encodeURIComponent(loc(e))+'&details='+encodeURIComponent(e.desc||'')}
 function h(s){return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
 function cal(){mlab.textContent=MESI[cur.getMonth()]+' '+cur.getFullYear();var f=(cur.getDay()+6)%7,n=new Date(cur.getFullYear(),cur.getMonth()+1,0).getDate(),o='';for(var i=0;i<f;i++)o+='<span class="wa-cal-d wa-cal-x"></span>';
  for(var d=1;d<=n;d++){var k=cur.getFullYear()+'-'+pad(cur.getMonth()+1)+'-'+pad(d),hs=data.filter(function(e){return e.date===k}),t=+new Date(cur.getFullYear(),cur.getMonth(),d)===+today?' wa-cal-t':'';
   o+=hs.length?'<button type="button" class="wa-cal-d wa-cal-on'+t+'" data-go="'+hs[0].id+'" aria-label="'+d+' '+MESI[cur.getMonth()]+': '+h(hs[0].title)+'">'+d+'</button>':'<span class="wa-cal-d'+t+'">'+d+'</span>';}
  days.innerHTML=o;}
 function card(e,isPast){var d=dt(e),ad=[e.address,e.city].filter(Boolean).join(', '),time=e.start?' · ore '+tm(e.start,e.start)+(e.end?'–'+tm(e.end,e.end):''):'';
  return '<article class="wa-ev-card'+(isPast?' wa-ev-past':'')+'" id="ev-'+e.id+'"><div class="wa-ev-date"><b>'+d.getDate()+'</b><span>'+MS[d.getMonth()]+'</span></div><div class="wa-ev-body"><p class="wa-ev-meta">'+(isPast?'Concluso · ':'')+GG[d.getDay()]+' '+d.getDate()+' '+MESI[d.getMonth()].toLowerCase()+time+'</p><h3>'+h(e.title)+'</h3>'
  +(e.place?'<p class="wa-ev-place">'+h(e.place)+'</p>':'')+(ad?'<a class="wa-ev-addr" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(loc(e))+'">'+h(ad)+' &#8599;</a>':'')+(e.desc?'<p class="wa-ev-desc">'+h(e.desc)+'</p>':'')
  +(isPast?'':'<div class="wa-ev-acts"><button type="button" class="wa-ev-btn" data-ics="'+e.id+'">Aggiungi al calendario</button><a class="wa-ev-btn wa-ev-ghost" target="_blank" rel="noopener" href="'+gc(e)+'">Google Calendar</a>'+(e.url?'<a class="wa-ev-btn wa-ev-ghost" href="'+h(e.url)+'">'+h(e.cta||'Prenota il tuo posto')+'</a>':'')+'</div>')+'</div></article>'}
 var empty=list.querySelector('.wa-ev-empty');
 if(!up.length){empty.hidden=false;}
 list.insertAdjacentHTML('beforeend',up.map(function(e){return card(e,false)}).join('')+past.map(function(e){return card(e,true)}).join(''));
 cal();
 sec.querySelector('[data-prev]').addEventListener('click',function(){cur=new Date(cur.getFullYear(),cur.getMonth()-1,1);cal()});
 sec.querySelector('[data-next]').addEventListener('click',function(){cur=new Date(cur.getFullYear(),cur.getMonth()+1,1);cal()});
 days.addEventListener('click',function(ev){var b=ev.target.closest('[data-go]');if(!b)return;var c=document.getElementById('ev-'+b.getAttribute('data-go'));if(!c)return;c.scrollIntoView({behavior:'smooth',block:'center'});c.classList.add('wa-ev-hl');setTimeout(function(){c.classList.remove('wa-ev-hl')},1800)});
 list.addEventListener('click',function(ev){var b=ev.target.closest('[data-ics]');if(!b)return;var e=data.filter(function(x){return x.id===b.getAttribute('data-ics')})[0];if(e)dl('within-'+e.date+'.ics',ics([e]))});
 sec.querySelector('[data-ics-all]').addEventListener('click',function(){dl('eventi-within.ics',ics(up.length?up:data))});
});
'''
js2 = js.replace("var GAP=12,EDGE=20;", EV_JS+"\nvar GAP=12,EDGE=20;",1)
assert EV_JS in js2

# ---------- schema
schema=copy.deepcopy(schema0)
schema['name']='Within · Blocchi'
schema.pop('presets',None)
schema['max_blocks']=50
for b in schema['blocks']:
    ids=[s.get('id') for s in b['settings']]
    if 'cta_label' in ids:
        i=ids.index('cta_label'); b['settings'].insert(i+1,U('cta_url','Link pulsante (vuoto = torna in cima)'))
    if 'link_label' in ids:
        i=ids.index('link_label'); b['settings'].insert(i+1,U('link_url','Link (vuoto = torna in cima)'))
NEWB=[
 {"type":"hero","name":"Hero","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo","Torna a piacerti allo specchio."),TA("sub","Sottotitolo",""),T("cta_label","Pulsante",""),U("cta_url","Link pulsante"),T("link_label","Link secondario",""),U("link_url","Link secondario · URL"),IMG("image","Immagine"),T("image_url","Immagine (link, usato se non carichi un file)",""),CB("dark","Tema scuro",False)]+PADS(96,56)},
 {"type":"statement","name":"Manifesto","settings":[T("eyebrow","Sopra-titolo",""),TA("statement","Frase grande","Una frase che resta."),{"type":"richtext","id":"text","label":"Testo"},IMG("image","Immagine (opz.)"),T("image_url","Immagine (link, opz.)",""),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"product_spot","name":"Prodotto in evidenza","settings":[{"type":"product","id":"product","label":"Prodotto"},T("eyebrow","Sopra-titolo",""),T("heading","Titolo (vuoto = nome prodotto)",""),TA("text","Testo",""),{"type":"textarea","id":"points","label":"Punti (uno per riga)"},CB("show_price","Mostra prezzo",True),T("cta_label","Pulsante","Scopri Within"),U("cta_url","Link (vuoto = pagina prodotto)"),IMG("image","Immagine (opz.)"),T("image_url","Immagine (link, opz.)",""),CB("reversed","Immagine a sinistra",False),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"contact","name":"Contatti e modulo","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo","Scrivici."),TA("text","Testo",""),T("email","Email",""),T("phone","Telefono",""),TA("address","Indirizzo",""),TA("hours","Orari",""),T("note","Tempi di risposta",""),{"type":"header","content":"Modulo"},T("form_title","Titolo modulo","Mandaci un messaggio"),T("privacy_label","Consenso privacy","Ho letto l'informativa privacy e acconsento al trattamento dei dati per ricevere una risposta."),T("button_label","Pulsante","Invia messaggio"),T("success","Messaggio di conferma","Grazie! Ti rispondiamo entro 24 ore lavorative."),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"events","name":"Calendario eventi","settings":[T("eyebrow","Sopra-titolo",""),T("heading","Titolo","Prossimi eventi"),TA("sub","Sottotitolo",""),T("download_label","Pulsante download","Scarica il calendario"),T("download_note","Nota sotto il download","File .ics: si apre con Apple Calendario, Google Calendar e Outlook."),T("empty_text","Testo se non ci sono eventi","Nuove date in arrivo. Torna a trovarci presto."),{"type":"paragraph","content":"Gli eventi si aggiungono con i blocchi \"Evento\" in questa stessa sezione."},CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"event","name":"Evento","settings":[T("title","Titolo evento","Evento"),T("date","Data (formato AAAA-MM-GG, es. 2026-11-21)",""),T("start","Ora inizio (HH:MM)",""),T("end","Ora fine (HH:MM)",""),T("place","Luogo (es. Farmacia Rossi)",""),T("address","Indirizzo",""),T("city","Città",""),TA("desc","Descrizione",""),U("link","Link prenotazione (opz.)"),T("link_label","Testo link","Prenota il tuo posto")]},
]
for b in NEWB:
    for s in b['settings']:
        if s.get('default')=="": del s['default']
schema['blocks']=NEWB[:1]+schema['blocks']+NEWB[1:]
for b in schema['blocks']:
    assert len(b['name'])<=25,b['name']
schema['presets']=[{"name":"Within · Blocchi","blocks":[{"type":"hero"}]}]

out='''{% comment %}
  Within · Blocchi — sezione generica a blocchi (homepage, Chi siamo, Contattaci, Eventi).
  Stessi moduli della product page + Hero, Manifesto, Prodotto in evidenza, Contatti e modulo, Calendario eventi, Evento.
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
open(REPO+'/sections/within-site.liquid','w').write(out)
print('within-site', len(out))

# ---------- templates
defs={b['type']:{s['id']:s['default'] for s in b['settings'] if 'default' in s} for b in schema['blocks']}
HDR='''/*
 * Template Within — generato da gen_site.py (repo alonqo/within-theme)
 */
'''
def section(blocks, sid='within'):
    bl={};order=[]
    for n,(t,st) in enumerate(blocks,1):
        k='%s_%d'%(t,n); s=dict(defs[t]); s.update(st); bl[k]={'type':t,'settings':s}; order.append(k)
    return {'type':'within-site','blocks':bl,'block_order':order,'settings':{}}
def write_tpl(name, blocks):
    tpl={'sections':{'within':section(blocks)},'order':['within']}
    open(REPO+'/templates/'+name,'w').write(HDR+json.dumps(tpl,ensure_ascii=False,indent=2))
SITE={'PROD':PROD,'I':I,'V':V}
import importlib.util
spec=importlib.util.spec_from_file_location('content',os.path.join(SP,'site_content.py'));C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
for name,blocks in C.build(SITE).items():
    write_tpl(name,blocks); print('template',name,len(blocks))
