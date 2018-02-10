import requests
import json
from bs4 import BeautifulSoup

def get_cards2():
    cards = []
    page = requests.get('https://gwentdb.com/cards?filter-display=1')
    return(page.status_code)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        rows = soup.find_all('tr')

def get_cards():
    cards = []
    page = requests.get('http://gwentdb.com/cards?filter-display=1')

    while page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        rows = soup.find_all('tr')[1:]
        for row in rows:
            card_url = row.td.a.get('href')

            card_page = requests.get('http://gwentdb.com' + card_url)

            if card_page.status_code == 200:
                card_dict = {}
                card_soup = BeautifulSoup(card_page.content, 'html.parser')

                card_name = card_soup.find('div', {'class': 'card-name'}). \
                        find('h1').get_text()
                card_name = card_name.splitlines()[1].lstrip()
                
                card_rarity = card_soup.find('div', {'class': 'card-rarity'}). \
                        find('span').get_text()
                card_group = card_soup.find('div', {'class': 'card-type'}). \
                        find('span').get_text()
                card_faction = card_soup.find('div', {'class': 'card-faction'}). \
                        find('a').get_text()
                 

                print(card_name)
                card_dict['name'] = card_name
                card_dict['rarity'] = card_rarity
                card_dict['group'] = card_group
                card_dict['faction'] = card_faction
                cards.append(card_dict)

        try:
            next_page = soup.find('ul', class_='b-pagination-list'). \
                                  find('a', rel='next').get('href')
            page = requests.get('http://gwentdb.com' + next_page)
        except:
            break

    return cards

def write_cards(cards_dict):
    with open('cards.json', 'w') as outfile:
        json.dump(cards_dict, outfile)

def read_cards():
    with open('cards.json') as infile:
        cards = json.load(infile)
        infile.close()
        return cards

if __name__ == '__main__':
    cards = get_cards()
    write_cards(cards)
    cards = read_cards()
