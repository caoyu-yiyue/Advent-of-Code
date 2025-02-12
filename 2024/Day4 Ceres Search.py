# %%
import numpy as np

# %%
words: np.array = np.genfromtxt("2024/data/day4.txt", delimiter=1, dtype="<U1")

# %%
# Rotate the Matrix to construct strings of lines horizontally, vertically,
# diagonally and anti-diagonally,
# then search 'XMAX' forth and back.

horizontal_lines = [''.join(line) for line in words]
vertical_lines = [''.join(line) for line in words.T]
diag_45 = [
    ''.join(np.diag(words, k=k))
    for k in range(-(words.shape[0] - 1), words.shape[1])
]

flipped_words = np.fliplr(words)
diag_135 = [
    ''.join(np.diag(flipped_words, k=k))
    for k in range(-(words.shape[0] - 1), words.shape[1])
]

# %%
counter = 0
for lines in [horizontal_lines, vertical_lines, diag_45, diag_135]:
    for line in lines:
        counter += line.count('XMAS')
        counter += line.count('SAMX')

print(counter)
