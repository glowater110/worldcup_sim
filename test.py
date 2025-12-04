from teams import *
from winprob import *
import networkx as nx
import copy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# # 1. 솔버 생성
# solver = MaxFlow()

# # 2. 간선 및 용량 추가 (노드 이름은 문자열, 숫자 뭐든 가능)
# solver.add_edge('S', 'A', 10)
# solver.add_edge('S', 'B', 10)
# solver.add_edge('A', 'B', 2)
# solver.add_edge('A', 'T', 4)
# solver.add_edge('B', 'T', 8)

# # 3. 해결
# result = solver.solve('S', 'T')

# print(f"최대 유량: {result}") 
# # 예상 정답: 14 
# # (S->A->T: 4, S->B->T: 8, S->A->B->T: 2  => 합계 14)

# g = Group('name',4)

# c1 = Country('name1','aaa',Continent.UEFA,1234)
# c2 = Country('name2','bbb',Continent.CAF,1111)
# g.alloc(c1,0)

# g2 = copy.deepcopy(g)
# g2.alloc(c2,1)

# if g.teams[1].name == 'name2':
#     print('뭔가 잘못되었음')
# else:
#     print('Good')

# items = crawl_data(True)
# for i in items:
#     print(i)

# for i in range(10):
#     if i % 3 == 0:
#         continue
#     elif i == 8:
#         break
#     print(i)

# a = Country('name','abbr',Continent.AFC,1234,12)
# a.name = 'new'
# print(a)

# view_by_group = 2
# view_by_group = True if view_by_group == 1 else False
# print(view_by_group)
    
# b = [5,6,7,8]
# c = [i*j for i,j in zip(a,b)]
# for idx,n in enumerate(c):
#     print(idx,n)

# a = Country('Country A','AAA',Continent.AFC,1000)
# b = Country('Country B','BBB',Continent.AFC,1000)

# for _ in range(100):
#     # print(gen_game_result_aet(a,b))
#     res = sim_game_penalty('Friendly Match',a,b,True)
#     print(res)

# for _ in range(100):
#     print(np.random.randint(0,2))

# score_prob(a,b)
# p = wdl_prob(0,0)
# print('\n\n\n')
# print(f'Win% : {p[0]}')
# print(f'Draw% : {p[1]}')
# print(f'Lose% : {p[2]}')

# win = [6,5,4,3,13,4,5,5,8,3,4,4,3,3,5,6,6,3,5,3,4,1,3,2,1,1,1]
# lose = [1,1,1,1,6,2,3,3,5,2,4,4,3,3,5,6,7,4,8,5,7,2,6,6,4,5,5]
# p = [w/(w+l) for w,l in zip(win,lose)]
# plt.hist(p,histtype='bar')
# plt.title('penalty shootout winning percentage')
# plt.show()

