import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

 

number=[]
name=[]
position=[]
age=[]
nation=[]
club=[]
value=[]

#1부터 4페이지까지 반복
for i in range(1, 5):
    Headers ={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    # page에 i가 1부터 4까지 차례로 들어간다.
    url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}'
    r = requests.get(url, headers=Headers)
    soup = bs(r.text, 'html.parser')
    player_info = soup.find_all('tr', class_= ['odd', 'even'])

    for info in player_info:
        player= info.find_all('td')
        number.append(player[0].text)
        name.append(player[3].text)
        position.append(player[4].text)
        age.append(player[5].text)
        nation_temp=[]
        for i in player[6].find_all('img'):
            nation_temp.append(i['title'])
        nation.append(' '.join(nation_temp))
        club.append(player[7].img['title'])
        value.append(player[8].text.strip())
    time.sleep(1)

df_100 = pd.DataFrame(
    {'number':number,
     'name':name,
     'position':position,
     'age':age,
     'nation':nation,
     'club':club,
     'value':value
    })
df_100

df_100.to_csv('player100.csv', index=False)

def find_player_info(player_name):
    player_row = df_100[df_100['name'] == player_name]
    if player_row.empty:
        return "선수를 찾을 수 없습니다."
    else:
        return player_row[['number', 'age', 'position','nation', 'club', 'value']].to_string(index=False)

while True:
    player_name = input("선수명을 입력하세요 (종료하려면 '종료' 입력): ")
    if player_name == '종료':
        break
    else:
        player_info = find_player_info(player_name)
        print(player_info)
