import requests
import json
from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen

def get_cards(faction):
    card_list = []
    cards_url = 'https://gwent.one/en/cards/'
    page = requests.get(cards_url + faction)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        #card_names = soup.find_all('div', {'class': 'gscard__title'})
        card_data = soup.find_all('div', {'class': 'card-data'})

        for card in card_data:
            card_name = card.find('div', {'class': 'card-name'}).find('a').text
            card_category = card.find('div', {'class': 'card-category'}).text
            card_body = card.find('div', {'class': 'card-body'}).text.replace("\n", " ").strip()
            card_href = card.find('a').get('href')
            card_provisions = card.get('data-provision')
            card_rarity = card.get('data-rarity')
            card_faction = card.get('data-faction')

            print(card_name)
            #card_page = requests.get(card_href)
            #if card_page.status_code == 200:
            #print(card_href)
            #card_soup = BeautifulSoup(card_page.content, 'html.parser')

            card_dict = {'name': card_name, 'href': card_href, 'rarity': card_rarity,
                         'faction': card_faction, 'category': card_category}
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

    # Get cards from the gwent.one database, one faction at a time
    cards = []
    for faction in ['Neutral', 'Nilfgaard', 'Northern-Realms', 'Scoiatael', 'Skellige', 'Monster', 'Syndicate']:
        print(faction)
        faction_cards = get_cards(faction)
        cards.extend(faction_cards)

    write_cards(cards)
    cards = read_cards()