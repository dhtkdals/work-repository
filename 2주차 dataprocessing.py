from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
import requests
from bs4 import BeautifulSoup

# 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'  # 한글 폰트 파일 경로

# 네이버 IT 기사 페이지 URL
url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"

# 페이지 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 기사 제목을 담을 리스트
titles = []


article_tags = soup.select('.cluster_text a')  # 예시 태그 및 클래스

for article_tag in article_tags:
    title = article_tag.get_text(strip=True)  # 공백 제거
    titles.append(title)


# KoNLPy를 사용하여 명사 추출
okt = Okt()
nouns = []
for title in titles:
    nouns += okt.nouns(title)

# 명사 빈도수 체크
noun_counter = Counter(nouns)

# WordCloud 생성
wordcloud = WordCloud(
    font_path=font_path,  # 한글 폰트 경로 지정
    background_color='white',
    width=800,
    height=400,
    stopwords=STOPWORDS,
)

# 단어 빈도 데이터를 WordCloud에 넣고 생성
wordcloud.generate_from_frequencies(noun_counter)

# 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
