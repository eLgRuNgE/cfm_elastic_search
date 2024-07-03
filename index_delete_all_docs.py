from elasticsearch import Elasticsearch

# Conectar a Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Eliminar todos los documentos en el índice "website"
delete_query = {
    "query": {
        "match_all": {}
    }
}

response = es.delete_by_query(index="website", body=delete_query)
print(f"Eliminados {response['deleted']} documentos del índice 'website'.")
