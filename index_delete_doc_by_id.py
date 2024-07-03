from elasticsearch import Elasticsearch

# Conectar a Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Buscar todos los documentos en el índice "website"
search_query = {
    "query": {
        "match_all": {}
    }
}

# Realizar la búsqueda
res = es.search(index="website", body=search_query, size=1000)  # Ajusta el tamaño según sea necesario

# Recorrer los documentos y eliminarlos uno a uno
for hit in res['hits']['hits']:
    doc_id = hit['_id']
    es.delete(index="website", id=doc_id)
    print(f"Documento con ID {doc_id} eliminado.")

print("Todos los documentos han sido eliminados.")
