"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Antonín Bergner
email: tonda.bergner@gmail.com
discord: #Tondoj
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

# Základní URL
MAIN_URL = "https://volby.cz/pls/ps2017nss/"

# Formátované selektory pro výběr buněk z tabulek
CODE = "t{}sa1 t{}sb1"
CITY = "t{}sa1 t{}sb2"
LINK = "t{}sa2"
CAND_PARTY = "t{}sa1 t{}sb2"
NUMBER = "t{}sa2 t{}sb3"

# Hlavička výsledného CSV souboru
FIRST_ROW = ["Code", "City", "Registered", "Envelopes", "Votes"]

def get_html(url):
    """Stáhne HTML stránku a vrátí jako BeautifulSoup objekt."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print("Chyba při stahování:", e)
        sys.exit(1)

def get_first_columns(soup):
    """
    Z hlavní stránky získá: kódy obcí,
                            názvy obcí,
                            odkazy na detailní stránky.
    Používá elementy s třídou "t3" a formátované hodnoty atributu headers.
    """
    tables = soup.find_all("div", class_="t3")
    codes, cities, links = [], [], []
    for idx, table in enumerate(tables, start=1):
        code_cells = table.find_all("td", headers=CODE.format(idx, idx))
        city_cells = table.find_all("td", headers=CITY.format(idx, idx))
        link_cells = table.find_all("td", headers=LINK.format(idx))
        for cell in code_cells:
            if cell.text.strip() != "-":
                codes.append(cell.text.strip())
        for cell in city_cells:
            if cell.text.strip() != "-":
                cities.append(cell.text.strip())
        for cell in link_cells:
            a = cell.find("a")
            if a and a.get("href"):
                links.append(a["href"])
    return codes, cities, links

def get_all_header_data(soup):
    """
    Ze stránky s agregovanými výsledky (tabulka s id "ps311_t1") získá: registrované voliče,
                                                                        vydané obálky,
                                                                        platné hlasy.
    Vrací seznam se třemi hodnotami jako řetězce.
    """
    table = soup.find("table", id="ps311_t1")
    if table:
        tds = table.find_all("td")
        reg = "".join([c for c in tds[3].text if c.isdigit()])
        env = "".join([c for c in tds[4].text if c.isdigit()])
        valid = "".join([c for c in tds[7].text if c.isdigit()])
        return [reg, env, valid]
    return ["", "", ""]

def get_cand_parties(soup):
    """
    Získání jmen kandidátských stran z dané stránky.
    Používá elementy <td> s atributem headers, který se formátuje dle CAND_PARTY.
    """
    parties = []
    divs = soup.find_all("div", class_="t2_470")
    for idx, div in enumerate(divs, start=1):
        for td in div.find_all("td", headers=CAND_PARTY.format(idx, idx)):
            if td.text.strip() != "-":
                parties.append(td.text.strip())
    return parties

def get_party_numbers(soup):
    """
    Ze stránky se získají hlasovací čísla pro kandidátské strany.
    Používá formátovaný selektor podle NUMBER.
    """
    numbers = []
    divs = soup.find_all("div", class_="t2_470")
    for idx, div in enumerate(divs, start=1):
        for td in div.find_all("td", headers=NUMBER.format(idx, idx)):
            if td.text.strip() != "-":
                numbers.append(td.text.strip())
    return numbers

def get_middle_links(soup):
    """
    Získání odkazů na jednotlivé okrsky, pokud obec není zobrazená agregovaně.
    Prohledá tabulky s třídou "table" a elementy s atributem headers="s1".
    """
    links = []
    tables = soup.find_all("table", class_="table")
    for table in tables:
        for td in table.find_all("td", headers="s1"):
            for a in td.find_all("a"):
                if a.get("href"):
                    links.append(a["href"])
    return links

def sum_header_data(middle_links):
    """
    Pro obce rozdělené do okrsků (neagregované) se získají
    registrovaní voliči, vydané obálky a platné hlasy ze všech okrsků a sečtou se.
    """
    total_reg = 0
    total_env = 0
    total_valid = 0
    for link in middle_links:
        url = MAIN_URL + link
        soup = get_html(url)
        tables = soup.find_all("table", id="ps311_6_t1")
        for table in tables:
            tds = table.find_all("td")
            reg = "".join([c for c in tds[1].text if c.isdigit()])
            env = "".join([c for c in tds[3].text if c.isdigit()])
            valid = "".join([c for c in tds[4].text if c.isdigit()])
            try:
                total_reg += int(reg)
                total_env += int(env)
                total_valid += int(valid)
            except:
                pass
    return [str(total_reg), str(total_env), str(total_valid)]

def get_sum_numbers(middle_numbers):
    """Sečtení čísel pro kandidátské strany a získání jednotlivých okrsků."""
    if not middle_numbers:
        return []
    sums = [0] * len(middle_numbers[0])
    for numbers in middle_numbers:
        for i, n in enumerate(numbers):
            sums[i] += int("".join(filter(str.isdigit, n)))
    return [str(s) for s in sums]

def sum_party_numbers(middle_links):
    """Ze všech okrsků se získají hlasovací čísla pro kandidátské strany a sečtou se pozicově."""
    all_numbers = []
    for link in middle_links:
        url = MAIN_URL + link
        soup = get_html(url)
        nums = []
        divs = soup.find_all("div", class_="t2_470")
        for idx, div in enumerate(divs, start=1):
            for td in div.find_all("td", headers=NUMBER.format(idx, idx)):
                if td.text.strip() != "-":
                    nums.append(td.text.strip())
        all_numbers.append(nums)
    return get_sum_numbers(all_numbers)

def get_second_data(links):
    """
    Zpracování detailů ze stránek obcí.
    Pokud odkaz obsahuje "vyber", předpokládá se, že obec je agregovaná,
    v opačném případě se použijí odkazy na jednotlivé okrsky a data se sečtou.
    Vrací seznam: základních údajů (registrovaní voliči, obálky, platné hlasy) pro každou obec,
                  jména kandidátských stran
                  hlasovací čísla kandidátských stran pro každou obec.
    """
    header_data_all = []
    party_numbers_all = []
    cand_parties = []
    for link in links:
        url = MAIN_URL + link
        soup = get_html(url)
        if "vyber" in link:
            header_data_all.append(get_all_header_data(soup))
            cand_parties = get_cand_parties(soup)
            party_numbers_all.append(get_party_numbers(soup))
        else:
            middle_links = get_middle_links(soup)
            header_data_all.append(sum_header_data(middle_links))
            party_numbers_all.append(sum_party_numbers(middle_links))
            # Předpokládáme, že jména kandidátských stran z jedné stránky jsou dostačující
            cand_parties = get_cand_parties(soup)
    return header_data_all, cand_parties, party_numbers_all

def save_to_csv(codes, cities, header_data_all, cand_parties, party_numbers_all, output_file):
    """
    Uloží data do CSV souboru. 
    Každý řádek obsahuje: kód obce,
                          název obce,
                          registrované voliče, vydané obálky, platné hlasy,
                          pro každou kandidátskou stranu sloupec s číslem hlasů.
    """
    with open(output_file, mode="w", newline="", encoding="Windows-1250") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(FIRST_ROW + cand_parties)
        for code, city, header_data, party_numbers in zip(codes, cities, header_data_all, party_numbers_all):
            row = [code, city] + header_data + party_numbers
            writer.writerow(row)

def main():
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL> <output.csv>")
        sys.exit(1)
    url = sys.argv[1]
    output_file = sys.argv[2]
    print("Stahuji data z:", url)
    main_soup = get_html(url)
    codes, cities, links = get_first_columns(main_soup)
    header_data_all, cand_parties, party_numbers_all = get_second_data(links)
    save_to_csv(codes, cities, header_data_all, cand_parties, party_numbers_all, output_file)
    print("Hotovo. Data uložena do", output_file)

if __name__ == "__main__":
    main()