import streamlit as st

# Importiamo le librerie necessarie
import gspread  # Per interagire con Google Sheets
from oauth2client.service_account import ServiceAccountCredentials  # Per autenticare con Google API

# Definiamo l'ambito di accesso (scope) richiesto
# - "https://spreadsheets.google.com/feeds": Permette di leggere/scrivere nei fogli Google
# - "https://www.googleapis.com/auth/drive": Necessario per accedere ai file su Google Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Carichiamo il file JSON delle credenziali (scaricato in precedenza)
# Sostituisci 'path/to/credentials.json' con il percorso reale del file JSON delle chiavi
creds = ServiceAccountCredentials.from_json_keyfile_name('manifest-quasar-442320-s3-6500c00441bc.json', scope)

# Autentichiamo il client con le credenziali
client = gspread.authorize(creds)

# Apriamo il foglio di calcolo utilizzando il suo nome
# Sostituisci "Nome del tuo foglio" con il nome reale del tuo foglio Google
sheet = client.open("Prenotazioni_Pullman").sheet1  # `.sheet1` indica il primo foglio del documento

# Esempio: Aggiungere una nuova riga al foglio
# La funzione append_row() aggiunge una riga alla fine del foglio
# Ogni elemento della lista corrisponde a una cella della riga
sheet.append_row(["Nome", "Tipo Prenotazione", "Numero Posto"])

# Per il tuo caso d'uso, puoi sostituire i valori statici con input dinamici
# Esempio:
nome = "Mario Rossi"
tipo_prenotazione = "VIP"
numero_posto = 12

# Aggiungiamo i valori al foglio
sheet.append_row([nome, tipo_prenotazione, numero_posto])

