# Within — Collagene Marino

Product page long-form (stile Apple) per il prodotto Shopify **Within - Collagene Marino**.

## File
- `sections/within-product-page.liquid` — **sezione Shopify a blocchi**, da mettere sotto l'hero del template prodotto. Ogni modulo è un blocco: riordinabile, attivabile/disattivabile, duplicabile e modificabile dal theme editor (testi, immagini, video, padding, colori).
- `product-page/within-collagene-marino.html` — la stessa pagina come HTML per la descrizione prodotto (versione attualmente caricata sul prodotto).
- `product-page/anteprima.html` — anteprima standalone da aprire nel browser.
- `prompts/prompt-immagini-within.txt` — prompt di tutte le immagini (foto prodotto reale come reference).

## Installare la sezione
1. Admin → Negozio online → Temi → `…` → Modifica codice.
2. `sections/` → Aggiungi nuova sezione → nome `within-product-page` → incolla il contenuto di `sections/within-product-page.liquid` → Salva.
3. Personalizza → template prodotto → Aggiungi sezione → **Within · Product Page** (sotto le informazioni prodotto).
4. Se usi la sezione, svuota la descrizione HTML del prodotto per non avere la pagina due volte.

## Immagini e video
Ogni slot immagine/video ha due campi: **file Shopify** (image/video picker) e **link** precompilato con l'immagine/video attuale (Higgsfield).
Se carichi un file viene usato quello, altrimenti il link. Consigliato: caricare i file in Shopify per non dipendere da link esterni.

Immagini: Higgsfield (gpt_image_2_5). Video UGC degli slider: Seedance 2.5.
