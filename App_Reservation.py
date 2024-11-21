# Importiamo le librerie necessarie
import streamlit as st
import gspread  # Per interagire con Google Sheets
from oauth2client.service_account import ServiceAccountCredentials  # Per autenticare con Google API
from datetime import datetime  # Per validare la data

def main():
    # Configurazione API Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('manifest-quasar-442320-s3-8cb96968a239.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Prenotazioni_Pullman").sheet1

    # Aggiunta di stile personalizzato per la pagina
    st.markdown(
        """
        <style>
        /* Sfondo della pagina */
        body {
            background-color: #000000;
            color: #ffffff;
        }
        /* Barra laterale */
        .css-18e3th9 {
            background-color: #000000 !important;
        }
        /* Titolo principale */
        h1 {
            text-align: center;
            color: #0074D9;
        }
        /* Testo nei campi input */
        input {
            background-color: #111111;
            color: white !important;
        }
        /* Pulsanti */
        .stButton>button {
            background-color: #0074D9;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #005bb5;
            color: white;
        }
        /* Intestazioni */
        .stRadio label, .stSelectbox label {
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titolo dell'app
    st.markdown("<h1>Prenotazione Pullman - Inter Club Forlì</h1>", unsafe_allow_html=True)

    # Input dell'utente
    nome = st.text_input("Nome").strip()
    cognome = st.text_input("Cognome").strip()
    citta_di_partenza = st.selectbox("Città di Partenza", ["Rimini Nord", "Forlì", "Faenza"])
    tipo_di_biglietto = st.selectbox("Tipo di Biglietto", ["Solo viaggio", "Viaggio e biglietto"])

    # Logica per la tessera del tifoso
    tdt = "N/D"
    codice_tdt = "N/D"  # Nuova colonna per il codice TDT
    data_di_nascita = "N/D"
    if tipo_di_biglietto == "Viaggio e biglietto":
        tdt_risposta = st.radio("Hai la tessera del tifoso?", ["Sì", "No"])
        if tdt_risposta == "Sì":
            tdt = "Sì"
            codice_tdt = st.text_input("Inserisci il codice della tua tessera del tifoso").strip()
            data_di_nascita = st.text_input("Inserisci la tua data di nascita (formato: GG/MM/AAAA)").strip()
        else:
            tdt = "No"

    # Messaggio iniziale
    campi_completi = True
    errori = []

    # Convalida dei campi obbligatori
    if not nome:
        campi_completi = False
        errori.append("Il campo Nome è obbligatorio.")
    if not cognome:
        campi_completi = False
        errori.append("Il campo Cognome è obbligatorio.")
    if tdt == "Sì":
        if not codice_tdt:
            campi_completi = False
            errori.append("Inserisci il codice della tessera del tifoso.")
        if not data_di_nascita:
            campi_completi = False
            errori.append("Inserisci la data di nascita.")
        else:
            try:
                datetime.strptime(data_di_nascita, "%d/%m/%Y")
            except ValueError:
                campi_completi = False
                errori.append("La data di nascita non è in un formato valido (GG/MM/AAAA).")

    # Mostra errori se ci sono
    if not campi_completi:
        st.warning("Compilare tutti i campi obbligatori prima di poter confermare la tua prenotazione e controllare che siano corretti.")
        for errore in errori:
            st.error(errore)
    else:
        # Pulsante di conferma disponibile solo se tutti i campi sono completi
        if st.button("Conferma Prenotazione"):
            try:
                # Sostituisci i campi vuoti con "N/D"
                citta_di_partenza = citta_di_partenza if citta_di_partenza.strip() else "N/D"
                tipo_di_biglietto = tipo_di_biglietto if tipo_di_biglietto.strip() else "N/D"
                tdt = tdt if tdt.strip() else "N/D"
                codice_tdt = codice_tdt if codice_tdt.strip() else "N/D"
                data_di_nascita = data_di_nascita if data_di_nascita.strip() else "N/D"

                # Aggiunge una nuova riga al foglio
                sheet.append_row([nome, cognome, citta_di_partenza, tipo_di_biglietto, tdt, codice_tdt, data_di_nascita])
                st.success("Prenotazione registrata con successo!")
            except Exception as e:
                st.error(f"Errore durante la registrazione: {e}")

if __name__ == '__main__':
    main()
