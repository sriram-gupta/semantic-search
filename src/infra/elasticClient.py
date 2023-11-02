from elasticsearch import Elasticsearch
client = Elasticsearch( "http://localhost:9200" )

print(client.info())


__all__ = ['client']