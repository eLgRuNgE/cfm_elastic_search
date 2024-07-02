# Demo de Elasticsearch para Búsqueda en Sitio Web

Este proyecto demuestra cómo utilizar Elasticsearch para implementar una función de búsqueda en el contenido de un sitio web corporativo.

## Descripción

Esta demo incluye:
- Un contenedor Docker con Elasticsearch y Kibana
- Scripts para indexar el contenido del sitio web
- Una interfaz web simple para realizar búsquedas

## Requisitos previos

- Docker y Docker Compose
- Python 3.7+
- Navegador web moderno

## Instalación

1. Clonar este repositorio:
> git clone https://github.com/eLgRuNgE/cfm_elastic_search
> cd cfm_elastic_search

2. Iniciar los contenedores de Elasticsearch y Kibana:
> docker-compose up -d

3. Instalar las dependencias de Python:
> pip install -r requirements.txt

## Uso

1. Indexar el contenido del sitio web:
> python index_content.py

2. Iniciar la interfaz web:
> python app.py

3. Abrir un navegador y visitar `http://localhost:5000`

## Estructura del proyecto

- `docker-compose.yml`: Configuración de Docker para Elasticsearch y Kibana
- `index_content.py`: Script para indexar el contenido del sitio web
- `app.py`: Aplicación web Flask para la interfaz de búsqueda
- `templates/`: Directorio con plantillas HTML
- `static/`: Directorio para archivos CSS y JavaScript

## Configuración

Puedes ajustar la configuración de Elasticsearch en el archivo `docker-compose.yml`.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.

## Licencia

Este proyecto está licenciado bajo Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

Esto significa que usted es libre de:
- Compartir — copiar y redistribuir el material en cualquier medio o formato

Bajo los siguientes términos:
- Atribución — Debe dar crédito adecuado, proporcionar un enlace a la licencia e indicar si se han realizado cambios. Puede hacerlo de cualquier manera razonable, pero no de una manera que sugiera que el licenciante lo respalda a usted o su uso.
- NoComercial — No puede utilizar el material con fines comerciales.
- NoDerivadas — Si remezcla, transforma o crea a partir del material, no puede difundir el material modificado.

Para más detalles, consulte la [licencia completa](http://creativecommons.org/licenses/by-nc-nd/4.0/).