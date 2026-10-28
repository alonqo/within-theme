# Content for Within site templates (home, chi siamo, contattaci, eventi)
def build(S):
    I,V,PROD=S['I'],S['V'],S['PROD']
    HOME_HERO=I('230608_aa23f9fd-8d25-4d7d-a202-f82454fd4b23')
    SEA=I('230608_220c2f4-16b4-4261-9660-c335d8933e60'.replace('220c2f4','220ca2f4'))
    EVENT=I('230609_1b82611d-26fb-4e17-89f1-95917f2c286e')
    vids1=['133042_88724a13-f607-470d-938c-d2e4fc6d8632','133042_aeef790c-4bbb-4f66-b426-cbc80055018c','133042_e533b3b9-6806-45a1-909c-64872cb3c19b','133043_c34741eb-2c7a-4a59-8935-147c26753a3e','133042_235fea3a-e893-4439-b1dc-ed5c36f99c4a','133043_01c6664e-e9ba-4131-a9b9-960ddda09368']
    caps1=['Marta, 57','Paola, 62','Silvia, 59','Elena, 56','Cristina, 64','Valentina, 61']
    ugc=dict({"eyebrow":"Ogni mattina, 25 secondi","heading":"Il gesto che si vede allo specchio."},**{"video_url_%d"%(i+1):V(v) for i,v in enumerate(vids1)},**{"caption_%d"%(i+1):c for i,c in enumerate(caps1)})
    home=[
      ("hero",{"eyebrow":"Within · Collagene marino","heading":"Torna a piacerti allo specchio.","sub":"Il collagene tripeptide che arriva davvero alla pelle. Un sachet al giorno, 25 secondi, 90 giorni per vedere la differenza.","cta_label":"Scopri Within","cta_url":PROD,"link_label":"La nostra storia →","link_url":"/pages/chi-siamo","image_url":HOME_HERO}),
      ("ugc_slider",ugc),
      ("feature_row",{}),
      ("benefits",{"link_label":"Scopri la formula →","link_url":PROD}),
      ("cinematic",{"eyebrow":"Il momento più bello","heading":"Quando ti chiedono: “Ma cosa ti sei fatta?”","image_url":I("145713_343258af-6373-4637-81d8-046328460d88"),"parallax":0.2}),
      ("how_it_works",{}),
      ("product_spot",{"product":"within-collagene-marino","eyebrow":"Il tuo percorso di 12 settimane","heading":"Within Collagene Marino","text":"Dieci sachet da 25 ml per box. Gusto mango e passion fruit, zero retrogusto di pesce. Si beve in 25 secondi, ovunque tu sia.","points":"5.000 mg di collagene marino tripeptide\n6 attivi per una pelle compatta e luminosa\nGià liquido, niente polveri da sciogliere\nGaranzia soddisfatta o rimborsata 90 giorni","cta_label":"Inizia oggi","cta_url":PROD,"image_url":I("133253_a095fd80-1e6b-4c1d-a9a9-8cc6d2128b44"),"tinted":True}),
      ("social_proof",{"cta_url":PROD,"tinted":False}),
      ("guarantee",{"cta_url":PROD}),
      ("faq",{}),
    ]
    about=[
      ("hero",{"eyebrow":"Chi siamo","heading":"La bellezza viene da dentro. Noi l'abbiamo presa sul serio.","sub":"Within nasce da una domanda semplice: perché così tanti collageni promettono tutto e non cambiano niente?","image_url":SEA}),
      ("statement",{"eyebrow":"Perché esistiamo","statement":"Il mercato è pieno di promesse. Noi volevamo un collagene che le mantenesse.","text":"<p>Dopo i 25 anni il corpo perde ogni anno l'1-1,5% del suo collagene. Le creme lavorano in superficie, e la maggior parte degli integratori usa molecole troppo grandi per arrivare dove servono.</p><p>Così siamo partiti da zero. Abbiamo scelto un collagene marino tripeptide sotto i 3.000 Dalton, aggiunto 1 miliardo di fermenti lattici per l'equilibrio dell'intestino e dosato ogni attivo al milligrammo.</p><p>Il risultato si chiama Within. Perché la bellezza che dura comincia da dentro.</p>"}),
      ("feature_row",{"heading":"Quello in cui crediamo.",
        "f1_image_url":I("133253_113ae570-8806-4947-b614-a6b1a28d0c82"),"f1_title":"Trasparenza","f1_text":"Peso molecolare, dosaggi e certificati: tutto dichiarato.",
        "f2_image_url":I("133239_3c10111a-879c-49fe-8e0c-b7b2fa3ad58f"),"f2_title":"Formula seria","f2_text":"Sei attivi scelti per lavorare insieme. Zero riempitivi.",
        "f3_image_url":I("133241_26746d27-a7ec-45d7-a193-1513087a5388"),"f3_title":"Semplicità","f3_text":"Un sachet, 25 secondi. Il gesto più facile della giornata.",
        "f4_image_url":I("145714_237bd89a-de61-49a4-8191-f497a547415b"),"f4_title":"Bellezza a ogni età","f4_text":"Non per sembrare un'altra. Per piacerti di nuovo."}),
      ("cinematic",{"eyebrow":"La nostra promessa","heading":"Niente miracoli. Solo una pelle che si vede.","image_url":I("133240_6e62d467-ccec-48a2-8db0-5be293d52d9e"),"parallax":0.2}),
      ("authority",{}),
      ("statement",{"eyebrow":"Il nostro impegno","statement":"Se in 90 giorni la tua pelle non cambia, ti restituiamo i soldi.","text":"<p>Perché crediamo in quello che facciamo. E perché tu non debba crederci sulla parola.</p>","tinted":True}),
      ("product_spot",{"product":"within-collagene-marino","eyebrow":"Pronta a iniziare?","heading":"Within Collagene Marino","text":"Il tuo percorso comincia con un sachet. Il resto lo vedrai allo specchio.","points":"Collagene tripeptide sotto i 3.000 Dalton\n1 miliardo di fermenti lattici\nGaranzia 90 giorni","cta_label":"Scopri Within","cta_url":PROD,"image_url":I("133239_332fc57d-882d-47db-8c71-ef9c0c432cf4")}),
    ]
    contact=[
      ("hero",{"eyebrow":"Contattaci","heading":"Siamo qui per te.","sub":"Domande sul prodotto, sul tuo ordine o sugli eventi? Scrivici: ti risponde una persona, non un bot.","padding_bottom":24}),
      ("contact",{"eyebrow":"Assistenza clienti","heading":"Parliamone.","text":"Compila il modulo o usa i nostri contatti diretti. Rispondiamo a tutte le richieste.","email":"[EMAIL DA COMPILARE]","phone":"[TELEFONO DA COMPILARE]","address":"[RAGIONE SOCIALE]\n[INDIRIZZO SEDE]\n[CAP CITTÀ (PROVINCIA)]","hours":"Lunedì-venerdì, 9:00-18:00","note":"Entro 24 ore lavorative","padding_top":40}),
      ("faq",{"tinted":True}),
    ]
    events=[
      ("hero",{"eyebrow":"Eventi Within","heading":"Vieni a provarlo dal vivo.","sub":"Degustazioni e consulenze nelle farmacie e nei negozi partner. Assaggi Within, fai le tue domande e scopri il percorso giusto per te.","image_url":EVENT}),
      ("events",{"heading":"Prossimi eventi","sub":"Scegli la data più vicina a te e salvala nel tuo calendario con un clic."}),
      ("event",{"title":"[ESEMPIO] Degustazione Within","date":"2026-11-21","start":"16:00","end":"19:00","place":"Farmacia [Nome]","address":"Via [Indirizzo], 1","city":"Milano","desc":"Evento di esempio: sostituiscilo con le date vere dal theme editor."}),
      ("event",{"title":"[ESEMPIO] Consulenza pelle e collagene","date":"2026-12-05","start":"10:00","end":"13:00","place":"Profumeria [Nome]","address":"Corso [Indirizzo], 10","city":"Roma","desc":"Evento di esempio: sostituiscilo con le date vere dal theme editor."}),
      ("hero",{"eyebrow":"Per farmacie e negozi","heading":"Vuoi un evento Within nella tua città?","sub":"Organizziamo degustazioni e giornate di consulenza nei punti vendita partner. Scrivici e troviamo una data insieme.","cta_label":"Contattaci","cta_url":"/pages/contact","dark":True,"padding_top":96,"padding_bottom":96}),
    ]
    return {'index.json':home,'page.chi-siamo.json':about,'page.contact.json':contact,'page.eventi.json':events}
