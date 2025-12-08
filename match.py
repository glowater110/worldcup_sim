from classdef import Country,Group,Game
from winprob import sim_game_penalty,sim_game
from round_of_32 import ROUND_OF_32_COMBINATIONS
from draw import ic_po_draw,uefa_po_draw,worldcup_gs_draw
from draw_real import ic_po_real,uefa_po_real,worldcup_gs_real

def sim_po(ic_path:list[Group], uefa_path:list[Group], verbose=False):
    """플레이오프 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (IC - UEFA 순서 / 패스번호 순서)
    # 2026-3-26 : Matchday 1
    # 2026-3-31 : Matchday 2 (Finals)
    
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Playoff...')
    
    if verbose:
        print('')
        print('📅 March 26, 2026')
    
    icposf_winner = [None,None]
    uefasf_winner = [None,None,None,None,None,None,None,None]
    
    for idx,ic in enumerate(ic_path):
        res = sim_game_penalty(ic.name,ic.teams[1],ic.teams[2],verbose)
        if len(res) != 5:
            # 승부차기 없이 종료
            if res[0] > res[1]:
                icposf_winner[idx] = ic.teams[1]
            else:
                icposf_winner[idx] = ic.teams[2]
        elif len(res) == 5:
            # 승부차기로 종료
            if res[3] > res[4]:
                icposf_winner[idx] = ic.teams[1]
            else:
                icposf_winner[idx] = ic.teams[2]
        
    for idx,uefa in enumerate(uefa_path[0:4]):
        res = sim_game_penalty(uefa.name,uefa.teams[0],uefa.teams[3],verbose)
        if len(res) != 5:
            # 승부차기 없이 종료
            if res[0] > res[1]:
                uefasf_winner[2*idx] = uefa.teams[0]
            else:
                uefasf_winner[2*idx] = uefa.teams[3]
        elif len(res) == 5:
            # 승부차기로 종료
            if res[3] > res[4]:
                uefasf_winner[2*idx] = uefa.teams[0]
            else:
                uefasf_winner[2*idx] = uefa.teams[3]
        res = sim_game_penalty(uefa.name,uefa.teams[1],uefa.teams[2],verbose)
        if len(res) != 5:
            # 승부차기 없이 종료
            if res[0] > res[1]:
                uefasf_winner[2*idx+1] = uefa.teams[1]
            else:
                uefasf_winner[2*idx+1] = uefa.teams[2]
        elif len(res) == 5:
            # 승부차기로 종료
            if res[3] > res[4]:
                uefasf_winner[2*idx+1] = uefa.teams[1]
            else:
                uefasf_winner[2*idx+1] = uefa.teams[2]
    
    if verbose:
        print('')
        print('📅 March 31, 2026')
    
    icpo_winner = [None,None]
    uefa_winner = [None,None,None,None]
    
    for idx,ic in enumerate(ic_path):
        res = sim_game_penalty(ic.name,ic.teams[0],icposf_winner[idx],verbose)
        if len(res) != 5:
            # 승부차기 없이 종료
            if res[0] > res[1]:
                icpo_winner[idx] = ic.teams[0]
            else:
                icpo_winner[idx] = icposf_winner[idx]
        elif len(res) == 5:
            # 승부차기로 종료
            if res[3] > res[4]:
                icpo_winner[idx] = ic.teams[0]
            else:
                icpo_winner[idx] = icposf_winner[idx]
    
    for idx,uefa in enumerate(uefa_path[0:4]):
        if uefa_path[4+idx]:
            # 1/4포트가 홈
            hometeam = uefasf_winner[2*idx]
            awayteam = uefasf_winner[2*idx+1]
        else:
            # 2/3포트가 홈
            hometeam = uefasf_winner[2*idx+1]
            awayteam = uefasf_winner[2*idx]
        res = sim_game_penalty(uefa.name,hometeam,awayteam,verbose)
        if len(res) != 5:
            # 승부차기 없이 종료
            if res[0] > res[1]:
                uefa_winner[idx] = hometeam
            else:
                uefa_winner[idx] = awayteam
        elif len(res) == 5:
            # 승부차기로 종료
            if res[3] > res[4]:
                uefa_winner[idx] = hometeam
            else:
                uefa_winner[idx] = awayteam
    
    if verbose:
        print('')
        print('📊 Results')
        for idx,ic in enumerate(ic_path):
            print(f'🏆 {ic.name} Qualified : {icpo_winner[idx]}')
        for idx,uefa in enumerate(uefa_path[0:4]):
            print(f'🏆 {uefa.name} Qualified : {uefa_winner[idx]}')
    
    return icpo_winner + uefa_winner

def sim_worldcup_gs(groups:list[Group], verbose=False, view_by_group=0):
    """월드컵 조별예선 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (조회 순서 선택 가능: 1. Match 번호 순서 | 2. 그룹 순서)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Playoff...')
        if view_by_group != 1 and view_by_group != 2:
            print('⚠️ Select the order of view')
            print('[1] By Group Order')
            print('[2] By Date Order')
        while view_by_group != 1 and view_by_group != 2:
            ans = input('>> ')
            try:
                view_by_group = int(ans)
            except:
                pass
        view_by_group = True if view_by_group == 1 else False
    
    # 조별리그 성적 저장 테이블 (res_table[group][pos][승무패득실])
    res_table = [[[0,0,0,0,0] for _ in range(len(g.teams))] for g in groups]
    # 조별리그 경기 결과 저장 테이블 (순서는 1vs2, 3vs4, 4vs2, 1vs3, 4vs1, 2vs3)
    match_record = [[] for _ in range(len(groups))]
    games = []
    
    def save_result(group_idx,home,away):
        """경기 결과를 시뮬레이션 후 저장"""
        res = sim_game(groups[group_idx].name,groups[group_idx].teams[home],groups[group_idx].teams[away],verbose)
        games.append(Game(groups[group_idx].name,groups[group_idx].teams[home],groups[group_idx].teams[away],res[0],res[1]))
        res_table[group_idx][home][3] += res[0]
        res_table[group_idx][home][4] += res[1]
        res_table[group_idx][away][3] += res[1]
        res_table[group_idx][away][4] += res[0]
        if res[0] > res[1]:
            res_table[group_idx][home][0] += 1
            res_table[group_idx][away][2] += 1
        elif res[0] < res[1]:
            res_table[group_idx][home][2] += 1
            res_table[group_idx][away][0] += 1
        elif res[0] == res[1]:
            res_table[group_idx][home][1] += 1
            res_table[group_idx][away][1] += 1
        match_record[group_idx].append(res)
    
    if view_by_group:
        if verbose:
            print('')
            print('📅 Matchday 1 (June 11-17, 2026)')
        for idx,g in enumerate(groups):
            # P1 vs P2
            save_result(idx,0,1)
            # P3 vs P4
            save_result(idx,2,3)
    else:
        # 2026-6-11 : M1(A1vsA2),M2(A3vsA4)
        if verbose:
            print('')
            print('📅 June 11, 2026')
        save_result(0,0,1)  # M1(A1vsA2)
        save_result(0,2,3)  # M2(A3vsA4)
        
        # 2026-6-12 : M3(B1vsB2),M4(D1vsD2)
        if verbose:
            print('')
            print('📅 June 12, 2026')
        save_result(1,0,1)  # M3(B1vsB2)
        save_result(3,0,1)  # M4(D1vsD2)
        
        # 2026-6-13 : M5(C3vsC4),M6(D3vsD4),M7(C1vsC2),M8(B3vsB4)
        if verbose:
            print('')
            print('📅 June 13, 2026')
        save_result(1,2,3)  # M8(B3vsB4)
        save_result(2,0,1)  # M7(C1vsC2)
        save_result(2,2,3)  # M5(C3vsC4)
        save_result(3,2,3)  # M6(D3vsD4)

        # 2026-6-14 : M9(E3vsE4),M10(E1vsE2),M11(F1vsF2),M12(F3vsF4)
        if verbose:
            print('')
            print('📅 June 14, 2026')
        save_result(4,0,1)  # M10(E1vsE2)
        save_result(5,0,1)  # M11(F1vsF2)
        save_result(4,2,3)  # M9(E3vsE4)
        save_result(5,2,3)  # M12(F3vsF4)
        
        # 2026-6-15 : M13(H3vsH4),M14(H1vsH2),M15(G3vsG4),M16(G1vsG2)
        if verbose:
            print('')
            print('📅 June 15, 2026')
        save_result(7,0,1)  # M14(H1vsH2)
        save_result(6,0,1)  # M16(G1vsG2)
        save_result(7,2,3)  # M13(H3vsH4)
        save_result(6,2,3)  # M15(G3vsG4)
        
        # 2026-6-16 : M17(I1vsI2),M18(I3vsI4),M19(J1vsJ2),M20(J3vsJ4)
        if verbose:
            print('')
            print('📅 June 16, 2026')
        save_result(8,0,1)  # M17(I1vsI2)
        save_result(8,2,3)  # M18(I3vsI4)
        save_result(9,0,1)  # M19(J1vsJ2)
        save_result(9,2,3)  # M20(J3vsJ4)
        
        # 2026-6-17 : M21(L3vsL4),M22(L1vsL2),M23(K1vsK2),M24(K3vsK4)
        if verbose:
            print('')
            print('📅 June 17, 2026')
        save_result(10,0,1) # M23(K1vsK2)
        save_result(11,2,3) # M21(L3vsL4)
        save_result(11,0,1) # M22(L1vsL2)
        save_result(10,2,3) # M24(K3vsK4)
    
    if view_by_group:
        if verbose:
            print('')
            print('📅 Matchday 2 (June 18-23, 2026)')
        for idx,g in enumerate(groups):
            # P4 vs P2
            save_result(idx,3,1)
            # P1 vs P3
            save_result(idx,0,2)
    else:
        # 2026-6-18 : M25(A4vsA2),M26(B4vsB2),M27(B1vsB3),M28(A1vsA3)
        if verbose:
            print('')
            print('📅 June 18, 2026')
        save_result(0,3,1)  # M25(A4vsA2)
        save_result(1,3,1)  # M26(B4vsB2)
        save_result(1,0,2)  # M27(B1vsB3)
        save_result(0,0,2)  # M28(A1vsA3)
        
        # 2026-6-19 : M29(C1vsC3),M30(C4vsC2),M31(D4vsD2),M32(D1vsD3)
        if verbose:
            print('')
            print('📅 June 19, 2026')
        save_result(3,0,2)  # M32(D1vsD3)
        save_result(2,3,1)  # M30(C4vsC2)
        save_result(2,0,2)  # M29(C1vsC3)
        save_result(3,3,1)  # M31(D4vsD2)
        
        # 2026-6-20 : M33(E1vsE3),M34(E4vsE2),M35(F1vsF3),M36(F4vsF2)
        if verbose:
            print('')
            print('📅 June 20, 2026')
        save_result(5,0,2)  # M35(F1vsF3)
        save_result(4,0,2)  # M33(E1vsE3)
        save_result(4,3,1)  # M34(E4vsE2)
        save_result(5,3,1)  # M36(F4vsF2)
        
        # 2026-6-21 : M37(H4vsH2),M38(H1vsH3),M39(G1vsG3),M40(G4vsG2)
        if verbose:
            print('')
            print('📅 June 21, 2026')
        save_result(7,0,2)  # M38(H1vsH3)
        save_result(8,0,2)  # M39(G1vsG3)
        save_result(7,3,1)  # M37(H4vsH2)
        save_result(8,3,1)  # M40(G4vsG2)
        
        # 2026-6-22 : M41(I4vsI2),M42(I1vsI3),M43(J1vsJ3),M44(J4vsJ2)
        if verbose:
            print('')
            print('📅 June 22, 2026')
        save_result(9,0,2)  # M43(J1vsJ3)
        save_result(8,0,2)  # M42(I1vsI3)
        save_result(8,3,1)  # M41(I4vsI2)
        save_result(9,3,1)  # M44(J4vsJ2)
        
        # 2026-6-23 : M45(L1vsL3),M46(L4vsL2),M47(K1vsK3),M48(K4vsK2)
        if verbose:
            print('')
            print('📅 June 23, 2026')
        save_result(10,0,2) # M47(K1vsK3)
        save_result(11,0,2) # M45(L1vsL3)
        save_result(11,3,1) # M46(L4vsL2)
        save_result(10,3,1) # M48(K4vsK2)
    
    if view_by_group:
        if verbose:
            print('')
            print('📅 Matchday 3 (June 24-27, 2026)')
        for idx,g in enumerate(groups):
            # P4 vs P1
            save_result(idx,3,0)
            # P2 vs P3
            save_result(idx,1,2)
    else:
        # 2026-6-24 : M49(C4vsC1),M50(C2vsC3),M51(B4vsB1),M52(B2vsB3),M53(A4vsA1),M54(A2vsA3)
        if verbose:
            print('')
            print('📅 June 24, 2026')
        save_result(1,3,0)  # M51(B4vsB1)
        save_result(1,1,2)  # M52(B2vsB3)
        save_result(2,3,0)  # M49(C4vsC1)
        save_result(2,1,2)  # M50(C2vsC3)
        save_result(0,3,0)  # M53(A4vsA1)
        save_result(0,1,2)  # M54(A2vsA3)
        
        # 2026-6-25 : M55(E2vsE3),M56(E4vsE1),M57(F2vsF3),M58(F4vsF1),M59(D4vsD1),M60(D2vsD3)
        if verbose:
            print('')
            print('📅 June 25, 2026')
        save_result(4,1,2)  # M55(E2vsE3)
        save_result(4,3,0)  # M56(E4vsE1)
        save_result(5,1,2)  # M57(F2vsF3)
        save_result(5,3,0)  # M58(F4vsF1)
        save_result(3,3,0)  # M59(D4vsD1)
        save_result(3,1,2)  # M60(D2vsD3)
        
        # 2026-6-26 : M61(I4vsI1),M62(I2vsI3),M63(G2vsG3),M64(G4vsG1),M65(H2vsH3),M66(H4vsH1)
        if verbose:
            print('')
            print('📅 June 26, 2026')
        save_result(8,3,0)  # M61(I4vsI1)
        save_result(8,1,2)  # M62(I2vsI3)
        save_result(7,1,2)  # M65(H2vsH3)
        save_result(7,3,0)  # M66(H4vsH1)
        save_result(6,1,2)  # M63(G2vsG3)
        save_result(6,3,0)  # M64(G4vsG1)
        
        # 2026-6-27 : M67(L4vsL1),M68(L2vsL3),M69(J2vsJ3),M70(J4vsJ1),M71(K4vsK1),M72(K2vsK3)
        if verbose:
            print('')
            print('📅 June 27, 2026')
        save_result(11,3,0) # M67(L4vsL1)
        save_result(11,1,2) # M68(L2vsL3)
        save_result(10,3,0) # M71(K4vsK1)
        save_result(10,1,2) # M72(K2vsK3)
        save_result(9,1,2)  # M69(J2vsJ3)
        save_result(9,3,0)  # M70(J4vsJ1)
    
    # 성적 순서대로 정렬
    # 정렬 순서 : 승점 -> 동률팀간 경기 승점 -> 동률팀간 경기 골득실 -> 동률팀간 경기 다득점
    #               -> 전체 경기에서의 골득실 -> 전체 경기에서의 다득점 -> 페어플레이 점수(미구현) -> 피파랭킹
    # 1,2위는 32강 진출
    
    def comp_rank_2(group_idx,team_a,team_b):
        """같은 조의 승점 동률 두 팀 간 순위 비교"""
        # 동률팀간 경기는 승점만 비교해도 괜찮음
        match [team_a,team_b]:
            # (순서는 1vs2, 3vs4, 4vs2, 1vs3, 4vs1, 2vs3)
            case [0,1]:
                game = match_record[group_idx][0]
                if game[0] > game[1]:
                    return [team_a,team_b]
                elif game[0] < game[1]:
                    return [team_b,team_a]
            case [0,2]:
                game = match_record[group_idx][3]
                if game[0] > game[1]:
                    return [team_a,team_b]
                elif game[0] < game[1]:
                    return [team_b,team_a]
            case [0,3]:
                game = match_record[group_idx][4]
                if game[0] < game[1]:
                    return [team_a,team_b]
                elif game[0] > game[1]:
                    return [team_b,team_a]
            case [1,2]:
                game = match_record[group_idx][5]
                if game[0] > game[1]:
                    return [team_a,team_b]
                elif game[0] < game[1]:
                    return [team_b,team_a]
            case [1,3]:
                game = match_record[group_idx][2]
                if game[0] < game[1]:
                    return [team_a,team_b]
                elif game[0] > game[1]:
                    return [team_b,team_a]
            case [2,3]:
                game = match_record[group_idx][1]
                if game[0] > game[1]:
                    return [team_a,team_b]
                elif game[0] < game[1]:
                    return [team_b,team_a]
        # 여기까지 넘어왔으면 승자승 같음
        if res_table[group_idx][team_a][3]-res_table[group_idx][team_a][4] > res_table[group_idx][team_b][3]-res_table[group_idx][team_b][4]:
            return [team_a,team_b]
        elif res_table[group_idx][team_a][3]-res_table[group_idx][team_a][4] < res_table[group_idx][team_b][3]-res_table[group_idx][team_b][4]:
            return [team_b,team_a]
        else:
            if res_table[group_idx][team_a][3] > res_table[group_idx][team_b][3]:
                return [team_a,team_b]
            elif res_table[group_idx][team_a][3] < res_table[group_idx][team_b][3]:
                return [team_b,team_a]
            else:
                if groups[group_idx].teams[team_a].elo > groups[group_idx].teams[team_b].elo:
                    return [team_a,team_b]
                else:
                    return [team_b,team_a]
    
    def comp_rank_3(group_idx,team_a,team_b,team_c):
        """같은 조의 승점 동률 세 팀 간 순위 비교"""
        # 동률팀간 성적 누산
        new_table = [[0,0,0,0,0] for _ in range(3)]
        output = []
        match [team_a,team_b]:
            case [0,1]:
                game = match_record[group_idx][0]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
            case [0,2]:
                game = match_record[group_idx][3]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
            case [0,3]:
                game = match_record[group_idx][4]
                if game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
            case [1,2]:
                game = match_record[group_idx][5]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
            case [1,3]:
                game = match_record[group_idx][2]
                if game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[1],game[0]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
            case [2,3]:
                game = match_record[group_idx][1]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
        
        match [team_b,team_c]:
            case [0,1]:
                game = match_record[group_idx][0]
                if game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [0,2]:
                game = match_record[group_idx][3]
                if game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [0,3]:
                game = match_record[group_idx][4]
                if game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[0],game[1]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[0],game[1]])]
            case [1,2]:
                game = match_record[group_idx][5]
                if game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [1,3]:
                game = match_record[group_idx][2]
                if game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[0],game[1]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[0],game[1]])]
            case [2,3]:
                game = match_record[group_idx][1]
                if game[0] > game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[1] = [o+a for o,a in zip(new_table[1],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
        
        match [team_a,team_c]:
            case [0,1]:
                game = match_record[group_idx][0]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [0,2]:
                game = match_record[group_idx][3]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [0,3]:
                game = match_record[group_idx][4]
                if game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[0],game[1]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[0],game[1]])]
            case [1,2]:
                game = match_record[group_idx][5]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
            case [1,3]:
                game = match_record[group_idx][2]
                if game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[0],game[1]])]
                elif game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[0],game[1]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[1],game[0]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[0],game[1]])]
            case [2,3]:
                game = match_record[group_idx][1]
                if game[0] > game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[1,0,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,0,1,game[1],game[0]])]
                elif game[0] < game[1]:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,0,1,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[1,0,0,game[1],game[0]])]
                else:
                    new_table[0] = [o+a for o,a in zip(new_table[0],[0,1,0,game[0],game[1]])]
                    new_table[2] = [o+a for o,a in zip(new_table[2],[0,1,0,game[1],game[0]])]
        
        # new_table 순서는 team_a, team_b, team_c
        # 승자승 승점 비교
        new_pts = [t[0]*3+t[1] for t in new_table]
        new_gd = [new_table[i][3]-new_table[i][4] for i in range(3)]
        prev_order = [team_a,team_b,team_c]
        new_order = sorted(range(3),key=lambda x: new_pts[x],reverse=True)
        # 승자승에서 승점 1위가 단독
        if new_pts[new_order[0]] != new_pts[new_order[1]]:
            output.append(prev_order[new_order[0]])
            # 나머지 두 팀 (승점 2/3위) 간 승점 비교
            if new_pts[new_order[1]] != new_pts[new_order[2]]:
                output.append(prev_order[new_order[1]])
                output.append(prev_order[new_order[2]])
            # 득실차 비교
            else:
                if new_gd[new_order[1]] > new_gd[new_order[2]]:
                    output.append(prev_order[new_order[1]])
                    output.append(prev_order[new_order[2]])
                elif new_gd[new_order[1]] < new_gd[new_order[2]]:
                    output.append(prev_order[new_order[2]])
                    output.append(prev_order[new_order[1]])
                # 다득점 비교
                else:
                    if new_table[new_order[1]][3] > new_table[new_order[2]][3]:
                        output.append(prev_order[new_order[1]])
                        output.append(prev_order[new_order[2]])
                    elif new_table[new_order[1]][3] < new_table[new_order[2]][3]:
                        output.append(prev_order[new_order[2]])
                        output.append(prev_order[new_order[1]])
                    # 두 팀 간 최종 비교
                    else:
                        output += comp_rank_2(group_idx,prev_order[new_order[1]],prev_order[new_order[2]])
        else:
            # 승자승에서 승점 1,2위 같음
            if new_pts[new_order[1]] != new_pts[new_order[2]]:
                # 득실차 비교
                if new_gd[new_order[0]] > new_gd[new_order[1]]:
                    output.append(prev_order[new_order[0]])
                    output.append(prev_order[new_order[1]])
                elif new_gd[new_order[0]] < new_gd[new_order[1]]:
                    output.append(prev_order[new_order[1]])
                    output.append(prev_order[new_order[0]])
                # 다득점 비교
                else:
                    if new_table[new_order[0]][3] > new_table[new_order[1]][3]:
                        output.append(prev_order[new_order[0]])
                        output.append(prev_order[new_order[1]])
                    elif new_table[new_order[0]][3] < new_table[new_order[1]][3]:
                        output.append(prev_order[new_order[1]])
                        output.append(prev_order[new_order[0]])
                    # 두 팀 간 최종 비교
                    else:
                        output += comp_rank_2(group_idx,prev_order[new_order[0]],prev_order[new_order[1]])
                # 3위는 확정
                output.append(prev_order[new_order[2]])
            # 승자승에서도 3팀 다 같음 : 득실차 비교
            else:
                # 어차피 new_order 0,1,2라 무의미하므로 재사용 가능
                new_order = sorted(range(3),key=lambda x: new_gd[x],reverse=True)
                # 승자승에서 득실차 1위가 단독
                if new_gd[new_order[0]] != new_gd[new_order[1]]:
                    output.append(prev_order[new_order[0]])
                    # 나머지 두 팀 (득실차 2/3위) 간 득실차 비교
                    if new_gd[new_order[1]] != new_gd[new_order[2]]:
                        output.append(prev_order[new_order[1]])
                        output.append(prev_order[new_order[2]])
                    # 다득점 비교
                    else:
                        if new_table[new_order[1]][3] > new_table[new_order[2]][3]:
                            output.append(prev_order[new_order[1]])
                            output.append(prev_order[new_order[2]])
                        elif new_table[new_order[1]][3] < new_table[new_order[2]][3]:
                            output.append(prev_order[new_order[2]])
                            output.append(prev_order[new_order[1]])
                        # 두 팀 간 최종 비교
                        else:
                            output += comp_rank_2(group_idx,prev_order[new_order[1]],prev_order[new_order[2]])
                else:
                    # 승자승에서 득실차 1,2위가 같음
                    if new_gd[new_order[1]] != new_gd[new_order[2]]:
                        # 다득점 비교
                        if new_table[new_order[0]][3] > new_table[new_order[1]][3]:
                            output.append(prev_order[new_order[0]])
                            output.append(prev_order[new_order[1]])
                        elif new_table[new_order[0]][3] < new_table[new_order[1]][3]:
                            output.append(prev_order[new_order[1]])
                            output.append(prev_order[new_order[0]])
                        # 두 팀 간 최종 비교
                        else:
                            output += comp_rank_2(group_idx,prev_order[new_order[0]],prev_order[new_order[1]])
                        # 3위는 확정
                        output.append(prev_order[new_order[2]])
                    # 승자승 득실차도 3팀 다 같음 : 다득점 비교
                    else:
                        # 어차피 new_order 0,1,2라 무의미하므로 재사용 가능
                        new_order = sorted(range(3),key=lambda x: new_table[x][3],reverse=True)
                        # 승자승에서 다득점 1위가 단독
                        if new_table[new_order[0]][3] != new_table[new_order[1]][3]:
                            output.append(prev_order[new_order[0]])
                            # 나머지 두 팀 (다득점 2/3위) 간 다득점 비교
                            if new_table[new_order[1]][3] != new_table[new_order[2]][3]:
                                output.append(prev_order[new_order[1]])
                                output.append(prev_order[new_order[2]])
                            # 두 팀 간 최종 비교
                            else:
                                output += comp_rank_2(group_idx,prev_order[new_order[1]],prev_order[new_order[2]])
                        else:
                            # 승자승에서 다득점 1,2위가 같음
                            if new_table[new_order[1]][3] != new_table[new_order[2]][3]:
                                # 두 팀 간 최종 비교
                                output += comp_rank_2(group_idx,prev_order[new_order[0]],prev_order[new_order[1]])
                                # 3위는 확정
                                output.append(prev_order[new_order[2]])
                            else:
                                # 승자승 다득점도 3팀 다 같음 : 전체 골득실 비교
                                gd = [res_table[group_idx][i][3]-res_table[group_idx][i][4] for i in range(3)]
                                new_order = sorted(range(3),key=lambda x: gd[x],reverse=True)
                                # 전체 골득실에서 1위 단독
                                if gd[new_order[0]] != gd[new_order[1]]:
                                    output.append(prev_order[new_order[0]])
                                    # 나머지 두 팀 (골득실 2/3위) 간 득실차 비교
                                    if gd[new_order[1]] != gd[new_order[2]]:
                                        output.append(prev_order[new_order[1]])
                                        output.append(prev_order[new_order[2]])
                                    # 다득점 비교
                                    else:
                                        if res_table[group_idx][new_order[1]][3] > res_table[group_idx][new_order[2]][3]:
                                            output.append(prev_order[new_order[1]])
                                            output.append(prev_order[new_order[2]])
                                        elif res_table[group_idx][new_order[1]][3] < res_table[group_idx][new_order[2]][3]:
                                            output.append(prev_order[new_order[2]])
                                            output.append(prev_order[new_order[1]])
                                        # 두 팀 간 최종 비교
                                        else:
                                            output += comp_rank_2(group_idx,prev_order[new_order[1]],prev_order[new_order[2]])
                                else:
                                    # 전체 골득실에서 1,2위 같음
                                    if gd[new_order[1]] != gd[new_order[2]]:
                                        # 다득점 비교
                                        if res_table[group_idx][new_order[0]][3] > res_table[group_idx][new_order[1]][3]:
                                            output.append(prev_order[new_order[0]])
                                            output.append(prev_order[new_order[1]])
                                        elif res_table[group_idx][new_order[0]][3] < res_table[group_idx][new_order[1]][3]:
                                            output.append(prev_order[new_order[1]])
                                            output.append(prev_order[new_order[0]])
                                        # 두 팀 간 최종 비교
                                        else:
                                            output += comp_rank_2(group_idx,prev_order[new_order[0]],prev_order[new_order[1]])
                                        # 3위는 확정
                                        output.append(prev_order[new_order[2]])
                                    # 전체 골득실도 3팀 다 같음 : 전체 다득점 비교
                                    else:
                                        # 어차피 new_order 0,1,2라 무의미하므로 재사용 가능
                                        new_order = sorted(range(3),key=lambda x: res_table[group_idx][x][3],reverse=True)
                                        # 전체 다득점에서 1위 단독
                                        if res_table[group_idx][new_order[0]][3] != res_table[group_idx][new_order[1]][3]:
                                            output.append(prev_order[new_order[0]])
                                            # 나머지 두 팀 (다득점 2/3위) 간 전체 다득점 비교
                                            if res_table[group_idx][new_order[1]][3] != res_table[group_idx][new_order[2]][3]:
                                                output.append(prev_order[new_order[1]])
                                                output.append(prev_order[new_order[2]])
                                            # 두 팀 간 최종 비교
                                            else:
                                                output += comp_rank_2(group_idx,prev_order[new_order[1]],prev_order[new_order[2]])
                                        else:
                                            # 전체 다득점에서 1,2위가 같음
                                            if res_table[group_idx][new_order[1]][3] != res_table[group_idx][new_order[2]][3]:
                                                # 두 팀 간 최종 비교
                                                output += comp_rank_2(group_idx,prev_order[new_order[0]],prev_order[new_order[1]])
                                                # 3위는 확정
                                                output.append(prev_order[new_order[2]])
                                            else:
                                                # 전체 다득점도 3팀 다 같음 : 피파랭킹으로 비교
                                                new_order = sorted(range(3),key=lambda x: groups[group_idx].teams[prev_order[x]].elo,reverse=True)
                                                output.append(prev_order[new_order[0]])
                                                output.append(prev_order[new_order[1]])
                                                output.append(prev_order[new_order[2]])
        
        return output
    
    def comp_rank_4(group_idx):
        """같은 조의 승점 동률 네 팀 간 순위 비교"""
        # 그럴 일은 없겠지만... 만약 네 팀 모두 승점이 같다면 동률팀간 비교 = 전체 비교
        # 따라서 승자승 승점 비교는 생략 (이게 안 돼서 넘어온 거잖아)
        # 승자승 다득점도 3팀 다 같음 : 전체 골득실 비교
        gd = [res_table[group_idx][i][3]-res_table[group_idx][i][4] for i in range(4)]
        output = []
        
        new_order = sorted(range(4),key=lambda x: gd[x],reverse=True)
        # 승자승 골득실 1위 단독
        if gd[new_order[0]] != gd[new_order[1]]:
            output.append(new_order[0])
            # 승자승 골득실 2/3/4위 비교
            # 승자승 골득실 2위 단독
            if gd[new_order[1]] != gd[new_order[2]]:
                output.append(new_order[1])
                # 승자승 골득실 3위 단독
                if gd[new_order[2]] != gd[new_order[3]]:
                    output.append(new_order[2])
                    output.append(new_order[3])
                # 승자승 골득실 3/4위 동률 : 다득점 비교
                else:
                    if res_table[group_idx][new_order[2]][3] > res_table[group_idx][new_order[3]][3]:
                        output.append(new_order[2])
                        output.append(new_order[3])
                    elif res_table[group_idx][new_order[2]][3] < res_table[group_idx][new_order[3]][3]:
                        output.append(new_order[3])
                        output.append(new_order[2])
                    # 승자승 다득점 동률 : 하위 승자승
                    else:
                        output += comp_rank_2(group_idx,new_order[2],new_order[3])
            else:
                # 승자승 골득실 2/3위 동률 : 다득점 비교
                if gd[new_order[2]] != gd[new_order[3]]:
                    if res_table[group_idx][new_order[1]][3] > res_table[group_idx][new_order[2]][3]:
                        output.append(new_order[1])
                        output.append(new_order[2])
                    elif res_table[group_idx][new_order[1]] < res_table[group_idx][new_order[2]]:
                        output.append(new_order[2])
                        output.append(new_order[1])
                    # 승자승 다득점 동률 : 하위 승자승
                    else:
                        output += comp_rank_2(group_idx,new_order[1],new_order[2])
                    # 4위는 확정
                    output.append(new_order[3])
                else:
                    # 승자승 골득실 2/3/4위 동률 : 다득점 비교
                    prev_order = [new_order[1],new_order[2],new_order[3]]
                    new_new_order = sorted(range(3),key=lambda x: res_table[group_idx][prev_order[x]][3],reverse=True)
                    # 승자승 다득점 2위 단독
                    if res_table[group_idx][prev_order[new_new_order[0]]][3] != res_table[group_idx][prev_order[new_new_order[1]]][3]:
                        output.append(prev_order[new_new_order[0]])
                        # 승자승 다득점 3/4위 비교
                        if res_table[group_idx][prev_order[new_new_order[1]]][3] > res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output.append(prev_order[new_new_order[1]])
                            output.append(prev_order[new_new_order[2]])
                        elif res_table[group_idx][prev_order[new_new_order[1]]][3] < res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output.append(prev_order[new_new_order[2]])
                            output.append(prev_order[new_new_order[1]])
                        # 승자승 다득점 3/4위 동률: 하위 승자승
                        else:
                            output += comp_rank_2(group_idx,prev_order[new_new_order[1]],prev_order[new_new_order[2]])
                    else:
                        # 승자승 다득점 2/3위 동률 : 하위 승자승
                        if res_table[group_idx][prev_order[new_new_order[1]]][3] != res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output += comp_rank_2(group_idx,prev_order[new_new_order[0]],prev_order[new_new_order[1]])
                            # 4위는 확정
                            output.append(prev_order[new_new_order[2]])
                        else:
                            # 승자승 다득점 2/3/4위 동률 : 하위 승자승
                            output += comp_rank_3(group_idx,prev_order[new_new_order[0]],prev_order[new_new_order[1]],prev_order[new_new_order[2]])
        else:
            # 승자승 골득실 1/2위 동률 : 다득점 비교
            if gd[new_order[1]] != gd[new_order[2]]:
                if res_table[group_idx][new_order[0]] > res_table[group_idx][new_order[1]]:
                    output.append(new_order[0])
                    output.append(new_order[1])
                elif res_table[group_idx][new_order[0]] < res_table[group_idx][new_order[1]]:
                    output.append(new_order[1])
                    output.append(new_order[0])
                # 승자승 골득실 1/2위 동률 : 하위 승자승
                else:
                    output += comp_rank_2(group_idx,new_order[0],new_order[1])
                # 승자승 골득실 3/4위 비교
                # 승자승 골득실 3위 단독
                if gd[new_order[2]] != gd[new_order[3]]:
                    output.append(new_order[2])
                    output.append(new_order[3])
                # 승자승 골득실 3/4위 동률 : 다득점 비교
                else:
                    if res_table[group_idx][new_order[2]][3] > res_table[group_idx][new_order[3]][3]:
                        output.append(new_order[2])
                        output.append(new_order[3])
                    elif res_table[group_idx][new_order[2]][3] < res_table[group_idx][new_order[3]][3]:
                        output.append(new_order[3])
                        output.append(new_order[2])
                    # 승자승 다득점 동률 : 하위 승자승
                    else:
                        output += comp_rank_2(group_idx,new_order[2],new_order[3])
            else:
                # 승자승 골득실 1/2/3위 동률 : 다득점 비교
                if gd[new_order[2]] != gd[new_order[3]]:
                    prev_order = [new_order[0],new_order[1],new_order[2]]
                    new_new_order = sorted(range(3),key=lambda x: res_table[group_idx][prev_order[x]][3],reverse=True)
                    # 승자승 다득점 1위 단독
                    if res_table[group_idx][prev_order[new_new_order[0]]][3] != res_table[group_idx][prev_order[new_new_order[1]]][3]:
                        output.append(prev_order[new_new_order[0]])
                        # 승자승 다득점 2/3위 비교
                        if res_table[group_idx][prev_order[new_new_order[1]]][3] > res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output.append(prev_order[new_new_order[1]])
                            output.append(prev_order[new_new_order[2]])
                        elif res_table[group_idx][prev_order[new_new_order[1]]][3] < res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output.append(prev_order[new_new_order[2]])
                            output.append(prev_order[new_new_order[1]])
                        # 승자승 다득점 2/3위 동률: 하위 승자승
                        else:
                            output += comp_rank_2(group_idx,prev_order[new_new_order[1]],prev_order[new_new_order[2]])
                    else:
                        # 승자승 다득점 1/2위 동률 : 하위 승자승
                        if res_table[group_idx][prev_order[new_new_order[1]]][3] != res_table[group_idx][prev_order[new_new_order[2]]][3]:
                            output += comp_rank_2(group_idx,prev_order[new_new_order[0]],prev_order[new_new_order[1]])
                            # 3위는 확정
                            output.append(prev_order[new_new_order[2]])
                        else:
                            # 승자승 다득점 1/2/3위 동률 : 하위 승자승
                            output += comp_rank_3(group_idx,prev_order[new_new_order[0]],prev_order[new_new_order[1]],prev_order[new_new_order[2]])
                    # 4위는 확정
                    output.append(new_order[3])
                else:
                    # 승자승 골득실 1/2/3/4위 동률 : 다득점 비교
                    new_order = sorted(range(4),key=lambda x: res_table[group_idx][x][3],reverse=True)
                    # 승자승 다득점 1위 단독
                    if res_table[group_idx][new_order[0]][3] != res_table[group_idx][new_order[1]][3]:
                        output.append(new_order[0])
                        # 승자승 다득점 2/3/4위 비교
                        # 승자승 다득점 2위 단독
                        if res_table[group_idx][new_order[1]][3] != res_table[group_idx][new_order[2]][3]:
                            output.append(new_order[1])
                            # 승자승 다득점 3/4위 비교
                            if res_table[group_idx][new_order[2]][3] != res_table[group_idx][new_order[3]][3]:
                                output.append(new_order[2])
                                output.append(new_order[3])
                            # 승자승 다득점 3/4위 동률: 하위 승자승
                            else:
                                output += comp_rank_2(group_idx,new_order[2],new_order[3])
                        else:
                            # 승자승 다득점 2/3위 동률 : 하위 승자승
                            if res_table[group_idx][new_order[2]][3] != res_table[group_idx][new_order[3]][3]:
                                output += comp_rank_2(group_idx,new_order[1],new_order[2])
                                # 4위는 확정
                                output.append(new_order[3])
                            else:
                                # 승자승 다득점 2/3/4위 동률 : 하위 승자승
                                output += comp_rank_3(group_idx,new_order[1],new_order[2],new_order[3])
                    else:
                        # 승자승 다득점 1/2위 동률 : 하위 승자승
                        if res_table[group_idx][new_order[1]][3] != res_table[group_idx][new_order[2]][3]:
                            output += comp_rank_2(group_idx,new_order[0],new_order[1])
                            # 승자승 다득점 3/4위 비교
                            if res_table[group_idx][new_order[2]][3] != res_table[group_idx][new_order[3]][3]:
                                output.append(new_order[2])
                                output.append(new_order[3])
                            else:
                                # 승자승 다득점 3/4위 동률 : 하위 승자승
                                output += comp_rank_2(group_idx,new_order[2],new_order[3])
                        else:
                            # 승자승 다득점 1/2/3위 동률 : 하위 승자승
                            if res_table[group_idx][new_order[2]][3] != res_table[group_idx][new_order[3]][3]:
                                output += comp_rank_3(group_idx,new_order[0],new_order[1],new_order[2])
                                # 4위는 확정
                                output.append(new_order[3])
                            else:
                                # 승자승 다득점 1/2/3/4위 동률 : 하위 승자승 없으므로 피파랭킹 비교
                                new_order = sorted(range(4),key=lambda x: groups[group_idx].teams[x].elo,reverse=True)
                                output.append(new_order[0])
                                output.append(new_order[1])
                                output.append(new_order[2])
                                output.append(new_order[3])
        return output
    
    rank1 = []
    rank2 = []
    rank3 = []
    rank4 = []
    for idx,g in enumerate(res_table):
        pts = [t[0]*3+t[1] for t in g]
        order = sorted(range(len(pts)),key=lambda x: pts[x],reverse=True)
        # 승점 1위가 단독
        if pts[order[0]] != pts[order[1]]:
            rank1.append(groups[idx].teams[order[0]])
            # 승점 2위 단독
            if pts[order[1]] != pts[order[2]]:
                rank2.append(groups[idx].teams[order[1]])
                if pts[order[2]] != pts[order[3]]:
                    rank3.append(groups[idx].teams[order[2]])
                    rank4.append(groups[idx].teams[order[3]])
                # 승점 3,4위 동률
                else:
                    rank = comp_rank_2(idx,order[2],order[3])
                    rank3.append(groups[idx].teams[rank[0]])
                    rank4.append(groups[idx].teams[rank[1]])
            else:
                # 승점 2,3위 동률
                if pts[order[2]] != pts[order[3]]:
                    rank = comp_rank_2(idx,order[1],order[2])
                    rank2.append(groups[idx].teams[rank[0]])
                    rank3.append(groups[idx].teams[rank[1]])
                    rank4.append(groups[idx].teams[order[3]])
                else:
                    # 승점 2,3,4위 동률
                    rank = comp_rank_3(idx,order[1],order[2],order[3])
                    rank2.append(groups[idx].teams[rank[0]])
                    rank3.append(groups[idx].teams[rank[1]])
                    rank4.append(groups[idx].teams[rank[2]])
        else:
            # 1,2위 승점 동률
            if pts[order[1]] != pts[order[2]]:
                rank = comp_rank_2(idx,order[0],order[1])                
                rank1.append(groups[idx].teams[rank[0]])
                rank2.append(groups[idx].teams[rank[1]])
                if pts[order[2]] != pts[order[3]]:
                    rank3.append(groups[idx].teams[order[2]])
                    rank4.append(groups[idx].teams[order[3]])
                # 3,4위 승점 동률
                else:
                    rank = comp_rank_2(idx,order[2],order[3])
                    rank3.append(groups[idx].teams[rank[0]])
                    rank4.append(groups[idx].teams[rank[1]])
            else:
                # 1,2,3위 승점 같음
                if pts[order[2]] != pts[order[3]]:
                    rank = comp_rank_3(idx,order[0],order[1],order[2])
                    rank1.append(groups[idx].teams[rank[0]])
                    rank2.append(groups[idx].teams[rank[1]])
                    rank3.append(groups[idx].teams[rank[2]])
                    rank4.append(groups[idx].teams[order[3]])
                else:
                    # 1,2,3,4위 승점 같음
                    rank = comp_rank_4(idx)
                    rank1.append(groups[idx].teams[rank[0]])
                    rank2.append(groups[idx].teams[rank[1]])
                    rank3.append(groups[idx].teams[rank[2]])
                    rank4.append(groups[idx].teams[rank[3]])
    
    if verbose:
        print('')
        print('📊 Results')
        for idx,g in enumerate(groups):
            print(f'🚩 {g.name}   W   D   L   GF   GA   GD   Pt')
            print(f'-------------------------------------------')
            rank1_idx = g.teams.index(rank1[idx])
            res = res_table[idx][rank1_idx]
            print(f' 1     {rank1[idx].abbr}   {res[0]}   {res[1]}   {res[2]}   {res[3]:2d}   {res[4]:2d}  {res[3]-res[4]:3d}    {res[0]*3+res[1]}')
            rank2_idx = g.teams.index(rank2[idx])
            res = res_table[idx][rank2_idx]
            print(f' 2     {rank2[idx].abbr}   {res[0]}   {res[1]}   {res[2]}   {res[3]:2d}   {res[4]:2d}  {res[3]-res[4]:3d}    {res[0]*3+res[1]}')
            rank3_idx = g.teams.index(rank3[idx])
            res = res_table[idx][rank3_idx]
            print(f' 3     {rank3[idx].abbr}   {res[0]}   {res[1]}   {res[2]}   {res[3]:2d}   {res[4]:2d}  {res[3]-res[4]:3d}    {res[0]*3+res[1]}')
            rank4_idx = g.teams.index(rank4[idx])
            res = res_table[idx][rank4_idx]
            print(f' 4     {rank4[idx].abbr}   {res[0]}   {res[1]}   {res[2]}   {res[3]:2d}   {res[4]:2d}  {res[3]-res[4]:3d}    {res[0]*3+res[1]}')
            print('')
    
    # 3위 간 성적 비교
    # 정렬 순서 : 승점 -> 전체경기 골득실 -> 전체경기 다득점 -> 페어플레이 점수(미구현) -> 피파랭킹
    rank3_table = [[0,0,0,0] for _ in range(len(rank3))]
    for idx,t in enumerate(rank3):
        pos = groups[idx].teams.index(t)
        rank3_table[idx][0] = res_table[idx][pos][0]*3+res_table[idx][pos][1]
        rank3_table[idx][1] = res_table[idx][pos][3]-res_table[idx][pos][4]
        rank3_table[idx][2] = res_table[idx][pos][3]
        rank3_table[idx][3] = t.elo
    rank3_rank = sorted(range(len(rank3_table)),key=lambda i: rank3_table[i],reverse=True)
    if verbose:
        print('📊 Ranking of third-placed teams')
        print(' Pos  Grp  Team  W  D  L  GF  GA   GD  Pt')
        print('------------------------------------------')
        for idx,r in enumerate(rank3_rank):
            pos = groups[r].teams.index(rank3[r])
            res = res_table[r][pos]
            print(f'  {idx+1:2d}    {chr(65+r)}   {rank3[r].abbr}  {res[0]}  {res[1]}  {res[2]}  {res[3]:2d}  {res[4]:2d}  {res[3]-res[4]:3d}   {res[0]*3+res[1]}')
            if idx == 7:
                print('------------------------------------------ <- Cut line for RO32')
        print('')
    adv_group = sorted(rank3_rank[:8])
    return [rank1,rank2,rank3,rank4,adv_group,games]

