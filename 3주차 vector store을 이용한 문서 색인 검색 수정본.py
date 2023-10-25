import pandas as pd
df = pd.read_csv("./kdrama.csv")

filter_df = df.drop(["Aired Date","Aired On","Duration","Content Rating","Production companies", "Rank"], axis=1);

import chromadb
client = chromadb.PersistentClient(path="../data")

collection = client.get_or_create_collection(
    name="k-drama",
    metadata={"hnsw:space": "cosine"}
)

# 데이터 준비
# 인덱스
ids = []
# 메타데이터
doc_meta = []
# 벡터로 변환 저장할 텍스트 데이터로 ChromaDB에 Embedding 데이터가 없으면 자동으로 벡터로 변환해서 저장한다고 한다. 
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

# DB 저장
collection.add(
    documents=documents,
    metadatas=doc_meta,
    ids=ids
)
# DB 쿼리
collection.query(
    query_texts=["medical drama about doctors"],
    n_results=5,
)
