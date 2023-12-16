
import nltk
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np

# nltk 라이브러리의 필요한 데이터를 다운로드
nltk.download('punkt')
nltk.download('stopwords')

# 문장 간의 유사도를 계산하는 함수
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = set()  # 불용어 목록이 제공되지 않으면 빈 집합으로 초기화

    # 단어 소문자로 변환
    sent1 = [word.lower() for word in sent1]
    sent2 = [word.lower() for word in sent2]

    # 모든 고유한 단어를 모아서 리스트를 생성
    all_words = list(set(sent1 + sent2))

    # 단어의 출현 횟수를 계산
    vector1 = np.array([sent1.count(word) for word in all_words if word not in stopwords])
    vector2 = np.array([sent2.count(word) for word in all_words if word not in stopwords])

    # 코사인 거리를 계산하여 두 문장의 유사도를 반환
    return 1 - cosine_distance(vector1, vector2)

# 문장 간의 유사도 행렬을 생성하는 함수
def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i, sent1 in enumerate(sentences):
        for j, sent2 in enumerate(sentences):
            if i != j and similarity_matrix[j, i] == 0:
                similarity_matrix[i, j] = similarity_matrix[j, i] = sentence_similarity(sent1, sent2, stop_words)

    return similarity_matrix

# 텍스트를 요약하는 함수(top_n=N, N:문장 개수)
def generate_summary(text, top_n=5):
    stop_words = set(stopwords.words('english'))  # 영어 불용어 목록을 불러오기(한글 출력도 가능)
    sentences = sent_tokenize(text)  # 입력 텍스트를 문장으로 분할
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)  # 문장 간의 유사도 행렬을 생성

    # 각 문장의 유사도 합을 계산
    scores = np.sum(sentence_similarity_matrix, axis=1)

    # 상위 N개의 중요한 문장을 선택
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[-top_n:]]

    # 선택된 문장을 결합하여 요약을 생성하고 반환
    return ' '.join(ranked_sentences)

# 텍스트 데이터 로드
with open('사회복지사.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 요약 생성
summary = generate_summary(text)  # 텍스트를 요약
print(summary)  # 요약된 텍스트를 출력
