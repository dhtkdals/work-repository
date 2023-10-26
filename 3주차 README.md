# 3주차 Vector store을 이용한 문서 색인&검

## 소개
ChromaDB를 활용하여 K-Drama(한국 드라마) 추천 시스템을 구현함. 사용자가 특정 키워드를 입력하면 관련 K-Drama를 추천받을 수 있다. 
(21년의 한국 드라마 데이터로 구성되어있음)

### 순서

●라이브러리 가져오기

       import pandas as pd
       import chromadb    
이 프로젝트를 시작하려면 먼저 필요한 라이브러리를 가져와야 함. pandas는 데이터 처리에 사용되고, chromadb는 ChromaDB를 활용하기 위한 라이브러리임.

●K-Drama 데이터셋 불러오기

    df = pd.read_csv("./kdrama.csv") 
이 프로젝트는 "kdrama.csv"라는 이름의 CSV 파일에 있는 K-Drama 데이터를 사용함. 이 코드는 해당 데이터를 Pandas DataFrame으로 불러옵.

●데이터 필터링

    filter_df = df.drop(["Aired Date", "Aired On", "Duration", "Content Rating", "Production companies", "Rank"], axis=1)
불필요한 열을 제거한 DataFrame. 이 DataFrame은 추천 시스템에서 사용됨.

●ChromaDB 초기화

    client = chromadb.PersistentClient(path="../data")
ChromaDB를 사용하기 위해 ChromaDB 클라이언트를 초기화합니다. 데이터 경로를 지정하여 ChromaDB를 설정합니다.

●컬렉션 생성

    collection = client.get_or_create_collection(
        name="k-drama",
        metadata={"hnsw:space": "cosine"}
    )
ChromaDB에서 데이터를 저장할 "k-drama"라는 이름의 컬렉션을 생성. 메타데이터 공간은 "cosine"으로 설정.

 ●데이터 준비
 
    ids = []
    doc_meta = []
    documents = []

    for idx in range(len(filter_df)):
        item = filter_df.iloc[idx]
       id = item['Name'].lower().replace(' ','-')
        document = f"{item['Name']}: {item['Synopsis']} : {str(item['Cast']).strip().lower()} : {str(item['Genre']).strip().lower()}"
        meta = {
            "rating" : item['Rating']
        }
    
         ids.append(id)
         doc_meta.append(meta)
         documents.append(document)


 ●ChromaDB에 데이터 저장
 
      collection.add(
       documents=documents,
       metadatas=doc_meta,
        ids=ids
    )

 ●ChromaDB 쿼리
 
     results = collection.query(
        query_texts=["medical drama about doctor"],
        n_results=5
    )




 ## 결과 : 분명 됐다가 다시 코랩에서 실행시키니 결과가 나오지 않는다..
