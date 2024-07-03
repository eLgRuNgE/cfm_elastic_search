from elasticsearch import Elasticsearch

# Conectar a Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Realizar una búsqueda para obtener todos los documentos
res = es.search(index="website", body={"query": {"match_all": {}}})

# Imprimir los resultados
print("Documentos encontrados:")
for hit in res['hits']['hits']:
    print(f"Título: {hit['_source']['title']}")
    print(f"Contenido: {hit['_source']['content']}")
    print(f"URL: {hit['_source']['url']}")
    print("---")
