# 🥕🥦 Arkiruokasovellus 🍆🍋
Sovelluksessa näkyy erilaisia ruokakategorioita kuten kasvisruuat, vegaaniset, alle 30min valmistusaika, jne. Kategorioihin voi lisätä omia reseptejä ja lukea muiden kirjoittamia reseptejä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee sovelluksen etusivulla listan kategorioista.
* Käyttäjä voi luoda kategoriaan uuden reseptin antamalla reseptille nimen ja kirjoittamalla ainekset, ohjeen sekä valmistusajan.
* Käyttäjä voi poistaa luomansa reseptin.
* Käyttäjä voi antaa arvion (tähdet ja kommentti) reseptistä ja lukea muiden antamia arvioita.
* Käyttäjä voi lisätä reseptejä omiin suosikkeihin.
* Käyttäjä voi etsiä sivustolta reseptejä, joiden osana on annettu sana, esim. “munakoiso”.
* Ylläpitäjä voi lisätä ja poistaa kategorioita.

# Käynnistysohjeet:
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=postgresql:///käyttäjänimi

SECRET_KEY=salainen-avain

(salaisen avaimen voit luoda Pythonilla esim. alla olevalla tavalla, joka tulostaa 16 merkkisen salaisen avaimen):

import secrets

secrets.token_hex(16)

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt

$ psql < schema.sql

Käynnistä sovellus komennolla 

$ flask run
