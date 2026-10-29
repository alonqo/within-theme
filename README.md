# Within — Collagene Marino

Product page long-form (stile Apple) per il prodotto Shopify **Within - Collagene Marino**.

## File
- `sections/within-product-page.liquid` — **sezione Shopify a blocchi**, da mettere sotto l'hero del template prodotto. Ogni modulo è un blocco: riordinabile, attivabile/disattivabile, duplicabile e modificabile dal theme editor (testi, immagini, video, padding, colori).
- `product-page/within-collagene-marino.html` — la stessa pagina come HTML per la descrizione prodotto (versione attualmente caricata sul prodotto).
- `product-page/anteprima.html` — anteprima standalone da aprire nel browser.
- `prompts/prompt-immagini-within.txt` — prompt di tutte le immagini (foto prodotto reale come reference).

- `sections/within-cart.liquid` + `templates/cart.json` — **pagina carrello** CRO: rassicurazione in testa, barra spedizione gratuita (soglia dal theme editor, 0 = nascosta), prezzo al giorno, box "Il tuo percorso" (giorni coperti su 90 con pulsante per arrivare al traguardo successivo: 3 / 6 / 9 box), riepilogo con CTA unica e pagamento rapido, Garanzia Specchio 90 giorni, "Cosa succede dopo il pagamento", FAQ delle obiezioni da carrello, barra di pagamento fissa su mobile e stato carrello vuoto. Quantità aggiornate via Ajax.

## Installare la sezione
1. Admin → Negozio online → Temi → `…` → Modifica codice.
2. `sections/` → Aggiungi nuova sezione → nome `within-product-page` → incolla il contenuto di `sections/within-product-page.liquid` → Salva.
3. Personalizza → template prodotto → Aggiungi sezione → **Within · Product Page** (sotto le informazioni prodotto).
4. Se usi la sezione, svuota la descrizione HTML del prodotto per non avere la pagina due volte.

## Immagini e video
Ogni slot immagine/video ha due campi: **file Shopify** (image/video picker) e **link** precompilato con l'immagine/video attuale (Higgsfield).
Se carichi un file viene usato quello, altrimenti il link. Consigliato: caricare i file in Shopify per non dipendere da link esterni.

Immagini: Higgsfield (gpt_image_2_5). Video UGC degli slider: Seedance 2.5.

## Carrello
1. Carica `sections/within-cart.liquid` in `sections/` e `templates/cart.json` in `templates/` (o sincronizza il tema da GitHub).
2. Impostazioni del tema → Carrello → tipo **Pagina** (non drawer), così dopo "Aggiungi al carrello" si arriva qui.
3. Nel theme editor apri il template Carrello e imposta la soglia di spedizione gratuita (quando decisa).
