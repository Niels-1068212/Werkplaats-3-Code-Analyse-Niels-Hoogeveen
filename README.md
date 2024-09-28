# wp3-2024-starter
Applicatie geproduceerd door Rachaan de Graaff, Anas Amhaou & Niels Hoogeveen. Deze 
applicatie is ontworpen voor Stichting Accessibility (zie ook de [opdracht](CASUS.md)) 




## Installatie
Voer al deze stappen uit in de opdrachtprompt (cmd)

1. **Maak een virtuele omgeving aan:**
    ```
    python3 -m venv myenv
    ```

2. **Activeer de virtuele omgeving:**
    ```
    myvenv\Scripts\activate
    ```

3. **Installeer de requirements:**
    ```
    pip install -r requirements.txt
    ```

4. **Start het met het draaien van de applicatie:**
    ```
    python root\manage.py runserver
    ```

5. **Openen van de applicatie:**
    Run de applicatie op [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

    Gebruik de volgende inloggegevens:
    - Beheerder:
        - Gebruikersnaam: test_rachaan
        - Wachtwoord: Test123N

    - Ervaringsdeskundige:
        - Gebruikersnaam: test_niels
        - Wachtwoord: Test123N



## Bronnen
De bronnen zijn te vinden in een apart bestand: [Bronnen bestand](docs/bronnen.md)


## ERD
De erd is te vinden in een apart GIF bestand: [ERD bestand](docs/Webmasters_erd.gif)


## Backlogs
Hier zijn de backlogs te vinden van de afgelopen 4 sprints:
1. [Backlog sprint 1](docs/Backlogs/1E5-Webmasters%20-%20Sprint%201%20-%20Backlog.csv)
2. [Backlog sprint 2](docs/Backlogs/1E5-Webmasters%20-%20Sprint2%20-%20Backlog.csv)
3. [Backlog sprint 3](docs/Backlogs/1E5-Webmasters%20-%20Sprint3%20-%20Backlog.csv)
4. [Backlog sprint 4](docs/Backlogs/1E5-Webmasters%20-%20Sprint%204%20-%20Backlog.csv)




## API documentatie
Voor de opzet om een onderzoek te posten of te updaten kijk dan naar: [test_data](docs/test_data.json)

API/organisatie/onderzoeken/<int:onderzoeks_id>?api={api_key}:

- **GET (1 specifiek onderzoek)**
    - Retourneert:
        - onderzoeks_id (integer)
        - organisatie (integer)
        - status (string)
        - titel (string)
        - omschrijving (string)
        - datum_vanaf (date)
        - datum_tot (date)
        - soort_onderzoek (string)
        - locatie (string)
        - met_beloning (boolean)
        - beloning (string)
        - doelgroep_leeftijd_van (integer)
        - doelgroep_leeftijd_tot (integer)
        - type_onderzoek (integer)
        - contact_opgenomen (boolean)
        - opmerkingen_beheerder (string)


- **PUT (1 specifiek onderzoek)**
    - Een JSON-object met de velden die bijgewerkt moeten worden:
        - titel (string): Titel van het onderzoek
        - omschrijving (string): Omschrijving van het onderzoek
        - datum_vanaf (date): Begindatum van het onderzoek
        - datum_tot (date): Einddatum van het onderzoek
        - soort_onderzoek (string): Soort onderzoek
        - locatie (string): Locatie van het onderzoek
        - met_beloning (boolean): Geeft aan of er een beloning is voor deelnemers
        - beloning (string): Omschrijving van de beloning (optioneel)
        - doelgroep_leeftijd_van (integer): Minimale leeftijd van de doelgroep
        - doelgroep_leeftijd_tot (integer): Maximale leeftijd van de doelgroep

        - beperkingen (array): Een array van objecten die de beperkingen van het onderzoek beschrijven. Elk object heeft een beperking_id veld dat het ID van de beperking vertegenwoordigt. Voor meer informatie, scroll verder naar beneden om te
        kijken welke id bij welke beperking hoort.

        - contact_opgenomen (boolean): Geeft aan of er contact is opgenomen met de doelgroep

    - Retourneert:
        - onderzoeks_id (integer)
        - organisatie (integer)
        - status (string)
        - titel (string)
        - omschrijving (string)
        - datum_vanaf (date)
        - datum_tot (date)
        - soort_onderzoek (string)
        - locatie (string)
        - met_beloning (boolean)
        - beloning (string)
        - doelgroep_leeftijd_van (integer)
        - doelgroep_leeftijd_tot (integer)
        - type_onderzoek (integer): 1 = locatie, 2 = telefonisch, 3 = online
        - contact_opgenomen (boolean)
        - opmerkingen_beheerder (string)



API/organisatie/<int:organisatie_id>/onderzoeken?api={api_key}:

- **POST (nieuw onderzoek aanmaken)**
    - Een JSON-object met de velden die bijgewerkt moeten worden:
        - titel (string): Titel van het onderzoek
        - omschrijving (string): Omschrijving van het onderzoek
        - datum_vanaf (date): Begindatum van het onderzoek
        - datum_tot (date): Einddatum van het onderzoek
        - soort_onderzoek (string): Soort onderzoek
        - locatie (string): Locatie van het onderzoek
        - met_beloning (boolean): Geeft aan of er een beloning is voor deelnemers
        - beloning (string): Omschrijving van de beloning (optioneel)
        - doelgroep_leeftijd_van (integer): Minimale leeftijd van de doelgroep
        - doelgroep_leeftijd_tot (integer): Maximale leeftijd van de doelgroep
        - type_onderzoek (integer): 1 = locatie, 2 = telefonisch, 3 = online

        - beperkingen (array): Een array van objecten die de beperkingen van het onderzoek beschrijven. Elk object heeft een beperking_id veld dat het ID van de beperking vertegenwoordigt. Voor meer informatie, scroll verder naar beneden om te
        kijken welke id bij welke beperking hoort.

        - contact_opgenomen (boolean): Geeft aan of er contact is opgenomen met de doelgroep
        - opmerkingen_beheerder (string): Eventuele opmerkingen van de beheerder

    - Retourneert:
        - onderzoeks_id (integer)
        - organisatie (integer)
        - status (string)
        - titel (string)
        - omschrijving (string)
        - datum_vanaf (date)
        - datum_tot (date)
        - soort_onderzoek (string)
        - locatie (string)
        - met_beloning (boolean)
        - beloning (string)
        - doelgroep_leeftijd_van (integer)
        - doelgroep_leeftijd_tot (integer)
        - type_onderzoek (integer)
        - contact_opgenomen (boolean)
        - opmerkingen_beheerder (string)

- **GET (alle onderzoeken ophalen)**
    - Retourneert:
        Een lijst van alle onderzoeken met de volgende velden:
        - onderzoeks_id (integer)
        - organisatie (integer)
        - status (string)
        - titel (string)
        - omschrijving (string)
        - datum_vanaf (date)
        - datum_tot (date)
        - soort_onderzoek (string)
        - locatie (string)
        - met_beloning (boolean)
        - beloning (string)
        - doelgroep_leeftijd_van (integer)
        - doelgroep_leeftijd_tot (integer)
        - type_onderzoek (integer)
        - contact_opgenomen (boolean)
        - opmerkingen_beheerder (string)




## Beperkingen
1. 	Doof	                        Auditieve beperking
2.	Slechthorend	                Auditieve beperking
3.	Doofblind	                    Auditieve beperking
4.	Blind	                        Visuele beperking
5.	Slechtziend	                    Visuele beperking
6.	Kleurenblind	                Visuele beperking
7.	Doofblind	                    Visuele beperking
8.	Amputatie of mismaaktheid	    Motorische / lichamelijke beperkingen
9.	Artritus	                    Motorische / lichamelijke beperkingen
10.	Fibromyalgie	                Motorische / lichamelijke beperkingen
11.	Reuma	                        Motorische / lichamelijke beperkingen
12.	Verminderde handvaardigheid	    Motorische / lichamelijke beperkingen
13.	Spierdystrofie	                Motorische / lichamelijke beperkingen
14.	RSI	                            Motorische / lichamelijke beperkingen
15.	Tremor en Spasmen	            Motorische / lichamelijke beperkingen
16.	Quadriplegie of tetraplegie	    Motorische / lichamelijke beperkingen
17.	ADHD	                        Cognitieve / neurologische beperkingen
18.	Autisme	                        Cognitieve / neurologische beperkingen
19.	Leerstoornis	                Cognitieve / neurologische beperkingen
20.	Geheugen beperking	            Cognitieve / neurologische beperkingen
21.	Multiple Sclerose	            Cognitieve / neurologische beperkingen
22.	Epilepsie	                    Cognitieve / neurologische beperkingen
23.	Migraine	                    Cognitieve / neurologische beperkingen
