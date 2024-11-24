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
    sheet = client.open("Prenotazioni_Pullman").worksheet("Foglio1")

    # Stile personalizzato della pagina
    st.markdown(
        """
        <style>
        body {
            background-color: #101820; /* Blu notte moderno */
            color: #F2F2F2; /* Testo chiaro per leggibilità */
        }
        h1 {
            text-align: center;
            color: #0078FF; /* Blu moderno */
            font-size: 3em;
            font-family: 'Arial Black', Gadget, sans-serif;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 10px;
            background-color: #1E1E1E;
            color: #CCCCCC;
            border-radius: 10px;
            font-size: 1.2em;
        }
        .warning {
            color: #FFCC00;
            font-size: 1em;
            font-weight: bold;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titolo dell'app
    st.markdown("<h1>Prenotazione Pullman - Inter Club Forlì</h1>", unsafe_allow_html=True)

    # Input dell'utente
    st.subheader("Compila i campi per prenotare il tuo posto:")
    nome = st.text_input("Nome", placeholder="Inserisci il tuo nome").strip()
    cognome = st.text_input("Cognome", placeholder="Inserisci il tuo cognome").strip()
    telefono = st.text_input("Numero di telefono (obbligatorio)", placeholder="Es. 3331234567").strip()

    # Nuova opzione: Sei socio del club?
    socio_club = st.radio("Sei socio del club?", ["Sì", "No"])

    # Messaggio se non si è soci
    if socio_club == "No":
        st.markdown("<p class='warning'>⚠️ Non essendo socio, si applica una quota aggiuntiva di 20€.</p>", unsafe_allow_html=True)

    # Selezione della città di partenza
    citta_di_partenza = st.selectbox("Città di Partenza", ["Rimini Nord", "Forlì", "Faenza"])
    partita = st.selectbox("Partita", ["Inter Parma", "Inter Lipsia", "Inter Brasov"])
    tipo_di_biglietto = st.selectbox("Tipo di Biglietto", ["Solo viaggio", "Viaggio e biglietto"])

    # Logica per tessera del tifoso
    tdt = "N/D"
    numero_tdt = "007"  # Prefisso fisso "007"
    data_di_nascita = "N/D"
    
    if tipo_di_biglietto == "Viaggio e biglietto":
        tdt_risposta = st.radio("Hai la tessera del tifoso?", ["Sì", "No"])
        if tdt_risposta == "Sì":
            tdt = "Sì"
            # Campo per inserire solo i restanti 9 caratteri (incluso il prefisso fisso "007")
            numero_tdt_inserito = st.text_input("Numero tessera del tifoso (inizia con 007)", value="007", max_chars=12)
            
            # Validazione per assicurarci che l'utente inserisca un totale di 12 caratteri (3 prefisso + 9 alfanumerici)
            if len(numero_tdt_inserito) == 12 and numero_tdt_inserito[:3] == "007" and numero_tdt_inserito[3:].isalnum():
                numero_tdt = numero_tdt_inserito
            else:
                st.warning("⚠️ Il numero della tessera del tifoso deve essere composto da 12 caratteri, di cui i primi 3 devono essere '007' seguiti da 9 caratteri alfanumerici.")
                
            data_di_nascita = st.text_input("Data di nascita (GG/MM/AAAA)", placeholder="Es. 01/01/2000").strip()
        else:
            tdt = "No"
            numero_tdt = "N/D"  # Se non ha la tessera, il numero della tessera deve essere N/D
            data_di_nascita = "N/D"  # Se non ha la tessera, la data di nascita deve essere N/D

    # Convalida campi obbligatori
    errori = []
    if not nome:
        errori.append("⚠️ Il campo Nome è obbligatorio.")
    if not cognome:
        errori.append("⚠️ Il campo Cognome è obbligatorio.")
    if not telefono:
        errori.append("⚠️ Il campo Numero di telefono è obbligatorio.")
    if tdt == "Sì" and (len(numero_tdt) != 12 or not numero_tdt.startswith("007") or not numero_tdt[3:].isalnum()):
        errori.append("⚠️ Il numero della tessera del tifoso deve essere composto da 12 caratteri, di cui i primi 3 devono essere '007' seguiti da 9 caratteri alfanumerici.")
    if tdt == "Sì" and (not data_di_nascita):
        errori.append("⚠️ Data di nascita è obbligatoria se hai la tessera del tifoso.")

    # Mostra errori
    if errori:
        st.markdown("<p class='error'>Correggi i seguenti errori:</p>", unsafe_allow_html=True)
        for errore in errori:
            st.write(errore)
    else:
        # Pulsante di conferma
        if st.button("Conferma Prenotazione"):
            try:
                sheet.append_row([nome, cognome, socio_club, citta_di_partenza, telefono, tipo_di_biglietto, tdt, numero_tdt, data_di_nascita])
                st.success("✅ Prenotazione registrata con successo!")
            except Exception as e:
                st.error(f"❌ Errore durante la registrazione: {e}")

    # Footer con i recapiti
    st.markdown(
        """
        <div class="footer">
            <p>Per ulteriori informazioni, contatta:</p>
            <p>📞 Filippo: <a href="tel:+393801770771" style="color: #0078FF;">380 177 0771</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    main()
