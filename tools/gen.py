import json,re
B="https://d8j0ntlcm91z4.cloudfront.net/user_3CoHflE6XwKC5XeJge3JDzQw5PH/hf_20261028_"
I=lambda x:B+x+'.png'
V=lambda x:(B[:-9]+x if x.startswith('2026') else B+x)+'.mp4'
html=open('/home/claude/within-apple-product.html').read()
css=re.search(r'<style>(.*?)</style>',html,re.S).group(1)
# scope css under section id
def scope(css):
    out=[]
    def sc(sel): return ','.join('#shopify-section-{{ section.id }} '+s.strip() for s in sel.split(','))
    i=0
    res=''
    # process top-level rules and @media blocks
    tokens=re.split(r'(@media[^{]*\{|\})',css)
    depth=0;buf=''
    lines=[]
    for rule in re.finditer(r'(@media[^{]*)\{((?:[^{}]*\{[^{}]*\})*)\s*\}|([^{}@]+)\{([^{}]*)\}',css):
        if rule.group(1):
            inner=''.join(sc(m.group(1))+'{'+m.group(2)+'}\n' for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',rule.group(2)))
            lines.append(rule.group(1).strip()+'{\n'+inner+'}')
        else:
            lines.append(sc(rule.group(3))+'{'+rule.group(4)+'}')
    return '\n'.join(lines)
scss=scope(css)
# replace color tokens with settings
scss=scss.replace('--bg:#ffffff;--bg-2:#f7f3ec;--ink:#1d1d1f;--muted:#6e6a64;--line:#ddd6cb;--line-soft:#ebe5db;--dark:#1C2B28;--on-dark:#f7f3ec;--on-dark-mut:#b5c2bd;--accent:#A8432E;--btn:#CC5B3E;--btn-hi:#A8432E;--accent-hi:#F2C05C;--gold:#F2C05C;',
 '--bg:{{ section.settings.bg_color }};--bg-2:{{ section.settings.surface2_color }};--ink:{{ section.settings.text_color }};--muted:{{ section.settings.muted_color }};--line:{{ section.settings.line_color }};--line-soft:#ebe5db;--dark:{{ section.settings.dark_color }};--on-dark:{{ section.settings.on_dark_color }};--on-dark-mut:{{ section.settings.on_dark_mut_color }};--accent:{{ section.settings.accent_color }};--btn:{{ section.settings.btn_color }};--btn-hi:{{ section.settings.btn_hover_color }};--accent-hi:{{ section.settings.accent_hi_color }};--gold:{{ section.settings.star_color }};')
scss=scss.replace('--maxw:1024px','--maxw:{{ section.settings.max_width }}px')
assert '{{ section.settings.bg_color }}' in scss
# padding via vars (bug #6)
scss=scss.replace('{padding:120px 22px}','{padding:var(--pt,120px) 22px var(--pb,120px)}')
scss=scss.replace('{padding:78px 20px}','{padding:min(var(--pt,120px),78px) 20px min(var(--pb,120px),78px)}')
scss+='\n#shopify-section-{{ section.id }} .wa-ugc-item{margin:0}'
scss+='\n#shopify-section-{{ section.id }} .wa-ugc{padding-top:var(--pt,90px);padding-bottom:var(--pb,90px)}'
scss+='\n#shopify-section-{{ section.id }} .wa-ph{display:flex;align-items:center;justify-content:center;min-height:300px;background:repeating-linear-gradient(135deg,#ece6dc 0 16px,#f4efe7 16px 32px);color:#8a8278;font-size:.84rem;font-weight:600;border-radius:var(--r)}'

def img(setting_pick, setting_url, attrs='', w=1400, alt='{{ block.settings.%s.alt | escape }}'):
    return ('{%% if block.settings.%s != blank %%}<img %ssrc="{{ block.settings.%s | image_url: width: %d }}" alt="{{ block.settings.%s.alt | escape }}" loading="lazy">'
            '{%% elsif block.settings.%s != blank %%}<img %ssrc="{{ block.settings.%s }}" alt="" loading="lazy">'
            '{%% else %%}<div class="wa-ph">Immagine</div>{%% endif %%}')%(setting_pick,attrs,setting_pick,w,setting_pick,setting_url,attrs,setting_url)
def dimg(prefix_pick, prefix_url, attrs='', w=900):
    # dynamic lookups with pre-assigned keys (bug #1); expects liquid vars kp, ku assigned
    return ('{%% if %s != blank %%}<img %ssrc="{{ %s | image_url: width: %d }}" alt="{{ %s.alt | escape }}" loading="lazy">'
            '{%% elsif %s != blank %%}<img %ssrc="{{ %s }}" alt="" loading="lazy">{%% else %%}<div class="wa-ph">Immagine</div>{%% endif %%}')%(prefix_pick,attrs,prefix_pick,w,prefix_pick,prefix_url,attrs,prefix_url)

PAD=' style="--pt:{{ block.settings.padding_top }}px;--pb:{{ block.settings.padding_bottom }}px;"'
TINT='{% if block.settings.tinted %} wa-tint{% endif %}'
EB='{% if block.settings.eyebrow != blank %}<p class="wa-eyebrow">{{ block.settings.eyebrow }}</p>{% endif %}'
body=r'''
<div class="wa-root">
{%- for block in section.blocks -%}
{%- case block.type -%}

{%- when 'ugc_slider' -%}
<section class="wa-ugc'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  {%- if block.settings.heading != blank or block.settings.eyebrow != blank -%}
  <div class="wa-ugc-head wa-reveal">'''+EB+'''{% if block.settings.heading != blank %}<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% endif %}</div>
  {%- endif -%}
  <div class="wa-ugc-track" data-autoscroll="{{ block.settings.autoscroll_ms }}">
  {%- for i in (1..8) -%}
    {%- assign vk = 'video_' | append: i -%}{%- assign uk = 'video_url_' | append: i -%}
    {%- assign v = block.settings[vk] -%}{%- assign vu = block.settings[uk] -%}{%- assign ck = 'caption_' | append: i -%}{%- assign cap = block.settings[ck] -%}
    {%- capture capt -%}{%- if cap != blank -%}<figcaption class="wa-ugc-cap"><b>{{ cap }}</b>{% if block.settings.verified_label != blank %}<span class="wa-ugc-ver"><i></i>{{ block.settings.verified_label }}</span>{% endif %}</figcaption>{%- endif -%}{%- endcapture -%}
    {%- if v != blank -%}<figure class="wa-ugc-item"><div class="wa-ugc-slide">{{ v | video_tag: autoplay: true, loop: true, muted: true, controls: false, playsinline: true, preload: 'metadata' }}{{ capt }}</div></figure>
    {%- elsif vu != blank -%}<figure class="wa-ugc-item"><div class="wa-ugc-slide"><video src="{{ vu }}" autoplay muted loop playsinline preload="metadata"></video>{{ capt }}</div></figure>{%- endif -%}
  {%- endfor -%}
  </div>
</section>

{%- when 'value_prop' -%}
<section class="wa-sect wa-opening wa-center'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wa-reveal">'''+EB+'''<h2 class="wa-display">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}
    {% if block.settings.show_cta %}<div class="wa-btn-row"><a class="wa-btn wa-top" href="#">{{ block.settings.cta_label }}</a></div>{% endif %}</div>
    <div class="wa-hero-img wa-reveal wa-blur">'''+img('image','image_url')+'''</div>
  </div>
</section>

{%- when 'cinematic' -%}
<section class="wa-cine" {{ block.shopify_attributes }}>
  {%- if block.settings.image != blank -%}<img class="wa-cine-img" data-parallax="{{ block.settings.parallax }}" src="{{ block.settings.image | image_url: width: 2200 }}" alt="" loading="lazy">
  {%- elsif block.settings.image_url != blank -%}<img class="wa-cine-img" data-parallax="{{ block.settings.parallax }}" src="{{ block.settings.image_url }}" alt="" loading="lazy">{%- endif -%}
  <div class="wa-cine-copy wa-reveal">'''+EB+'''{% if block.settings.heading != blank %}<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% endif %}{% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}</div>
</section>

{%- when 'benefits' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-feat{% if block.settings.reversed %} wa-rev{% endif %}">
      <div class="wa-feat-copy wa-reveal">
        {%- if block.settings.bignum != blank -%}<p class="wa-bignum"><span data-count="{{ block.settings.bignum }}">{{ block.settings.bignum }}</span>{% if block.settings.bignum_unit != blank %}<small>{{ block.settings.bignum_unit }}</small>{% endif %}</p>{%- endif -%}
        '''+EB+'''
        <h2 class="wa-h2">{{ block.settings.heading }}</h2>
        {% if block.settings.sub != blank %}<p class="wa-sub wa-left wa-narrow">{{ block.settings.sub }}</p>{% endif %}
        {% if block.settings.link_label != blank %}<p style="margin-top:22px"><a class="wa-link wa-top" href="#">{{ block.settings.link_label }}</a></p>{% endif %}
      </div>
      <div class="wa-feat-media wa-reveal">'''+img('image','image_url','data-parallax="0.08" ',1200)+'''</div>
    </div>
  </div>
</section>

{%- when 'feature_row' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide wa-center">
    {% if block.settings.heading != blank %}<h2 class="wa-h2 wa-reveal" style="margin-bottom:56px">{{ block.settings.heading }}</h2>{% endif %}
    <div class="wa-frow">
    {%- for i in (1..4) -%}
      {%- assign tk = 'f' | append: i | append: '_title' -%}{%- assign t = block.settings[tk] -%}
      {%- if t != blank -%}
        {%- assign pk = 'f' | append: i | append: '_image' -%}{%- assign p = block.settings[pk] -%}
        {%- assign uk = 'f' | append: i | append: '_image_url' -%}{%- assign u = block.settings[uk] -%}
        {%- assign xk = 'f' | append: i | append: '_text' -%}{%- assign d = forloop.index0 | times: 0.08 -%}
        <div class="wa-fcard wa-reveal" style="--d:{{ d }}s"><div class="wa-fimg">'''+dimg('p','u',w=600)+'''</div><h3>{{ t }}</h3><p>{{ block.settings[xk] }}</p></div>
      {%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'how_it_works' -%}
<section class="wa-sect{% if block.settings.dark %} wa-dark{% endif %}" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide wa-center">
    {% if block.settings.eyebrow != blank %}<p class="wa-eyebrow wa-reveal">{{ block.settings.eyebrow }}</p>{% endif %}
    <h2 class="wa-h2 wa-reveal"{% if block.settings.dark %} style="color:#fff"{% endif %}>{{ block.settings.heading }}</h2>
    <div class="wa-steps">
    {%- for i in (1..4) -%}
      {%- assign tk = 'step' | append: i | append: '_title' -%}{%- assign t = block.settings[tk] -%}
      {%- if t != blank -%}
        {%- assign pk = 'step' | append: i | append: '_image' -%}{%- assign p = block.settings[pk] -%}
        {%- assign uk = 'step' | append: i | append: '_image_url' -%}{%- assign u = block.settings[uk] -%}
        {%- assign xk = 'step' | append: i | append: '_text' -%}{%- assign d = forloop.index0 | times: 0.12 -%}
        <div class="wa-step wa-reveal" style="--d:{{ d }}s">'''+dimg('p','u',w=800)+'''<span class="wa-n">Step {{ forloop.index }}</span><h3>{{ t }}</h3><p>{{ block.settings[xk] }}</p></div>
      {%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'closeup' -%}
<section class="wa-cl'''+TINT+'''" data-horizontal="{{ block.settings.mobile_horizontal }}" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-cl-grid">
      <div class="wa-cl-sticky wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub wa-left wa-narrow">{{ block.settings.sub }}</p>{% endif %}</div>
      <div class="wa-cl-media">
      {%- for i in (1..4) -%}
        {%- assign pk = 'image_' | append: i -%}{%- assign p = block.settings[pk] -%}
        {%- assign uk = 'image_url_' | append: i -%}{%- assign u = block.settings[uk] -%}
        {%- if p != blank or u != blank -%}<div class="wa-reveal">'''+dimg('p','u',w=1100)+'''</div>{%- endif -%}
      {%- endfor -%}
      </div>
    </div>
  </div>
</section>

{%- when 'whats_inside' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    {% if block.settings.eyebrow != blank %}<p class="wa-eyebrow wa-center wa-reveal" style="margin-bottom:8px">{{ block.settings.eyebrow }}</p>{% endif %}
    {% if block.settings.heading != blank %}<h2 class="wa-h2 wa-center wa-reveal" style="margin-bottom:16px">{{ block.settings.heading }}</h2>{% endif %}
    {% if block.settings.sub != blank %}<p class="wa-sub wa-reveal" style="text-align:center;margin-bottom:56px">{{ block.settings.sub }}</p>{% endif %}
    <div class="wa-gal">
    {%- for i in (1..3) -%}
      {%- assign pk = 'g' | append: i | append: '_image' -%}{%- assign p = block.settings[pk] -%}
      {%- assign uk = 'g' | append: i | append: '_image_url' -%}{%- assign u = block.settings[uk] -%}
      {%- assign ck = 'g' | append: i | append: '_caption' -%}{%- assign c = block.settings[ck] -%}{%- assign d = forloop.index0 | times: 0.1 -%}
      <figure class="wa-reveal" style="--d:{{ d }}s"><div class="wa-gimg">'''+dimg('p','u',w=800)+'''</div>{% if c != blank %}<figcaption>{{ c }}</figcaption>{% endif %}</figure>
    {%- endfor -%}
    </div>
    <div class="wa-spec wa-reveal">
    {%- for i in (1..8) -%}
      {%- assign nk = 'ing' | append: i | append: '_name' -%}{%- assign n = block.settings[nk] -%}
      {%- if n != blank -%}
        {%- assign tk = 'ing' | append: i | append: '_tag' -%}{%- assign dk = 'ing' | append: i | append: '_desc' -%}{%- assign qk = 'ing' | append: i | append: '_dose' -%}
        <div class="wa-spec-row"><span class="wa-spec-tag">{{ block.settings[tk] }}</span><span class="wa-spec-name">{{ n }}<span>{{ block.settings[dk] }}</span></span><span class="wa-spec-dose">{{ block.settings[qk] }}</span></div>
      {%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'objections' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    {% if block.settings.heading != blank %}<h2 class="wa-h2 wa-center wa-reveal" style="margin-bottom:48px">{{ block.settings.heading }}</h2>{% endif %}
    <div class="wa-ob">
    {%- for i in (1..6) -%}
      {%- assign qk = 'q' | append: i -%}{%- assign q = block.settings[qk] -%}
      {%- if q != blank -%}{%- assign ak = 'a' | append: i -%}<div class="wa-ob-cell wa-reveal"><p class="wa-ob-q">{{ q }}</p><p class="wa-ob-a">{{ block.settings[ak] }}</p></div>{%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'social_proof' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    {% if block.settings.eyebrow != blank %}<p class="wa-eyebrow wa-center wa-reveal">{{ block.settings.eyebrow }}</p>{% endif %}
    {% if block.settings.heading != blank %}<h2 class="wa-h2 wa-center wa-reveal" style="margin-bottom:54px">{{ block.settings.heading }}</h2>{% endif %}
    <div class="wa-stats wa-reveal">
    {%- for i in (1..3) -%}
      {%- assign pk = 'stat' | append: i | append: '_prefix' -%}{%- assign ck = 'stat' | append: i | append: '_count' -%}{%- assign sk = 'stat' | append: i | append: '_suffix' -%}{%- assign lk = 'stat' | append: i | append: '_label' -%}
      <div class="wa-s"><div class="wa-sn">{{ block.settings[pk] }}<span data-count="{{ block.settings[ck] }}">{{ block.settings[ck] }}</span>{{ block.settings[sk] }}</div><div class="wa-sl">{{ block.settings[lk] }}</div></div>
    {%- endfor -%}
    </div>
    {% if block.settings.source_note != blank %}<p class="wa-src wa-reveal">{{ block.settings.source_note }}</p>{% endif %}
    <div class="wa-revs">
    {%- for i in (1..3) -%}
      {%- assign rk = 'r' | append: i | append: '_quote' -%}{%- assign rq = block.settings[rk] -%}
      {%- if rq != blank -%}
        {%- assign pk = 'r' | append: i | append: '_image' -%}{%- assign p = block.settings[pk] -%}
        {%- assign uk = 'r' | append: i | append: '_image_url' -%}{%- assign u = block.settings[uk] -%}
        {%- assign nk = 'r' | append: i | append: '_name' -%}{%- assign mk = 'r' | append: i | append: '_meta' -%}{%- assign d = forloop.index0 | times: 0.1 -%}
        <div class="wa-rev wa-reveal" style="--d:{{ d }}s">'''+dimg('p','u',w=700)+'''<div class="wa-rev-b"><div class="wa-stars">★★★★★</div><p>{{ rq }}</p><div class="wa-who"><b>{{ block.settings[nk] }}</b>, {{ block.settings[mk] }}<br><span class="wa-ver">{{ block.settings.verified_label }}</span></div></div></div>
      {%- endif -%}
    {%- endfor -%}
    </div>
    {% if block.settings.big_quote != blank %}<blockquote class="wa-quote wa-reveal">{{ block.settings.big_quote }}{% if block.settings.big_quote_cite != blank %}<cite>{{ block.settings.big_quote_cite }}</cite>{% endif %}</blockquote>{% endif %}
    {% if block.settings.cta_label != blank %}<div class="wa-btn-row wa-reveal"><a class="wa-btn wa-top" href="#">{{ block.settings.cta_label }}</a></div>{% endif %}
  </div>
</section>

{%- when 'authority' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide wa-reveal">
    <div class="wa-auth">
      <div class="wa-auth-img">'''+img('image','image_url',w=1000)+'''</div>
      <div class="wa-auth-panel">'''+EB+'''<blockquote>{{ block.settings.quote }}</blockquote>
        <ul class="wa-auth-list">{%- for i in (1..5) -%}{%- assign lk = 'point' | append: i -%}{%- assign l = block.settings[lk] -%}{%- if l != blank -%}<li>{{ l }}</li>{%- endif -%}{%- endfor -%}</ul>
        <div class="wa-sig"><b>{{ block.settings.name }}</b>{{ block.settings.role }}</div>
      </div>
    </div>
  </div>
</section>

{%- when 'guarantee' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-feat wa-gar{% if block.settings.reversed %} wa-rev{% endif %}">
      <div class="wa-feat-copy wa-reveal">
        '''+EB+'''
        {%- if block.settings.days != blank -%}<p class="wa-bignum"><span data-count="{{ block.settings.days }}">{{ block.settings.days }}</span>{% if block.settings.days_unit != blank %}<small>{{ block.settings.days_unit }}</small>{% endif %}</p>{%- endif -%}
        <h2 class="wa-h2">{{ block.settings.heading }}</h2>
        {% if block.settings.sub != blank %}<p class="wa-sub wa-left wa-narrow">{{ block.settings.sub }}</p>{% endif %}
        <div class="wa-paths">
        {%- for i in (1..3) -%}
          {%- assign tk = 'path' | append: i | append: '_title' -%}{%- assign t = block.settings[tk] -%}
          {%- if t != blank -%}{%- assign xk = 'path' | append: i | append: '_text' -%}<div class="wa-path{% if forloop.last %} wa-path-hi{% endif %}"><b>{{ t }}</b><p>{{ block.settings[xk] }}</p></div>{%- endif -%}
        {%- endfor -%}
        </div>
        {% if block.settings.cta_label != blank %}<div class="wa-btn-row"><a class="wa-btn wa-top" href="#">{{ block.settings.cta_label }}</a></div>{% endif %}
      </div>
      <div class="wa-feat-media wa-reveal">'''+img('image','image_url','data-parallax="0.08" ',1200)+'''</div>
    </div>
  </div>
</section>

{%- when 'faq' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    {% if block.settings.heading != blank %}<h2 class="wa-h2 wa-center wa-reveal">{{ block.settings.heading }}</h2>{% endif %}
    <div class="wa-faq wa-reveal">
    {%- for i in (1..8) -%}
      {%- assign qk = 'q' | append: i -%}{%- assign q = block.settings[qk] -%}
      {%- if q != blank -%}{%- assign ak = 'a' | append: i -%}<details{% if forloop.first %} open{% endif %}><summary>{{ q }}<span class="wa-pm"></span></summary><div class="wa-ans">{{ block.settings[ak] }}</div></details>{%- endif -%}
    {%- endfor -%}
    </div>
    {% if block.settings.disclaimer != blank %}<div class="wa-disc">{{ block.settings.disclaimer }}</div>{% endif %}
  </div>
</section>

{%- endcase -%}
{%- endfor -%}
</div>
'''
js=re.search(r'<script>(.*?)</script>',html,re.S).group(1)
js=js.replace("var R=document.getElementById('wa-root'); if(!R)return;","var S=document.getElementById('shopify-section-{{ section.id }}'); if(!S)return; var R=S.querySelector('.wa-root'); if(!R)return;")
js=js.replace("var cl=document.getElementById('wa-cl')","var cl=R.querySelector('.wa-cl')")
js=js.replace("function mode(){if(!cl)return;if(mq.matches)","function mode(){if(!cl)return;if(mq.matches&&cl.getAttribute('data-horizontal')!=='false')")
js=js.replace("var GAP=12,EDGE=20;","var GAP=12,EDGE=20;\nR.querySelectorAll('.wa-top').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();window.scrollTo({top:0,behavior:'smooth'});});});")
assert "S.querySelector('.wa-root')" in js and "R.querySelector('.wa-cl')" in js and "data-horizontal" in js

def T(i,l,d=None): s={"type":"text","id":i,"label":l}; d is not None and s.update(default=d); return s
def TA(i,l,d): return {"type":"textarea","id":i,"label":l,"default":d}
def IMG(i,l): return {"type":"image_picker","id":i,"label":l}
def URL(i,l,d): return {"type":"text","id":i,"label":l+" (link, usato se non carichi un file)","default":d}
def CB(i,l,d): return {"type":"checkbox","id":i,"label":l,"default":d}
def PADS(t=120,b=120): return [{"type":"range","id":"padding_top","label":"Spazio sopra","min":0,"max":200,"step":4,"unit":"px","default":t},{"type":"range","id":"padding_bottom","label":"Spazio sotto","min":0,"max":200,"step":4,"unit":"px","default":b}]

CAPS1=[('Marta', 57), ('Paola', 62), ('Silvia', 59), ('Elena', 56), ('Cristina', 64), ('Valentina', 61)]
CAPS2=[('Anna', 63), ('Federica', 58), ('Roberta', 60), ('Simona', 61), ('Daniela', 55), ('Chiara', 65)]
vids1=['20261029_184341_e68f8b61-6bc7-457b-810d-a44e3c73d407', '20261029_184342_64f3d0ad-d01a-4980-a471-7b242893ff48', '20261029_184342_abd90abb-51b9-4161-b9c3-a6da8edb15b3', '20261029_184341_7aaed507-54ee-468b-b442-ddaf36fa6ff1', '20261029_184342_104cddd0-62dc-41cf-a271-44c2ead6a075', '20261029_184434_8bc687d3-8f91-4143-8a5d-d28fd8086a20']
vids2=['20261029_184341_29598c0b-fc61-4c8a-a7ee-07eba51bbcb6', '20261029_184435_faa23e77-2ae0-4bde-8a57-685582bef192', '20261029_184606_7a623b5d-5f89-4a64-941a-ab975c1dd333', '20261029_184434_d07edb6f-ad59-4fe4-9625-ea4f802d90bb', '20261029_184434_9af3f471-8a98-43fa-ae54-6fa542ea8359', '20261029_184435_8e025d44-915c-40b8-93b4-7c9632ee8997']
ugc_set=[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),T("verified_label","Etichetta verificato","Acquisto verificato"),{"type":"range","id":"autoscroll_ms","label":"Auto-scroll","min":2000,"max":8000,"step":500,"unit":"ms","default":4000}]
for i in range(1,9):
    ugc_set+= [{"type":"video","id":"video_%d"%i,"label":"Video %d (file Shopify)"%i}, T("video_url_%d"%i,"Video %d (link mp4, usato se non carichi un file)"%i, ""), T("caption_%d"%i,"Video %d · didascalia (es. Marta, 45)"%i,"")]
