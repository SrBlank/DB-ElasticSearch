from elasticsearch import Elasticsearch
import csv

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Delete the existing index if it exists
if es.indices.exists(index="lyrics"):
    es.indices.delete(index="lyrics")

# Define improved index settings and mappings
index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard",
                    "stopwords": "_english_"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "Rank": {"type": "integer"},
            "Song": {"type": "text"},
            "Artist": {"type": "text"},  # Changed to text to allow partial matches
            "Year": {"type": "integer"},
            "Lyrics": {"type": "text"},  # Changed to text to allow full text search
            "Source": {"type": "keyword"}
        }
    }
}

# Create an index with custom settings and mappings
es.indices.create(index="lyrics", body=index_settings)

# Indexing function
def index_csv_to_elasticsearch(csv_file):
    with open(csv_file, newline='', encoding='iso-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            es.index(index="lyrics", id=idx, document=row)

# Function to perform search and return specific fields
def search_lyrics(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Song", "Artist", "Lyrics"]
            }
        },
        "_source": ["Rank", "Song", "Artist", "Year"],  # Fields to return
        "highlight": {
            "fields": {
                "Lyrics": {}  # Generate snippets from Lyrics
            }
        }
    }
    return es.search(index="lyrics", body=body)

# Index the CSV data
csv_file_path = './lyrics.csv'
index_csv_to_elasticsearch(csv_file_path)

# Example search
results = search_lyrics("love")
for hit in results['hits']['hits']:
    print(hit['_source'], hit.get('highlight', {}))
