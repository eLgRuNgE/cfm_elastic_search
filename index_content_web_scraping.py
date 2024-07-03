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

# Configuración de Elasticsearch
es = Elasticsearch("http://localhost:9200")

# URLs de inicio para hacer scraping
start_urls = [
    'https://www.comfama.com',
    'https://www.comfama.com/conoce-comfama/',
    'https://www.comfama.com/mapa-de-sedes/',
    'https://www.comfama.com/ayuda/',
    'https://www.comfama.com/informe2021/',
    'https://www.comfama.com/conoce-comfama/categorias-de-afiliacion/',
    'https://www.comfama.com/conoce-comfama/beneficios/',
    'https://www.comfama.com/trabajo-con-proposito/empleo/trabaja-con-nosotros/',
    'https://www.comfama.com/conoce-comfama/transparencia-acceso-informacion-publica/',
    'https://www.comfama.com/conoce-comfama/nuestras-politicas/',
    'https://serviciosenlinea.comfama.com/webinicio/CondicionesDeUso.html?_gl=1*1jle87d*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_1V3L85HTHH*MTcyMDAzOTI0Ny41LjEuMTcyMDAzOTQwOS4xOS4wLjA.',
    'https://www.comfama.com/notificaciones-judiciales/',

    'https://www.comfama.com/conoce-comfama/contactanos/',
    'https://www.comfama.com/peticiones/',
    'https://www.comfama.com/conoce-comfama/carta-deberes-y-derechos-afiliados/',
    'https://serviciosenlinea.comfama.com/contenidos/servicios/Nuestra%20organizaci%C3%B3n/compromisos-con-la-etica-y-gobierno-corporativo/compromisos-frente-a-la-etica-y-GC-VF.pdf?_gl=1*1bdb4au*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_1V3L85HTHH*MTcyMDAzOTI0Ny41LjEuMTcyMDAzOTQwOS4xOS4wLjA.',
    'https://forms.cemtrik.com/formulario/R01X2I',
    'https://www.comfama.com/conoce-comfama/mapa-de-sitio/',

    'https://www.comfama.com/portal-servicios/personas/afiliaciones',
    'https://www.comfama.com/portal-servicios/personas/certificados/',
    'https://www.comfama.com/finanzas/creditos-con-proposito/',
    'https://www.comfama.com/subsidio/',
    'https://www.comfama.com/servicio-de-empleo/',
    'https://www.comfama.com/salud-y-cuidado/vacunacion/',
    'https://www.comfamapro.com/?_gl=1*15ie1ux*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_PJT5623MFZ*MTcyMDAzNzE2My41LjEuMTcyMDAzOTQwOC4yMS4wLjA.',

    'https://tienda.comfama.com/?_gl=1*ux4vbs*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_1V3L85HTHH*MTcyMDAzOTI0Ny41LjEuMTcyMDAzOTQwOS4xOS4wLjA.',
    'https://www.comfamapro.com/?_gl=1*15ie1ux*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_PJT5623MFZ*MTcyMDAzNzE2My41LjEuMTcyMDAzOTQwOC4yMS4wLjA.',
    'https://www.viajescomfama.com/?_gl=1*84lxon*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_1V3L85HTHH*MTcyMDAzOTI0Ny41LjEuMTcyMDAzOTQwOS4xOS4wLjA.*_ga_PJT5623MFZ*MTcyMDAzNzE2My41LjEuMTcyMDAzOTQwOC4yMS4wLjA.',
    'https://www.cosmoschools.co/?_gl=1*1i9j8xr*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_PJT5623MFZ*MTcyMDAzNzE2My41LjEuMTcyMDAzOTQwOC4yMS4wLjA.',
    'https://agenda.comfama.com/',
    'https://www.comfama.com/https://www.comfama.com/nutricion-saludable/',
    'https://www.experienciascomfama.com.co/?_gl=1*1i9j8xr*_gcl_au*MTUyNDUzNTM3NS4xNzE4NzE4MTU0*_ga*MjExNDQyNzU3Ni4xNzE4NzE4MTU0*_ga_PJT5623MFZ*MTcyMDAzNzE2My41LjEuMTcyMDAzOTQwOC4yMS4wLjA.#/',
    'https://caminoamicasa.comfama.com/login',
    'https://www.comfama.com/aprendizaje/temporada-escolar/',
    
    'https://comfama.buk.co/'
]

# Lista para almacenar los documentos
documents = []

# Profundidad máxima URLs
max_depth_user = 5

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
    title = soup.title.string.strip() if soup.title and soup.title.string else url
    content = ' '.join([p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()])

    documents.append({
        'title': title,
        'content': content,
        'url': url,
        'suggest': {
            'input': title.split(),  # Separar palabras del título para sugerencias
            'weight': 1  # Peso de las sugerencias, puedes ajustar según sea necesario
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

# Asegúrate de que el índice exista
if not es.indices.exists(index="website"):
    es.indices.create(index="website")

# Indexar los documentos
for doc in documents:
    es.index(index="website", body=doc)

print(f"Indexación completada. Total de documentos indexados: {len(documents)}")
