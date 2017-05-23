import requests
from bs4 import BeautifulSoup

def get_cards():
    cards = []
    page = requests.get('http://gwentify.com/cards/?view=table')

    while page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        rows = soup.find('table').find_all('tr')
        for row in rows:
            card_url = row.td.a.get('href')

            card_page = requests.get(card_url)

            if page.status_code == 200:
                card_dict = {}
                card_soup = BeautifulSoup(card_page.content, 'html.parser')
                card_main = card_soup.find('div', id='primary').main
                card_name = card_main.find('h1').get_text()
                print(card_name)
                card_dict['name'] = card_name

                for entry in card_main.select('ul.card-cats > li'):
                    property = entry.strong.get_text().strip()

                    if property == 'Group:':
                        card_dict['group'] = entry.a.get_text().strip()
                    elif property == 'Rarity:':
                        card_dict['rarity'] = entry.a.get_text().strip()
                    elif property == 'Faction':
                        card_dict['faction'] = entry.a.get_text().strip()

                cards.append(card_dict)

        try:
            next_page = soup.find('ul', class_='pagination'). \
                                  find('a', class_='nextpostslink').get('href')
            page = requests.get(next_page)
        except:
            break

    return cards

def write_cards(cards_dict):
    with open('cards.json', 'w') as outfile:
        json.dump(cards_dict, outfile)

def read_cards():
    with open('cards.json') as infile:
        cards = json.loads(infile)
        infile.close()
        return cards

if __name__ == '__main__':
    cards = get_cards()
    write_cards(cards)
    read_cards()
    






#get_cards()

#print(soup.prettify())
#print(page.json())

"""
next_list = requests.get(test.json()['next'])

h2 class = 'entry-title'
a rel = 'bookmark'
ul class = card-cats

page = requests.get('http://dataquestio.github.io/web-scraping-pages/simple.htlm')
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
"""