# 제공해주신 텍스트 데이터를 가공한 리스트입니다.
# penalty_stats_data = [
#     {"team": "Argentina", "wins": 12, "losses": 6},
#     {"team": "Brazil", "wins": 8, "losses": 7},
#     {"team": "Uruguay", "wins": 7, "losses": 7},
#     {"team": "Germany", "wins": 6, "losses": 1},
#     {"team": "Nigeria", "wins": 6, "losses": 3},
#     {"team": "South Korea", "wins": 6, "losses": 3},
#     {"team": "United States", "wins": 6, "losses": 3},
#     {"team": "Egypt", "wins": 6, "losses": 4},
#     {"team": "Spain", "wins": 6, "losses": 6},
#     {"team": "Italy", "wins": 6, "losses": 7},
#     {"team": "Panama", "wins": 5, "losses": 2},
#     {"team": "Cameroon", "wins": 5, "losses": 4},
#     {"team": "Colombia", "wins": 5, "losses": 5},
#     {"team": "Mexico", "wins": 5, "losses": 6},
#     {"team": "Ivory Coast", "wins": 5, "losses": 6},
#     {"team": "Saudi Arabia", "wins": 4, "losses": 1},
#     {"team": "Croatia", "wins": 4, "losses": 1},
#     {"team": "Chile", "wins": 4, "losses": 2},
#     {"team": "Portugal", "wins": 4, "losses": 3},
#     {"team": "Paraguay", "wins": 4, "losses": 4},
#     {"team": "France", "wins": 4, "losses": 5},
#     {"team": "Honduras", "wins": 3, "losses": 1},
#     {"team": "Algeria", "wins": 3, "losses": 2},
#     {"team": "Congo-Kinshasa", "wins": 3, "losses": 2},
#     {"team": "Burkina Faso", "wins": 3, "losses": 3},
#     {"team": "Tunisia", "wins": 3, "losses": 3},
#     {"team": "South Africa", "wins": 3, "losses": 3},
#     {"team": "Japan", "wins": 3, "losses": 4},
#     {"team": "Iran", "wins": 3, "losses": 6},
#     {"team": "England", "wins": 3, "losses": 7},
#     {"team": "Czechoslovakia", "wins": 2, "losses": 0},
#     {"team": "Iraq", "wins": 2, "losses": 0},
#     {"team": "Mali", "wins": 2, "losses": 1},
#     {"team": "China", "wins": 2, "losses": 1},
#     {"team": "Denmark", "wins": 2, "losses": 2},
#     {"team": "Peru", "wins": 2, "losses": 2},
#     {"team": "Canada", "wins": 2, "losses": 4},
#     {"team": "Netherlands", "wins": 2, "losses": 6},
#     {"team": "Belgium", "wins": 1, "losses": 0},
#     {"team": "Bulgaria", "wins": 1, "losses": 0},
#     {"team": "Czech Rep.", "wins": 1, "losses": 0},
#     {"team": "Ukraine", "wins": 1, "losses": 0},
#     {"team": "Turkey", "wins": 1, "losses": 0},
#     {"team": "Bahrain", "wins": 1, "losses": 0},
#     {"team": "Vietnam", "wins": 1, "losses": 0},
#     {"team": "Benin", "wins": 1, "losses": 0},
#     {"team": "Madagascar", "wins": 1, "losses": 0},
#     {"team": "Tajikistan", "wins": 1, "losses": 0},
#     {"team": "Qatar", "wins": 1, "losses": 0},
#     {"team": "Guatemala", "wins": 1, "losses": 0},
#     {"team": "Poland", "wins": 1, "losses": 1},
#     {"team": "Rep. Ireland", "wins": 1, "losses": 1},
#     {"team": "Sweden", "wins": 1, "losses": 1},
#     {"team": "Zambia", "wins": 1, "losses": 1},
#     {"team": "Thailand", "wins": 1, "losses": 1},
#     {"team": "Kuwait", "wins": 1, "losses": 1},
#     {"team": "Russia", "wins": 1, "losses": 1},
#     {"team": "Australia", "wins": 1, "losses": 1},
#     {"team": "Equat. Guinea", "wins": 1, "losses": 1},
#     {"team": "Morocco", "wins": 1, "losses": 2},
#     {"team": "United Arab Em.", "wins": 1, "losses": 3},
#     {"team": "Senegal", "wins": 1, "losses": 3},
#     {"team": "Switzerland", "wins": 1, "losses": 4},
#     {"team": "Costa Rica", "wins": 1, "losses": 5},
#     {"team": "Ghana", "wins": 1, "losses": 5},
#     {"team": "Yugoslavia", "wins": 0, "losses": 1},
#     {"team": "Greece", "wins": 0, "losses": 1},
#     {"team": "Libya", "wins": 0, "losses": 1},
#     {"team": "Martinique", "wins": 0, "losses": 1},
#     {"team": "El Salvador", "wins": 0, "losses": 1},
#     {"team": "Cambodia", "wins": 0, "losses": 1},
#     {"team": "Trinidad & Tob.", "wins": 0, "losses": 1},
#     {"team": "Syria", "wins": 0, "losses": 1},
#     {"team": "Cape Verde", "wins": 0, "losses": 1},
#     {"team": "Slovenia", "wins": 0, "losses": 1},
#     {"team": "Jordan", "wins": 0, "losses": 2},
#     {"team": "Venezuela", "wins": 0, "losses": 2},
#     {"team": "Ecuador", "wins": 0, "losses": 2},
#     {"team": "Romania", "wins": 0, "losses": 2},
#     {"team": "Gabon", "wins": 0, "losses": 3},
#     {"team": "Uzbekistan", "wins": 0, "losses": 3}
# ]

