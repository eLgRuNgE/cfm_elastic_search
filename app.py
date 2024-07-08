#####
# Copyright (c) [2024] [Fabian Callejas - Comfama]
# This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/
#####


from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Conexión a Elasticsearch
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'hits': []})
    
    search_query = {
        "query": {
            "multi_match" : {
                "query": query,
                "fields": ["title", "content"]
            }
        }
    }
    
    res = es.search(index="website", body=search_query)
    
    hits = []
    for hit in res['hits']['hits']:
        hits.append({
            'title': hit['_source']['title'],
            'content': hit['_source']['content'],
            'url': hit['_source']['url']
        })
    
    return jsonify({'hits': hits})

@app.route('/suggest')
def suggest():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    suggest_query = {
        "suggest": {
            "website-suggest": {
                "prefix": query.lower(),
                "completion": {
                    "field": "suggest",
                    "fuzzy": {
                        "fuzziness": "auto"
                    }
                }
            }
        }
    }

    res = es.search(index="website", body=suggest_query)
    
    suggestions = set()  # Usar un set para evitar duplicados
    for option in res['suggest']['website-suggest'][0]['options']:
        suggestions.add(option['text'].lower())

    return jsonify(list(suggestions))

if __name__ == '__main__':
    app.run(debug=True)
