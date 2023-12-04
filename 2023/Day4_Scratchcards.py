"""
Advent of Code 2023 / Day 4
url: https://adventofcode.com/2023/day/4
"""

# %%
import re

# %%
card_partern = re.compile(r'^.+\: (.+) \| (.+)$', flags=re.MULTILINE)

# %%
with open('data/day4.txt') as f:
    cards = f.read()

# %%
# Get out winning and holding cards pairs.
card_pairs = card_partern.findall(cards)

points = 0
matching_counts = []  # Matching counts for each card
for card in card_pairs:
    winning_nums = set(re.split(r'\s+', card[0]))
    holding_nums = set(re.split(r'\s+', card[1]))

    # Counts intersection.
    same_counts = len(winning_nums.intersection(holding_nums))
    matching_counts.append(same_counts)
    if same_counts >= 1:
        points += 2**(same_counts - 1)

print(points)

# %%
# Part 2
card_counts = [1] * len(card_pairs)

# Loop for each card number, starting by 0 instead of 1.
for i in range(len(card_counts)):

    # For every card, Add the Count() of current card to the next "number of
    # matching" cards.
    for forward_i in range(i + 1, i + 1 + matching_counts[i]):

        # Stop forwarding if out of range, as well as no more cards to win.
        if forward_i >= len(card_pairs):
            break

        # Add cards to the forward_i by the counts of current card (card i).
        card_counts[forward_i] += card_counts[i]

# %%
print(sum(card_counts))