# # 1. DataFrame 생성
# df_stats = pd.DataFrame(penalty_stats_data)

# # 2. 총 전적(Total Matches) 및 승률(Win Rate) 계산
# df_stats['total'] = df_stats['wins'] + df_stats['losses']
# df_stats['win_rate'] = df_stats['wins'] / df_stats['total']

# # 3. 승부차기 경험이 많은 순서대로 상위 10개국 출력
# print(df_stats.sort_values(by='total', ascending=False).head(10))

a_win = 0
b_win = 0
win_table = [[0 for _ in range(21)] for __ in range(21)]

for _ in range(1000000):
    res = shootout()
    if res[0] > res[1]:
        a_win += 1
    else:
        b_win += 1
    if res[0] <= 20 and res[1] <= 20:
        if res[0] > res[1]:
            win_table[res[0]][res[1]] += 1
        else:
            win_table[res[1]][res[0]] += 1

win_table = [[x / 1000000 for x in row] for row in win_table]
for idx_r,row in enumerate(win_table):
    for idx_c,col in enumerate(row):
        if idx_r <= idx_c:
            break
        print(f'{col:.3f}',end='\t')
    print('')
print('\n')
print(a_win,b_win)

# for _ in range(10):
#     shootout(True)

# from collections import defaultdict

# scores = [10, 30, 20, 30, 10, 30]

# # 1. 같은 값끼리 인덱스 모으기
# idx_dict = defaultdict(list)
# for idx, score in enumerate(scores):
#     idx_dict[score].append(idx)

# # idx_dict 상태: {10: [0, 4], 30: [1, 3, 5], 20: [2]}

# # 2. 점수가 높은 순서대로 그룹 정렬 (내림차순)
# # items()를 가져와서 key(점수)를 기준으로 정렬
# sorted_groups = sorted(idx_dict.items(), key=lambda x: x[0], reverse=True)

# # 3. 결과 확인
# for score, indices in sorted_groups:
#     print(f"점수: {score}, 인덱스 그룹: {indices}")

# # 최종 결과 리스트만 필요하다면:
# final_indices = [indices for score, indices in sorted_groups]
# print(final_indices) 
# # 출력: [[1, 3, 5], [2], [0, 4]] -> (30점들, 20점들, 10점들 순)

# a = 2
# b = 2
# match [a,b]:
#     case [1,2]:
#         print('?')
#     case [2,2]:
#         print('!')

# a = 10
# b = 20
# c = 20

# l = [a,b,c]
# [na,nb,nc] = sorted(range(len(l)),key=lambda x:l[x],reverse=True)
# print(na,nb,nc)

# data = [
#     [0, 1, 2, 3], # Index 0
#     [1, 4, 3, 1], # Index 1
#     [0, 0, 3, 1], # Index 2
#     [0, 1, 1, 4], # Index 3
#     [1, 1, 1, 10]  # Index 4
# ]

# # We sort the indices (0, 1, 2, 3, 4)
# # key=lambda i: data[i] tells Python: "Don't sort the numbers 0-4, 
# # sort based on the row located at that index."
# sorted_indices = sorted(range(len(data)), key=lambda i: data[i], reverse=True)

# print(sorted_indices)
# # Output: [1, 2, 0, 3, 4]

# a = 'A'
# print(a[-1])

# a = list(range(10))
# print(a.index(8))

