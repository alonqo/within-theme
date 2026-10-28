# Builds sections/within-pdp.liquid (new CRO product page, sales-letter structure) and patches templates/product.within.json
import json, os
SP=os.path.dirname(os.path.abspath(__file__))
ns={}; exec(open(os.path.join(SP,'gen.py')).read(), ns)
scss, js, scope = ns['scss'], ns['js'], ns['scope']
T,TA,IMG,CB,PADS,I,V = [ns[k] for k in 'T TA IMG CB PADS I V'.split()]
def R(i,l,mn,mx,st,d,unit=None):
    r={"type":"range","id":i,"label":l,"min":mn,"max":mx,"step":st,"default":d}
    if unit: r["unit"]=unit
    return r
PAD=' style="--pt:{{ block.settings.padding_top }}px;--pb:{{ block.settings.padding_bottom }}px;"'
TINT='{% if block.settings.tinted %} wa-tint{% endif %}'
EB='{% if block.settings.eyebrow != blank %}<p class="wa-eyebrow">{{ block.settings.eyebrow }}</p>{% endif %}'
def ATC(label, cls='wa-btn'):
    return ('{%- if section.settings.cta_action == "cart" and product != blank -%}'
            '<form method="post" action="{{ routes.cart_add_url }}" class="wp-atc"><input type="hidden" name="form_type" value="product"><input type="hidden" name="utf8" value="✓">'
            '<input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}"><input type="hidden" name="quantity" value="1">'
            '<button type="submit" class="'+cls+'">'+label+'</button></form>'
            '{%- else -%}<a class="'+cls+' wa-top" href="#">'+label+'</a>{%- endif -%}')
CTA_ROW='{% if block.settings.cta_label != blank %}<div class="wp-cta">'+ATC('{{ block.settings.cta_label }}')+'{% if block.settings.cta_note != blank %}<p class="wp-cta-note">{{ block.settings.cta_note }}</p>{% endif %}</div>{% endif %}'
def IM(pick,url,cls='',w=1400):
    return ('{%% if block.settings.%s != blank %%}<img class="%s" src="{{ block.settings.%s | image_url: width: %d }}" alt="{{ block.settings.%s.alt | escape }}" loading="lazy">'
            '{%% elsif block.settings.%s != blank %%}<img class="%s" src="{{ block.settings.%s }}" alt="" loading="lazy">{%% endif %%}')%(pick,cls,pick,w,pick,url,cls,url)
def DIM(p,u,cls='',w=900):
    return ('{%% if %s != blank %%}<img class="%s" src="{{ %s | image_url: width: %d }}" alt="{{ %s.alt | escape }}" loading="lazy">'
            '{%% elsif %s != blank %%}<img class="%s" src="{{ %s }}" alt="" loading="lazy">{%% endif %%}')%(p,cls,p,w,p,u,cls,u)
def LINES(setting, var='ln'):
    return "{%%- assign %s_all = block.settings.%s | newline_to_br | split: '<br />' -%%}"%(var,setting)

