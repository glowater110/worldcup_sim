import os
import sys
import time
from pathlib import Path
from teams import load_data,crawl_data,reconst_data,save_data,find_team
from match import sim_after_draw

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

# N번 실행 시 모든 국가의 성적 분포
n = 10000
ranks = [0 for _ in range(8)]
total_time = 0
team_list = ['Canada','Mexico','USA','Spain','Argentina','France','England','Brazil','Portugal','Netherlands','Belgium','Germany',
             'Croatia','Morocco','Colombia','Uruguay','Switzerland','Japan','Senegal','IR Iran','Korea Republic','Ecuador','Austria','Australia',
             'Norway','Panama','Egypt','Algeria','Scotland','Paraguay','Tunisia','Côte d\'Ivoire','Uzbekistan','Qatar','Saudi Arabia','South Africa',
             'Jordan','Cabo Verde','Ghana','Curaçao','Haiti','New Zealand',
             'Italy','Wales','Bosnia and Herzegovina','Northern Ireland','Ukraine','Poland','Albania','Sweden','Türkiye','Slovakia','Kosovo','Romania','Denmark','Czechia','Republic of Ireland','North Macedonia',
             'Congo DR','New Caledonia','Jamaica','Iraq','Bolivia','Suriname'
]
ranks = [[0 for _ in range(8)] for __ in range(len(team_list))]
for idx,t in enumerate(team_list):
    team_list[idx] = find_team(teams,t)
    
for i in range(n):
    start_time = time.perf_counter()
    res = sim_after_draw(teams,verbose,1)
    end_time = time.perf_counter()
    total_time += end_time-start_time
    sys.stdout.write('\033[F\033[K')
    print(f'Simulation {i+1} : Executed in {end_time-start_time:.1f} seconds')
    rem_time = (n-i-1)*(total_time/(i+1))
    print(f'Estimated Remaining Time : {int(rem_time/3600)} hour {int(rem_time/60)%60} min {rem_time%60:.1f} sec')
    for idx,t in enumerate(team_list):
        try:
            rank = res[0].index(t)+1
            if rank <= 4:
                ranks[idx][rank-1] += 1
            elif rank <= 8:
                ranks[idx][4] += 1
            elif rank <= 16:
                ranks[idx][5] += 1
            elif rank <= 32:
                ranks[idx][6] += 1
            else:
                ranks[idx][7] += 1
        except:
            pass

sys.stdout.write('\033[F\033[K')
print('')
print(f'Total Execute Time : {int(total_time/3600)} hour {int(total_time/60)%60} min {total_time%60:.1f} sec')
print(f'Average Execute Time : {total_time/n:.1f} sec')
print('')
print(f'📊 Rank Statistics ({n} times)')
for idx,t in enumerate(team_list):
    print('')
    print(f'🏳️  {t}')
    print(f'🥇 1st Place : {ranks[idx][0]}')
    print(f'🥈 2nd Place : {ranks[idx][1]}')
    print(f'🥉 3rd Place : {ranks[idx][2]}')
    print(f'🏅 4th Place : {ranks[idx][3]}')
    print(f'✅ Quarterfinal : {ranks[idx][4]}')
    print(f'✅ Round of 16 : {ranks[idx][5]}')
    print(f'✅ Round of 32 : {ranks[idx][6]}')
    print(f'✅ Group Stage : {ranks[idx][7]}')

top_winner = sorted(range(len(team_list)),key=lambda x: ranks[x],reverse=True)
print('')
print(f'📊 Most Possible Winner ({n} times)')
for idx in top_winner:
    print(f'🏳️  {team_list[idx]} : {ranks[idx][0]}')