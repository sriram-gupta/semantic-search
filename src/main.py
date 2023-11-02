
from dotenv import load_dotenv
load_dotenv()
import os 


from infra.elasticClient import client
from infra.mysqlClient import dbClient as db
from utils import embeddText
import pandas as pd
import pymysql
import json


def indexAllProductsToEs():
  cursor = db.cursor(pymysql.cursors.DictCursor) 
  # Define batch size
  batch_size = 1000  # Choose an appropriate batch size

  # Fetch products in smaller batches using a cursor
  query = "SELECT * FROM products WHERE is_active = 1"
  cursor.execute(query)


  while True:
      products_batch = cursor.fetchmany(batch_size)
      if not products_batch:
          break

      # Process the batch of products
      for product in products_batch:
          # print(product)
          # Assuming the 'embeddText' function returns a dense vector
          complete_text = str(product['display_name']) + str( product['description'])
          complete_text_emb = embeddText(complete_text).tolist()

          # Index each product into Elasticsearch
          index_name = 'products_index'  # Change to the desired index name
          product['complete_text_emb'] = complete_text_emb

          # Index the product document into Elasticsearch
          client.index(index=index_name, body=product)

  # Close the cursor and database connection
  cursor.close()




def semanticProductSearch(text):
    # Assuming 'embeddText' is a function that returns a dense vector
    query_vector = embeddText(text).tolist()  # Get the query vector
    search_body = {
        "size": 10,
          "_source": ["display_name", "description"], 
          "query": {
            "script_score": {
              "query": {
                "match_all": {}
              },
              "script": {
                "source": "cosineSimilarity(params.queryVector, 'complete_text_emb') + 10.0",
                "params": {
                  "queryVector": query_vector
                }
              }
            }
          }
        }

    # Perform the search using the 'search' method
    return client.search(index="products_index", body=search_body)

print(semanticProductSearch("video game for kids"))











