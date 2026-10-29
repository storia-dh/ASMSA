# Formule Google Sheets — Versione 2
# Mapping completo per tutte le schede del progetto

## Struttura colonne — Gruppo A (Dublin Core uniforme)
# Colonna:  A                  B              C                    D            E       F         G                                    H                           I                   J               K                    L
# Campo:    dcterms:title      dcterms:date   dcterms:description  oc:location  geo:lat geo:long  Arco Network:archivalRecordIdentifier dcterms:bibliographicCitation dcterms:publisher  dcterms:created dcterms:references   schema.org:contentUrl

## ════════════════════════════════════════════════════════════════
## SCHEDA: export_torri
## Unisce torri_srd + torri_cat + torri_crs in un unico output
## ════════════════════════════════════════════════════════════════
## Incolla questa formula in A1 della scheda export_torri:

={
  {"id","nome","localita","comune","lat","lon","stato_conservazione","periodo","note_ricerca","fonti","arco_id","url"};
  ARRAYFORMULA(IF(torri_srd!A2:A="","",{
    "TS"&TEXT(ROW(torri_srd!A2:A)-1,"000"),
    torri_srd!A2:A,
    torri_srd!D2:D,
    torri_srd!D2:D,
    torri_srd!E2:E,
    torri_srd!F2:F,
    "nd",
    IF(torri_srd!B2:B="","nd",torri_srd!B2:B),
    torri_srd!C2:C,
    torri_srd!H2:H,
    torri_srd!G2:G,
    torri_srd!L2:L
  }));
  ARRAYFORMULA(IF(torri_cat!A2:A="","",{
    "TC"&TEXT(ROW(torri_cat!A2:A)-1,"000"),
    torri_cat!A2:A,
    torri_cat!D2:D,
    torri_cat!D2:D,
    torri_cat!E2:E,
    torri_cat!F2:F,
    "nd",
    IF(torri_cat!B2:B="","nd",torri_cat!B2:B),
    torri_cat!C2:C,
    torri_cat!H2:H,
    torri_cat!G2:G,
    torri_cat!L2:L
  }));
  ARRAYFORMULA(IF(torri_crs!A2:A="","",{
    "TCR"&TEXT(ROW(torri_crs!A2:A)-1,"000"),
    torri_crs!A2:A,
    torri_crs!D2:D,
    torri_crs!D2:D,
    torri_crs!E2:E,
    torri_crs!F2:F,
    "nd",
    IF(torri_crs!B2:B="","nd",torri_crs!B2:B),
    torri_crs!C2:C,
    torri_crs!H2:H,
    torri_crs!G2:G,
    torri_crs!L2:L
  }))
}

## Prefissi ID generati automaticamente:
##   TS001, TS002… = torri Sardegna
##   TC001, TC002… = torri Corona d'Aragona/Catalogna
##   TCR001…       = torri Corsica


## ════════════════════════════════════════════════════════════════
## SCHEDA: export_infrastrutture
## Unisce porti_scale + peschiere + saline + tonnare
## ════════════════════════════════════════════════════════════════
## Incolla questa formula in A1 della scheda export_infrastrutture:

={
  {"id","tipo","nome","localita","comune","lat","lon","periodo","note","fonti","arco_id","url"};
  ARRAYFORMULA(IF(porti_scale!A2:A="","",{
    "P"&TEXT(ROW(porti_scale!A2:A)-1,"000"),
    "porto",
    porti_scale!A2:A,
    porti_scale!D2:D,
    porti_scale!D2:D,
    porti_scale!E2:E,
    porti_scale!F2:F,
    IF(porti_scale!B2:B="","nd",porti_scale!B2:B),
    porti_scale!C2:C,
    porti_scale!H2:H,
    porti_scale!G2:G,
    porti_scale!L2:L
  }));
  ARRAYFORMULA(IF(peschiere!A2:A="","",{
    "F"&TEXT(ROW(peschiere!A2:A)-1,"000"),
    "peschera",
    peschiere!A2:A,
    peschiere!D2:D,
    peschiere!D2:D,
    peschiere!E2:E,
    peschiere!F2:F,
    IF(peschiere!B2:B="","nd",peschiere!B2:B),
    peschiere!C2:C,
    peschiere!H2:H,
    peschiere!G2:G,
    peschiere!L2:L
  }));
  ARRAYFORMULA(IF(saline!A2:A="","",{
    "S"&TEXT(ROW(saline!A2:A)-1,"000"),
    "salina",
    saline!A2:A,
    saline!D2:D,
    saline!D2:D,
    saline!E2:E,
    saline!F2:F,
    IF(saline!B2:B="","nd",saline!B2:B),
    saline!C2:C,
    saline!H2:H,
    saline!G2:G,
    saline!L2:L
  }));
  ARRAYFORMULA(IF(tonnare!A2:A="","",{
    "TN"&TEXT(ROW(tonnare!A2:A)-1,"000"),
    "tonnara",
    tonnare!A2:A,
    tonnare!D2:D,
    tonnare!D2:D,
    tonnare!E2:E,
    tonnare!F2:F,
    IF(tonnare!B2:B="","nd",tonnare!B2:B),
    tonnare!C2:C,
    tonnare!H2:H,
    tonnare!G2:G,
    tonnare!L2:L
  }))
}

