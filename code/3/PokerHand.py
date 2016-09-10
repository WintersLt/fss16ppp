"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *
import random


class PokerHand(Hand):
    # List with has_ func in priority
    # the most probable should come last
    has_funcs = ['straight_flush', 'four_of_a_kind', 'full_house', 'flush',
            'straight', 'three_of_a_kind', 'two_pairs', 'pair']

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1


    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
    
    def check_seq(self, card_ranks):
        ''' Takes a list of integer ranks of cards
            returns true if they form a seq as per rules'''
        card_ranks = list(set(sorted(card_ranks)))
        ct = 1
        prev_rank = card_ranks[0]
        for rank in card_ranks[1:]:
            if rank - prev_rank == 1 or (prev_rank == 13 and ct == 4 and card_ranks[0] == 1):
                ct+=1
                if ct >= 5:
                     return True
            else:
                ct = 1
            prev_rank = rank

        # 10 11 12 13 and 1
        if prev_rank == 13 and ct == 4 and card_ranks[0] == 1:
            return True
        return False


    def has_straight_flush(self):
        self.suit_hist()
        for card_suit, ct in self.suits.iteritems():
            if ct >= 5:
                return self.check_seq([card.rank for card in self.cards if card.suit == card_suit])
        return False
    
    def has_four_of_a_kind(self):
        self.rank_hist()
        for rank_ct in self.ranks.values():
            if rank_ct >= 4:
                return True
        return False

    def has_full_house(self):
        self.rank_hist()
        has_3 = False
        has_2 = False
        cts = self.ranks.values()
        cts = sorted([x for x in cts if x >= 2], reverse = True)
        if len(cts) >= 2 and cts[0] >= 3:
            return True
        return False

       #for rank_ct in sorted(self.ranks.values()):
       #    if not has_3 and rank_ct >= 3:
       #        has_3 = True
       #    elif has_3 and not has_2 and rank_ct >= 2:
       #        has_2 = True
       #    if has_3 and has_2:
       #        return True
       #return False
    
    def has_straight(self):
       #if self.check_seq([card.rank for card in self.cards]):
       #    print self
       #    print ''
       #card_ranks = [card.rank for card in self.cards]
       #if 5 ==  sorted(card_ranks)[0]:
       #    print "card_ranks",card_ranks, self.check_seq([card.rank for card in self.cards])
        return self.check_seq([card.rank for card in self.cards])

    def has_three_of_a_kind(self):
        self.rank_hist()
        for rank_ct in self.ranks.values():
            if rank_ct >= 3:
                return True
        return False
    
    def has_two_pairs(self):
        self.rank_hist()
        num_pairs = 0
        for rank_ct in self.ranks.values():
            if rank_ct >= 2:
                num_pairs+=1
            if num_pairs == 2:
                return True
        return False
            
    def has_pair(self):
        self.rank_hist()
        for rank_ct in self.ranks.values():
            if rank_ct >= 2:
                return True
        return False

    def classify(self):
        self.labels = []
        for has_func in self.has_funcs:
            func = getattr(self, 'has_' + has_func)
            if func():
                if not self.label:
                    self.label = has_func
                self.labels += [has_func]


'''
pair: two cards with the same rank

two pair: two pairs of cards with the same rank

three of a kind: three cards with the same rank

straight: five cards with ranks in sequence (aces can be high or low, so Ace-2-3-4-5 is a straight
and so is 10-Jack-Queen-King-Ace, but Queen-King-Ace-2-3 is not.)

flush: five cards with the same suit

full house: three cards with one rank, two cards with another

four of a kind: four cards with the same rank

straight flush: five cards in sequence (as defined above) and with the same suit
'''

def find_probabilities():
    random.seed(1201)
    counts={}
    for i in xrange(10000): # num trials
        deck = Deck()
        deck.shuffle()

        # deal the cards and classify the hands
        for i in range(7):
            hand = PokerHand()
            deck.move_cards(hand, 7)
            hand.classify()
            for label in hand.labels:
                counts[label] = counts.get(label, 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda x: x[1])
    for label, count in sorted_counts:
        if count:
            print label, "chances for this are one in", 70000.00/count


if __name__ == '__main__':
    # make a deck
    find_probabilities()

