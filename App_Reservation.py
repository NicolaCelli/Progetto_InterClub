
# Importiamo le librerie necessarie
import streamlit as st
import gspread  # Per interagire con Google Sheets
from oauth2client.service_account import ServiceAccountCredentials  # Per autenticare con Google API

def main():
    # Definiamo l'ambito di accesso (scope) richiesto
    # - "https://spreadsheets.google.com/feeds": Permette di leggere/scrivere nei fogli Google
    # - "https://www.googleapis.com/auth/drive": Necessario per accedere ai file su Google Drive
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Carichiamo il file JSON delle credenziali (scaricato in precedenza)
    # Sostituisci 'path/to/credentials.json' con il percorso reale del file JSON delle chiavi
    creds = ServiceAccountCredentials.from_json_keyfile_name('manifest-quasar-442320-s3-8cb96968a239.json', scope)

    # Autentichiamo il client con le credenziali
    client = gspread.authorize(creds)

    # Apriamo il foglio di calcolo utilizzando il suo nome
    # Sostituisci "Nome del tuo foglio" con il nome reale del tuo foglio Google
    sheet = client.open("Prenotazioni_Pullman").sheet1  # `.sheet1` indica il primo foglio del documento

    # Interfaccia utente con Streamlit
    st.title("Prenotazione Pullman - Inter Club Forlì")

    # Input dell'utente
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    citta_di_partenza = st.selectbox("Città di Partenza", ["Rimini Nord", "Forlì", "Faenza"])
    tipo_di_biglietto = st.selectbox("Tipo di Biglietto", ["Solo viaggio", "Viaggio e biglietto"])

    # Logica condizionale per "Viaggio e biglietto"
    tdt = "N/D"  # Default per Tessera del Tifoso
    data_di_nascita = "N/D"  # Default per Data di Nascita
    if tipo_di_biglietto == "Viaggio e biglietto":
        tdt_risposta = st.radio("Hai la tessera del tifoso?", ["Sì", "No"])
        if tdt_risposta == "Sì":
            tdt = "Sì"
            data_di_nascita = st.text_input("Inserisci la tua data di nascita (formato: GG/MM/AAAA)")
        else:
            tdt = "No"

    # Pulsante per confermare la prenotazione
    if st.button("Conferma Prenotazione"):
        # Sostituisci i campi vuoti con "N/D"
        nome = nome if nome.strip() else "N/D"
        cognome = cognome if cognome.strip() else "N/D"
        citta_di_partenza = citta_di_partenza if citta_di_partenza.strip() else "N/D"
        tipo_di_biglietto = tipo_di_biglietto if tipo_di_biglietto.strip() else "N/D"
        tdt = tdt if tdt.strip() else "N/D"
        data_di_nascita = data_di_nascita if data_di_nascita.strip() else "N/D"

        # Verifica che tutti i campi obbligatori siano compilati correttamente
        if nome == "N/D" or cognome == "N/D":
            st.error("Nome e Cognome sono obbligatori.")
        elif tdt == "Sì" and data_di_nascita == "N/D":
            st.error("Se hai la tessera del tifoso, devi inserire la data di nascita.")
        else:
            # Aggiunge una nuova riga al foglio
            sheet.append_row([nome, cognome, citta_di_partenza, tipo_di_biglietto, tdt, data_di_nascita])
            st.success("Prenotazione registrata con successo!")

if __name__ == '__main__':
    main()
