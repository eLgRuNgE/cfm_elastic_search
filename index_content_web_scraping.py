#####
# Copyright (c) [2024] [Fabian Callejas - Comfama]
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
#####

from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

# Configuración de Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Definir el mapeo para el campo suggest
mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "url": {"type": "keyword"},
            "suggest": {
                "type": "completion"
            }
        }
    }
}

# Crear el índice con el mapeo
index_name = "website"
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name, body=mapping)

# URLs de inicio para hacer scraping
start_urls = [
    'https://www.comfama.com',
    'https://serviciosenlinea.comfama.com/',
    'https://forms.cemtrik.com/formulario/R01X2I',
    'https://www.comfamapro.com/',
    'https://tienda.comfama.com/',
    'https://www.viajescomfama.com/',
    'https://www.cosmoschools.co/',
    'https://agenda.comfama.com/',
    'https://www.experienciascomfama.com.co/',
    'https://caminoamicasa.comfama.com/',    
    'https://comfama.buk.co/'
]

# Lista para almacenar los documentos
documents = []

# Profundidad máxima URLs
max_depth_user = 5

# Función para limpiar el texto eliminando caracteres no válidos y caracteres nulos
def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Eliminar caracteres no ASCII
    text = text.replace('\x00', ' ')  # Eliminar caracteres nulos
    return text.strip()

# Función para realizar scraping de una URL y sus enlaces
def scrape(url, base_url, depth, max_depth, visited):
    if depth > max_depth or url in visited:
        return
    
    visited.add(url)
    print(f"Scraping: {url} (Depth: {depth})")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    title = clean_text(soup.title.string.strip()) if soup.title and soup.title.string else url
    content = ' '.join([clean_text(p.get_text().strip()) for p in soup.find_all('p') if p.get_text().strip()])

    suggestions = list(set(title.split() + content.split()))  # Unir palabras del título y contenido, eliminar duplicados
    
    documents.append({
        'title': title,
        'content': content,
        'url': url,
        'suggest': {
            'input': suggestions,
            'weight': 1
        }
    })
    
    if depth < max_depth:
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            if urlparse(next_url).netloc == urlparse(base_url).netloc and next_url not in visited:
                time.sleep(1)  # Pausa para ser respetuoso con el servidor
                scrape(next_url, base_url, depth + 1, max_depth, visited)

# Realizar scraping desde cada URL inicial hasta [max_depth_user] niveles de profundidad
for start_url in start_urls:
    visited_urls = set()
    scrape(start_url, start_url, 0, max_depth_user, visited_urls)

# Indexar los documentos
for doc in documents:
    try:
        es.index(index=index_name, body=doc)
    except Exception as e:
        print(f"Error al indexar el documento: {e}")

print(f"Indexación completada. Total de documentos indexados: {len(documents)}")