## Prefissi ID generati automaticamente:
##   P001…  = porti e scale
##   F001…  = peschiere
##   S001…  = saline
##   TN001… = tonnare


## ════════════════════════════════════════════════════════════════
## SCHEDA: export_connessioni
## Compilata manualmente o da una scheda master "connessioni"
## ════════════════════════════════════════════════════════════════
## Se crei una scheda "connessioni" con questi campi, usa:
##   =connessioni!A:H
##
## Campi richiesti (riga 1 intestazione):
## id_torre | id_infrastruttura | tipo_relazione | distanza_km | visibilita | certezza | fonti | note
##
## Valori validi:
##   tipo_relazione : visiva  /  funzionale  /  visiva+funzionale
##   visibilita     : diretta  /  probabile  /  ricostruita
##   certezza       : alta  /  media  /  bassa
##
## Per il campo fonti puoi richiamare i portolani con:
##   =IFERROR(VLOOKUP(A2, portolani!A:T, 20, 0), "")
##   (colonna 20 = dcterms:bibliographicCitation in portolani)


## ════════════════════════════════════════════════════════════════
## SCHEDA: export_fonti  (opzionale — per portolani e corsari)
## Alimenta il pannello "fonti" nell'app quando si seleziona una torre
## ════════════════════════════════════════════════════════════════

={
  {"id","tipo","titolo","data","autore","localita","descrizione","citazione","url"};
  ARRAYFORMULA(IF(portolani!A2:A="","",{
    "PORT"&TEXT(ROW(portolani!A2:A)-1,"000"),
    "portolano",
    portolani!A2:A,
    IF(portolani!E2:E="","nd",portolani!E2:E),
    IF(portolani!I2:I="","nd",portolani!I2:I),
    IF(portolani!G2:G="","nd",portolani!G2:G),
    portolani!H2:H,
    portolani!T2:T,
    portolani!AC2:AC
  }));
  ARRAYFORMULA(IF(corsari_attacchi!A2:A="","",{
    "CORS"&TEXT(ROW(corsari_attacchi!A2:A)-1,"000"),
    "attacco_corsaro",
    corsari_attacchi!A2:A,
    IF(corsari_attacchi!B2:B="","nd",corsari_attacchi!B2:B),
    "nd",
    corsari_attacchi!A2:A,
    corsari_attacchi!D2:D,
    corsari_attacchi!C2:C,
    "nd"
  }))
}

## Mapping portolani (29 colonne):
## A=dcterms:title  B=schema.org:description  C=san-lod:has_livelloSuperiore
## D=dcterms:alternative  E=dcterms:date  F=arco:endTime  G=oc:location
## H=dcterms:description  I=san-lod:autore  J=Arco Network:archivalRecordIdentifier
## K=san-lod:consistenza  L=dcterms:medium  M=dcterms:language
## N=oad:conditionsGoverningAccess  O=oad:conditionsGoverningReproduction
## P=san-lod:has_conservatore  Q=schema.org:producer  R=scripto:transcription
## S=schema.org:author  T=dcterms:bibliographicCitation  U=dcterms:contributor
## V=arco:startTime  W=dcterms:format  X=dcterms:extent  Y=dcterms:creator
## Z=dcterms:pubblisher  AA=dcterms:created  AB=dcterms:references  AC=schema.org:contentUrl

## Mapping corsari_attacchi (4 colonne):
## A=Località  B=Anno  C=Fonte  D=Descrizione


## ════════════════════════════════════════════════════════════════
## COME PUBBLICARE LE SCHEDE EXPORT
## ════════════════════════════════════════════════════════════════
##
## Per ciascuna scheda export_*:
## 1. File → Condividi → Pubblica sul web
## 2. Seleziona la scheda (es. "export_torri")
## 3. Formato: CSV
## 4. Clicca Pubblica — copia l'URL
##
## Formato URL generato da Google:
## https://docs.google.com/spreadsheets/d/ID/gviz/tq?tqx=out:csv&sheet=export_torri
##
## L'app costruisce questi URL automaticamente dal solo ID foglio.
## Aggiornamento: Google Sheets propaga le modifiche entro ~5 minuti.
