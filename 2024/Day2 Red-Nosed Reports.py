# %%
import numpy as np

# %%
with open('2024/data/day2.txt') as f:
    data_txt = f.read().splitlines()

unusal_data: list = list(
    map(lambda line: list(map(int, line.split())), data_txt))

# %%
is_safe_record = []
for line in unusal_data:
    diff_result = np.diff(line)
    if (all(diff_result > 0) or all(diff_result < 0)) and \
            all(1 <= num <= 3 for num in abs(diff_result)):
        is_safe_record.append(True)
    else:
        is_safe_record.append(False)

# %%
result_1 = sum(is_safe_record)
print(result_1)

# %%
# ================================================================================


def check_if_safe(line: list) -> bool:
    diff_result = np.diff(line)

    if (all(diff_result > 0) or all(diff_result < 0)) and \
            all(1 <= num <= 3 for num in abs(diff_result)):
        return True
    else:
        return False


is_safe_record_2 = []
for line in unusal_data:
    if check_if_safe(line):
        is_safe_record_2.append(True)
        # print(line, 'True with All.')
    else:
        for idx in range(len(line)):
            if check_if_safe(line[:idx] + line[idx + 1:]):
                is_safe_record_2.append(True)
                # print(line, 'True with drop.', line[idx])
                break
        else:
            is_safe_record_2.append(False)
            # print(line, 'False.')

# %%
result_2 = sum(is_safe_record_2)
print(result_2)
