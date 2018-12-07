import requests
import json
from bs4 import BeautifulSoup

def get_cards():
    # A simple function to scrape just name and href from the gwentdb.net website
    card_list = []
    page = requests.get('https://gwentdb.net/card_info')

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        cards = soup.find_all('div', {'class': 'card_name'})

        for card in cards:
            card_name = card.get('name')
            card_href = card.find('a').get('href')

            print(card_name)
            card_dict = {'name': card_name, 'href': card_href}
            card_list.append(card_dict)

    return card_list

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
