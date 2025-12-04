import numpy as np
from scipy.stats import poisson
from classdef import Country

avg_goal = 1.344        # 2022 월드컵 경기 당 득점평균 = 1.344
elo_scale = 600

def calc_win_prob_elo(elo_a, elo_b):
    """Elo 기반 A의 승률 계산"""
    elo_diff = elo_a - elo_b
    return 1 / (10**(-elo_diff/elo_scale)+1)

def calc_xg_coeff(avg_goal, elo_diff, verbose=False):
    """Elo 100점 차이 당 평균득점 차이 계산"""
    # 가정1: 모든 득점은 독립적 사건
    # 가정2: Elo 차이와 xG 차이는 비례관계
    win_exp = calc_win_prob_elo(elo_diff,0)    # Elo 기반 예측 승률
    xG_coeff = 0                            # Elo 100점에 따른 xG 변동
    iter_val = 0.5                          # xG_coeff 변화값
    stop_iter = False
    while stop_iter == False:
        avg_goal_a = np.exp(np.log(avg_goal) + xG_coeff * elo_diff/100)
        avg_goal_b = np.exp(np.log(avg_goal) - xG_coeff * elo_diff/100)
        goal_a = [poisson.pmf(a,avg_goal_a) for a in range(11)]
        goal_b = [poisson.pmf(b,avg_goal_b) for b in range(11)]
        a_win = 0
        b_win = 0
        for a in range(11):
            for b in range(11):
                if a > b:
                    a_win += goal_a[a]*goal_b[b]
                elif a < b:
                    b_win += goal_a[a]*goal_b[b]
        win_prob = a_win/(a_win+b_win)
        win_prob_diff = (win_prob - win_exp)
        if elo_diff < 0:
            win_prob_diff *= -1 
        if verbose:
            print(f'Current xG_coeff = {xG_coeff}')
            print(f'Win Probability (by Poisson) : {win_prob}')
            print(f'Win Probability (by Elo) : {win_exp}')
        if win_prob_diff > 0.00001:     # 예상보다 승률이 높음 -> 득점차이 너프
            xG_coeff -= iter_val
        elif win_prob_diff < -0.00001:  # 예상보다 승률이 낮음 -> 득점차이 버프
            xG_coeff += iter_val
        else:                           # 얼추 승률이 비슷함 -> 득점차이 고정
            stop_iter = True
        iter_val *= 0.5                 # 매 iteration마다 간격 0.5씩 감소
    return xG_coeff

def result_prob(elo_a, elo_b, score_a, score_b):
    """주어진 Elo에서 해당 점수가 나올 확률"""
    elo_diff = elo_a - elo_b
    xG_coeff = calc_xg_coeff(avg_goal,elo_diff)
    xG_a = np.exp(np.log(avg_goal) + xG_coeff * elo_diff/100)
    xG_b = np.exp(np.log(avg_goal) - xG_coeff * elo_diff/100)
    return poisson.pmf(score_a,xG_a) * poisson.pmf(score_b,xG_b)

def score_prob(country_a:Country, country_b:Country):
    """Elo에 따른 스코어가 나올 확률을 표로 정리"""
    print(f'{country_a.abbr}\{country_b.abbr}',end='\t')
    for idx in range(11):
        print(f'{idx:5d}',end='\t')
    print('')
    for score_a in range(11):
        print(f'{score_a:4d}',end='\t')
        for score_b in range(11):
            print(f'{result_prob(country_a.elo,country_b.elo,score_a,score_b):7.3f}',end='\t')
        print('')

def wdl_prob(elo_a, elo_b):
    """Elo에 따른 승무패 확률"""
    win = 0
    draw = 0
    lose = 0
    for score_a in range(11):
        for score_b in range(11):
            if score_a > score_b:
                win += result_prob(elo_a,elo_b,score_a,score_b)
            elif score_a < score_b:
                lose += result_prob(elo_a,elo_b,score_a,score_b)
            else:
                draw += result_prob(elo_a,elo_b,score_a,score_b)
    return [win, draw, lose]

def gen_game_result(country_a:Country, country_b:Country):
    """랜덤 결과 생성"""
    elo_diff = country_a.elo - country_b.elo
    xG_coeff = calc_xg_coeff(avg_goal,elo_diff)
    xG_a = np.exp(np.log(avg_goal) + xG_coeff * elo_diff/100)
    xG_b = np.exp(np.log(avg_goal) - xG_coeff * elo_diff/100)
    score_a = np.random.poisson(xG_a)
    score_b = np.random.poisson(xG_b)
    return [score_a, score_b]

def gen_game_result_aet(country_a:Country, country_b:Country):
    """랜덤 결과 생성(연장전)"""
    elo_diff = country_a.elo - country_b.elo
    xG_coeff = calc_xg_coeff(avg_goal/3,elo_diff)
    xG_a = np.exp(np.log(avg_goal/3) + xG_coeff * elo_diff/100)
    xG_b = np.exp(np.log(avg_goal/3) - xG_coeff * elo_diff/100)
    score_a = np.random.poisson(xG_a)
    score_b = np.random.poisson(xG_b)
    return [score_a, score_b]

