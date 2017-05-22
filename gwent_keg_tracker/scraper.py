import requests
from bs4 import BeautifulSoup

endpoints = {
'href': 'https://api.gwentapi.com/v0/', # Return a mapping of resources name to href.
'all_cards': 'https://api.gwentapi.com/v0/cards/', # Return all cards.
'specific_card': 'https://api.gwentapi.com/v0/cards/:id', # Return a specific card.
'all_leaders': 'https://api.gwentapi.com/v0/cards/leaders',	# Return all leader cards.
'specific_faction_cards': 'https://api.gwentapi.com/v0/cards/factions/:factionID', # Return all cards from the corresponding faction.
'specific_card_variations': 'https://api.gwentapi.com/v0/cards/:id/variations', # Return the variations of a specific card.
'all_factions': 'https://api.gwentapi.com/v0/factions/', # Return all card factions.
'specific_card_faction': 'https://api.gwentapi.com/v0/factions/:id', # Return a specific card faction.
'all_rarities': 'https://api.gwentapi.com/v0/rarities/', # Return all card rarities.
'specific_card_rarity': 'https://api.gwentapi.com/v0/rarities/:id',	# Return a specific card rarity.
'all_group_types': 'https://api.gwentapi.com/v0/groups/', # Return all group types.
'specific_card_group': 'https://api.gwentapi.com/v0/groups/:id', # Return a specific card group.
'all_categories': 'https://api.gwentapi.com/v0/categories/', # Return all categories.
'specific_card_category': 'https://api.gwentapi.com/v0/categories/:id', # Return a specific category.
}


page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.htlm")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
