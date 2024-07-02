#####
# Copyright (c) [2024] [Fabian Callejas - Comfama]
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
#####


from elasticsearch import Elasticsearch

# Cambia esta línea
es = Elasticsearch("http://localhost:9200")

# El resto del código permanece igual
documents = [
    {
        'title': 'Página de inicio',
        'content': 'Bienvenido a Comfama. Somos una empresa comprometida con el bienestar de las familias.',
        'url': 'https://www.comfama.com'
    },
    {
        'title': 'Servicios',
        'content': 'Ofrecemos una variedad de servicios incluyendo salud, educación y recreación.',
        'url': 'https://www.comfama.com/servicios'
    },
    {
        'title': 'Contacto',
        'content': 'Ponte en contacto con nosotros para más información sobre nuestros programas.',
        'url': 'https://www.comfama.com/contacto'
    }
]

# Asegúrate de que el índice exista
if not es.indices.exists(index="website"):
    es.indices.create(index="website")

for doc in documents:
    es.index(index="website", body=doc)

print("Indexación completada.")

# Búsqueda de prueba
search_query = {
    "query": {
        "multi_match" : {
            "query": "comfama",
            "fields": ["title", "content"]
        }
    }
}

res = es.search(index="website", body=search_query)

print("Resultados de la búsqueda:")
for hit in res['hits']['hits']:
    print(f"Título: {hit['_source']['title']}")
    print(f"URL: {hit['_source']['url']}")
    print("---")