body='''
<div class="wa-root wp">
{%- for block in section.blocks -%}
{%- case block.type -%}

{%- when 'trust' -%}
<div class="wp-trust" {{ block.shopify_attributes }}>
  <div class="wp-trust-in">
  {%- for i in (1..4) -%}{%- assign k = 'item_' | append: i -%}{%- assign t = block.settings[k] -%}
    {%- if t != blank -%}<div class="wp-trust-i"><span class="wp-ico wp-ico-{{ i }}" aria-hidden="true"></span><span>{{ t }}</span></div>{%- endif -%}
  {%- endfor -%}
  </div>
</div>

{%- when 'ugc' -%}
<section class="wa-ugc'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  {%- if block.settings.heading != blank or block.settings.eyebrow != blank -%}<div class="wa-ugc-head wa-reveal">'''+EB+'''{% if block.settings.heading != blank %}<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% endif %}</div>{%- endif -%}
  <div class="wa-ugc-track" data-autoscroll="{{ block.settings.autoscroll_ms }}">
  {%- for i in (1..8) -%}
    {%- assign vk = 'video_' | append: i -%}{%- assign uk = 'video_url_' | append: i -%}{%- assign ck = 'caption_' | append: i -%}
    {%- assign v = block.settings[vk] -%}{%- assign vu = block.settings[uk] -%}{%- assign cap = block.settings[ck] -%}
    {%- capture capt -%}{%- if cap != blank -%}<figcaption class="wa-ugc-cap"><b>{{ cap }}</b>{% if block.settings.verified_label != blank %}<span class="wa-ugc-ver"><i></i>{{ block.settings.verified_label }}</span>{% endif %}</figcaption>{%- endif -%}{%- endcapture -%}
    {%- if v != blank -%}<figure class="wa-ugc-item"><div class="wa-ugc-slide">{{ v | video_tag: autoplay: true, loop: true, muted: true, controls: false, playsinline: true, preload: 'metadata' }}{{ capt }}</div></figure>
    {%- elsif vu != blank -%}<figure class="wa-ugc-item"><div class="wa-ugc-slide"><video src="{{ vu }}" autoplay muted loop playsinline preload="metadata"></video>{{ capt }}</div></figure>{%- endif -%}
  {%- endfor -%}
  </div>
</section>

{%- when 'lead' -%}
<section class="wa-sect wp-lead'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide wp-lead-g">
    <div class="wp-lead-media wa-reveal">'''+IM('image','image_url','',1200)+'''</div>
    <div class="wp-lead-copy wa-reveal">'''+EB+'''
      <h2 class="wp-h">{{ block.settings.heading }}</h2>
      <div class="wp-prose">{{ block.settings.text }}</div>
      {% if block.settings.kicker != blank %}<p class="wp-kicker">{{ block.settings.kicker }}</p>{% endif %}
    </div>
  </div>
</section>

{%- when 'mechanism' -%}
<section class="wa-sect wp-mech wa-dark" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-center wa-reveal wp-mech-head">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub">{{ block.settings.sub }}</p>{% endif %}</div>
    <div class="wp-vs">
      <div class="wp-vs-c wp-vs-bad wa-reveal">
        <p class="wp-vs-l">{{ block.settings.a_label }}</p>
        <div class="wp-mol wp-mol-big" aria-hidden="true"><i></i><i></i><i></i></div>
        <p class="wp-vs-n">{{ block.settings.a_big }}</p>
        '''+LINES('a_points','a')+'''<ul>{%- for l in a_all -%}{%- assign t = l | strip -%}{%- if t != blank -%}<li>{{ t }}</li>{%- endif -%}{%- endfor -%}</ul>
      </div>
      <div class="wp-vs-c wp-vs-good wa-reveal" style="--d:.12s">
        <p class="wp-vs-l">{{ block.settings.b_label }}</p>
        <div class="wp-mol wp-mol-small" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
        <p class="wp-vs-n">{{ block.settings.b_big }}</p>
        '''+LINES('b_points','b')+'''<ul>{%- for l in b_all -%}{%- assign t = l | strip -%}{%- if t != blank -%}<li>{{ t }}</li>{%- endif -%}{%- endfor -%}</ul>
      </div>
    </div>
    {% if block.settings.note != blank %}<div class="wp-mech-note wa-reveal"><span class="wp-key" aria-hidden="true">2</span><p>{{ block.settings.note }}</p></div>{% endif %}
  </div>
</section>

{%- when 'benefits' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide wp-ben">
    <div class="wp-ben-media">'''+IM('image','image_url','',1200)+'''</div>
    <div class="wp-ben-copy">
      <div class="wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2></div>
      <ul class="wp-ben-list">
      {%- for i in (1..6) -%}{%- assign tk = 'b' | append: i | append: '_title' -%}{%- assign xk = 'b' | append: i | append: '_text' -%}
        {%- if block.settings[tk] != blank -%}<li class="wa-reveal"><b>{{ block.settings[tk] }}</b> {{ block.settings[xk] }}</li>{%- endif -%}
      {%- endfor -%}
      </ul>
      '''+CTA_ROW+'''
    </div>
  </div>
</section>

{%- when 'formula' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wp-head wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2>{% if block.settings.sub != blank %}<p class="wa-sub wa-left">{{ block.settings.sub }}</p>{% endif %}</div>
    <div class="wp-form">
    {%- for i in (1..6) -%}{%- assign nk = 'i' | append: i | append: '_name' -%}
      {%- if block.settings[nk] != blank -%}{%- assign dk = 'i' | append: i | append: '_dose' -%}{%- assign tk = 'i' | append: i | append: '_tag' -%}{%- assign xk = 'i' | append: i | append: '_text' -%}
      <div class="wp-ing wa-reveal" style="--d:{{ forloop.index0 | times: 0.05 }}s"><span class="wp-ing-tag">{{ block.settings[tk] }}</span><p class="wp-ing-dose">{{ block.settings[dk] }}</p><h3>{{ block.settings[nk] }}</h3><p>{{ block.settings[xk] }}</p></div>
      {%- endif -%}
    {%- endfor -%}
    </div>
    {% if block.settings.footnote != blank %}<p class="wp-foot wa-reveal">{{ block.settings.footnote }}</p>{% endif %}
  </div>
</section>

{%- when 'timeline' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wa-center wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2></div>
    <ol class="wp-tl">
    {%- for i in (1..3) -%}{%- assign wk = 's' | append: i | append: '_when' -%}{%- assign tk = 's' | append: i | append: '_title' -%}{%- assign xk = 's' | append: i | append: '_text' -%}
      {%- if block.settings[tk] != blank -%}<li class="wa-reveal" style="--d:{{ forloop.index0 | times: 0.12 }}s"><span class="wp-tl-w">{{ block.settings[wk] }}</span><h3>{{ block.settings[tk] }}</h3><p>{{ block.settings[xk] }}</p></li>{%- endif -%}
    {%- endfor -%}
    </ol>
    {% if block.settings.note != blank %}<p class="wp-tl-note wa-reveal">{{ block.settings.note }}</p>{% endif %}
  </div>
</section>

{%- when 'reviews' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-wide">
    <div class="wa-center wa-reveal">'''+EB+'''<h2 class="wa-h2 wp-quote-h">{{ block.settings.heading }}</h2>
      {% if block.settings.rating != blank %}<p class="wp-rating"><span class="wa-stars">★★★★★</span> {{ block.settings.rating }}</p>{% endif %}
    </div>
    {%- if block.settings.stat1 != blank -%}
    <div class="wp-stats wa-reveal">{%- for i in (1..3) -%}{%- assign sk = 'stat' | append: i -%}{%- assign lk = 'stat' | append: i | append: '_label' -%}{%- if block.settings[sk] != blank -%}<div><b>{{ block.settings[sk] }}</b><span>{{ block.settings[lk] }}</span></div>{%- endif -%}{%- endfor -%}</div>
    {% if block.settings.stats_note != blank %}<p class="wa-src wa-reveal">{{ block.settings.stats_note }}</p>{% endif %}
    {%- endif -%}
    <div class="wp-revs">
    {%- for i in (1..3) -%}{%- assign qk = 'r' | append: i | append: '_quote' -%}
      {%- if block.settings[qk] != blank -%}{%- assign hk = 'r' | append: i | append: '_title' -%}{%- assign nk = 'r' | append: i | append: '_name' -%}{%- assign pk = 'r' | append: i | append: '_image' -%}{%- assign uk = 'r' | append: i | append: '_image_url' -%}{%- assign p = block.settings[pk] -%}{%- assign u = block.settings[uk] -%}
      <figure class="wp-rev wa-reveal" style="--d:{{ forloop.index0 | times: 0.1 }}s">
        <div class="wa-stars">★★★★★</div>
        {% if block.settings[hk] != blank %}<h3>{{ block.settings[hk] }}</h3>{% endif %}
        <blockquote>{{ block.settings[qk] }}</blockquote>
        <figcaption>'''+DIM('p','u','',200)+'''<span><b>{{ block.settings[nk] }}</b><em class="wa-ugc-ver" style="color:#2e7d5b"><i></i>{{ block.settings.verified_label }}</em></span></figcaption>
      </figure>
      {%- endif -%}
    {%- endfor -%}
    </div>
  </div>
</section>

{%- when 'compare' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wa-center wa-reveal" style="margin-bottom:40px">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2></div>
    <div class="wh-cmp wa-reveal" role="table">
      <div class="wh-cmp-r wh-cmp-h" role="row"><span role="columnheader"></span><span class="wh-cmp-w" role="columnheader">{{ block.settings.col_a }}</span><span role="columnheader">{{ block.settings.col_b }}</span><span role="columnheader">{{ block.settings.col_c }}</span></div>
      {%- for i in (1..7) -%}{%- assign lk = 'r' | append: i | append: '_label' -%}
        {%- if block.settings[lk] != blank -%}{%- assign ak = 'r' | append: i | append: '_a' -%}{%- assign bk = 'r' | append: i | append: '_b' -%}{%- assign ck = 'r' | append: i | append: '_c' -%}
        <div class="wh-cmp-r" role="row"><span class="wh-cmp-l" role="rowheader">{{ block.settings[lk] }}</span><span class="wh-cmp-w" role="cell">{{ block.settings[ak] }}</span><span role="cell">{{ block.settings[bk] }}</span><span role="cell">{{ block.settings[ck] }}</span></div>
        {%- endif -%}
      {%- endfor -%}
    </div>
    '''+CTA_ROW+'''
  </div>
</section>

{%- when 'guarantee' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wp-gar wa-reveal">
      <div class="wp-seal" aria-hidden="true"><svg viewBox="0 0 200 200"><defs><path id="wpsc" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text><textPath href="#wpsc" startOffset="0">{{ block.settings.seal_text }}</textPath></text></svg><b>{{ block.settings.seal_big }}</b><span>{{ block.settings.seal_small }}</span></div>
      <div class="wp-gar-c">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2><div class="wp-prose">{{ block.settings.text }}</div>'''+CTA_ROW+'''</div>
    </div>
  </div>
</section>

{%- when 'faq' -%}
<section class="wa-sect'''+TINT+'''" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wa-inner">
    <div class="wa-center wa-reveal">'''+EB+'''<h2 class="wa-h2">{{ block.settings.heading }}</h2></div>
    <div class="wa-faq wa-reveal">
    {%- for i in (1..8) -%}{%- assign qk = 'q' | append: i -%}{%- assign q = block.settings[qk] -%}
      {%- if q != blank -%}{%- assign ak = 'a' | append: i -%}<details{% if forloop.first %} open{% endif %}><summary>{{ q }}<span class="wa-pm"></span></summary><div class="wa-ans">{{ block.settings[ak] }}</div></details>{%- endif -%}
    {%- endfor -%}
    </div>
    {% if block.settings.disclaimer != blank %}<div class="wa-disc">{{ block.settings.disclaimer }}</div>{% endif %}
  </div>
</section>

{%- when 'final' -%}
<section class="wp-final" {{ block.shopify_attributes }}'''+PAD+'''>
  <div class="wp-final-media">'''+IM('image','image_url','wh-cover',2200)+'''</div>
  <div class="wp-final-in wa-reveal">'''+EB+'''<h2 class="wp-final-h">{{ block.settings.heading }}</h2>{% if block.settings.text != blank %}<p class="wa-sub">{{ block.settings.text }}</p>{% endif %}'''+CTA_ROW+'''</div>
</section>

{%- endcase -%}
{%- endfor -%}

{%- if section.settings.sticky and product != blank -%}
<div class="wp-sticky" data-sticky>
  <div class="wp-sticky-in">
    {%- if product.featured_image != blank -%}<img src="{{ product.featured_image | image_url: width: 120 }}" alt="" width="46" height="46">{%- endif -%}
    <div class="wp-sticky-t"><b>{{ product.title }}</b><span>{% if product.price > 0 %}{{ product.price | money }} · {% endif %}{{ section.settings.sticky_note }}</span></div>
    '''+ATC('{{ section.settings.sticky_label }}','wa-btn wp-sticky-b')+'''
  </div>
</div>
{%- endif -%}
</div>
'''

