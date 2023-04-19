import random
from itertools import combinations

NUM_SIMULATIONS=10000

def evaluate(cards):
    # Separate the pocket cards and community cards
    pocket_cards = cards[:2]
    community_cards = cards[2:]
    
    # Create all possible combinations of hands with community cards
    community_hands = set()
    for community in combinations(community_cards, 3):
        community_hands.add(tuple(sorted(community)))
    possible_hands = [pocket_cards + list(community) for community in community_hands]

    # Determine the best hand for the player
    value = (0,0,())
    for hand in possible_hands:
        test_value = hand_value(hand)
        value = max(value, test_value, key=lambda x: (x[0], x[1], x[2]))
        
    return value
    

def hand_value(hand):
    # Convert the cards to values and suits
    values = [(card % 13) + 1 for card in hand]
    suits = [card // 13 for card in hand]

    # Check for a flush
    flush = len(set(suits)) == 1
    
    # Check for a straight
    straight_values = values
    if {1, 10, 11, 12, 13}.issubset(straight_values):
        straight = True
        values = [10, 11, 12, 13, 1]
    else:
        straight = len(straight_values) == 5 and max(values) - min(values) == 4

    # Count the occurrences of each value
    value_counts = [values.count(value) for value in set(values)]

    # Determine the rank of the hand
    if 4 in value_counts:
        rank = 8  # Four of a Kind
        value = value_counts.index(4) + 1
        kicker = tuple(sorted([v for v in values if v != value], reverse=True))
    elif 3 in value_counts and 2 in value_counts:
        rank = 7  # Full House
        value = value_counts.index(3) + 1
        kicker = value_counts.index(2) + 1
    elif 3 in value_counts:
        rank = 4  # Three of a Kind
        value = value_counts.index(3) + 1
        kicker = tuple(sorted([v for v in values if v != value], reverse=True))
    elif value_counts.count(2) == 2:
        rank = 3  # Two Pair
        pairs = sorted([i + 1 for i, v in enumerate(value_counts) if v == 2], reverse=True)
        value = pairs[0]
        kicker = pairs[1]
    elif 2 in value_counts:
        rank = 2  # One Pair
        value = value_counts.index(2) + 1
        kicker = tuple(sorted([v for v in values if v != value], reverse=True))
    else:
        if straight and flush:
            if max(values) == 14:
                rank = 10  # Royal Flush
                value = None
                kicker = ()
            else:
                rank = 9  # Straight Flush
                value = max(values)
                kicker = ()
        elif flush:
            rank = 6  # Flush
            value = None
            kicker = tuple(sorted(values, reverse=True))
        elif straight:
            rank = 5  # Straight
            value = max(values)
            kicker = ()
        else:
            rank = 1  # High Card
            value = tuple(sorted(values, reverse=True))
            kicker = ()

    return (rank, value, kicker)

def simulate_game(pocket_cards, community_cards):
    # If pocket_cards or community_cards are bigger than 2 or 5 respectively, raise an error
    if len(pocket_cards[0]) != 2 or len(community_cards) > 5:
        raise ValueError('Invalid number of cards')
    
    # If pocket_cards or community_cards have numbers bigger than 51 or smaller than 0, raise an error
    if not all([0 <= card <= 51 for player_pocket_cards in pocket_cards for card in player_pocket_cards]):
        raise ValueError('Invalid card number')
    if not all([0 <= card <= 51 for card in community_cards]):
        raise ValueError('Invalid card number')
    
    # Create dealing deck and counts array
    deck = [card for card in range(52) if card not in pocket_cards and card not in community_cards]
    counts = [0.0 for _ in range(len(pocket_cards)+1)]

    for _ in range(NUM_SIMULATIONS):
        # Deal the needed community cards and create all hands
        random.shuffle(deck)
        new_community_cards = community_cards + deck[:5 - len(community_cards)]
        all_hands = [player_pocket_cards + new_community_cards for player_pocket_cards in pocket_cards]

        # Evaluate each hand and define a key function that returns a tuple with the rank, value, and kicker of a hand
        hand_ranks = [evaluate(hand) for hand in all_hands]

        # Use the key function with max to determine the winning hand(s)        
        key = lambda hand: (hand[0], hand[1], hand[2])
        max_key = max([key(hand) for hand in hand_ranks])
        winners = [i for i, hand in enumerate(hand_ranks) if key(hand) == max_key]
        if len(winners) == 1:       
            for winner in winners:
                counts[winner] += 1
        else:
            counts[-1] += 1
        
        # If 5 community cards are already given, return the counts
        if len(community_cards) == 5:
            return counts
    
    # Divide the counts by the number of simulations to get the probabilities
    return [round(count / NUM_SIMULATIONS, 6) for count in counts]

pocket_cards = [[22,23], [10,37], [35,36]] # Three players, each with two pocket cards
community_cards = [51,14,28,24,23] # The five community cards
#community_cards = [12,8,0] # The five community cards
probabilities = simulate_game(pocket_cards, community_cards)

print(probabilities)