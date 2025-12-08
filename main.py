import os
import sys
import time
from pathlib import Path
from teams import *
from match import *
from draw_real import *

file_name = Path(__file__).parent / 'team_data.pkl'
if os.path.exists(file_name):
    print(f'File data found - Loading data from team_data.pkl...')
    teams = load_data()
else:
    print('File data not found - Want to load from the webpage? (Y/N)')
    ans = ''
    while ans != 'Y' and ans != 'y' and ans != 'N' and ans != 'n':
        ans = input('>> ')
    if ans == 'Y' or ans == 'y':
        print('Loading Data... (may take some time)')
        data = crawl_data()
        teams = reconst_data(data)
        save_data(teams)
        print('✅ Successfully loaded data - saved as team_data.pkl')
    else:
        sys.exit()

# 자세한 내용 펼치기
verbose = True

# # for _ in range(10):
#     ic_path = ic_po_draw(teams,True)
#     for path in ic_path:
#         path.name = 'ICPO ' + path.name

#     # UEFA PO 패스 추첨 시뮬레이션
#     uefa_path = uefa_po_draw(teams,True)
#     for path in uefa_path[0:4]:
#         path.name = 'UEFA ' + path.name

#     # 월드컵 조별예선 추첨 시뮬레이션
#     wc_groups = worldcup_gs_draw(teams,uefa_path,ic_path,True)

# N번 실행 시 한국의 성적 분포
# n = 10000
# ranks = [0 for _ in range(8)]
# total_time = 0
# for _ in range(n):
#     start_time = time.perf_counter()
#     res = sim_after_draw(teams,verbose,1)
#     end_time = time.perf_counter()
#     print(f'Simulation {_+1} : Executed in {end_time-start_time:.1f} seconds')
#     total_time += end_time-start_time
#     # 한국 팀의 결과
#     kor = find_team(teams, 'Korea Republic')
#     rank = res[0].index(kor)+1
#     # if rank <= 4:
#     #     print('')
#     #     print('📊 Korea Republic Games')
#     #     for g in find_all_games(kor,res[1]):
#     #         print(g)
#     print(f'Ranking : {rank}')
#     if rank <= 4:
#         ranks[rank-1] += 1
#     elif rank <= 8:
#         ranks[4] += 1
#     elif rank <= 16:
#         ranks[5] += 1
#     elif rank <= 32:
#         ranks[6] += 1
#     else:
#         ranks[7] += 1

# print('')
# print(f'Total Execute Time : {total_time:.1f}')
# print(f'Average Execute Time : {total_time/n:.1f}')
# print('')
# print(f'📊 Korea Republic Rank Statistics ({n} times)')
# print(f'🥇 1st Place : {ranks[0]}')
# print(f'🥈 2nd Place : {ranks[1]}')
# print(f'🥉 3rd Place : {ranks[2]}')
# print(f'🏅 4th Place : {ranks[3]}')
# print(f'✅ Quarterfinal : {ranks[4]}')
# print(f'✅ Round of 16 : {ranks[5]}')
# print(f'✅ Round of 32 : {ranks[6]}')
# print(f'✅ Group Stage : {ranks[7]}')

# N번 실행 시 조 추첨 상대 결과
# ic_path = ic_po_real(teams)
# uefa_path = uefa_po_real(teams)
# kor = find_team(teams,'Korea Republic')
# # 월드컵 본선 진출국
# qualified = ['Canada',          # Host1
#              'Mexico',          # Host2
#              'USA',             # Host3
#              'Germany',         # UEFA GroupA1
#              'Switzerland',     # UEFA GroupB1
#              'Scotland',        # UEFA GroupC1
#              'France',          # UEFA GroupD1
#              'Spain',           # UEFA GroupE1
#              'Portugal',        # UEFA GroupF1
#              'Netherlands',     # UEFA GroupG1
#              'Austria',         # UEFA GroupH1
#              'Norway',          # UEFA GroupI1
#              'Belgium',         # UEFA GroupJ1
#              'England',         # UEFA GroupK1
#              'Croatia',         # UEFA GroupL1
#              'Argentina',       # CONMEBOL Qual1
#              'Ecuador',         # CONMEBOL Qual2
#              'Colombia',        # CONMEBOL Qual3
#              'Uruguay',         # CONMEBOL Qual4
#              'Brazil',          # CONMEBOL Qual5
#              'Paraguay',        # CONMEBOL Qual6
#              'Egypt',           # CAF GroupA1
#              'Senegal',         # CAF GroupB1
#              'South Africa',    # CAF GroupC1
#              'Cabo Verde',      # CAF GroupD1
#              'Morocco',         # CAF GroupE1
#              'Côte d\'Ivoire',  # CAF GroupF1
#              'Algeria',         # CAF GroupG1
#              'Tunisia',         # CAF GroupH1
#              'Ghana',           # CAF GroupI1
#              'Panama',          # CONCACAF GroupA1
#              'Curaçao',         # CONCACAF GroupB1
#              'Haiti',           # CONCACAF GroupC1
#              'IR Iran',         # AFC GroupA1
#              'Uzbekistan',      # AFC GroupA2
#              'Korea Republic',  # AFC GroupB1
#              'Jordan',          # AFC GroupB2
#              'Japan',           # AFC GroupC1
#              'Australia',       # AFC GroupC2
#              'Qatar',           # AFC POGSA1
#              'Saudi Arabia',    # AFC POGSB1
#              'New Zealand',     # OFC FQWinner
# ]
# sorted = []
# for name in qualified:
#     sorted.append(find_team(teams,name))
# pot1 = []
# for _ in range(3):
#     pot1.append(sorted.pop(0))
# sorted.sort(key=lambda x: x.elo,reverse=True)
# pot1 = pot1 + sorted[0:9]
# pot2 = sorted[9:21]
# pot3 = sorted[21:33]
# pot4 = sorted[33:]
# pot4 += uefa_path[0:4]
# pot4 += ic_path
# qual = pot1+pot2+pot3+pot4
# count = [0 for _ in range(len(qual))]

# n = 1000
# total_time = 0
# for _ in range(n):
#     start_time = time.perf_counter()
#     res = worldcup_gs_draw(teams,uefa_path,ic_path,False)
#     end_time = time.perf_counter()
#     print(f'Simulation {_+1} : Executed in {end_time-start_time:.1f} seconds')
#     total_time += end_time-start_time
#     for g in res:
#         if kor in g.teams:
#             for t in g.teams:
#                 count[qual.index(t)] += 1
#             break

# print('')
# print(f'Total Execute Time : {total_time:.1f}')
# print(f'Average Execute Time : {total_time/n:.1f}')
# print('')
# print(f'📊 Korea Republic Opponent Statistics ({n} times)')
# for idx,t in enumerate(qual):
#     if int(idx/12) == 1:
#         continue
#     if idx % 12 == 0:
#         print(f'Pot {idx/12 + 1:.0f}')
#     print(f'🏳️  {t} - {count[idx]}')
#     if idx % 12 == 11:
#         print('')