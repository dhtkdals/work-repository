# Transfermarkt 선수 데이터 웹 스크레이퍼

## 소개

이 Python 스크립트는 Transfermarkt 웹사이트에서 축구 선수 데이터를 스크레이핑하여 가져오는 프로그램입니다. 이 코드는 코드 작성자가 Transfermarkt의 가치가 가장 높은 상위 100명의 선수에 대한 정보를 스크레이핑하고, 이 정보를 CSV 파일에 저장하며, 사용자가 선수를 검색할 수 있는 간단한 인터페이스를 제공합니다.

## 코드 설명


    import requests
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import time
requests, BeautifulSoup, pandas, time 등 필요한 라이브러리를 임포트합니다.

    number = []
    name = []
    position = []
    age = []
    nation = []
    club = []
    value = []
데이터를 저장할 리스트를 초기화합니다. 각 리스트는 스크레이핑한 데이터의 특정 부분을 저장합니다.

    for i in range(1, 5):
        Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        url = f'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page={i}'
        r = requests.get(url, headers=Headers)
        soup = bs(r.text, 'html.parser')
1에서 4페이지까지 반복하며, HTTP 요청을 보내고 웹 페이지를 파싱합니다. User-Agent 헤더를 사용하여 웹 브라우저처럼 동작하도록 합니다.

    player_info = soup.find_all('tr', class_=['odd', 'even'])
플레이어 정보가 들어있는 행을 찾습니다. 'odd' 또는 'even' 클래스를 가진 모든 행을 가져옵니다.

    for info in player_info:
        player = info.find_all('td')
        number.append(player[0].text)
        name.append(player[3].text)
        position.append(player[4].text)
        age.append(player[5].text)
각 행에서 필요한 정보를 추출하고, 해당 정보를 미리 초기화한 리스트에 추가합니다.

    nation_temp = []
    for i in player[6].find_all('img'):
        nation_temp.append(i['title'])
        nation.append(' '.join(nation_temp))
        club.append(player[7].img['title'])
        value.append(player[8].text.strip())
국적 정보와 클럽 정보를 추출하고, 리스트에 추가합니다.

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
데이터를 데이터프레임으로 변환합니다.

    df_100.to_csv('player100.csv', index=False)
데이터프레임을 CSV 파일로 저장합니다.

    def find_player_info(player_name):
        player_row = df_100[df_100['name'] == player_name]
        if player_row.empty:
            return "선수를 찾을 수 없습니다."
        else:
            return player_row[['number', 'age', 'position', 'nation', 'club', 'value']].to_string(index=False)
사용자가 입력한 선수명을 받아 해당 선수의 정보를 찾아주는 함수를 정의합니다.

    while True:
        player_name = input("선수명을 입력하세요 (종료하려면 '종료' 입력): ")
        if player_name == '종료':
            break
        else:
            player_info = find_player_info(player_name)
            print(player_info)
사용자에게 선수명을 입력받고, 종료를 원할 경우 '종료'를 입력합니다. 그렇지 않은 경우 입력된 선수의 정보를 출력합니다.

#주의사항
웹 스크래핑 에티켓: 웹 스크래핑은 웹사이트의 이용 약관을 준수해야 합니다. Transfermarkt의 정책을 확인하고 준수해야 합니다.

웹사이트 변경: Transfermarkt 웹사이트의 구조가 변경될 경우 코드가 작동하지 않을 수 있습니다. 주기적인 유지보수가 필요할 수 있습니다.

데이터 정확성: 웹 스크래핑은 웹 페이지의 구조에 의존합니다. 구조가 변경되거나 누락된 또는 잘못된 데이터가 있을 경우 오류가 발생할 수 있습니다.

요청 속도 제한: 서버에 너무 빈번한 요청을 보내는 것을 피하기 위해 요청 사이에 지연을 넣었습니다. 이 지연을 줄이거나 짧은 시간 내에 너무 많은 요청을 보내면 IP 주소가 차단될 수 있습니다.

입력 유효성 검사: 사용자 입력값을 검증하고 방어적인 프로그래밍을 통해 보안 취약점을 방지하십시오.

go
