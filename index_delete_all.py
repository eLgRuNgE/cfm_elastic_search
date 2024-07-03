from elasticsearch import Elasticsearch

# Configuración de Elasticsearch
es = Elasticsearch("http://localhost:9200")

def delete_all_indices():
    # Obtener la lista de todos los índices
    indices = es.indices.get_alias(index="*")
    if not indices:
        print("No se encontraron índices.")
        return

    # Borrar cada índice
    for index in indices:
        try:
            es.indices.delete(index=index)
            print(f"Índice '{index}' borrado exitosamente.")
        except Exception as e:
            print(f"Error al borrar el índice '{index}': {e}")

if __name__ == "__main__":
    delete_all_indices()
