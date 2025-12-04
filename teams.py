from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import gzip
import pickle
from pathlib import Path
from classdef import Continent,Country

def crawl_data(verbose=False):
    """FIFA 공식 홈페이지에 접근해서 랭킹 데이터 추출"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if verbose:
        print('Accessing website...')
    driver.get('https://inside.fifa.com/fifa-world-ranking/men')

    time.sleep(5)

    if verbose:
        print('Scanning network requests...')

    target_data = None
    for request in driver.requests:
        if request.response:
            if 'ranking-overview' in request.url:
                if verbose:
                    print(f'\nFound API request: {request.url}')
                
                body_bytes = request.response.body
                
                try:
                    body_str = gzip.decompress(body_bytes).decode('utf-8')
                except:
                    body_str = body_bytes.decode('utf-8')
                
                try:
                    target_data = json.loads(body_str)
                    if verbose:
                        print('Data Sniffing Successful')
                    break
                except:
                    print('JSON conversion failed')
    driver.quit()
    
    if target_data:
        if verbose:
            print(f'\nData Key List: {target_data.keys()}')
        items = target_data.get('rankings', [])
        if verbose:
            print(f'Get data for a total of {len(items)} countries')
        return items
    else:
        print('The desired API request was not found')
        return None

def reconst_data(items):
    """읽어온 데이터를 형식에 맞게 가공"""
    teams = []
    for item in items:        
        teams.append(Country(item['rankingItem']['name'],item['rankingItem']['countryCode'],Continent[item['tag']['text']],item['rankingItem']['totalPoints'],item['rankingItem']['rank']))
    return teams

def save_data(teams):
    """생성한 Country 객체를 딕셔너리 형태로 저장"""
    file_path = Path(__file__).parent / 'team_data.pkl'
    with open(file_path, "wb") as f:
        pickle.dump(teams, f)

def load_data():
    file_path = Path(__file__).parent / 'team_data.pkl'
    with open(file_path, "rb") as f:
        return pickle.load(f)

def find_team(teams:list[Country],name):
    for team in teams:
        if name == team.name:
            return team
    print('ERROR - Cannot find a matching team')