
from dotenv import load_dotenv
load_dotenv()
import os 


from infra.elasticClient import client
from infra.mysqlClient import dbClient as db
from utils import embeddText
import pandas as pd
import json


df  = pd.read_sql("select * from products where is_active = 1 limit 10", db)
json_response = df.to_dict(orient='records')


for i in range(len(json_response)):
    json_response[i]['complete_text'] = str(json_response[i]['display_name'])  + str(json_response[i]['description']) 
    json_response[i]['complete_text_emb'] = embeddText(json_response[i]['complete_text']).tolist() 
    # print(json_response[i]['complete_text_emb'].shape) # 384 dimensional vector

print(type(json_response))

# # Index data into Elasticsearch
index_name = 'products_index'  # Change to the desired index name

# Index each document into Elasticsearch
for idx, doc in enumerate(json_response):
    client.index(index=index_name, id=idx, body=doc)

print("Data indexed to Elasticsearch.")




def semanticProductSearch(text):
    # Assuming 'embeddText' is a function that returns a dense vector
    query_vector = embeddText(text).tolist()  # Get the query vector
    search_body = {
        ""
          "_source": ["display_name"], 
          "query": {
            "script_score": {
              "query": {
                "match_all": {}
              },
              "script": {
                "source": "cosineSimilarity(params.queryVector, 'complete_text_emb') + 1.0",
                "params": {
                  "queryVector": query_vector
                }
              }
            }
          }
        }

    # Perform the search using the 'search' method
    return client.search(index="products_index", body=search_body)

# print(semanticProductSearch(" i want a safe grill for home"))











