import copy
import networkx as nx
import numpy as np
from pulp import LpProblem,LpMaximize,LpVariable,lpSum,PULP_CBC_CMD,LpStatus
from classdef import Continent,Country,Group
from teams import find_team

def ic_po_real(teams:list[Country]):
    """대륙 PO 조 추첨 실제 결과"""
    icpo1 = Group('ICPO Pathway 1',3)
    icpo1.alloc(find_team(teams,'Congo DR'),0)
    icpo1.alloc(find_team(teams,'New Caledonia'),1)
    icpo1.alloc(find_team(teams,'Jamaica'),2)

    icpo2 = Group('ICPO Pathway 2',3)
    icpo2.alloc(find_team(teams,'Iraq'),0)
    icpo2.alloc(find_team(teams,'Bolivia'),1)
    icpo2.alloc(find_team(teams,'Suriname'),2)
    
    return [icpo1,icpo2]

def uefa_po_real(teams:list[Country]):
    """UEFA PO 패스 추첨 실제 결과"""
    uefa1 = Group('UEFA Path A',4)
    uefa1.alloc(find_team(teams,'Italy'),0)
    uefa1.alloc(find_team(teams,'Wales'),1)
    uefa1.alloc(find_team(teams,'Bosnia and Herzegovina'),2)
    uefa1.alloc(find_team(teams,'Northern Ireland'),3)

    uefa2 = Group('UEFA Path B',4)
    uefa2.alloc(find_team(teams,'Ukraine'),0)
    uefa2.alloc(find_team(teams,'Poland'),1)
    uefa2.alloc(find_team(teams,'Albania'),2)
    uefa2.alloc(find_team(teams,'Sweden'),3)

    uefa3 = Group('UEFA Path C',4)
    uefa3.alloc(find_team(teams,'Türkiye'),0)
    uefa3.alloc(find_team(teams,'Slovakia'),1)
    uefa3.alloc(find_team(teams,'Kosovo'),2)
    uefa3.alloc(find_team(teams,'Romania'),3)

    uefa4 = Group('UEFA Path D',4)
    uefa4.alloc(find_team(teams,'Denmark'),0)
    uefa4.alloc(find_team(teams,'Czechia'),1)
    uefa4.alloc(find_team(teams,'Republic of Ireland'),2)
    uefa4.alloc(find_team(teams,'North Macedonia'),3)
    
    return [uefa1,uefa2,uefa3,uefa4,False,True,False,False]

def worldcup_gs_real(teams:list[Country], uefa_po, ic_po):
    """월드컵 조 추첨 실제 결과"""
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
    
    groups[0].alloc(find_team(teams,'Mexico'),0)
    groups[0].alloc(find_team(teams,'South Africa'),1)
    groups[0].alloc(find_team(teams,'Korea Republic'),2)
    groups[0].alloc(uefa_po[3],3)
    
    groups[1].alloc(find_team(teams,'Canada'),0)
    groups[1].alloc(uefa_po[0],1)
    groups[1].alloc(find_team(teams,'Qatar'),2)
    groups[1].alloc(find_team(teams,'Switzerland'),3)
    
    groups[2].alloc(find_team(teams,'Brazil'),0)
    groups[2].alloc(find_team(teams,'Morocco'),1)
    groups[2].alloc(find_team(teams,'Haiti'),2)
    groups[2].alloc(find_team(teams,'Scotland'),3)
    
    groups[3].alloc(find_team(teams,'USA'),0)
    groups[3].alloc(find_team(teams,'Paraguay'),1)
    groups[3].alloc(find_team(teams,'Australia'),2)
    groups[3].alloc(uefa_po[2],3)
    
    groups[4].alloc(find_team(teams,'Germany'),0)
    groups[4].alloc(find_team(teams,'Curaçao'),1)
    groups[4].alloc(find_team(teams,'Côte d\'Ivoire'),2)
    groups[4].alloc(find_team(teams,'Ecuador'),3)
    
    groups[5].alloc(find_team(teams,'Netherlands'),0)
    groups[5].alloc(find_team(teams,'Japan'),1)
    groups[5].alloc(uefa_po[1],2)
    groups[5].alloc(find_team(teams,'Tunisia'),3)
    
    groups[6].alloc(find_team(teams,'Belgium'),0)
    groups[6].alloc(find_team(teams,'Egypt'),1)
    groups[6].alloc(find_team(teams,'IR Iran'),2)
    groups[6].alloc(find_team(teams,'New Zealand'),3)
    
    groups[7].alloc(find_team(teams,'Spain'),0)
    groups[7].alloc(find_team(teams,'Cabo Verde'),1)
    groups[7].alloc(find_team(teams,'Saudi Arabia'),2)
    groups[7].alloc(find_team(teams,'Uruguay'),3)
    
    groups[8].alloc(find_team(teams,'France'),0)
    groups[8].alloc(find_team(teams,'Senegal'),1)
    groups[8].alloc(ic_po[1],2)
    groups[8].alloc(find_team(teams,'Norway'),3)
    
    groups[9].alloc(find_team(teams,'Argentina'),0)
    groups[9].alloc(find_team(teams,'Algeria'),1)
    groups[9].alloc(find_team(teams,'Austria'),2)
    groups[9].alloc(find_team(teams,'Jordan'),3)
    
    groups[10].alloc(find_team(teams,'Portugal'),0)
    groups[10].alloc(ic_po[0],1)
    groups[10].alloc(find_team(teams,'Uzbekistan'),2)
    groups[10].alloc(find_team(teams,'Colombia'),3)
    
    groups[11].alloc(find_team(teams,'England'),0)
    groups[11].alloc(find_team(teams,'Croatia'),1)
    groups[11].alloc(find_team(teams,'Ghana'),2)
    groups[11].alloc(find_team(teams,'Panama'),3)
    
    return groups