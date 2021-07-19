from typing import Tuple


def dict_scores(txt: str) -> Tuple[int]:
    nums_tree = [0]
    a_base = 96  # 'a' character code is 97 and ord('a') - a_base = 1
    n_sum = 0
    for ch in txt:
        n_sum += ord(ch) - a_base
        nums_tree.append(n_sum)
    return tuple(nums_tree)


n_in, q_in = map(int, input().split())
song = input()
answer_list = []
song_score = dict_scores(song)
for _ in range(q_in):
    start, end = map(int, input().split())
    answer_list.append(song_score[end] - song_score[start - 1])
print(*answer_list, sep='\n')
