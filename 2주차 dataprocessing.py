import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Daum 뉴스 URL
news_url = 'https://news.daum.net/'

# Daum 뉴스 크롤링 함수
def crawl_daum_news_home(url, keyword=None):
    response = requests.get(url)
    if response.status_code != 200:
        print("페이지를 찾지 못했습니다")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # 뉴스 제목, 링크 불러오기
    news_articles = []
    article_tags = soup.find_all('strong', class_='tit_g')
    for tag in article_tags:
        article_title = tag.get_text().strip()
        article_link = tag.a['href']
        if keyword is None or keyword.lower() in article_title.lower():
            article = {
                'title': article_title,
                'link': article_link
            }
            news_articles.append(article)

    return news_articles

# Konlpy Okt를 사용하여 텍스트 토큰화
def tokenize_text(text):
    okt = Okt()
    tokens = okt.nouns(text)
    return tokens

# 불용어 제거
def remove_stopwords(tokens):
    stopwords = ["을", "를", "이", "가", "은", "는", "의"]
    return [word for word in tokens if word not in stopwords]

# 메인 함수
def main():
    # 사용자로부터 검색 키워드 입력 받기
    find_keyword = input("검색할 키워드를 입력하세요: ")

    # Daum 뉴스 크롤링
    news_data = crawl_daum_news_home(news_url, keyword=find_keyword)

    # 뉴스 기사 텍스트 데이터 모으기
    text_data = ""
    for article in news_data:
        article_url = article['link']
        article_content = crawl_daum_news_article(article_url)
        text_data += article_content

    # 텍스트 데이터 정제 (특수 문자 및 숫자 제거)
    text_data = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text_data)

    # 텍스트 토큰화 및 불용어 제거
    tokens = tokenize_text(text_data)
    filtered_tokens = remove_stopwords(tokens)

    # 단어 빈도수 카운트
    word_counts = Counter(filtered_tokens)

    # 워드 클라우드 생성
    wordcloud = WordCloud(font_path="/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf", background_color='white').generate_from_frequencies(word_counts)


    # 워드 클라우드 시각화
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
