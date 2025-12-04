import copy
import networkx as nx
import numpy as np
from pulp import LpProblem,LpMaximize,LpVariable,lpSum,PULP_CBC_CMD,LpStatus
from classdef import Continent,Country,Group
from teams import find_team

def ic_po_draw(teams:list[Country], verbose=False):
    """대륙 PO 조 추첨 시뮬레이션"""
    if verbose:
        print('==================================================')
        print('🔀 Simulating IC Playoff Draw...')
        print('')
    
    # 대륙 PO 진출국
    qualified = ['Bolivia',         # CONMEBOL Qual7
                 'Congo DR',        # CAF POWinner
                 'Jamaica',         # CONCACAF FQ1
                 'Suriname',        # CONCACAF FQ2
                 'Iraq',            # AFC POKSWinner
                 'New Caledonia'    # OFC FQRunnerUp
    ]
    unseeded = []
    for name in qualified:
        unseeded.append(find_team(teams,name))

    # FIFA Ranking 1,2위는 각 Path1,2 결승 직행
    unseeded.sort(key=lambda x: x.elo,reverse=True)
    path1 = Group('Pathway 1',3)
    path2 = Group('Pathway 2',3)
    path1.alloc(unseeded.pop(0),0)
    if verbose:
        print(f'🏳️  {path1.teams[0]} -> {path1.name} (by FIFA Ranking)')
    path2.alloc(unseeded.pop(0),0)
    if verbose:
        print(f'🏳️  {path2.teams[0]} -> {path2.name} (by FIFA Ranking)')
    
    def multicommflow(teams:list[Country], groups:list[Group]):
        """정수 다품종 유량 계산으로 데드락 감지"""
        prob = LpProblem("Check_Deadlock",LpMaximize)
        choices = LpVariable.dicts("Choice",((t.name, g.name) for t in teams for g in groups),cat='Binary')
        for t in teams:
            prob += lpSum([choices[t.name, g.name] for g in groups]) == 1
        for g in groups:
            prob += lpSum([choices[t.name, g.name] for t in teams]) == len(g.remaining_seats())
        for g in groups:
            for continent in Continent:
                continent_teams = [t for t in teams if type(t) == Country and t.cont == continent]
                quota = g.cont_limit()[continent.value]
                prob += lpSum([choices[t.name, g.name] for t in continent_teams]) <= quota
        prob.solve(PULP_CBC_CMD(msg=False))
        return LpStatus[prob.status] == 'Optimal'
        
    def maxflow(teams:list[Country], groups:list[Group]):
        """최대유량 계산으로 데드락 감지"""
        G = nx.DiGraph()
        for t in teams:
            G.add_edge('Source',f'{t.abbr}',capacity=1)
            for g in groups:
                if g.is_valid(t):
                    G.add_edge(f'{t.abbr}',g.name,capacity=1)
        for g in groups:
            G.add_edge(g.name,'Sink',capacity=len(g.remaining_seats()))
        if nx.maximum_flow(G,'Source','Sink')[0] == len(teams):
            return True
        else:
            return False
    
    while len(unseeded) > 0:
        team = unseeded.pop(np.random.randint(0,len(unseeded)))
        # 자리 순서대로 문제가 생기는지 검사, 없으면 그 자리에 할당
        # 규칙에 따라 우선 Path 1에 배정 시도
        to_path1 = True
        if len(path1.remaining_seats()) > 0:
            # Path 1에 자리가 있음
            if path1.is_valid(team) == False:
                # 근데 스스로 대륙제한 걸림 => Path 2 배정
                to_path1 = False
            else:
                p1 = copy.deepcopy(path1)
                p2 = copy.deepcopy(path2)
                # path1에 임시로 배치하고 데드락 발생 확인
                p1.alloc(team,p1.remaining_seats()[0])
                if multicommflow(unseeded,[p1,p2]) == False:
                    to_path1 = False
        else:
            to_path1 = False
        if to_path1:
            # Path 1에 배정
            path1.alloc(team,path1.remaining_seats()[0])
            if verbose:
                print(f'🏳️  {team} -> {path1.name}')
        else:
            # Path 2에 배정
            path2.alloc(team,path2.remaining_seats()[0])
            if verbose:
                print(f'🏳️  {team} -> {path2.name}')
    
    if verbose:
        print('')
        print(f'✅ {path1.name} - {" ".join(str(team) for team in path1.teams)}')
        print(f'✅ {path2.name} - {" ".join(str(team) for team in path2.teams)}')
    
    return [path1,path2]

