# Asentaminen Debian-ympäristöön

Voit asentaa Varasto-ohjelman Debian 12 -ympäristöön tämän ohjeen
avulla.

Kaikki ohjeen komennot ajetan root-käyttäjällä ellei kohdassa ole
eriseen merkitty sudo-komentoa käyttäjän vaihtamiseen.

**HUOM!** Ohjeessa ja esimerkkitiedostoissa on käytetty palvelulle
osoitetta `varasto.example.org`.  Se pitää tietysti vaihtaa palvelun
oikeaan osoitteeseen komennoissa ja tiedostoissa.

## Vaiheet

 1. Asetetaan Suomen aikavyöhyke

        timedatectl set-timezone Europe/Helsinki

 2. Asennetaan lokaalit

    Poistetaan kommentti-merkit lokaaleiden C, en_US, en_GB, en_DK ja
    fi_FI edestä tiedostossa `/etc/locale.gen`.  Tämä voidaan tehdä
    komennolla `nano /etc/locale.gen` tai tällä sed-komennolla:

        sed -i -E 's/# ((C|en_(US|GB|DK)|fi_FI).UTF-8.*)/\1/' /etc/locale.gen

    Tämän jälkeen generoidaan valitut lokaalit:

        locale-gen

 3. Asennetaan päivitykset

        apt update
        apt upgrade

 4. Asennetaan tarvittavat Debian-paketit

        apt install postgresql nginx git etckeeper \
            python3.11-venv python3.11-dev build-essential libpq-dev

 5. Luodaan varasto-käyttäjä

        adduser --system --disabled-login --group varasto
        gpasswd -a varasto www-data
        etckeeper commit "Add varasto user"

 6. Haetaan koodi /var/www/varasto/code -kansioon

        cd /var/www
        mkdir varasto
        cd varasto
        git clone https://github.com/Raision-seudun-koulutuskuntayhtyma/varastohallinta.git code
        chown root:varasto code
        chmod u=rwx,g=rx,o= code

 7. Luodaan ja aktivoidaan virtuaaliympäristö:

        cd /var/www/varasto
        python3.11 -m venv venv
        . venv/bin/activate

 8. Asennetaan requirementit virtuaaliympäristöön

        cd code
        pip install -r requirements.txt

    Jos muisti ei riitä (tulee virhe "Killed"), niin tämä voi auttaa:

        pip install --no-cache-dir -r requirements.txt

 9. Deaktivoidaan virtuaaliympäristö

        deactivate

10. Luodaan .env -tiedosto

        cd /var/www/varasto/code/
        touch .env
        chmod u=rw,g=r,o= .env
        chown root:varasto .env
        nano .env

    Tiedoston sisältö:

        DEBUG=0
        ALLOWED_HOSTS=varasto.example.org
        SECRET_KEY=korvaa-tämä-teksti-satunnaisella-merkkijonolla
        STATIC_ROOT=/var/www/varasto/static
        MEDIA_ROOT=/var/www/varasto/media
        DATABASE_URL=postgres:///varasto
        EMAIL_URL=smtps://tunnus:salasana@postipalvelin.example.com:587
        DEFAULT_FROM_EMAIL=joku@varasto.example.org

    `SECRET_KEY` on Djangon käyttämä salausavain, jonka olisi hyvä olla
    vähintään 30 merkkiä pitkä satunnainen merkkijono sekä sisältää
    pieniä ja isoja kirjaimia sekä numeroita.

    `EMAIL_URL` määrittelee sähköpostin lähetykseen käytettävän palvelimen
    osoitteen ja tunnuksen sinne.

    `DEFAULT_FROM_EMAIL` määrittelee mitä sähköpostiosoitetta käytetään
    viestin From-kentässä, kun järjestelmä lähettää sähköpostia.

11. Luodaan postgresql-käyttäjät ja tietokanta

        sudo -u postgres createuser --superuser root
        createuser varasto
        createdb --owner=varasto varasto

12. Luodaan kansio mediatiedostoille (käyttäjien lataamat tiedostot)

        cd /var/www/varasto
        mkdir media
        chown varasto:www-data media
        chmod u=rwx,g=rxs,o= media

13. Luodaan systemd-käynnistystiedostot gunicornille

        nano /etc/systemd/system/gunicorn@.service
        nano /etc/systemd/system/gunicorn@.socket
        systemctl enable --now gunicorn@varasto.socket

    Tiedostojen sisältö löytyy samasta kansiosta kuin tämä ohje.

14. Luodaan nginx-asetukset

        cd /etc/nginx
        nano sites-available/varasto-site.conf
        ln -sr sites-available/varasto-site.conf sites-enabled/
        rm sites-enabled/default
        systemctl reload nginx

    Tiedoston sisältö löytyy samasta kansiosta kuin tämä ohje.

15. Tallennetaan muutokset etckeeperiin

        etckeeper commit "Varasto-app gunicorn-palvelu ja nginx-asetukset"

16. Ajetaan update-skripti

        cd /var/www/varasto/code
        ./update

    Skripti päivittää koodin Gitistä, asentaa requirementit (jos niihin
    on vaikka tullut muutoksia), esikääntää pyc-tiedostot
    (`compileall`), kerää staattiset tiedostot (`collectstatic`),
    päivittää tietokannan (`migrate`) ja käynnistää gunicorn-palvelun
    uudelleen.


## TLS-sertifikaatin asentaminen

Sovellettu ohjeesta
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-debian-11

    apt install certbot python3-certbot-nginx
    certbot --nginx -d varasto.example.org
    etckeeper commit "Setup Let's Encrypt Certbot"
    systemctl status certbot.timer
    certbot renew --dry-run