CSS='''
.wp .wa-sect{padding:var(--pt,120px) 22px var(--pb,120px)}
.wp-cta{margin-top:34px;display:flex;flex-direction:column;align-items:flex-start;gap:10px}
.wa-center .wp-cta,.wp-final .wp-cta,.wa-inner>.wp-cta{align-items:center}
.wp-atc{margin:0}
.wp-cta .wa-btn{min-height:56px;padding:16px 34px;font-size:1.08rem}
.wp-cta-note{margin:0;font-size:.84rem;color:var(--muted)}
.wp-trust{background:var(--bg);border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft)}
.wp-trust-in{max-width:var(--wide);margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:20px 22px}
.wp-trust-i{display:flex;align-items:center;gap:12px;font-size:.92rem;font-weight:600;color:var(--ink)}
.wp-ico{flex:0 0 auto;width:34px;height:34px;border-radius:50%;background:var(--bg-2);position:relative}
.wp-ico::after{content:"";position:absolute;inset:0;margin:auto;width:9px;height:15px;border:solid var(--accent);border-width:0 2.4px 2.4px 0;transform:translate(0,-2px) rotate(45deg)}
.wp-h{font-size:clamp(2.2rem,4.8vw,3.6rem);font-weight:650;line-height:1.05;letter-spacing:-.03em;margin:0 0 26px;color:var(--ink)}
.wp-prose{font-size:1.18rem;line-height:1.62;color:var(--ink)}
.wp-prose p{margin:0 0 18px}
.wp-prose strong{font-weight:650}
.wp-kicker{margin:26px 0 0;font-size:clamp(1.3rem,2.4vw,1.7rem);font-weight:650;letter-spacing:-.015em;color:var(--accent);line-height:1.25}
.wp-lead-g{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(32px,6vw,88px);align-items:center}
.wp-lead-media{border-radius:var(--r-lg);overflow:hidden;aspect-ratio:4/5;background:var(--bg-2)}
.wp-lead-media img{width:100%;height:100%!important;object-fit:cover}
.wp-lead-copy{max-width:56ch}
.wp-mech-head{max-width:820px;margin:0 auto 56px}
.wp-mech .wa-h2{color:#fff}
.wp-vs{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1040px;margin:0 auto}
.wp-vs-c{border-radius:var(--r-lg);padding:clamp(26px,4vw,44px);background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1)}
.wp-vs-good{background:var(--bg);color:var(--ink);border-color:transparent;box-shadow:0 30px 70px rgba(0,0,0,.35)}
.wp-vs-l{margin:0;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--on-dark-mut)}
.wp-vs-good .wp-vs-l{color:var(--accent)}
.wp-vs-n{margin:14px 0 18px;font-size:clamp(2.6rem,5vw,3.8rem);font-weight:650;letter-spacing:-.04em;line-height:1;color:#fff}
.wp-vs-good .wp-vs-n{color:var(--accent)}
.wp-vs-c ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.wp-vs-c li{position:relative;padding-left:30px;font-size:1.04rem;color:var(--on-dark-mut)}
.wp-vs-good li{color:var(--ink)}
.wp-vs-c li::before{content:"";position:absolute;left:0;top:.25em;width:18px;height:18px;border-radius:50%;background:rgba(255,255,255,.12)}
.wp-vs-bad li::after{content:"\\00d7";position:absolute;left:5px;top:-.02em;font-size:1rem;color:#e99}
.wp-vs-good li::before{background:var(--accent)}
.wp-vs-good li::after{content:"";position:absolute;left:6.5px;top:.42em;width:4px;height:8px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}
.wp-mol{height:96px;margin:22px 0 4px;display:flex;align-items:center;gap:10px}
.wp-mol-big i{width:84px;height:84px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.35),rgba(255,255,255,.08));border:1px solid rgba(255,255,255,.18)}
.wp-mol-small{flex-wrap:wrap;align-content:center;max-width:220px;gap:8px}
.wp-mol-small i{width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#f2c05c,#cc5b3e);animation:wp-float 3s ease-in-out infinite}
.wp-mol-small i:nth-child(2n){animation-delay:.6s}.wp-mol-small i:nth-child(3n){animation-delay:1.2s}
@keyframes wp-float{50%{transform:translateY(-6px)}}
.wp-mech-note{display:flex;gap:18px;align-items:flex-start;max-width:820px;margin:44px auto 0;padding:24px 28px;border-radius:var(--r-lg);border:1px solid rgba(255,255,255,.14)}
.wp-mech-note p{margin:0;font-size:1.08rem;line-height:1.55;color:var(--on-dark)}
.wp-key{flex:0 0 auto;width:36px;height:36px;border-radius:50%;background:var(--accent-hi);color:var(--dark);font-weight:700;display:flex;align-items:center;justify-content:center}
.wp-ben{display:grid;grid-template-columns:1fr 1fr;gap:clamp(32px,6vw,80px);align-items:start}
.wp-ben-media{position:sticky;top:90px;border-radius:var(--r-lg);overflow:hidden;aspect-ratio:4/5;background:var(--bg-2)}
.wp-ben-media img{width:100%;height:100%!important;object-fit:cover}
.wp-ben-list{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:0;border-top:1px solid var(--line)}
.wp-ben-list li{position:relative;padding:20px 0 20px 44px;border-bottom:1px solid var(--line);font-size:1.1rem;line-height:1.5;color:var(--muted)}
.wp-ben-list li b{color:var(--ink);font-weight:650}
.wp-ben-list li::before{content:"";position:absolute;left:0;top:22px;width:26px;height:26px;border-radius:50%;background:var(--accent)}
.wp-ben-list li::after{content:"";position:absolute;left:9.5px;top:28px;width:5px;height:10px;border:solid #fff;border-width:0 2.2px 2.2px 0;transform:rotate(45deg)}
.wp-head{display:grid;grid-template-columns:1fr 1fr;gap:16px 56px;align-items:end;margin-bottom:44px}
.wp-head .wa-eyebrow{grid-column:1/-1;margin:0}.wp-head .wa-h2{margin:0}
.wp-form{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.wp-ing{background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:28px;transition:transform .4s,box-shadow .4s}
.wp-ing:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(28,43,40,.08)}
.wp-ing-tag{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);background:rgba(168,67,46,.08);padding:5px 10px;border-radius:var(--r-pill)}
.wp-ing-dose{margin:16px 0 4px;font-size:2rem;font-weight:650;letter-spacing:-.03em;color:var(--ink)}
.wp-ing h3{margin:0 0 8px;font-size:1.1rem;font-weight:600}
.wp-ing p:last-child{margin:0;color:var(--muted);font-size:.98rem}
.wp-foot{margin:22px 0 0;font-size:.8rem;color:var(--muted)}
.wp-tl{list-style:none;margin:56px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px;position:relative}
.wp-tl::before{content:"";position:absolute;left:8px;right:8px;top:9px;height:2px;background:linear-gradient(90deg,var(--line),var(--accent))}
.wp-tl li{position:relative;padding-top:38px}
.wp-tl li::before{content:"";position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;background:var(--bg);border:3px solid var(--accent)}
.wp-tl li:last-child::before{background:var(--accent)}
.wp-tl-w{font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.wp-tl h3{margin:8px 0 6px;font-size:1.35rem;font-weight:600;letter-spacing:-.015em}
.wp-tl p{margin:0;color:var(--muted);font-size:1.04rem}
.wp-tl-note{margin:44px auto 0;max-width:56ch;text-align:center;font-size:1.06rem;color:var(--ink);font-weight:500}
.wp-quote-h{max-width:22ch;margin-left:auto;margin-right:auto}
.wp-rating{margin:6px 0 0;color:var(--muted);font-size:.98rem}
.wp-stats{display:grid;grid-template-columns:repeat(3,1fr);max-width:820px;margin:44px auto 14px;border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;background:var(--bg)}
.wp-stats div{padding:24px 16px;text-align:center;border-right:1px solid var(--line)}
.wp-stats div:last-child{border-right:0}
.wp-stats b{display:block;font-size:2.2rem;font-weight:650;letter-spacing:-.03em;color:var(--accent)}
.wp-stats span{font-size:.88rem;color:var(--muted)}
.wp-revs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
.wp-rev{margin:0;background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:28px;display:flex;flex-direction:column}
.wp-rev h3{margin:12px 0 8px;font-size:1.12rem;font-weight:650;letter-spacing:-.01em}
.wp-rev blockquote{margin:0 0 22px;font-size:1.02rem;line-height:1.55;color:var(--muted);flex:1}
.wp-rev figcaption{display:flex;align-items:center;gap:12px}
.wp-rev figcaption img{width:46px;height:46px!important;border-radius:50%;object-fit:cover}
.wp-rev figcaption span{display:grid;gap:2px;font-size:.92rem}
.wp-rev figcaption em{font-style:normal;font-size:.76rem;display:flex;align-items:center;gap:6px}
.wh-cmp{border-radius:var(--r-lg);border:1px solid var(--line);overflow:hidden;background:var(--bg)}
.wh-cmp-r{display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr;border-bottom:1px solid var(--line-soft)}
.wh-cmp-r:last-child{border-bottom:0}
.wh-cmp-r span{padding:18px 20px;font-size:1rem;color:var(--muted);display:flex;align-items:center}
.wh-cmp-h span{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)}
.wh-cmp-l{color:var(--ink)!important;font-weight:600}
.wh-cmp-r .wh-cmp-w{background:rgba(168,67,46,.07);color:var(--ink);font-weight:600}
.wh-cmp-h .wh-cmp-w{background:var(--accent);color:#fff}
.wp-gar{display:grid;grid-template-columns:auto 1fr;gap:clamp(28px,5vw,64px);align-items:center;background:var(--bg);border:2px solid var(--accent);border-radius:var(--r-lg);padding:clamp(28px,5vw,60px)}
.wp-seal{position:relative;width:200px;height:200px;border-radius:50%;background:var(--accent);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 20px 50px rgba(168,67,46,.35)}
.wp-seal svg{position:absolute;inset:0;width:100%;height:100%;animation:wp-spin 30s linear infinite}
.wp-seal text{fill:#fff;font-size:13px;font-weight:700;letter-spacing:3.2px;text-transform:uppercase}
.wp-seal b{font-size:3.4rem;font-weight:700;line-height:1;letter-spacing:-.04em}
.wp-seal span{font-size:.8rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
@keyframes wp-spin{to{transform:rotate(360deg)}}
.wp-gar .wp-prose{font-size:1.08rem;color:var(--muted)}
.wp-final{position:relative;min-height:min(86vh,800px);display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;background:var(--dark);color:#fff;padding:var(--pt,120px) 22px var(--pb,120px)}
.wp-final-media{position:absolute;inset:0;opacity:.55}
.wh-cover{position:absolute;inset:0;width:100%;height:100%!important;object-fit:cover}
.wp-final::after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(14,22,20,.35),rgba(14,22,20,.85))}
.wp-final-in{position:relative;z-index:2;max-width:780px}
.wp-final-h{font-size:clamp(2.2rem,5vw,3.8rem);font-weight:650;line-height:1.06;letter-spacing:-.03em;margin:0 0 20px;color:#fff}
.wp-final .wa-sub{color:rgba(255,255,255,.86);margin:0 auto}
.wp-final .wa-eyebrow{color:var(--accent-hi)}
.wp-final .wp-cta-note{color:rgba(255,255,255,.7)}
.wp-sticky{position:fixed;left:0;right:0;bottom:0;z-index:60;transform:translateY(110%);transition:transform .35s cubic-bezier(.16,.8,.26,1);padding:10px 14px calc(10px + env(safe-area-inset-bottom))}
.wp-sticky.is-on{transform:none}
.wp-sticky-in{max-width:880px;margin:0 auto;display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.88);-webkit-backdrop-filter:blur(18px) saturate(170%);backdrop-filter:blur(18px) saturate(170%);border:1px solid var(--line);border-radius:22px;padding:10px 10px 10px 12px;box-shadow:0 16px 40px rgba(28,43,40,.18)}
.wp-sticky-in img{border-radius:12px;object-fit:cover;flex:0 0 auto}
.wp-sticky-t{flex:1;min-width:0;display:grid;line-height:1.25}
.wp-sticky-t b{font-size:.95rem;font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--ink)}
.wp-sticky-t span{font-size:.8rem;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wp-sticky .wa-btn{min-height:46px;padding:0 22px;font-size:.95rem;white-space:nowrap}
@media (prefers-reduced-motion:reduce){.wp-seal svg,.wp-mol-small i{animation:none}}
@media (max-width:860px){
.wp .wa-sect{padding:min(var(--pt,120px),76px) 20px min(var(--pb,120px),76px)}
.wp-trust-in{grid-template-columns:1fr 1fr;gap:14px 10px;padding:16px 20px}
.wp-trust-i{font-size:.8rem;gap:9px}.wp-ico{width:28px;height:28px}.wp-ico::after{width:7px;height:12px}
.wp-lead-g,.wp-ben{grid-template-columns:1fr;gap:28px}
.wp-lead-media{aspect-ratio:4/3}
.wp-prose{font-size:1.08rem}
.wp-vs{grid-template-columns:1fr}
.wp-mol{height:70px;margin:16px 0 0}.wp-mol-big i{width:60px;height:60px}
.wp-ben-media{position:relative;top:0;aspect-ratio:4/3}
.wp-head{grid-template-columns:1fr;gap:10px}
.wp-form{grid-template-columns:1fr 1fr;gap:10px}.wp-ing{padding:18px}.wp-ing-dose{font-size:1.5rem}.wp-ing h3{font-size:.98rem}.wp-ing p:last-child{font-size:.86rem}
.wp-tl{grid-template-columns:1fr;gap:26px;margin-top:36px}
.wp-tl::before{left:9px;right:auto;top:8px;bottom:8px;width:2px;height:auto;background:linear-gradient(180deg,var(--line),var(--accent))}
.wp-tl li{padding:0 0 0 40px}
.wp-stats b{font-size:1.5rem}.wp-stats span{font-size:.72rem}.wp-stats div{padding:16px 6px}
.wp-revs{grid-template-columns:1fr}
.wh-cmp-r span{padding:12px 8px;font-size:.78rem}.wh-cmp-h span{font-size:.6rem;letter-spacing:.03em}
.wp-gar{grid-template-columns:1fr;justify-items:center;text-align:center}
.wp-gar .wp-cta{align-items:center}
.wp-seal{width:160px;height:160px}.wp-seal b{font-size:2.6rem}.wp-seal text{font-size:12px}
.wp-sticky-in{border-radius:18px}
.wp-sticky .wa-btn{padding:0 16px}
}
'''
scss2=scss+'\n'+scope(CSS)
STICKY_JS=r'''
var sk=R.querySelector('[data-sticky]');
if(sk){var mainF=null;document.querySelectorAll('form[action*="/cart/add"]').forEach(function(f){if(!mainF&&!f.classList.contains('wp-atc'))mainF=f;});
 var past=false,ft=false;function skU(){var on;if(mainF){var r=mainF.getBoundingClientRect();on=r.bottom<0;}else{on=scrollY>700;}
 var fin=R.querySelector('.wp-final');if(fin){var fr=fin.getBoundingClientRect();if(fr.top<innerHeight*.6&&fr.bottom>0)on=false;}
 sk.classList.toggle('is-on',on);}
 addEventListener('scroll',function(){if(!ft){ft=true;requestAnimationFrame(function(){ft=false;skU();});}},{passive:true});skU();
 document.body.appendChild(sk);}
'''
js2=js.replace("var GAP=12,EDGE=20;", STICKY_JS+"\nvar GAP=12,EDGE=20;",1)
assert STICKY_JS in js2

