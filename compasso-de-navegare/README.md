# Compasso de Navigare · Atlante interattivo

Applicazione statica italiana in un solo `index.html`: Deck.gl 9.1.14, MapLibre GL JS 4.7.1, Plotly 2.35.2 e Papa Parse 5.4.1, caricati da CDN. Nessun backend, compilazione o token Mapbox. Internet è richiesto per librerie e cartografia; i dati dell’allegato sono già incorporati nell’HTML.

## Avvio

1. Estrarre l’archivio e aprire un terminale nella cartella `compasso`.
2. Eseguire `python -m http.server 8000` (su alcuni sistemi `python3 -m http.server 8000`).
3. Aprire <http://localhost:8000>.
4. Per leggere il rapporto senza dipendenze esterne, aprire `analisi.html`.

Si può tentare anche l’apertura diretta di `index.html`, ma il server locale evita le restrizioni del protocollo `file://` sui caricamenti remoti.

## Dati effettivamente ricevuti

Il file allegato è Excel, non CSV. Sono stati estratti senza correggere nomi, coordinate o collegamenti:

- `PELEGGI LUOGHI`: 67 righe, colonne `ID, LUOGO, LAT, LONG, NOME`.
- `PELEGGI CONNESSIONI`: 53 righe, colonne `source_id, target_id`.
- 52 traversate valide. Riga Excel 54: origine 61, destinazione vuota; esclusa dai calcoli e registrata in `audit.json`.
- LUOGO e NOME coincidono su tutte le righe. Non sono disponibili grafie medievali indipendenti, denominazioni internazionali, distanze storiche o direzioni testuali.

Gli ID numerici interi sono serializzati come stringhe intere durante l’estrazione. Gli originali non sono stati modificati.

## Caricamento automatico da Google

All’avvio l’app visualizza subito l’estrazione incorporata, quindi tenta l’aggiornamento dal link Google fornito. Se la rete, la pubblicazione o CORS impediscono il caricamento, mantiene il dataset incorporato e lo segnala.

Un URL con `output=csv` esporta **un solo foglio**. L’app cerca gli altri `gid` nell’indice `pubhtml` del documento pubblicato e riconosce i ruoli dalle intestazioni. La scoperta è un tentativo: struttura dell’indice, CORS e pubblicazione di singoli fogli possono impedirla.

In tal caso, aprire **Fonti, fogli e corrispondenza delle colonne** e indicare gli URL CSV separati oppure i `gid` reali dei due fogli. Il secondo foglio **non** ha necessariamente `gid=1`. I `gid` si leggono dagli URL dei fogli in Google Sheets; entrambi devono essere pubblicati sul web. Non condividere l’intero documento con permessi di modifica per consentire la sola lettura dei CSV.

Alternativa: selezionare `nodes.csv` ed `edges.csv` nei due controlli di caricamento locale. Il pulsante **Dati del file allegato** ripristina il dataset verificato e le macroaree redazionali.

La scoperta non unisce automaticamente più fogli con lo stesso schema: in presenza di ambiguità richiede URL espliciti. Nessun arco è generato dall’ordine delle righe, dalla vicinanza o dall’uguaglianza dei nomi.

## Controlli

- Mappa regionale 3D: trascinamento per spostare, Maiusc + trascinamento per inclinare/ruotare, rotella per zoom. Il controller Deck.gl gestisce la camera; la base MapLibre viene sincronizzata.
- Hover: evidenziazione colore e dettaglio; clic su arco o pulsante nella tabella per selezione persistente e spessore maggiore. Clic su nodo per filtrare.
- **Entra tra gli archi**: vera `FirstPersonView`, indipendente dal vincolo orbitale della mappa; trascinare per guardare, rotella/frecce per muoversi, +/− per quota.
- **Percorri selezione**: movimento guidato per 18 secondi sul segmento tra gli estremi, a quota grafica costante di 12 km. Non segue una traiettoria storica né la sommità dell’arco. Movimento manuale, **Ferma** o Esc interrompono l’animazione. **Vista regionale** ritorna alla mappa.
- Altezza degli archi: artificio visivo regolabile, senza significato storico o altimetrico. Proiezione regionale Mercatore; l’app non offre un globo terrestre.
- Filtri: ID di luogo, da/per, macroarea di almeno un estremo, distanza geodetica minima/massima e quadrante di azimut. Il quadrante descrive la direzione iniziale, non una suddivisione in quattro aree del Mediterraneo.
- I nodi isolati nel corpus possono essere mostrati con l’apposita casella. Non sono collegati artificialmente. Tutti i grafici seguono i filtri.
- Tabella rotte e dettaglio persistente disponibili da tastiera; tabella nomi ricercabile. I grafici WebGL non costituiscono l’unico accesso ai dati.
- Esportazione rotte CSV, audit JSON e configurazione. Le tabelle visibili sono limitate a 300 rotte e 500 nomi; l’export rotte include tutta la selezione.

## Distanze e confronto storico

Inversa di Vincenty su WGS84: distanza geodetica minima, in km, e azimut iniziale da Nord in senso orario. Coincidenze coordinate danno distanza zero e azimut indeterminato. Coppie non convergenti sono segnalate ed escluse; non viene usato un ripiego sferico silenzioso.

