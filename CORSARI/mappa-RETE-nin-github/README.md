# Mappa crediti NIN

Mappa Leaflet responsiva che legge in tempo reale le colonne E, F e G del foglio Google pubblicato. I punti con le stesse coordinate vengono aggregati: il cerchio cresce in proporzione al numero di occorrenze.

## Pubblicazione con GitHub Pages

1. Crea un repository GitHub e carica `index.html`.
2. Apri **Settings → Pages**.
3. In **Build and deployment**, scegli **Deploy from a branch**, quindi `main` e `/ (root)`.
4. GitHub mostrerà l'indirizzo pubblico della mappa.

## Incorporamento

```html
<iframe
  src="https://TUO-UTENTE.github.io/TUO-REPOSITORY/"
  title="Mappa crediti NIN"
  loading="lazy"
  style="width:100%;height:clamp(420px,70vh,760px);border:0"
  allowfullscreen>
</iframe>
```

Le colonne E–G devono includere una latitudine e una longitudine numeriche. La terza colonna viene mostrata nel popup. Il foglio deve rimanere pubblicato sul web. La base predefinita usa immagini satellitari e toponimi Esri. Rotella del mouse, doppio clic, trascinamento e pinch-to-zoom sono abilitati.
