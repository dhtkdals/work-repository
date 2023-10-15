from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np


with open('대한민국헌법.txt', 'r', encoding='utf-8') as f:
    text = f.read()


okt = Okt()
nouns = okt.nouns(text)  # 명사만 추출

# 폰트 설정
plt.rc('font', family='NanumBarunGothic')

words = [n for n in nouns if len(n) > 1]  # 단어의 길이가 1개인 것은 제외


c = Counter(words)  # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함



# 워드클라우드 생성
wc = WordCloud(width=400, height=400, scale=2.0, max_font_size=300)
gen = wc.generate_from_frequencies(c)



# 시각화
plt.figure()
plt.imshow(gen)
plt.axis("off")
plt.show()
