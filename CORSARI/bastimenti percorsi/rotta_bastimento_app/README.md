# Rotta del bastimento

App Streamlit che legge un file CSV o XLSX con colonne `nome`, `long`, `lat` e mostra su mappa lo spostamento di un bastimento seguendo l'ordine delle righe.

## Avvio

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Apri l'indirizzo indicato da Streamlit, carica il foglio e usa **Avvia**, **Pausa** o il cursore delle tappe sotto la mappa.

## Formato dati

Sono accettati file `.csv` e `.xlsx`. Le intestazioni non distinguono maiuscole/minuscole e gli spazi esterni vengono rimossi. Le coordinate devono rispettare:

- `long`: da -180 a 180
- `lat`: da -90 a 90

Il percorso collega le località nell'ordine in cui compaiono nel file.
