# 1주차 크롤링

## 크롤링 한 사이트와 이유 : Transfermarkt
평소에도 축구에 관심이 많아 축구 선수 시장 가치 사이트인 Transfermarkt을 크롤링 해보고 싶었음.

### 코드 목적
Transfermarkt 웹사이트에서 Transfermarkt의 가치가 가장 높은 상위 100명의 선수에 대한 축구 선수 데이터를 크롤링하여 가져옴. 이 정보를 CSV 파일에 저장하며, 사용자가 선수를 검색할 수 있는 간단한 인터페이스를 제공함.

## 코드 설명

    import requests
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import time
requests, BeautifulSoup, pandas, time 등 필요한 라이브러리를 임포트함.


    number = []
    name = []
    position = []
    age = []
    nation = []
    club = []
    value = []
데이터를 저장할 리스트를 초기화, 각 리스트는 스크레이핑한 데이터의 특정 부분을 저장.

    for i in range(1, 5):
        Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}'
        r = requests.get(url, headers=Headers)
        soup = bs(r.text, 'html.parser')
1에서 4페이지까지 반복하며, HTTP 요청을 보내고 웹 페이지를 파싱함. User-Agent 헤더를 사용하여 컴퓨터가 아니라 사람인 척 함.


    player_info = soup.find_all('tr', class_=['odd', 'even'])
플레이어 정보가 들어있는 행을 찾음. 'odd' 또는 'even' 클래스를 가진 모든 행을 가져옴.


    for info in player_info:
        player = info.find_all('td')
        number.append(player[0].text)
        name.append(player[3].text)
        position.append(player[4].text)
        age.append(player[5].text)
각 행에서 필요한 정보를 추출, 해당 정보를 미리 초기화한 리스트에 추가.


    nation_temp = []
    for i in player[6].find_all('img'):
        nation_temp.append(i['title'])
        nation.append(' '.join(nation_temp))
        club.append(player[7].img['title'])
        value.append(player[8].text.strip())
국적 정보와 클럽 정보를 추출, 리스트에 추가.


    time.sleep(1)
각 페이지 요청 사이에 1초의 지연을 생성하여 서버에 부하를 줄입니다.


    df_100 = pd.DataFrame(
        {'number': number,
         'name': name,
         'position': position,
         'age': age,
         'nation': nation,
         'club': club,
         'value': value
         })
데이터를 데이터프레임으로 변환.


    df_100.to_csv('player100.csv', index=False)
데이터프레임을 CSV 파일로 저장.


    def find_player_info(player_name):
        player_row = df_100[df_100['name'] == player_name]
        if player_row.empty:
            return "선수를 찾을 수 없습니다."
        else:
            return player_row[['number', 'age', 'position', 'nation', 'club', 'value']].to_string(index=False)
사용자가 입력한 선수명을 받아 해당 선수의 정보를 찾아주는 함수를 정의.


    while True:
        player_name = input("선수명을 입력하세요 (종료하려면 '종료' 입력): ")
        if player_name == '종료':
            break
        else:
            player_info = find_player_info(player_name)
            print(player_info)
사용자에게 선수명을 입력받고, 종료를 원할 경우 '종료'를 입력. 그렇지 않은 경우 입력된 선수의 정보를 출력.

# 어려웠던 점
첫 과제이니 만큼 많은 시간을 공들여서 하였고 선수 중 이중 국적을 가진 선수에 국적을 나타낼때 오류가 생김.(해결)
csv 파일을 엑셀에서 열었을때 선수 명이 꺠지는 현상이 발생함.(해결)