def uefa_po_draw(teams:list[Country], verbose=False):
    """UEFA PO 패스 추첨 시뮬레이션"""
    if verbose:
        print('==================================================')
        print('🔀 Simulating UEFA Playoff Draw...')
    # UEFA PO 진출국
    qualified = ['Slovakia',                # GroupA2
                 'Kosovo',                  # GroupB2
                 'Denmark',                 # GroupC2
                 'Ukraine',                 # GroupD2
                 'Türkiye',                 # GroupE2
                 'Republic of Ireland',     # GroupF2
                 'Poland',                  # GroupG2
                 'Bosnia and Herzegovina',  # GroupH2
                 'Italy',                   # GroupI2
                 'Wales',                   # GroupJ2
                 'Albania',                 # GroupK2
                 'Czechia',                 # GroupL2
                 'Romania',                 # UNL1
                 'Sweden',                  # UNL2
                 'North Macedonia',         # UNL3
                 'Northern Ireland'         # UNL4
    ]
    g2 = []     # Qualified by GS
    pot4 = []   # Qualified by UNL (Assigned in Pot 4)
    for name in qualified:
        if len(g2) < 12:
            g2.append(find_team(teams,name))
        else:
            pot4.append(find_team(teams,name))
    
    # GS Runner-up : FIFA 랭킹 순으로 1~3포트 정렬
    g2.sort(key=lambda x: x.elo,reverse=True)
    pot1 = g2[0:4]
    pot2 = g2[4:8]
    pot3 = g2[8:12]
    
    # Draw
    path_a = Group('Path A',4)
    path_b = Group('Path B',4)
    path_c = Group('Path C',4)
    path_d = Group('Path D',4)
    
    def draw_group(pot:list[Country], groups:list[Group], verbose=False):
        """조 추첨 로직 (UEFA PO)"""
        group_idxs = list(range(len(groups)))
        while len(group_idxs) > 0:
            team = pot.pop(np.random.randint(0,len(pot)))
            sel = group_idxs.pop(0)
            pos = groups[sel].remaining_seats()[0]
            if verbose:
                print(f'🏳️  {team} -> {groups[sel].name}')
            groups[sel].alloc(team,pos)

    if verbose:
        print('')
        print('Drawing Pot 1...')
    draw_group(pot1,[path_a,path_b,path_c,path_d],verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 2...')
    draw_group(pot2,[path_a,path_b,path_c,path_d],verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 3...')
    draw_group(pot3,[path_a,path_b,path_c,path_d],verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 4...')
    draw_group(pot4,[path_a,path_b,path_c,path_d],verbose)
    
    if verbose:
        print('')
        print(f'✅ Path A - {" ".join(str(team) for team in path_a.teams)}')
        print(f'✅ Path B - {" ".join(str(team) for team in path_b.teams)}')
        print(f'✅ Path C - {" ".join(str(team) for team in path_c.teams)}')
        print(f'✅ Path D - {" ".join(str(team) for team in path_d.teams)}')
    
    # 결승전 홈팀 추첨 : True(1,4포트)/False(2,3포트)
    home_a = np.random.choice([True,False])
    home_b = np.random.choice([True,False])
    home_c = np.random.choice([True,False])
    home_d = np.random.choice([True,False])
    return path_a,path_b,path_c,path_d,home_a,home_b,home_c,home_d

def worldcup_gs_draw(teams:list[Country], uefa_po, ic_po, verbose=False):
    """월드컵 조 추첨 시뮬레이션"""
    if verbose:
        print('==================================================')
        print('🔀 Simulating World Cup Group Stage Draw...')
    # 월드컵 본선 진출국
    qualified = ['Canada',          # Host1
                 'Mexico',          # Host2
                 'USA',             # Host3
                 'Germany',         # UEFA GroupA1
                 'Switzerland',     # UEFA GroupB1
                 'Scotland',        # UEFA GroupC1
                 'France',          # UEFA GroupD1
                 'Spain',           # UEFA GroupE1
                 'Portugal',        # UEFA GroupF1
                 'Netherlands',     # UEFA GroupG1
                 'Austria',         # UEFA GroupH1
                 'Norway',          # UEFA GroupI1
                 'Belgium',         # UEFA GroupJ1
                 'England',         # UEFA GroupK1
                 'Croatia',         # UEFA GroupL1
                 'Argentina',       # CONMEBOL Qual1
                 'Ecuador',         # CONMEBOL Qual2
                 'Colombia',        # CONMEBOL Qual3
                 'Uruguay',         # CONMEBOL Qual4
                 'Brazil',          # CONMEBOL Qual5
                 'Paraguay',        # CONMEBOL Qual6
                 'Egypt',           # CAF GroupA1
                 'Senegal',         # CAF GroupB1
                 'South Africa',    # CAF GroupC1
                 'Cabo Verde',      # CAF GroupD1
                 'Morocco',         # CAF GroupE1
                 'Côte d\'Ivoire',  # CAF GroupF1
                 'Algeria',         # CAF GroupG1
                 'Tunisia',         # CAF GroupH1
                 'Ghana',           # CAF GroupI1
                 'Panama',          # CONCACAF GroupA1
                 'Curaçao',         # CONCACAF GroupB1
                 'Haiti',           # CONCACAF GroupC1
                 'IR Iran',         # AFC GroupA1
                 'Uzbekistan',      # AFC GroupA2
                 'Korea Republic',  # AFC GroupB1
                 'Jordan',          # AFC GroupB2
                 'Japan',           # AFC GroupC1
                 'Australia',       # AFC GroupC2
                 'Qatar',           # AFC POGSA1
                 'Saudi Arabia',    # AFC POGSB1
                 'New Zealand',     # OFC FQWinner
    ]
    sorted = []
    for name in qualified:
        sorted.append(find_team(teams,name))
    
    # 개최국은 1포트 자동배정
    pot1 = []
    for _ in range(3):
        pot1.append(sorted.pop(0))
    
    # 나머지는 랭킹 순서대로 1~4포트 배정
    sorted.sort(key=lambda x: x.elo,reverse=True)
    pot1 = pot1 + sorted[0:9]
    pot2 = sorted[9:21]
    pot3 = sorted[21:33]
    pot4 = sorted[33:]
    # UEFA PO, 대륙 PO는 4포트에 배정
    pot4 += uefa_po[0:4]
    pot4 += ic_po
    
    # Draw
    groups:list[Group] = []
    groups.append(Group('Group A',4))
    groups.append(Group('Group B',4))
    groups.append(Group('Group C',4))
    groups.append(Group('Group D',4))
    groups.append(Group('Group E',4))
    groups.append(Group('Group F',4))
    groups.append(Group('Group G',4))
    groups.append(Group('Group H',4))
    groups.append(Group('Group I',4))
    groups.append(Group('Group J',4))
    groups.append(Group('Group K',4))
    groups.append(Group('Group L',4))
    
    def draw_group_pot1(pot:list[Country | Group], groups:list[Group], verbose=False):
        """조 추첨 로직 (WC GS), 1포트 전용"""
        # 멕시코 -> A1 | 캐나다 -> B1 | 미국 -> D1
        can = pot.pop(0)    # 캐나다
        mex = pot.pop(0)    # 멕시코
        usa = pot.pop(0)    # 미국
        if verbose:
            print(f'🏳️  {mex} -> {groups[0].name}, Position 1 (Host)')
            print(f'🏳️  {can} -> {groups[1].name}, Position 1 (Host)')
            print(f'🏳️  {usa} -> {groups[3].name}, Position 1 (Host)')
        groups[0].alloc(mex,0)
        groups[1].alloc(can,0)
        groups[3].alloc(usa,0)
        
        def sel_group(team:Country, groups:list[Group]):
            """랭킹 1~4위 팀이 조건에 맞게 배치되도록 조를 선정"""
            # Pot 1 제한조건
            # 1~4위는 (조 1위 통과 시) 준결승 전까지 만나지 않는 조에 편성되어야 함
            # 그 중 1위와 2위는 (조 1위 통과 시) 결승 전까지 만나지 않는 조에 편성되어야 함
            # D,G,H / E,F,I : 준결승1(M101)
            # A,C,L / B,J,K : 준결승2(M102)
            acl = [0,2,11]
            bjk = [1,9,10]
            dgh = [3,6,7]
            efi = [4,5,8]
            # 랭킹 1~4위 팀의 조번호
            r1 = None
            r2 = None
            r3 = None
            r4 = None
            possible_idx = []
            
            for idx,g in enumerate(groups):
                if g.teams[0].rank != None:
                    # 어느 팀이 조에 들어가있음
                    if g.teams[0].rank <= 4:
                        match g.teams[0].rank:
                            case 1:
                                r1 = idx
                            case 2:
                                r2 = idx
                            case 3:
                                r3 = idx
                            case 4:
                                r4 = idx
                else:
                    # 일단은 조가 비어있음
                    possible_idx.append(idx)
            
            def remove_idx1(list):
                """list에 있는 값을 possible_idx에서 제거"""
                for l in list:
                    if l in possible_idx:
                        possible_idx.remove(l)
            
            def remove_idx2(target):
                """target이 소속된 조 번호 제거"""
                if target in acl:
                    remove_idx1(acl)
                if target in bjk:
                    remove_idx1(bjk)
                if target in dgh:
                    remove_idx1(dgh)
                if target in efi:
                    remove_idx1(efi)
                    
            def check_reserved(target):
                """target에 1~4위 자리가 남아있는지 보장할 것"""
                rem = 3
                for i in target:
                    team:Country = groups[i].teams[0]
                    if team.rank != None:
                        if team.rank <= 4:
                            # 4위 이내 팀이 이미 배정되어 있으므로 노상관
                            return
                        # 아니면 그냥 자리만 까먹음
                        rem -= 1
                if rem == 1:
                    # 여기까지 왔으면 4위 이내 팀은 target에 없음
                    # 그런데 남는 자리가 1개면 그 자리는 4위 이내 팀이어야 함
                    remove_idx1(target)
            
            if team.rank <= 4:
                if team.rank <= 2:
                    # 할당할 국가가 1~2위
                    if r1 in acl+bjk or r2 in acl+bjk:
                        remove_idx1(acl+bjk)
                    if r1 in dgh+efi or r2 in dgh+efi:
                        remove_idx1(dgh+efi)
                    remove_idx2(r3)
                    remove_idx2(r4)
                else:
                    # 할당할 국가가 3~4위
                    remove_idx2(r1)
                    remove_idx2(r2)
                    if r3 in acl+bjk or r4 in acl+bjk:
                        remove_idx1(acl+bjk)
                    if r3 in dgh+efi or r4 in dgh+efi:
                        remove_idx1(dgh+efi)
            else:
                # 할당할 국가가 4위 바깥: acl,bjk,dgh,efi에 1~4위 자리를 마련할 것
                check_reserved(acl)
                check_reserved(bjk)
                check_reserved(dgh)
                check_reserved(efi)
            
            # 이제 possible_idx 계산이 마무리되었으니 가능한 첫 조에 배정
            match team.rank:
                case 1:
                    r1 = possible_idx[0]
                case 2:
                    r2 = possible_idx[0]
                case 3:
                    r3 = possible_idx[0]
                case 4:
                    r4 = possible_idx[0]
            return possible_idx[0]
        
        while len(pot) > 0:
            team = pot.pop(np.random.randint(0,len(pot)))
            # 어느 조에 배정할지 결정
            sel = sel_group(team,groups)
            pos = groups[sel].remaining_seats()[0]
            if verbose:
                print(f'🏳️  {team} -> {groups[sel].name}, Position {pos+1}')
            groups[sel].alloc(team,pos)
    
    def draw_group(pot2:list[Country], pot3:list[Country], pot4:list[Country | Group], groups:list[Group], verbose=False):
        """조 추첨 로직 (WC GS), 2/3/4포트용"""
        def multicommflow(pot2:list[Country], pot3:list[Country], pot4:list[Country | Group], groups:list[Group]):
            """정수 다품종 유량 계산으로 데드락 감지"""
            prob = LpProblem("Check_Deadlock",LpMaximize)
            teams = pot2+pot3+pot4
            choices = LpVariable.dicts("Choice",((t.name, g.name) for t in teams for g in groups),cat='Binary')
            for t in teams:
                prob += lpSum([choices[t.name, g.name] for g in groups]) == 1
            for g in groups:
                for pot in [pot2, pot3, pot4]:
                    if len(pot) == 0:
                        continue
                    pot_teams = [t for t in teams if t in pot]
                    limit = 1
                    if len(pot2) != 0:
                        # Pot 2 배치 중 -> pot3,4는 1씩 배치
                        if pot == pot2 and len(g.remaining_seats()) == 2:
                            # Pot 2 남은 자리 2개면 이미 참
                            limit = 0
                    elif len(pot3) != 0:
                        # Pot 3 배치 중 -> pot4는 1씩 배치
                        if pot == pot3 and len(g.remaining_seats()) == 1:
                            limit = 0
                    elif len(pot4) != 0:
                        # Pot 4 배치 중
                        if pot == pot4 and len(g.remaining_seats()) == 0:
                            limit = 0
                    prob += lpSum([choices[t.name, g.name] for t in pot_teams]) == limit
            for g in groups:
                for continent in Continent:
                    continent_teams = [t for t in teams if type(t) == Country and t.cont == continent]
                    continent_teams += [t for t in teams if type(t) == Group and t.cont_count()[continent.value] == 1]
                    quota = g.cont_limit()[continent.value]
                    prob += lpSum([choices[t.name, g.name] for t in continent_teams]) <= quota
                    if g.cont_count2()[Continent.UEFA.value] == 0 and continent == Continent.UEFA:
                        prob += lpSum([choices[t.name, g.name] for t in continent_teams]) >= 1
            prob.solve(PULP_CBC_CMD(msg=False))
            return LpStatus[prob.status] == 'Optimal'
            
        # pot2부터 pot4 순서대로 진행
        exp_rem = 0
        if len(pot2) > 0:
            pot = pot2
            exp_rem = 3
        elif len(pot3) > 0:
            pot = pot3
            exp_rem = 2
        else:
            pot = pot4
            exp_rem = 1
        
        two_uefa = 4
        for g in groups:
            if g.cont_count2()[Continent.UEFA.value] == 2:
                two_uefa -= 1
        
        while len(pot) > 0:
            team = pot.pop(np.random.randint(0,len(pot)))
            for idx,g in enumerate(groups):
                if g.is_valid(team) == False:
                    # 같은 대륙이 이미 한계만큼 존재
                    continue
                else:
                    # 이미 배정된 조인 경우
                    if len(g.remaining_seats()) != exp_rem:
                        continue
                    # UEFA 1팀 의무배치 확인용
                    if two_uefa == 0:
                        if type(team) == Country:
                            if team.cont == Continent.UEFA:
                                if g.cont_count2()[Continent.UEFA.value] == 1:
                                    continue
                            else:
                                if g.cont_count2()[Continent.UEFA.value] == 0:
                                    continue
                        elif type(team) == Group:
                            if team.cont_count()[Continent.UEFA.value] != 0:
                                if g.cont_count2()[Continent.UEFA.value] == 1:
                                    continue
                            else:
                                if g.cont_count2()[Continent.UEFA.value] == 0:
                                    continue
                    # 롤백 위한 복사본 준비
                    g_cpy = copy.deepcopy(groups)
                    g_cpy[idx].alloc(team,g_cpy[idx].remaining_seats()[0])
                    if multicommflow(pot2,pot3,pot4,g_cpy) == True:
                        # 배치에 문제 없음
                        pos = (idx+exp_rem+1)%3+1
                        if verbose:
                            print(f'🏳️  {team} -> {groups[idx].name}, Position {pos+1}')
                        groups[idx].alloc(team,pos)
                        break
    
    if verbose:
        print('')
        print('Drawing Pot 1...')
    draw_group_pot1(pot1,groups,verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 2...')
    draw_group(pot2,pot3,pot4,groups,verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 3...')
    draw_group(pot2,pot3,pot4,groups,verbose)
    
    if verbose:
        print('')
        print('Drawing Pot 4...')
    draw_group(pot2,pot3,pot4,groups,verbose)
    
    if verbose:
        print('')
        for group in groups:
            print(f'✅ {group.name} - {" ".join(str(team) for team in group.teams)}')
    
    return groups