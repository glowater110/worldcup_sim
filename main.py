import os
import sys
from pathlib import Path
from teams import *
from match import *

# 자세한 내용 펼치기
verbose = False

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

# 반복 시행 코드
# repeat = True
# while repeat:
#     # 대륙 PO 패스 추첨 시뮬레이션
#     res = complete_sim(teams,verbose,1)
    
#     # 최종 결과 정리
#     print('')
#     print('📊 Final Ranking')
#     print(' Rank  Team  W  D  L  GF  GA   GD   Pt')
#     print('---------------------------------------')
#     for idx,t in enumerate(res[0]):
#         w = 0
#         d = 0
#         l = 0
#         gf = 0
#         ga = 0
#         gd = 0
#         pt = 0
#         games = find_all_games(t,res[1])
#         for g in games:
#             if t.name == g.home.name:
#                 gf += g.score_home
#                 ga += g.score_away
#                 gd += g.score_home - g.score_away
#                 if g.score_home > g.score_away:
#                     w += 1
#                     pt += 3
#                 elif g.score_home == g.score_away:
#                     d += 1
#                     pt += 1
#                 else:
#                     l += 1
#             if t.name == g.away.name:
#                 gf += g.score_away
#                 ga += g.score_home
#                 gd += g.score_away - g.score_home
#                 if g.score_home < g.score_away:
#                     w += 1
#                     pt += 3
#                 elif g.score_home == g.score_away:
#                     d += 1
#                     pt += 1
#                 else:
#                     l += 1
#         print(f'   {idx+1:2d}   {t.abbr}  {w}  {d}  {l}  {gf:2d}  {ga:2d}  {gd:3d}   {pt:2d}')
#     print('')    

#     print('Restart? (Y/N)')
#     ans = ''
#     while ans != 'Y' and ans != 'y' and ans != 'N' and ans != 'n':
#         ans = input('>> ')
#     if ans == 'N' or ans == 'n':
#         repeat = False

# N번 실행 시 한국의 성적 분포
n = 1000
ranks = [0 for _ in range(8)]
for _ in range(n):
    # 대륙 PO 패스 추첨 시뮬레이션
    res = complete_sim(teams,verbose,1)
    
    # 한국 팀의 결과
    kor = find_team(teams, 'Korea Republic')
    print('')
    print('📊 Korea Republic Games')
    for g in find_all_games(kor,res[1]):
        print(g)
    rank = res[0].index(kor)+1
    print(f'Ranking : {rank}')
    if rank <= 4:
        ranks[rank-1] += 1
    elif rank <= 8:
        ranks[4] += 1
    elif rank <= 16:
        ranks[5] += 1
    elif rank <= 32:
        ranks[6] += 1
    else:
        ranks[7] += 1

print('')
print(f'📊 Korea Republic Rank Statistics ({n} times)')
print(f'🥇 1st Place : {ranks[0]}')
print(f'🥈 2nd Place : {ranks[1]}')
print(f'🥉 3rd Place : {ranks[2]}')
print(f'🏅 4th Place : {ranks[3]}')
print(f'✅ Quarterfinal : {ranks[4]}')
print(f'✅ Round of 16 : {ranks[5]}')
print(f'✅ Round of 32 : {ranks[6]}')
print(f'✅ Group Stage : {ranks[7]}')