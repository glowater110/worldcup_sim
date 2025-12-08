import os
import sys
import time
from pathlib import Path
from teams import load_data,crawl_data,reconst_data,save_data
from match import sim_after_draw,find_all_games

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

repeat = True
while repeat:
    # 대륙 PO 패스 추첨 시뮬레이션
    res = sim_after_draw(teams,verbose,1)
    
    # 최종 결과 정리
    print('')
    print('📊 Final Ranking')
    print(' Rank  Team  W  D  L  GF  GA   GD   Pt')
    print('---------------------------------------')
    for idx,t in enumerate(res[0]):
        w = 0
        d = 0
        l = 0
        gf = 0
        ga = 0
        gd = 0
        pt = 0
        games = find_all_games(t,res[1])
        for g in games:
            if t.name == g.home.name:
                gf += g.score_home
                ga += g.score_away
                gd += g.score_home - g.score_away
                if g.score_home > g.score_away:
                    w += 1
                    pt += 3
                elif g.score_home == g.score_away:
                    d += 1
                    pt += 1
                else:
                    l += 1
            if t.name == g.away.name:
                gf += g.score_away
                ga += g.score_home
                gd += g.score_away - g.score_home
                if g.score_home < g.score_away:
                    w += 1
                    pt += 3
                elif g.score_home == g.score_away:
                    d += 1
                    pt += 1
                else:
                    l += 1
        print(f'   {idx+1:2d}   {t.abbr}  {w}  {d}  {l}  {gf:2d}  {ga:2d}  {gd:3d}   {pt:2d}')
    print('')    

    print('Restart? (Y/N)')
    ans = ''
    while ans != 'Y' and ans != 'y' and ans != 'N' and ans != 'n':
        ans = input('>> ')
    if ans == 'N' or ans == 'n':
        repeat = False