# %%
import numpy as np

# %%
WORDS: np.array = np.genfromtxt("2024/data/day4.txt", delimiter=1, dtype="<U1")

# %%
# Rotate the Matrix to construct strings of lines horizontally, vertically,
# diagonally and anti-diagonally,
# then search 'XMAX' forth and back.

horizontal_lines = [''.join(line) for line in WORDS]
vertical_lines = [''.join(line) for line in WORDS.T]
diag_45 = [
    ''.join(np.diag(WORDS, k=k))
    for k in range(-(WORDS.shape[0] - 1), WORDS.shape[1])
]

flipped_words = np.fliplr(WORDS)
diag_135 = [
    ''.join(np.diag(flipped_words, k=k))
    for k in range(-(WORDS.shape[0] - 1), WORDS.shape[1])
]

# %%
counter = 0
for lines in [horizontal_lines, vertical_lines, diag_45, diag_135]:
    for line in lines:
        counter += line.count('XMAS')
        counter += line.count('SAMX')

print(counter)

# =============================================================================
# Part 2
# 1. 先找到所有的 A
# 2. 在 A 的四角两条线上的字母，判断是否是 {'M', 'S'}，两线符合即计数

# %%
A_idx = np.argwhere(WORDS == 'A')

# Delete the idxes of the edge.
largest_idx = WORDS.shape[0] - 1
center_mask = np.where(~((A_idx[:, 0] == 0) | (A_idx[:, 0] == largest_idx)
                         | (A_idx[:, 1] == 0)
                         | (A_idx[:, 1] == largest_idx)))
center_A_idx = A_idx[center_mask]


# %%
# Loop through the four directions of the center A.
def check_mas(A_idx: np.array) -> bool:
    # Rows and Columns
    diag = [[A_idx[0] - 1, A_idx[0] + 1], [A_idx[1] - 1, A_idx[1] + 1]]
    anti_diag = [[A_idx[0] - 1, A_idx[0] + 1], [A_idx[1] + 1, A_idx[1] - 1]]

    if set(WORDS[diag[0], diag[1]]) == {'M', 'S'} and set(
            WORDS[anti_diag[0], anti_diag[1]]) == {'M', 'S'}:
        return True
    else:
        return False


counter_part2 = 0
for idx in center_A_idx:
    if check_mas(idx):
        counter_part2 += 1

# %%
print(counter_part2)
