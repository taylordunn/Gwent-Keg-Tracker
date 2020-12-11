import requests
import json
from bs4 import BeautifulSoup

def get_cards_bs(faction):
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

def get_cards_selenium():
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    card_list = []
    cards_url = 'https://gwent.one/en/cards/'

    driver = webdriver.Chrome()

    # The order of the factions is important here because we use the number to get the webpage
    factions = ['Neutral', 'Monsters', 'Nilfgaard', 'Northern-Realms', 'Scoiatael', 'Skellige', 'Syndicate']
    for i,faction in enumerate(factions):
        print(faction)
        search_num = 2**i

        driver.get(cards_url + '?faction=' + str(search_num))
        # Wait for the page to load
        delay = 10 # seconds
        try:
            my_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'pages-top')))
        except TimeoutException:
            print('Loading this url took longer than ' + str(3) + ' seconds: ' + cards_url + '?faction=' + str(search_num))

        # Get the buttons to select pages of cards
        pages = driver.find_element_by_id('pages-top').find_elements_by_class_name('page-link')
        # The first and last buttons can be removed
        pages = pages[1:-1]

        for j in range(len(pages)):
            print("Page " + str(j + 1))
            pages[j].click()

            # Wait for the page to load
            delay = 10 # seconds
            try:
                my_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-data-test')))
            except TimeoutException:
                print('Loading this page took longer than ' + str(delay) + ' seconds')

            card_data = driver.find_elements_by_class_name('card-data')
            for card in card_data:
                card_name = card.text.split('\n')[0]
                card_color = card.get_attribute('data-color')
                card_set = card.get_attribute('data-set')
                card_type = card.get_attribute('data-type')
                card_rarity = card.get_attribute('data-rarity')
                card_faction = card.get_attribute('data-faction')

                print("\t" + card_name)
                card_dict = {'name': card_name, 'rarity': card_rarity,
                            'faction': card_faction, 'color': card_color,
                            'set': card_set, 'type': card_type}

                card_list.append(card_dict)

            # Need to generate the list of pages again because we've changed pages
            pages = driver.find_element_by_id('pages-top').find_elements_by_class_name('page-link')
            pages = pages[1:-1]

    return card_list

def write_cards(cards_dict):
    with open('cards.json', 'w') as outfile:
        json.dump(cards_dict, outfile)

def read_cards():
    with open('cards.json') as infile:
        cards = json.load(infile)
        infile.close()
        return cards

if __name__ == '__main__soup':
    # Get cards from the gwent.one database, one faction at a time, using BeautifulSoup
    cards = []
    for faction in ['Neutral', 'Nilfgaard', 'Northern-Realms', 'Scoiatael', 'Skellige', 'Monster', 'Syndicate']:
        print(faction)
        faction_cards = get_cards(faction)
        cards.extend(faction_cards)

    write_cards(cards)
    cards = read_cards()

if __name__ == '__main__':
    # Get the cars using selenium
    cards = get_cards_selenium()

    write_cards(cards)
    cards = read_cards()