def sim_ro32(rank1:list[Country], rank2:list[Country], rank3:list[Country], rank3_group:list[int], verbose=True):
    """월드컵 결선 토너먼트 32강 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Round of 32...')
        
    # 32강 대진표 완성 준비
    p3_alphabet = [chr(65+i) for i in rank3_group]
    qualifying_set = ROUND_OF_32_COMBINATIONS[frozenset(p3_alphabet)]
    winner = []
    loser = []
    games = []
    
    def i(str):
        return ord(str[-1])-65
    
    def save_result(match_name,home,away):
        res = sim_game_penalty(match_name,home,away,verbose)
        if len(res) == 2:
            games.append(Game(match_name,home,away,res[0],res[1]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        elif len(res) == 3:
            games.append(Game(match_name,home,away,res[0],res[1],res[2]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        else:
            games.append(Game(match_name,home,away,res[0],res[1],res[2],res[3],res[4]))
            # 승부차기로 종료
            if res[3] > res[4]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
    
    # June 28, 2026
    if verbose:
        print('')
        print('📅 June 28, 2026')
    save_result('Round of 32',rank2[i('A')],rank2[i('B')])      # M73(A2vsB2)
    
    # June 29, 2026
    if verbose:
        print('')
        print('📅 June 29, 2026')
    save_result('Round of 32',rank1[i('C')],rank2[i('F')])      # M76(C1vsF2)
    idx = i(qualifying_set['1E'])
    save_result('Round of 32',rank1[i('E')],rank3[idx])         # M74(E1vsA3/B3/C3/D3/F3)
    save_result('Round of 32',rank1[i('F')],rank2[i('C')])      # M75(F1vsC2)
    
    # June 30, 2026
    if verbose:
        print('')
        print('📅 June 30, 2026')
    save_result('Round of 32',rank2[i('E')],rank2[i('I')])      # M78(E2vsI2)
    idx = i(qualifying_set['1I'])
    save_result('Round of 32',rank1[i('I')],rank3[idx])         # M77(I1vsC3/D3/F3/G3/H3)
    idx = i(qualifying_set['1A'])
    save_result('Round of 32',rank1[i('A')],rank3[idx])         # M79(A1vsC3/E3/F3/H3/I3)
    
    # July 1, 2026
    if verbose:
        print('')
        print('📅 July 1, 2026')
    idx = i(qualifying_set['1L'])
    save_result('Round of 32',rank1[i('L')],rank3[idx])         # M80(L1vsE3/H3/I3/J3/K3)
    idx = i(qualifying_set['1G'])
    save_result('Round of 32',rank1[i('G')],rank3[idx])         # M82(G1vsA3/E3/H3/I3/J3)
    idx = i(qualifying_set['1D'])
    save_result('Round of 32',rank1[i('D')],rank3[idx])         # M81(D1vsB3/E3/F3/I3/J3)
    
    # July 2, 2026
    if verbose:
        print('')
        print('📅 July 2, 2026')
    save_result('Round of 32',rank1[i('H')],rank2[i('J')])      # M84(H1vsJ2)
    save_result('Round of 32',rank2[i('K')],rank2[i('L')])      # M83(K2vsL2)
    idx = i(qualifying_set['1B'])
    save_result('Round of 32',rank1[i('B')],rank3[idx])         # M85(B1vsE3/F3/G3/I3/J3)
    
    # July 3, 2026
    if verbose:
        print('')
        print('📅 July 3, 2026')
    save_result('Round of 32',rank2[i('D')],rank2[i('G')])      # M88(D2vsG2)
    save_result('Round of 32',rank1[i('J')],rank2[i('H')])      # M86(J1vsH2)
    idx = i(qualifying_set['1K'])
    save_result('Round of 32',rank1[i('K')],rank3[idx])         # M87(K1vsD3/E3/I3/J3/L3)
    
    if verbose:
        print('')
        print('📊 Results')
        for w in winner:
            print(f'🏆 Advanced to Round of 16 : {w}')
            
    return [winner,loser,games]

def sim_ro16(teams:list[Country], verbose=True):
    """월드컵 결선 토너먼트 16강 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Round of 16...')
        
    winner = []
    loser = []
    games = []
    
    def save_result(match_name,home,away):
        res = sim_game_penalty(match_name,home,away,verbose)
        if len(res) == 2:
            games.append(Game(match_name,home,away,res[0],res[1]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        elif len(res) == 3:
            games.append(Game(match_name,home,away,res[0],res[1],res[2]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        else:
            games.append(Game(match_name,home,away,res[0],res[1],res[2],res[3],res[4]))
            # 승부차기로 종료
            if res[3] > res[4]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
    
    # 32강은 M73~M88
    
    # July 4, 2026
    if verbose:
        print('')
        print('📅 July 4, 2026')
    save_result('Round of 16',teams[0],teams[2])        # M90(M73vsM75)
    save_result('Round of 16',teams[1],teams[4])        # M89(M74vsM77)
    
    # July 5, 2026
    if verbose:
        print('')
        print('📅 July 5, 2026')
    save_result('Round of 16',teams[3],teams[5])        # M91(M76vsM78)
    save_result('Round of 16',teams[6],teams[7])        # M92(M79vsM80)
    
    # July 6, 2026
    if verbose:
        print('')
        print('📅 July 6, 2026')
    save_result('Round of 16',teams[10],teams[11])      # M93(M83vsM84)
    save_result('Round of 16',teams[8],teams[9])        # M94(M81vsM82)
    
    # July 7, 2026
    if verbose:
        print('')
        print('📅 July 7, 2026')
    save_result('Round of 16',teams[13],teams[15])      # M95(M86vsM88)
    save_result('Round of 16',teams[12],teams[14])      # M96(M85vsM87)
    
    if verbose:
        print('')
        print('📊 Results')
        for w in winner:
            print(f'🏆 Advanced to Quarterfinals : {w}')
            
    return [winner,loser,games]

def sim_qf(teams:list[Country], verbose=True):
    """월드컵 결선 토너먼트 8강 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Quarterfinals...')
        
    winner = []
    loser = []
    games = []
    
    def save_result(match_name,home,away):
        res = sim_game_penalty(match_name,home,away,verbose)
        if len(res) == 2:
            games.append(Game(match_name,home,away,res[0],res[1]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        elif len(res) == 3:
            games.append(Game(match_name,home,away,res[0],res[1],res[2]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        else:
            games.append(Game(match_name,home,away,res[0],res[1],res[2],res[3],res[4]))
            # 승부차기로 종료
            if res[3] > res[4]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
    
    # 16강은 M89~M96
    
    # July 9, 2026
    if verbose:
        print('')
        print('📅 July 9, 2026')
    save_result('Quarterfinals',teams[0],teams[1])      # M97(M89vsM90)
    
    # July 10, 2026
    if verbose:
        print('')
        print('📅 July 10, 2026')
    save_result('Quarterfinals',teams[4],teams[5])      # M98(M93vsM94)
    
    # July 11, 2026
    if verbose:
        print('')
        print('📅 July 11, 2026')
    save_result('Quarterfinals',teams[2],teams[3])      # M99(M91vsM92)
    save_result('Quarterfinals',teams[6],teams[7])      # M100(M95vsM96)
    
    if verbose:
        print('')
        print('📊 Results')
        for w in winner:
            print(f'🏆 Advanced to Semifinals : {w}')
            
    return [winner,loser,games]

def sim_sf(teams:list[Country], verbose=True):
    """월드컵 결선 토너먼트 4강 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Semifinals...')
        
    winner = []
    loser = []
    games = []
    
    def save_result(match_name,home,away):
        res = sim_game_penalty(match_name,home,away,verbose)
        if len(res) == 2:
            games.append(Game(match_name,home,away,res[0],res[1]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        elif len(res) == 3:
            games.append(Game(match_name,home,away,res[0],res[1],res[2]))
            # 승부차기 없이 종료
            if res[0] > res[1]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
        else:
            games.append(Game(match_name,home,away,res[0],res[1],res[2],res[3],res[4]))
            # 승부차기로 종료
            if res[3] > res[4]:
                winner.append(home)
                loser.append(away)
            else:
                winner.append(away)
                loser.append(home)
    
    # 8강은 M97~M100
    
    # July 14, 2026
    if verbose:
        print('')
        print('📅 July 14, 2026')
    save_result('Semifinals',teams[0],teams[1])      # M101(M97vsM98)
    
    # July 15, 2026
    if verbose:
        print('')
        print('📅 July 15, 2026')
    save_result('Semifinals',teams[2],teams[3])      # M102(M99vsM100)
    
    if verbose:
        print('')
        print('📊 Results')
        for w in winner:
            print(f'🏆 Advanced to Final : {w}')
        for l in loser:
            print(f'🥉 Advanced to Bronze Final : {l}')
            
    return [winner,loser,games]

def sim_bf(teams:list[Country], verbose=True):
    """월드컵 결선 토너먼트 동메달 결정전 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Bronze Final...')
        
    winner = None
    loser = None
    game = None
    
    # July 18, 2026
    if verbose:
        print('')
        print('📅 July 18, 2026')
    
    res = sim_game_penalty('Bronze Final',teams[0],teams[1],verbose)
    if len(res) == 2:
        game = Game('Bronze Final',teams[0],teams[1],res[0],res[1])
        # 승부차기 없이 종료
        if res[0] > res[1]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
    elif len(res) == 3:
        game = Game('Bronze Final',teams[0],teams[1],res[0],res[1],res[2])
        # 승부차기 없이 종료
        if res[0] > res[1]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
    else:
        game = Game('Bronze Final',teams[0],teams[1],res[0],res[1],res[2],res[3],res[4])
        # 승부차기로 종료
        if res[3] > res[4]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
    
    if verbose:
        print('')
        print('📊 Results')
        print(f'🥉 3rd Place : {winner}')
        print(f'🏅 4th Place : {loser}')
            
    return [winner,loser,game]

def sim_final(teams:list[Country], verbose=True):
    """월드컵 결선 토너먼트 동메달 결정전 시뮬레이션"""
    # 매치 일정은 공식 문서 참고하였음 (날짜 순서대로 진행)
    if verbose:
        print('==================================================')
        print('🏁 Simulating World Cup Final...')
        
    winner = None
    loser = None
    game = None
    
    # July 19, 2026
    if verbose:
        print('')
        print('📅 July 19, 2026')
    
    res = sim_game_penalty('Final',teams[0],teams[1],verbose)
    
    if len(res) == 2:
        game = Game('Final',teams[0],teams[1],res[0],res[1])
        # 승부차기 없이 종료
        if res[0] > res[1]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
    elif len(res) == 3:
        game = Game('Final',teams[0],teams[1],res[0],res[1],res[2])
        # 승부차기 없이 종료
        if res[0] > res[1]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
    else:
        game = Game('Final',teams[0],teams[1],res[0],res[1],res[2],res[3],res[4])
        # 승부차기로 종료
        if res[3] > res[4]:
            winner = teams[0]
            loser = teams[1]
        else:
            winner = teams[1]
            loser = teams[0]
        
    if verbose:
        print('')
        print('📊 Results')
        print(f'🥇 1st Place : {winner}')
        print(f'🥈 2nd Place : {loser}')
            
    return [winner,loser,game]

def complete_sim(teams:list[Country], verbose=False, view_by_group=0):
    """PO 조 추첨부터 완전 시뮬레이션"""
    ic_path = ic_po_draw(teams,verbose)
    for path in ic_path:
        path.name = 'ICPO ' + path.name

    # UEFA PO 패스 추첨 시뮬레이션
    uefa_path = uefa_po_draw(teams,verbose)
    for path in uefa_path[0:4]:
        path.name = 'UEFA ' + path.name

    # 월드컵 조별예선 추첨 시뮬레이션
    wc_groups = worldcup_gs_draw(teams,uefa_path,ic_path,verbose)

    # 대륙 PO / UEFA PO 시뮬레이션 (동시 진행)
    po_winner = sim_po(ic_path,uefa_path,verbose)

    # PO 결과를 월드컵 조에 이식
    for g in wc_groups:
        for idx,t in enumerate(g.teams):
            if type(t) == Group:
                for w in po_winner:
                    if w in t.teams:
                        g.teams[idx] = w
                        break

    # 월드컵 조별예선 시뮬레이션
    gs_res = sim_worldcup_gs(wc_groups,verbose,view_by_group)
    
    # 월드컵 결선 토너먼트 시뮬레이션
    ro32_res = sim_ro32(gs_res[0],gs_res[1],gs_res[2],gs_res[4],verbose)
    ro16_res = sim_ro16(ro32_res[0],verbose)
    qf_res = sim_qf(ro16_res[0],verbose)
    sf_res = sim_sf(qf_res[0],verbose)
    bf_res = sim_bf(sf_res[1],verbose)
    final_res = sim_final(sf_res[0],verbose)
    
    # 함수 반환값은 최종순위(PO 탈락팀 제외) + 본선 시합
    total_games = gs_res[5]+ro32_res[2]+ro16_res[2]+qf_res[2]+sf_res[2]
    total_games.append(bf_res[2])
    total_games.append(final_res[2])
    teams_rank = []
    # 1~4위는 결승전/동메달결정전으로 결정
    teams_rank.append(final_res[0])
    teams_rank.append(final_res[1])
    teams_rank.append(bf_res[0])
    teams_rank.append(bf_res[1])
    
    # 8강 이하 나열 순서: 승점 > 득실차 > 다득점 > 피파랭킹
    def rank_teams(teams:list[Country]):
        """최종 순위 계산법"""
        rank_table = [[0,0,0,0] for _ in range(len(teams))]
        for t in teams:
            for idx,t in enumerate(teams):
                rank_table[idx][3] = t.elo
                games = find_all_games(t,total_games)
                for g in games:
                    if t.name == g.home.name:
                        rank_table[idx][1] += g.score_home - g.score_away
                        rank_table[idx][2] += g.score_home
                        if g.score_home > g.score_away:
                            rank_table[idx][0] += 3
                        elif g.score_home == g.score_away:
                            rank_table[idx][0] += 1
                    elif t.name == g.away.name:
                        rank_table[idx][1] += g.score_away - g.score_home
                        rank_table[idx][2] += g.score_away
                        if g.score_home < g.score_away:
                            rank_table[idx][0] += 3
                        elif g.score_home == g.score_away:
                            rank_table[idx][0] += 1
        rank = sorted(range(len(rank_table)),key=lambda i: rank_table[i],reverse=True)
        res:list[Country] = []
        for r in rank:
            res.append(teams[r])
        return res
    
    # 8강 탈락팀 순위비교
    teams_rank += rank_teams(qf_res[1])
    # 16강 탈락팀 순위비교
    teams_rank += rank_teams(ro16_res[1])
    # 32강 탈락팀 순위비교
    teams_rank += rank_teams(ro32_res[1])
    
    # 조별리그 탈락팀 순위비교
    noadv_group = list(range(12))
    for idx in gs_res[4]:
        noadv_group.remove(idx)
    noadv_teams = [gs_res[2][i] for i in noadv_group] + gs_res[3]
    teams_rank += rank_teams(noadv_teams)
    
    return [teams_rank,total_games]

def sim_after_draw(teams:list[Country], verbose=False, view_by_group=0):
    """현실 조 추첨 결과에서 시작"""
    ic_path = ic_po_real(teams)
    uefa_path = uefa_po_real(teams)
    wc_groups = worldcup_gs_real(teams,uefa_path,ic_path)

    # 대륙 PO / UEFA PO 시뮬레이션 (동시 진행)
    po_winner = sim_po(ic_path,uefa_path,verbose)

    # PO 결과를 월드컵 조에 이식
    for g in wc_groups:
        for idx,t in enumerate(g.teams):
            if type(t) == Group:
                for w in po_winner:
                    if w in t.teams:
                        g.teams[idx] = w
                        break

    # 월드컵 조별예선 시뮬레이션
    gs_res = sim_worldcup_gs(wc_groups,verbose,view_by_group)
    
    # 월드컵 결선 토너먼트 시뮬레이션
    ro32_res = sim_ro32(gs_res[0],gs_res[1],gs_res[2],gs_res[4],verbose)
    ro16_res = sim_ro16(ro32_res[0],verbose)
    qf_res = sim_qf(ro16_res[0],verbose)
    sf_res = sim_sf(qf_res[0],verbose)
    bf_res = sim_bf(sf_res[1],verbose)
    final_res = sim_final(sf_res[0],verbose)
    
    # 함수 반환값은 최종순위(PO 탈락팀 제외) + 본선 시합
    total_games = gs_res[5]+ro32_res[2]+ro16_res[2]+qf_res[2]+sf_res[2]
    total_games.append(bf_res[2])
    total_games.append(final_res[2])
    teams_rank = []
    # 1~4위는 결승전/동메달결정전으로 결정
    teams_rank.append(final_res[0])
    teams_rank.append(final_res[1])
    teams_rank.append(bf_res[0])
    teams_rank.append(bf_res[1])
    
    # 8강 이하 나열 순서: 승점 > 득실차 > 다득점 > 피파랭킹
    def rank_teams(teams:list[Country]):
        rank_table = [[0,0,0,0] for _ in range(len(teams))]
        for t in teams:
            for idx,t in enumerate(teams):
                rank_table[idx][3] = t.elo
                games = find_all_games(t,total_games)
                for g in games:
                    if t.name == g.home.name:
                        rank_table[idx][1] += g.score_home - g.score_away
                        rank_table[idx][2] += g.score_home
                        if g.score_home > g.score_away:
                            rank_table[idx][0] += 3
                        elif g.score_home == g.score_away:
                            rank_table[idx][0] += 1
                    elif t.name == g.away.name:
                        rank_table[idx][1] += g.score_away - g.score_home
                        rank_table[idx][2] += g.score_away
                        if g.score_home < g.score_away:
                            rank_table[idx][0] += 3
                        elif g.score_home == g.score_away:
                            rank_table[idx][0] += 1
        rank = sorted(range(len(rank_table)),key=lambda i: rank_table[i],reverse=True)
        res:list[Country] = []
        for r in rank:
            res.append(teams[r])
        return res
    
    # 8강 탈락팀 순위비교
    teams_rank += rank_teams(qf_res[1])
    # 16강 탈락팀 순위비교
    teams_rank += rank_teams(ro16_res[1])
    # 32강 탈락팀 순위비교
    teams_rank += rank_teams(ro32_res[1])
    
    # 조별리그 탈락팀 순위비교
    noadv_group = list(range(12))
    for idx in gs_res[4]:
        noadv_group.remove(idx)
    noadv_teams = [gs_res[2][i] for i in noadv_group] + gs_res[3]
    teams_rank += rank_teams(noadv_teams)
    
    return [teams_rank,total_games]

def find_all_games(team:Country, games:list[Game]):
    """팀의 모든 경기 찾기"""
    res:list[Game] = []
    for g in games:
        if team.name == g.home.name or team.name == g.away.name:
            
            res.append(g)
    return res