from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

def search_by_lyric(lyric):
    query = {
        "query": {
            "match": {
                "Lyrics": lyric
            }
        }
    }
    return es.search(index="lyrics", body=query)

results = search_by_lyric("can't")
print(results)

analysis = es.indices.analyze(index="lyrics", body={"text": "can't"})
print(analysis)