I valori dipendono dalle identificazioni e dalle coordinate fornite. La base è contemporanea. La geodetica può attraversare la terraferma e non misura una rotta nautica effettivamente percorribile.

Quando si aggiungono distanze storiche numeriche, l’app riconosce colonne come `miglia`, `miglia_medievali`, `distanza_storica`, `distanza`, `pari`, oppure quella indicata nel campo di configurazione. Si raccomanda di usare un campo separato `unita`. Il fattore **km per miglio medievale** è inizialmente vuoto: una conversione è applicata solo a righe esplicitamente in miglia o con unità assegnata dall’utente. `pari` non è convertito. La semplice parola `distanza` non implica miglia.

Valori testuali come `cento`, `12 miglia` o frazioni non decimali sono conservati ma non interpretati automaticamente. Per le miglia convertibili il tooltip mostra km ipotetici e scarto rispetto alla geodetica; lo scarto non è presentato come errore storico dimostrato.

## Toponimi e macroaree

Per l’allegato, `LUOGO` è mostrato come forma del dataset: non viene attestato come grafia medievale. La classificazione automatica individua solo indizi lessicali (capo, isola, porto, golfo); lascia indeterminati i casi non riconoscibili. Non inventa etimologie o nomi internazionali. Il CSV può essere arricchito con `internazionale`, `tipo`, `macroarea`, `note`, `fonte`.

Le macroaree del dataset incorporato sono proposte redazionali moderne per ID, definite nell’oggetto `EDITORIAL_AREAS` e riportate negli export; i dati originali restano invariati. Sardegna, Corsica, Baleari e Sicilia sono distinte. Per nuovi CSV, si usa `macroarea` quando disponibile; altrimenti i rettangoli geografici forniscono solo una proposta grezza, segnalata come da verificare. Per una pubblicazione scientifica compilare macroarea e tipo in modo controllato.

Gli ID distinti sono mantenuti, anche per coordinate uguali. Il rapporto quantifica la sensibilità del grafo alla fusione dei soli punti esattamente coincidenti. Non è una riconciliazione automatica delle attestazioni.

## Pubblicazione su GitHub Pages

Caricare i file nella cartella pubblicata del repository; l’app richiede soltanto `index.html`. Conservare anche i CSV e il rapporto per la riproducibilità. Abilitare GitHub Pages per la cartella scelta, secondo la configurazione del repository. Non richiede build Node né Streamlit.

Per configurare una fonte permanente, modificare `DEFAULT_URL` e i valori HTML di URL/gid. Oppure usare il collegamento con parametri generato da **Esporta configurazione**: il JSON contiene l’URL configurato, non è importato automaticamente nell’app. I file locali selezionati non vengono memorizzati nella configurazione. Non inserire segreti negli URL.

Per incorporare l’app su Drupal, dopo averla pubblicata, usare un iframe con l’URL effettivo di Pages, per esempio:

```html
<iframe src="https://TUO-ACCOUNT.github.io/TUO-REPOSITORY/"
        title="Compasso de Navigare: atlante delle traversate"
        style="width:100%;height:1100px;border:0"
        loading="lazy" allowfullscreen></iframe>
```

Il formato di testo Drupal deve consentire iframe; le policy del sito ospitante devono consentire il dominio pubblicato. L’iframe isola gli stili dell’app. Per personalizzare il tema usare le variabili CSS all’inizio di `index.html`; l’app ha sfondo chiaro per mantenere leggibili mappa e grafici.

## Contenuti e verifiche

- `index.html`: SPA completa con sorgente incorporata e caricamento remoto.
- `analisi.html`: analisi del corpus, limiti, grafi, macroaree e tutte le traversate.
- `nodes.csv`, `edges.csv`: estrazione originale dei due fogli.
- `traversate_calcolate.csv`: distanze WGS84, azimut, venti convenzionali e macroaree.
- `confronto_toponimi.csv`: forme della fonte e campi mancanti espliciti.
- `source_snapshot.json`: estrazione e impronta SHA-256 dell’Excel.
- `audit.json`, `analysis.json`: controlli e risultati riproducibili.
- `build_analysis.cjs`, `tests/`: ricalcolo e controlli, eseguibili con Node senza pacchetti.

```bash
node tests/core.test.cjs
node tests/ui.test.cjs
node build_analysis.cjs
```

I test numerici includono segmenti WGS84 di riferimento, casi degeneri, validazione, filtri e grafo reale. Il test UI usa un DOM simulato e non verifica WebGL, camera, cartografia o disponibilità dei CDN. Il browser Chromium non è disponibile nell’ambiente di produzione del file: resta da verificare la resa 3D su un browser moderno con WebGL2 e accesso alle risorse esterne.

Documentazione tecnica: [Deck.gl ArcLayer](https://deck.gl/docs/api-reference/layers/arc-layer), [FirstPersonView](https://deck.gl/docs/api-reference/core/first-person-view), [FirstPersonController](https://deck.gl/docs/api-reference/core/first-person-controller). I nomi dei venti nell’app sono etichette orientative moderne, non trascrizioni del Compasso.
