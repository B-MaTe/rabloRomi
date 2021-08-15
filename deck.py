import collections
import random
from settings import Settings


Card = collections.namedtuple("Card", ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self.settings = Settings()
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]
        for _ in range(self.settings.Jokers):
            self._cards.append(Card("J", False))
        
        ### SHUFFLE THE CARDS
        random.shuffle(self._cards)


    def __len__(self):
        return len(self._cards)


    def __getitem__(self, pos):
        return self._cards[pos]
    
    def getRandomCard(self):
        return self._cards[random.randint(0, len(FrenchDeck()))]
    
    
    

"""
card_no1 = Card('2', 'spades')
# print(card_no1)

deck = FrenchDeck()
# print(len(deck))

# print(deck[:])

random_card = random.choice(deck)
# print(random_card)

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


for card in sorted(deck, key=spades_high):  # doctest: +ELLIPSIS
    print(card)
"""