ugc_set+=[{"type":"paragraph","content":"Autoplay, muti, in loop. 3 visibili su mobile, 5 su desktop."},CB("tinted","Sfondo tinta",False)]+PADS(88,88)

schema={"name":"Within · Product Page","tag":"section","class":"wa-section","max_blocks":24,
"settings":[{"type":"range","id":"max_width","label":"Larghezza contenuto","min":900,"max":1280,"step":20,"unit":"px","default":1020},
 {"type":"header","content":"Colori"},
 {"type":"color","id":"bg_color","label":"Sfondo","default":"#ffffff"},
 {"type":"color","id":"surface2_color","label":"Sfondo sezioni tinta","default":"#f7f3ec"},
 {"type":"color","id":"text_color","label":"Testo","default":"#1d1d1f"},
 {"type":"color","id":"muted_color","label":"Testo secondario","default":"#6e6a64"},
 {"type":"color","id":"line_color","label":"Linee","default":"#ddd6cb"},
 {"type":"color","id":"dark_color","label":"Sezioni scure","default":"#1C2B28"},
 {"type":"color","id":"on_dark_color","label":"Testo su scuro","default":"#f7f3ec"},
 {"type":"color","id":"on_dark_mut_color","label":"Testo su scuro (secondario)","default":"#b5c2bd"},
 {"type":"color","id":"accent_color","label":"Accento","default":"#A8432E"},
 {"type":"color","id":"accent_hi_color","label":"Accento su scuro","default":"#F2C05C"},
 {"type":"color","id":"btn_color","label":"Pulsante","default":"#CC5B3E"},
 {"type":"color","id":"btn_hover_color","label":"Pulsante hover","default":"#A8432E"},
 {"type":"color","id":"star_color","label":"Stelle","default":"#F2C05C"}],
"blocks":[
 {"type":"ugc_slider","name":"Slider video UGC","settings":ugc_set},
 {"type":"value_prop","name":"1 · Apertura","settings":[T("eyebrow","Sopra-titolo","Pelle compatta. Rughe meno visibili. Luce."),T("heading","Titolo grande","Torna a piacerti allo specchio."),TA("sub","Sottotitolo","Pelle più idratata dalla terza settimana. Più compatta e liscia in 8-12 settimane. Senza aghi, senza bisturi, senza creme da 80 euro: un sachet al giorno."),IMG("image","Immagine"),URL("image_url","Immagine",I("133239_332fc57d-882d-47db-8c71-ef9c0c432cf4")),CB("show_cta","Mostra pulsante",False),T("cta_label","Testo pulsante","Inizia oggi"),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"cinematic","name":"Banda cinematic","settings":[T("eyebrow","Sopra-titolo","Perché questa volta funziona"),T("heading","Titolo","Sotto i 3.000 Dalton. Arriva dove serve: alla tua pelle."),T("sub","Sottotitolo (opz.)",""),IMG("image","Immagine"),URL("image_url","Immagine",I("133240_6e62d467-ccec-48a2-8db0-5be293d52d9e")),{"type":"range","id":"parallax","label":"Intensità parallax","min":0,"max":0.5,"step":0.1,"default":0.2}]},
 {"type":"benefits","name":"Feature highlight","settings":[T("bignum","Numero gigante (opz.)","5000"),T("bignum_unit","Unità numero (opz.)","mg"),T("eyebrow","Sopra-titolo (opz.)",""),T("heading","Titolo","5 grammi di collagene che la tua pelle riesce davvero a usare."),TA("sub","Sottotitolo","Il collagene generico è troppo grande: lo digerisci come una bistecca e alla pelle non arriva niente. Per questo non hai visto risultati. I tripeptidi di Within sono tre volte più piccoli: arrivano al derma e riaccendono la produzione di nuovo collagene. Non era colpa tua. Era il collagene."),T("link_label","Link (torna su, opz.)","Voglio provarlo →"),IMG("image","Immagine"),URL("image_url","Immagine",I("133239_3c10111a-879c-49fe-8e0c-b7b2fa3ad58f")),CB("reversed","Immagine a sinistra",False),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"feature_row","name":"Riga mini-feature","settings":[T("heading","Titolo","Quello che noterai. E che noteranno gli altri.")]+sum([[IMG("f%d_image"%i,"%d · immagine"%i),URL("f%d_image_url"%i,"%d · immagine"%i,u),T("f%d_title"%i,"%d · titolo"%i,t),T("f%d_text"%i,"%d · testo"%i,x)] for i,(u,t,x) in enumerate([(I("232314_d7058a51-b5f2-4ecf-98b5-37b864909911"),"Pelle compatta","Il viso ritrova tono e smette di cedere."),(I("232314_9d01a565-4696-4718-b0f2-f56842afbc13"),"Rughe meno visibili","Contorno occhi e linee della bocca più distesi."),(I("232314_838c8e40-9df8-4307-bd33-19339ae3bf5d"),"Luce senza trucco","Esci con il viso nudo. E ti piace."),(I("232313_e963b647-9e4f-4f27-be56-b6943056bdf6"),"Idratata da dentro","Niente più pelle che tira a metà giornata.")],1)],[])+[CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"how_it_works","name":"Come funziona","settings":[T("eyebrow","Sopra-titolo","Il tuo percorso"),T("heading","Titolo","Cosa cambia, settimana dopo settimana.")]+sum([[IMG("step%d_image"%i,"Step %d · immagine"%i),URL("step%d_image_url"%i,"Step %d · immagine"%i,u),T("step%d_title"%i,"Step %d · titolo"%i,t),T("step%d_text"%i,"Step %d · testo"%i,x)] for i,(u,t,x) in enumerate([(I("133241_b04083cf-2797-417c-a668-1d31438e7ebf"),"Settimane 1-3: idratazione","La pelle beve. Meno secchezza, meno fondotinta per coprire, un viso più riposato."),(I("133241_a4ddb530-ae66-412d-a16f-b29af692d74b"),"Settimane 4-7: luminosità","Il colorito si accende. Le amiche iniziano a chiederti cosa stai facendo di diverso."),(I("133240_4ced341c-f117-401a-b5a7-d4080dacac47"),"Settimane 8-12: compattezza","Viso più tonico, rughe sottili meno visibili. Ti guardi allo specchio e ti riconosci."),("","","")],1)],[])+[CB("dark","Tema scuro",True)]+PADS()},
 {"type":"closeup","name":"Close-up","settings":[T("eyebrow","Sopra-titolo","Guarda da vicino"),T("heading","Titolo","Liquido. Già sciolto. Pronto da bere."),TA("sub","Sottotitolo","Sa di mango e passion fruit, zero pesce. Sta in borsa, si beve in 25 secondi. Il gesto di bellezza più facile della tua giornata.")]+sum([[IMG("image_%d"%i,"Macro %d"%i),URL("image_url_%d"%i,"Macro %d"%i,u)] for i,u in enumerate([I("133254_e48850f5-6671-4e5b-bc13-494ca45bfb60"),I("133252_e40b715d-aac4-4a66-ab0e-1bf472fb3790"),I("133253_a095fd80-1e6b-4c1d-a9a9-8cc6d2128b44"),""],1)],[])+[CB("mobile_horizontal","Mobile: pin + scroll orizzontale",True),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"whats_inside","name":"Formula","settings":[T("eyebrow","Sopra-titolo","La formula"),T("heading","Titolo","Costruisci. Proteggi. Attiva."),T("sub","Sottotitolo","Sei attivi che lavorano insieme per una pelle più compatta, protetta e luminosa.")]+sum([[IMG("g%d_image"%i,"Foto %d"%i),URL("g%d_image_url"%i,"Foto %d"%i,u),T("g%d_caption"%i,"Foto %d · didascalia"%i,c)] for i,(u,c) in enumerate([(I("133253_30982ea6-2615-4a32-b502-41790e54d059"),"6 attivi, nessun riempitivo"),(I("133253_d338bb4a-03f7-48f0-a1bc-0da4d5fca874"),"Il sistema a 3 livelli"),(I("133254_352c07bd-f5b1-4d7d-a673-f432152ad6f9"),"10 sachet da 25 ml")],1)],[])+[{"type":"header","content":"Ingredienti"}]+sum([[T("ing%d_tag"%i,"%d · livello"%i,a),T("ing%d_name"%i,"%d · nome"%i,b),T("ing%d_desc"%i,"%d · descrizione"%i,c),T("ing%d_dose"%i,"%d · dose"%i,d)] for i,(a,b,c,d) in enumerate([("Costruisci","Collagene marino tripeptide","Riaccende la produzione di collagene: pelle più compatta ed elastica","5.000 mg"),("Costruisci","Vitamina C","Contribuisce alla normale formazione del collagene per la normale funzione della pelle*","80 mg"),("Proteggi","Estratto di cranberry","Protegge il tuo collagene dai radicali liberi","500 mg"),("Proteggi","Zinco","Contribuisce al mantenimento di pelle e capelli normali*","10 mg"),("Attiva","Acido ialuronico","Idrata in profondità e rimpolpa le linee sottili","100 mg"),("Attiva","Probiotici Lactobacillus","Intestino in equilibrio, collagene assorbito al massimo","1 mld CFU"),("","","",""),("","","","")],1)],[])+[CB("tinted","Sfondo tinta",True)]+PADS()},
 {"type":"objections","name":"Obiezioni","settings":[T("heading","Titolo","Le domande che ti fai prima di provarlo.")]+sum([[T("q%d"%i,"Dubbio %d"%i,q),TA("a%d"%i,"Risposta %d"%i,a) if a else T("a%d"%i,"Risposta %d"%i,"")] for i,(q,a) in enumerate([("\"Il collagene non viene digerito e basta?\"","Quello generico, sì. Per questo non hai visto niente. I tripeptidi di Within sono così piccoli da arrivare fino alla pelle."),("\"Ne ho già provati altri. Niente.\"","Erano collageni troppo grandi per arrivare a destinazione. Con Within la tua pelle riceve finalmente quello che le serve. Non era colpa tua."),("\"Gli studi li pagano le aziende.\"","Hai ragione a diffidare. Per questo ti diamo 90 giorni: la prova non sono gli studi, è il tuo specchio."),("\"Quanto devo aspettare?\"","Pelle più idratata in 2-3 settimane. Compattezza e rughe meno visibili in 8-12. E hai 90 giorni di garanzia per vederlo con i tuoi occhi."),("\"E i metalli pesanti?\"","Il Clean Label Project ha trovato tracce di metalli pesanti nel 64% dei collageni venduti su Amazon. Ogni lotto Within è testato, e il certificato è pubblico."),("\"E se non vedo nessuna differenza?\"","Ci scrivi entro 90 giorni dall'acquisto e ti rimborsiamo. Il rischio è nostro, non tuo.")],1)],[])+[CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"social_proof","name":"Recensioni","settings":[T("eyebrow","Sopra-titolo","Cosa dice la ricerca"),T("heading","Titolo","Risultati che si misurano. E che si vedono."),{"type":"header","content":"Statistiche"}]+sum([[T("stat%d_prefix"%i,"Stat %d · prefisso"%i,p),T("stat%d_count"%i,"Stat %d · numero"%i,n),T("stat%d_suffix"%i,"Stat %d · suffisso"%i,x),T("stat%d_label"%i,"Stat %d · etichetta"%i,l)] for i,(p,n,x,l) in enumerate([("+","23","%","idratazione"),("−","17","%","rughe contorno occhi"),("+","15","%","compattezza")],1)],[])+[TA("source_note","Nota fonte","Risultati medi da studi clinici su peptidi di collagene, dopo 8-12 settimane di assunzione quotidiana."),{"type":"header","content":"Recensioni"},T("verified_label","Etichetta verificato","Acquisto verificato")]+sum([[IMG("r%d_image"%i,"%d · foto"%i),URL("r%d_image_url"%i,"%d · foto"%i,u),TA("r%d_quote"%i,"%d · testo"%i,q),T("r%d_name"%i,"%d · nome"%i,n),T("r%d_meta"%i,"%d · età · città"%i,m)] for i,(u,q,n,m) in enumerate([(I("022310_72453d34-0f9b-4a13-84b2-0ee0f50c6841"),"\"Dopo tre settimane la pelle è visibilmente più idratata. Le colleghe mi hanno chiesto cosa uso.\"","Laura","58 · Milano"),(I("022311_9c358caf-86cc-4057-b42c-4a569e68826b"),"\"Avevo provato tre integratori senza risultati. Con Within ho visto la differenza dopo circa sei settimane.\"","Francesca","56 · Roma"),(I("022311_c44c87da-8b75-4660-9b9d-063661e85a11"),"\"Il gusto è buonissimo, sembra un succo. È l'unico integratore che non dimentico mai di prendere.\"","Giulia","60 · Torino")],1)],[])+[T("big_quote","Citazione grande","\"Per la prima volta ho capito cosa stavo bevendo, e perché.\""),T("big_quote_cite","Citazione · autore","— Francesca, 56"),T("cta_label","Pulsante (torna su)","Voglio questi risultati"),CB("tinted","Sfondo tinta",True)]+PADS()},
 {"type":"authority","name":"Autorità","settings":[T("eyebrow","Sopra-titolo","Trasparenza radicale"),IMG("image","Immagine"),URL("image_url","Immagine",I("133253_113ae570-8806-4947-b614-a6b1a28d0c82")),TA("quote","Citazione","\"Gli altri ti chiedono di fidarti. Noi ti diamo i documenti per controllare.\""),T("point1","Punto 1","Peso molecolare dichiarato: sotto i 3.000 Da"),T("point2","Punto 2","Certificato di analisi per ogni lotto"),T("point3","Punto 3","Test metalli pesanti, pubblicato"),T("point4","Punto 4","Ogni dose al milligrammo, niente formule segrete"),T("point5","Punto 5 (opz.)","Formulato per la pelle dopo i 35 anni"),T("name","Firma","Il team Within"),T("role","Ruolo","Ricerca e Sviluppo"),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"guarantee","name":"Garanzia","settings":[T("eyebrow","Sopra-titolo","Garanzia 90 giorni"),T("days","Numero gigante","90"),T("days_unit","Unità","giorni"),T("heading","Titolo","Se la tua pelle non cambia, non paghi."),TA("sub","Testo","Bevilo per 90 giorni. Se allo specchio non vedi una pelle più compatta e luminosa, ti restituiamo i soldi. Il rischio è tutto nostro."),{"type":"header","content":"Le 3 strade (l'ultima è evidenziata)"}]+sum([[T("path%d_title"%i,"Strada %d · titolo"%i,t),TA("path%d_text"%i,"Strada %d · testo"%i,x)] for i,(t,x) in enumerate([("Se non fai niente","Ogni anno perdi l'1-1,5% del tuo collagene. E le rughe si scavano un po' di più."),("Se scegli un collagene qualunque","Spendi 30-70 € al mese per qualcosa che il corpo digerisce prima che arrivi alla pelle."),("Se scegli Within","In 12 settimane ti guardi allo specchio e ti piaci di nuovo. Oppure ti rimborsiamo.")],1)],[])+[T("cta_label","Pulsante (torna su)","Inizia il tuo percorso"),IMG("image","Immagine"),URL("image_url","Immagine",I("133253_a095fd80-1e6b-4c1d-a9a9-8cc6d2128b44")),CB("reversed","Immagine a sinistra",False),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"faq","name":"FAQ","settings":[T("heading","Titolo","Buono a sapersi.")]+sum([[T("q%d"%i,"Domanda %d"%i,q),(TA("a%d"%i,"Risposta %d"%i,a) if a else T("a%d"%i,"Risposta %d"%i,""))] for i,(q,a) in enumerate([("Quanto dura una confezione?","Ogni box contiene 10 sachet: con uno al giorno dura 10 giorni. Per un mese completo servono 3 box."),("Mattina o sera?","Quando preferisci. Conta la costanza quotidiana, non l'orario."),("Sa di pesce?","No. Gusto mango e frutto della passione, fresco e piacevole."),("Contiene lattosio o glutine?","No. Contiene però collagene di origine marina: se sei allergica al pesce, consulta il tuo medico."),("Quando vedo i risultati?","Idratazione in 2-3 settimane, luminosità in 4-6, compattezza e rughe meno visibili in 8-12 settimane di uso quotidiano."),("Se smetto, torna tutto come prima?","Il collagene che hai prodotto resta. Ma dopo i 25 anni il corpo ne perde l'1-1,5% l'anno: per mantenere i risultati, continua."),("In cosa è diverso dagli altri collageni?","Due cose. Un collagene tre volte più piccolo, che arriva davvero alla pelle. E 1 miliardo di fermenti lattici che ne fanno assorbire di più. Risultato: la pelle cambia, e si vede."),("Come funziona la garanzia?","Se entro 90 giorni dall'acquisto non sei soddisfatta, scrivici e ti rimborsiamo. Il rischio è nostro, non tuo.")],1)],[])+[TA("disclaimer","Disclaimer legale","Within è un integratore alimentare. Gli integratori non vanno intesi come sostituti di una dieta varia ed equilibrata e di uno stile di vita sano. Non superare la dose giornaliera consigliata. Tenere fuori dalla portata dei bambini al di sotto dei 3 anni. *Claim autorizzati dall'EFSA per Vitamina C e Zinco. I risultati possono variare da persona a persona. Garanzia soddisfatta o rimborsata di 90 giorni secondo le condizioni di vendita."),CB("tinted","Sfondo tinta",True)]+PADS()}
],
"presets":[{"name":"Within · Product Page","blocks":[
 {"type":"ugc_slider","settings":dict({"eyebrow":"Ogni mattina, 25 secondi","heading":"Il gesto che si vede allo specchio."},**{"video_url_%d"%(i+1):V(v) for i,v in enumerate(vids1)},**{"caption_%d"%(i+1):"%s, %d"%c for i,c in enumerate(CAPS1)})},
 {"type":"value_prop"},{"type":"cinematic"},{"type":"benefits"},
 {"type":"benefits","settings":{"bignum":"","bignum_unit":"","eyebrow":"Quello che gli altri collageni non hanno","heading":"Una pelle luminosa comincia dalla pancia.","sub":"Se l'intestino è in disordine, assorbi meno e la pelle si spegne. 1 miliardo di fermenti lattici Lactobacillus rimettono in equilibrio l'intestino, così ogni sorso di collagene lavora fino in fondo. Nessun altro collagene in Italia lo fa.","link_label":"","image_url":I("133240_ee766943-416e-4325-b47c-79f0d5d04a3e"),"reversed":True,"tinted":True}},
 {"type":"feature_row"},
 {"type":"cinematic","settings":{"eyebrow":"Il momento più bello","heading":"Quando ti chiedono: “Ma cosa ti sei fatta?”","image_url":I("232315_b4edd37c-9815-423b-8762-11bce1d2ce17"),"parallax":0.2}},
 {"type":"how_it_works"},{"type":"closeup"},{"type":"whats_inside"},
 {"type":"ugc_slider","settings":dict({"eyebrow":"","heading":"Loro hanno già iniziato."},**{"video_url_%d"%(i+1):V(v) for i,v in enumerate(vids2)},**{"caption_%d"%(i+1):"%s, %d"%c for i,c in enumerate(CAPS2)})},
 {"type":"objections"},{"type":"social_proof"},{"type":"authority"},{"type":"guarantee"},{"type":"faq"}]}]}
# drop empty-string defaults (Shopify rejects empty default on some types)
for b in schema['blocks']:
    for s in b['settings']:
        if s.get('default')=="" : del s['default']
out='''{% comment %}
  Within · Collagene Marino — Product Page "stile Apple" (product-page-builder, profilo Apple)
  Sezione a blocchi da mettere sotto l'hero del template prodotto. CSS scoped, font del tema.
  Ogni immagine/video: carica un file dal theme editor oppure lascia il link precompilato.
{% endcomment %}
{% style %}
'''+scss+'''
{% endstyle %}
'''+body+'''
<script>'''+js+'''</script>

{% schema %}
'''+json.dumps(schema,ensure_ascii=False,indent=2)+'''
{% endschema %}
'''
open('/home/claude/within-theme/sections/within-product-page.liquid','w').write(out)
print(len(out))

import os
if os.environ.get('WITHIN_PP_TEMPLATE')=='1':
    # ---- rebuild templates/product.within.json section from preset + defaults ----
    T_PATH='/home/claude/within-theme/templates/product.within.json'
    raw=open(T_PATH).read(); k=raw.find('{'); head=raw[:k]; tpl=json.loads(raw[k:])
    defs={b['type']:{s['id']:s['default'] for s in b['settings'] if 'default' in s} for b in schema['blocks']}
    blocks={}; order=[]
    for n,pb in enumerate(schema['presets'][0]['blocks'],1):
        bid='%s_%d'%(pb['type'],n); st=dict(defs[pb['type']]); st.update(pb.get('settings',{}))
        blocks[bid]={'type':pb['type'],'settings':st}; order.append(bid)
    tpl['sections']['within_pp']['blocks']=blocks; tpl['sections']['within_pp']['block_order']=order
    open(T_PATH,'w').write(head+json.dumps(tpl,ensure_ascii=False,indent=2))
    print('template blocks',len(order))
