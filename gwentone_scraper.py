import requests
import json
from bs4 import BeautifulSoup

def get_cards(faction):
    card_list = []
    cards_url = 'https://gwent.one/en/cards/'
    page = requests.get(cards_url + faction)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        card_names = soup.find_all('div', {'class': 'gscard__title'})

        for card in card_names:
            card_name = card.find('a').text.strip()
            card_href = card.find('a').get('href')

            print(card_name)
            #card_page = requests.get(card_href)
            #if card_page.status_code == 200:
            #print(card_href)
            #card_soup = BeautifulSoup(card_page.content, 'html.parser')

            card_dict = {'name': card_name, 'href': card_href, 'group': '', 'faction': faction}
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
    # As of 2019-07-13, these are the numbers of leaders per faction
    faction_nleaders = {'Neutral': 0, 'Nilfgaard': 6, 'Northern-Realms': 6, 'Scoiatael': 6, 'Skellige': 6,
                        'Monster': 6, 'Syndicate': 5}

    # Get cards from the gwent.one fan wiki, one faction at a time
    cards = []
    for faction in ['Neutral', 'Nilfgaard', 'Northern-Realms', 'Scoiatael', 'Skellige', 'Monster', 'Syndicate']:
        print(faction)
        faction_cards = get_cards(faction)
        cards.extend(faction_cards)

        # Leaders are at the head of the list of cards
        n_leaders = faction_nleaders[faction]
        for i in range(0, n_leaders):
            faction_cards[i]['group'] = 'Leader'
    write_cards(cards)
    cards = read_cards()