from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

app = Flask(__name__)
es = Elasticsearch("http://projeslatic.internal:9200")

GOOGLE_API = os.getenv('GOOGLE_API')
CX = os.getenv('CX')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    apiKey = GOOGLE_API
    cx = CX
    url = f"https://www.googleapis.com/customsearch/v1?key={apiKey}&cx={cx}&q={query}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/lyrics_search')
def lyrics_search():
    return render_template('lyric_search.html')

@app.route('/song_details/<song_id>')
def song_details(song_id):
    # Fetch song details by ID
    response = es.get(index="lyrics", id=song_id)
    song = response['_source']
    
    # Render a template with the song details
    return render_template('song_details.html', song=song)


@app.route('/searchLyrics', methods=['GET'])
def search_lyrics():
    query = request.args.get('query')
    if query.isdigit():
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["Year", "Rank"]
                }
            },
            "_source": ["Rank", "Song", "Artist", "Year", "Lyrics", "Source"],  # Fields to return
            "highlight": {
                "fields": {
                    "Lyrics": {}
                }
            }
        }
    else:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["Song", "Artist", "Lyrics"]
                }
            },
            "_source": ["Rank", "Song", "Artist", "Year", "Lyrics", "Source"],  # Fields to return
            "highlight": {
                "fields": {
                    "Lyrics": {}
                }
            }
        }

    # Execute the search query
    response = es.search(index="lyrics", body=body)
    
    # Extract hits
    hits = response['hits']['hits']
    results = [{
        '_id': hit['_id'],
        '_source': hit['_source'],
        'highlight': hit.get('highlight', {})
    } for hit in hits]

    # Return JSON response
    return jsonify(results)


#if __name__ == '__main__':
#    app.run(debug=True)
