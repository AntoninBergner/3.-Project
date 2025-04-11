# **Election Scraper**
## **3. projekt pro Engeto Akademii**

- Autor: Antonín Bergner
- Kontakt: tonda.bergner@gmail.com
- Discord: #Tondoj

Celkově mi psaní samotného programu zabralo přibližně 40-50 hodin. Psal jsem ho částečně i na dvakrát, protože prvotní verze mi nefungovala tak jak měla. Sice mi stáhla veškerá data, ale import do CSV souboru nebyl úplný a nebo různě přeházený, takže jsem vlastně začínal skoro od začátku. K funkcím jsem vypsal podrobnější komentáře, co dělají.

## **Popis programu**
Tento program byl napsaný pro účely stažení a zpracování výsledků voleb v ČR, pro rok 2017. 
Konkrétně stahuje data ze stránky [www.volby.cz](https://www.volby.cz/), v nich po vybrání konkrétního okresu vytáhne jednotlivé obce, vypíše v nich všechny hlasy, vyselektuje platné hlasy a vypíše jednotlivé strany a hlasy, které získaly. 

## **Obsah repozitáře**
- Election_Scraper.py - hlavní skript, který provádí stahování a parsování dat.
- requirements.txt - seznam všech požadovaných knihoven
- readme.md - to je tento soubor s celkový popisem projektu a instrukcemi
- vysledky_prostejov.csv - výsledná tabulka, obsahující veškerá data

## **Funkce**
- Stahování HTML - skript využívá knihovnu "requests" pro stažení HTML stránky www.volby.cz.
- Parsování dat pomocí knihovny "BeautifulSoup" jsou výše vypsaná data z HTML extrahována data, např.: kódy obcí, jejich názvy, počet voličů, vydané obálky, platné hlasy a soupis jednotlivých stran a jejich hlasů, které získaly.
- Agregace výsledků - data z různých sekcí nebo okrsků se sčítají a ukládají do tabulky v souboru .csv
- Uložení dat do CSV - výsledky se uloží do CSV souboru, kde je každý řádek věnován konkrétní obci.

## **Instalace**
1. Nainstalujte Python ve verzi 3.6 nebo novější.
2. Získání repozitáře - pokud máte Git, můžete si jej naklonovat pomocí následujícího příkazového řádku: git clone https://github.com/AntoninBergner/3.-Project.
   Případně si můžete jednotlivé části repozitáře stáhnout či nakopírovat.
3. Vytvoření a aktivace virtuálního prostředí:
    - otevřete terminál v hlavním adresáři projektu a spusťte tento řádek: python -m venv .venv
    - aktivujte virtuální prostředí (CMD): .venv\Scripts\activate
    - pokud používáte (PowerShell): .\.venv\Scripts\activate.ps1
    - pokud pracujete v Linuxu / macOS: source .venv/bin/activate
4. Instalace potřebných knihoven - pokud jste splnili výše uvedené úkony, nyní si nainstalujte potřebné knihovny, pomocí následujících příkazů:
    - pip install -r requirements.txt
	- pip install requests
	- pip instal beautifulsoup4
5. Spuštění - pro spuštění programu se používají argumenty v příkazovém řádku. Tyto argumenty musí obsahovat typ + název programu, URL adresu konkrétního okresu a název konečného csv souboru. 
              Přesný popis je takto: python Election_Scraper.py "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ&xobec=123456" vysledky-mesto.csv.
	          Jakmile napíšete tuto podobu v příkazovém řádku, program se spustí a bude chvilku pracovat a stahovat data, většinou to trvá od 1 do 3 minut přibližně.

## **Poznámky**
V mém případě se CSV soubor stáhne a otevře v excel tabulce. Kde je sice poměrně přehledný, ale není to vyloženě úhledná tabulka. Pokud si budete chtít data více upravit, stačí v excelu kliknout v horní liště na Data > Z Text/CSV > Nalézt uložený CSV soubor > Importovat > Potvrdit volbu, která vám bude vyhovovat. Následně si tabulku můžete doupravit dle své volby. 
Pokud by došlo ke změně HTML struktury na webu volby.cz, je potřeba upravit selektory v kódu.