def shootout_battlefield(a_succ, b_succ, kick_order, turn):
    """승부차기 승부처 계산"""
    # 승리 승부처 : 1 / 패배 승부처 : 2
    if kick_order <= 5:
        if turn == 0:
            if a_succ > b_succ:
                if a_succ-b_succ == 6-kick_order:
                    return 1
            elif a_succ < b_succ:
                if b_succ-a_succ == 6-kick_order:
                    return 2
        else:
            if a_succ > b_succ:
                if a_succ-b_succ == 6-kick_order:
                    return 2
            elif a_succ <= b_succ:
                if b_succ-a_succ == 5-kick_order:
                    return 1
    else:
        if turn == 1:
            if a_succ > b_succ:
                return 2
            elif a_succ == b_succ:
                return 1
    return 0

def shootout(verbose=False):
    """승부차기 시뮬레이션"""
    a_succ = 0
    b_succ = 0
    kick_order = 1
    while kick_order <= 5:
        quick_over = False
        for turn in range(2):
            # 승부차기 기본 성공률 75%
            succ_rate = 0.75
            # 1~2번 키커는 +5%p
            if kick_order < 3:
                succ_rate += 0.05
            # 4~5번 키커는 -5%p
            elif kick_order > 3:
                succ_rate -= 0.05
            
            # 조기종료 Flag
            quick_over_win = False
            quick_over_lose = False
            
            match shootout_battlefield(a_succ,b_succ,kick_order,turn):
                case 1:
                    # 승리 승부처에서 +15%p
                    succ_rate += 0.15
                    quick_over_win = True
                case 2:
                    # 패배 승부처에서 -10%p
                    succ_rate -= 0.15
                    quick_over_lose = True
            
            val = np.random.rand()
            if val <= succ_rate:
                if turn == 0:
                    a_succ += 1
                    if verbose:
                        print(f'1st mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Success ({a_succ} - {b_succ})')
                else:
                    b_succ += 1
                    if verbose:
                        print(f'2nd mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Success ({a_succ} - {b_succ})')
                if quick_over_win:
                    quick_over = True
                    break
            else:
                if verbose:
                    if turn == 0:
                        print(f'1st mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Failed ({a_succ} - {b_succ})')
                    else:
                        print(f'2nd mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Failed ({a_succ} - {b_succ})')
                if quick_over_lose:
                    quick_over = True
                    break
        if quick_over:
            break
        kick_order += 1
    while a_succ == b_succ:
        # 6번 키커 이후는 -10%p (65%)
        succ_rate = 0.65
        for turn in range(2):
            match shootout_battlefield(a_succ,b_succ,kick_order,turn) == 1:
                case 1:
                    # 승리 승부처에서 +15%p
                    succ_rate += 0.15
                case 2:
                    # 패배 승부처에서 -10%p
                    succ_rate -= 0.1
            val = np.random.rand()
            if val <= succ_rate:
                if turn == 0:
                    a_succ += 1
                    if verbose:
                        print(f'1st mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Success ({a_succ} - {b_succ})')
                else:
                    b_succ += 1
                    if verbose:
                        print(f'2nd mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Success ({a_succ} - {b_succ})')
            else:
                if verbose:
                    if turn == 0:
                        print(f'1st mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Failed ({a_succ} - {b_succ})')
                    else:
                        print(f'2nd mover Player {kick_order} (Success% {np.round(succ_rate*100,0)} : Failed ({a_succ} - {b_succ})')
        kick_order += 1
    if verbose:
        print(f'\nRESULT : {a_succ} - {b_succ}\n')
    return [a_succ,b_succ]

def sim_game(group_name, country_a:Country, country_b:Country, verbose=False):
    """경기 진행 및 결과 출력"""
    res = gen_game_result(country_a,country_b)
    if verbose:
        print(f'🚩 {group_name} - {country_a} {res[0]} vs {res[1]} {country_b}')
    return res

def sim_game_penalty(group_name, country_a:Country, country_b:Country, verbose=False):
    """경기 진행 및 결과 출력(승부차기)"""
    res = gen_game_result(country_a,country_b)
    so_res = None
    aet = False
    if res[0] == res[1]:
        aet = True
        # 동점 -> 연장전 진행
        aet_res = gen_game_result_aet(country_a,country_b)
        res = [r + a for r,a in zip(res,aet_res)]
        if res[0] == res[1]:
            # 코인 토스로 선축/후축 정함
            # 통계적 의미는 없다만 현실성을 높이기 위해 추가함
            # shootout 함수에는 팀을 특정하는 기능이 없으므로 단순히 결과를 뒤집어서 구현
            so_res = shootout()
            if np.random.randint(0,2) == 1:
                so_res = so_res[::-1]
    if aet == False:
        if verbose:
            print(f'🚩 {group_name} - {country_a} {res[0]} vs {res[1]} {country_b}')
        return res
    elif so_res == None:
        if verbose:
            print(f'🚩 {group_name} - {country_a} {res[0]} vs {res[1]} (a.e.t) {country_b} ')
        return res + [aet]
    else:
        if verbose:
            print(f'🚩 {group_name} - {country_a} {res[0]} ({so_res[0]}) vs ({so_res[1]}) {res[1]} (a.e.t) {country_b}')
        return res + [aet] + so_res