ug=[T("eyebrow","Sopra-titolo",""),T("heading","Titolo",""),T("verified_label","Etichetta verificato","Acquisto verificato"),R("autoscroll_ms","Auto-scroll",2000,8000,500,4000,"ms")]
for i in range(1,9):
    ug+=[{"type":"video","id":"video_%d"%i,"label":"Video %d (file Shopify)"%i},T("video_url_%d"%i,"Video %d (link mp4)"%i,""),T("caption_%d"%i,"Video %d · didascalia"%i,"")]
ug+=[CB("tinted","Sfondo tinta",False)]+PADS(88,88)
RT=lambda x:{"type":"richtext","id":x[0],"label":x[1]}
schema={"name":"Within · Pagina prodotto","tag":"section","class":"wa-section","max_blocks":30,
"settings":ns['schema']['settings']+[{"type":"header","content":"Pulsanti e barra d'acquisto"},
 {"type":"select","id":"cta_action","label":"I pulsanti della pagina","options":[{"value":"cart","label":"Aggiungono al carrello"},{"value":"top","label":"Riportano in cima"}],"default":"cart"},
 CB("sticky","Barra d'acquisto fissa in basso",True),T("sticky_label","Pulsante barra","Aggiungi al carrello"),T("sticky_note","Testo barra","Garanzia 90 giorni")],
"blocks":[
 {"type":"trust","name":"Striscia fiducia","settings":[T("item_%d"%i,"Voce %d"%i,"") for i in range(1,5)]},
 {"type":"ugc","name":"Video clienti","settings":ug},
 {"type":"lead","name":"Apertura (storia)","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),RT(("text","Testo")),T("kicker","Frase finale evidenziata",""),IMG("image","Immagine"),T("image_url","Immagine (link)",""),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"mechanism","name":"Meccanismo (confronto)","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),TA("sub","Sottotitolo","x"),T("a_label","Sinistra · etichetta",""),T("a_big","Sinistra · numero",""),TA("a_points","Sinistra · punti (uno per riga)","x"),T("b_label","Destra · etichetta",""),T("b_big","Destra · numero",""),TA("b_points","Destra · punti (uno per riga)","x"),TA("note","Nota sotto (seconda chiave)","x")]+PADS()},
 {"type":"benefits","name":"Benefici","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),IMG("image","Immagine"),T("image_url","Immagine (link)","")]+sum([[T("b%d_title"%i,"%d · in grassetto"%i,""),TA("b%d_text"%i,"%d · testo"%i,"x")] for i in range(1,7)],[])+[T("cta_label","Pulsante",""),T("cta_note","Nota sotto il pulsante",""),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"formula","name":"Formula","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),TA("sub","Sottotitolo","x")]+sum([[T("i%d_tag"%i,"%d · livello"%i,""),T("i%d_dose"%i,"%d · dose"%i,""),T("i%d_name"%i,"%d · nome"%i,""),TA("i%d_text"%i,"%d · a cosa serve"%i,"x")] for i in range(1,7)],[])+[TA("footnote","Nota a piè di pagina","x"),CB("tinted","Sfondo tinta",True)]+PADS()},
 {"type":"timeline","name":"Tempi dei risultati","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x")]+sum([[T("s%d_when"%i,"%d · quando"%i,""),T("s%d_title"%i,"%d · titolo"%i,""),TA("s%d_text"%i,"%d · testo"%i,"x")] for i in range(1,4)],[])+[TA("note","Nota finale","x"),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"reviews","name":"Recensioni","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),T("rating","Valutazione (es. 4,8/5 · 1.234 recensioni)",""),T("verified_label","Etichetta verificato","Acquisto verificato")]+sum([[T("stat%d"%i,"Statistica %d · numero"%i,""),T("stat%d_label"%i,"Statistica %d · etichetta"%i,"")] for i in range(1,4)],[])+[TA("stats_note","Nota statistiche","x")]+sum([[T("r%d_title"%i,"%d · titolo"%i,""),TA("r%d_quote"%i,"%d · testo"%i,"x"),T("r%d_name"%i,"%d · nome, età, città"%i,""),IMG("r%d_image"%i,"%d · foto"%i),T("r%d_image_url"%i,"%d · foto (link)"%i,"")] for i in range(1,4)],[])+[CB("tinted","Sfondo tinta",True)]+PADS()},
 {"type":"compare","name":"Confronto","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),T("col_a","Colonna evidenziata","Within"),T("col_b","Colonna 2",""),T("col_c","Colonna 3","")]+sum([[T("r%d_label"%i,"Riga %d · voce"%i,""),T("r%d_a"%i,"Riga %d · evidenziata"%i,""),T("r%d_b"%i,"Riga %d · colonna 2"%i,""),T("r%d_c"%i,"Riga %d · colonna 3"%i,"")] for i in range(1,8)],[])+[T("cta_label","Pulsante",""),T("cta_note","Nota sotto il pulsante",""),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"guarantee","name":"Garanzia","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),RT(("text","Testo")),T("seal_big","Sigillo · numero","90"),T("seal_small","Sigillo · sotto","giorni"),T("seal_text","Sigillo · testo circolare","Soddisfatta o rimborsata · Soddisfatta o rimborsata · "),T("cta_label","Pulsante",""),T("cta_note","Nota sotto il pulsante",""),CB("tinted","Sfondo tinta",False)]+PADS()},
 {"type":"faq","name":"Domande frequenti","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x")]+sum([[T("q%d"%i,"Domanda %d"%i,""),TA("a%d"%i,"Risposta %d"%i,"x")] for i in range(1,9)],[])+[TA("disclaimer","Disclaimer","x"),CB("tinted","Sfondo tinta",True)]+PADS()},
 {"type":"final","name":"Chiusura","settings":[T("eyebrow","Sopra-titolo",""),TA("heading","Titolo","x"),TA("text","Testo","x"),T("cta_label","Pulsante",""),T("cta_note","Nota sotto il pulsante",""),IMG("image","Immagine di sfondo"),T("image_url","Immagine (link)","")]+PADS()},
],
"presets":[{"name":"Within · Pagina prodotto","blocks":[{"type":"lead"}]}]}
for b in schema['blocks']:
    assert len(b['name'])<=25,b['name']
    for s in b['settings']:
        if s.get('default') in ("","x"): s.pop('default',None)

