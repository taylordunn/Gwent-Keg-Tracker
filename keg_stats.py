import numpy as np
import pandas as pd
import json
import datetime
import matplotlib.pylab as plt

def load_cards(cards_json):
    """
    Opens the specified JSON file containing card details (name, group
    and rarity). Returns a pandas dataframe of the data.
    """
    with open(cards_json) as infile:
        cards = json.load(infile)
        infile.close()
    cards_dict = {}
    cards_dict['name'] = [card['name'] for card in cards]
    cards_dict['group'] = [card['group'] for card in cards]
    cards_dict['rarity'] = [card['rarity'] for card in cards]
    df = pd.DataFrame(cards_dict)
    df.set_index('name', inplace=True)
    return df


if __name__ == '__main__':
    cards_df_current = load_cards('cards.json')

    # Patch on August 30 added new cards, and renamed/reclassified old ones.
    cards_df_170831 = load_cards('old/cards_170831.json')
    date_170831 = pd.to_datetime("2017-08-30")

    kegs_df = pd.read_csv('kegs_autoload.csv')
    kegs_df = kegs_df[['date', 'card1', 'card2', 'card3', 'card4',
                       'picked_card']]
    kegs_df.date = pd.to_datetime(kegs_df.date)
    n_kegs = len(kegs_df.index)
    n_cards = 5 * n_kegs 
    
    rarity_counts = {}
    premium_counts = {'total': 0}
    for rarity in cards_df_current.rarity.unique():
        rarity_counts[rarity] = 0
        premium_counts[rarity] = 0

    keg_number = []
    counter = {}
    counter['Rare'] = []
    counter['Epic'] = []
    counter['Legendary'] = []
    kegs_df = kegs_df.reindex(index=kegs_df.index[::-1])
    for row,(idx,keg) in enumerate(kegs_df.iterrows()):
        print(row)
        keg_number.append(row+1)
        for rarity in ['Rare', 'Epic', 'Legendary']:
            if row == 0: counter[rarity].append(0)
            else: counter[rarity].append(counter[rarity][row-1])
        
        # Determine which patch this keg was opened on, and assign the
        #  appropriate card database
        card_date = keg.loc['date']
        if card_date < date_170831:
            cards_df = cards_df_170831
        else:
            cards_df = cards_df_current

        for key in ['card1', 'card2', 'card3', 'card4', 'picked_card']:
            card_name = keg.loc[key]
            if '*' in card_name:
                card_name = card_name.split('*')[0] 
                card_rarity = cards_df.ix[card_name].rarity
                premium_counts[card_rarity] += 1
                premium_counts['total'] += 1
            else:
                card_rarity = cards_df.ix[card_name].rarity
            rarity_counts[card_rarity] += 1
            if card_rarity != 'Common': counter[card_rarity][-1] += 1
    
    print('Out of %d kegs (%d cards)' % (n_kegs, n_cards))
    print('---------------------------------')
    count = rarity_counts['Legendary']
    for rarity in ['Legendary', 'Epic', 'Rare']:
        count = rarity_counts[rarity]
        perc = count / n_kegs
        try: kegs_per = n_kegs / count
        except: kegs_per = 0
        print('{0}: {1} ({2:.2%} or 1 in {3:.1f} kegs)'.format(rarity, count,
                                                         perc, kegs_per))
    count = premium_counts['total']
    perc = count / n_kegs
    try: kegs_per = n_kegs / count
    except: kegs_per = 0
    print('---------------------------------')
    print('Premiums: {0} ({1:.2%} or 1 in {2:.1f} kegs)'.format(count,
                                                         perc, kegs_per))
    for rarity in ['Legendary', 'Epic', 'Rare']:
        count = premium_counts[rarity]
        perc = count / n_kegs
        try: kegs_per = n_kegs / count
        except: kegs_per = 0
        print('{0}: {1} ({2:.2%} or 1 in {3:.1f} kegs)'.format(rarity, count,
                                                         perc, kegs_per))
    

    plt.plot(keg_number, counter['Legendary'],
            color="#ffbf00", label='Legendary')
    plt.plot(keg_number, counter['Epic'],
            color="#663399", label='Epic')
    x = np.arange(0, n_kegs, 0.1)
    y1 = 0.2*x
    y2 = 0.1*x
    y3 = 0.05*x
    plt.plot(x, y1, 'k-', label = "1 in 5 kegs")
    plt.plot(x, y2, 'k--', label = "1 in 10 kegs")
    plt.plot(x, y3, 'k:', label = "1 in 20 kegs")

    plt.xlabel('Keg number')
    plt.ylabel('Card count')
    plt.legend()
    plt.savefig('card_count.pdf')


