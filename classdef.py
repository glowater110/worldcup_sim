from enum import Enum
from typing import Self

class Continent(Enum):
    UEFA = 0
    CONMEBOL = 1
    CAF = 2
    CONCACAF = 3
    AFC = 4
    OFC = 5

class Country:
    def __init__(self, name=None, abbr=None, cont:Continent=None, elo=None, rank=None):
        self.name = name
        self.abbr = abbr
        self.cont = cont
        self.elo = elo
        self.rank = rank
    def __repr__(self):
        return f'{self.name} ({self.abbr}, {self.elo})'
    def __eq__(self, value):
        return self.name == value.name

class Group:
    def __init__(self, name, len):
        self.name = name
        self.teams = [Country() for _ in range(len)]
        
    def __repr__(self):
        res = f'{self.name} ('
        for team in self.teams:
            res += team.abbr
            if team != self.teams[-1]:
                res += ', '
            else:
                res += ')'
        return res
    
    def is_valid(self, team:Country|Self):
        """국가/대륙PO 적합성 판단"""
        if type(team) == Country:
            return self.is_valid_country(team)
        elif type(team) == Group:
            return self.is_valid_continent(team)
    
    def is_valid_country(self, country:Country):
        """국가 적합성 판단"""
        # UEFA, CONMEBOL, CAF, CONCACAF, AFC, OFC
        limits = self.cont_limit()
        return limits[country.cont.value] > 0
    
    def is_valid_continent(self, group:Self):
        """대륙PO 적합성 판단"""
        # UEFA, CONMEBOL, CAF, CONCACAF, AFC, OFC
        counts = group.cont_count()
        limits = self.cont_limit()
        return all(c <= l for c, l in zip(counts, limits))

    def remaining_seats(self):
        """남는 자리를 배열로 전달"""
        res = []
        for idx, team in enumerate(self.teams):
            if team.name == None:
                res.append(idx)
        return res
    
    def alloc(self, country:Country, pos):
        """빈 자리에 국가 할당"""
        self.teams[pos] = country
    
    def cont_limit(self):
        """대륙별 남는 자리 계산"""
        limits = [2,1,1,1,1,1]
        rem_seat = 4
        for team in self.teams:
            if type(team) == Country:
                if team.cont != None:
                    rem_seat -= 1
                    limits[team.cont.value] -= 1
            if type(team) == Group:
                limits = [l - c for l,c in zip(limits,team.cont_count())]
        for i in range(len(limits)):
            limits[i] = min(limits[i],rem_seat)
        return limits
    
    def cont_count(self):
        """그룹이 포함하는 대륙 반환"""
        res = [0,0,0,0,0,0]
        for t in self.teams:
            if type(t) == Country:
                if t.cont != None:
                    res[t.cont.value] = 1
            if type(t) == Group:
                for t2 in t.teams:
                    res[t2.cont.value] = 1
        return res
    
    def cont_count2(self):
        """그룹에 들어있는 각 대륙별 국가 수 반환"""
        res = [0,0,0,0,0,0]
        for t in self.teams:
            if type(t) == Country:
                if t.cont != None:
                    res[t.cont.value] += 1
            if type(t) == Group:
                res = [r+c for r,c in zip(res,t.cont_count())]
        return res

class Game:
    def __init__(self, name, home:Country, away:Country, score_home:int, score_away:int, aet = False, penalty_home=0, penalty_away=0):
        self.name = name
        self.home = home
        self.away = away
        self.score_home = score_home
        self.score_away = score_away
        self.aet = aet
        self.penalty_home = penalty_home
        self.penalty_away = penalty_away
    
    def __repr__(self):
        if self.aet == False:
            return f'🚩 {self.name} - {self.home} {self.score_home} vs {self.score_away} {self.away}'
        else:
            if self.score_home != self.score_away:
                return f'🚩 {self.name} - {self.home} {self.score_home} vs {self.score_away} (a.e.t) {self.away}'
            else:
                return f'🚩 {self.name} - {self.home} {self.score_home} ({self.penalty_home}) vs ({self.penalty_away}) {self.score_away} (a.e.t) {self.away}'