out='''{% comment %}
  Within · Pagina prodotto — struttura CRO a lettera di vendita (sotto l'hero del tema).
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
open(REPO+'/sections/within-pdp.liquid','w').write(out); print('within-pdp',len(out))

import importlib.util
spec=importlib.util.spec_from_file_location('pc',os.path.join(SP,'pdp_content.py'));C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
blocks=C.build(I,V)
defs={b['type']:{s['id']:s['default'] for s in b['settings'] if 'default' in s} for b in schema['blocks']}
bl={};order=[]
for n,(t,st) in enumerate(blocks,1):
    k='%s_%d'%(t,n); s=dict(defs[t]); s.update(st); bl[k]={'type':t,'settings':s}; order.append(k)
p=REPO+'/templates/product.within.json'; raw=open(p).read(); h=raw[:raw.find('{')]; tpl=json.loads(raw[raw.find('{'):])
sec_settings={s['id']:s['default'] for s in schema['settings'] if 'default' in s}
tpl['sections'].pop('within_pp',None)
tpl['sections']['within_pdp']={'type':'within-pdp','blocks':bl,'block_order':order,'settings':sec_settings}
o=[x for x in tpl['order'] if x not in ('within_pp','within_pdp')]
o.insert(o.index('main')+1 if 'main' in o else 0,'within_pdp')
tpl['order']=o
open(p,'w').write(h+json.dumps(tpl,ensure_ascii=False,indent=2)); print('template order',o,len(order))
