import requests
from bs4 import BeautifulSoup
import re
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def crawl_daum_news_home(url, keyword=None):
    response = requests.get(url)
    if response.status_code != 200:
        print("페이지를 찾지 못했습니다..ㅜ")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

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

def crawl_daum_news_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("기사를 불러오지 못했습니다...ㅜ")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    article_content = soup.find('div', class_='article_view')
    if article_content:
        content = article_content.get_text()
    else:
        content = "글이 없는 기사 입니다."

    return content

def generate_wordcloud_from_text(text_data):
    text_data = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣\s]", "", text_data)
    okt = Okt()
    tokens = okt.nouns(text_data)
    stopwords = ["을", "를", "이", "가", "은", "는", "의"]
    filtered_tokens = [word for word in tokens if word not in stopwords]
    word_counts = Counter(filtered_tokens)
    wordcloud = WordCloud(font_path="/content/drive/MyDrive/Colab Notebooks/NanumGothic-ExtraBold.ttf", background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    news_url = 'https://news.daum.net/'
    find_keyword = input("검색할 키워드를 입력하세요: ")
    
    all_news_data = []
    news_data = crawl_daum_news_home(news_url, keyword=find_keyword)

    for article in news_data:
        title = article['title'].replace('\n', '').strip()
        article_url = article['link']
        article_content = crawl_daum_news_article(article_url)

        all_news_data.append({
            'title': title,
            'link': article_url,
            'content': article_content.replace('\n', '').strip()
        })

    text_data = str(all_news_data)

    for selected_news in all_news_data:
        generate_wordcloud_from_text(selected_news['content'])
