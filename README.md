# 🥕🥦 Arkiruokasovellus 🍆🍋
Sovelluksessa näkyy erilaisia ruokakategorioita kuten kasvisruuat, vegaaniset, alle 30min valmistusaika, jne. Kategorioihin voi lisätä omia reseptejä ja lukea muiden kirjoittamia reseptejä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee sovelluksen etusivulla listan kategorioista, sekä top 3 reseptit arvostelujen mukaan.
* Käyttäjä voi luoda kategoriaan uuden reseptin antamalla reseptille nimen ja kirjoittamalla ainekset, ohjeen sekä valmistusajan.
* Käyttäjä voi poistaa luomansa reseptin.
* Käyttäjä voi antaa arvion (tähdet ja kommentti) reseptistä ja lukea muiden antamia arvioita.
* Käyttäjä voi lisätä reseptejä omiin suosikkeihin.
* Käyttäjä voi etsiä sivustolta reseptejä, joiden osana on annettu sana, esim. “munakoiso”.
* Ylläpitäjä voi lisätä ja poistaa kategorioita.

# Käynnistysohjeet:
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Jos haluat luoda uuden tietokannan tätä sovellusta varten, tee seuraavat komennot:
```
$ psql
user=# CREATE DATABASE uusidb;
```
Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
```
DATABASE_URL=postgresql:///uusidb
SECRET_KEY=salainen-avain
```
(salaisen avaimen voit luoda Pythonilla esim. alla olevalla tavalla, joka tulostaa 16 merkkisen salaisen avaimen):
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r ./requirements.txt
(venv) $ psql < schema.sql
```
TAI jos loit uuden tietokannan niin
```
(venv) $ psql -d uusinimi < schema.sql
```
Käynnistä sovellus komennolla 
```
(venv) $ flask run
```
