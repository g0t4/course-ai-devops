from pprint import pprint
from elasticsearch import Elasticsearch
import requests
import json
import time

def categorize_log_entry(log_entry):
    log_format = (
        '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent '
            '"$http_referer" "$http_user_agent"'
    )

    prompt = (
        f"Nginx Log Format: {log_format}\n"
            f"Log Entry: {log_entry}\n\n"
            "Based on the above log entry, categorize the request as 'Bot', 'Attacker', or 'Human'. Human and Bot both mean likely benign intent. No other word choices. Respond with ONE word only. No explanations."
    )

    # FYI! provide your own instance of ollama!
    api_url = "http://ollama.lan:11434/api/generate"

    payload = {
        # "model": "qwen2.5-coder:0.5b-instruct-q8_0",
        # "model": "qwen2.5-coder:1.5b-instruct-q8_0",
        # "model": "qwen2.5-coder:3b-instruct-q8_0",
        "model": "qwen2.5-coder:7b-instruct-q8_0",
        # btw 7b is doing better at identifying possible attacks (.htpasswd, SQL injection)
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response from API.")
    else:
        return f"API request failed with status code {response.status_code}: {response.text}"

# FYI! if you change the name of the service (container) in Docker, then update the hostname here:
es_client = Elasticsearch([{'scheme': 'http', 'host': 'elasticsearch', 'port': 9200}])

query_all = {
    "_source": ["*"],  # Get all fields from the document
    "size": 200
}
query_not_categorized = {
    "query": {
        "bool": {
            "must_not": [
                {"exists": {"field": "category"}}
            ]
        }
    },
    "_source": ["*"],  # Get all fields from the document
    "size": 200
}

def categorize_document(hit):
    _source = hit['_source']
    message = _source.get('message')
    if message is None:
        # log field fallback
        message = _source.get("log")
        if message is None:
            print(f"  couldn't find 'message' or 'log' field")
            return None
    
    print("  message: ", message)
    tries = 0
    while tries < 3:
        try:
            category = categorize_log_entry(message)
            print("  category: ", category)

            if category == "Human":
                return "Human"
            elif category == "Bot":
                return "Bot"
            elif category == "Attacker":
                return "Attacker"
            else:
                print(f"  Unexpected category: {category}")
                tries += 1
        except Exception as e:
            print(f"  Failed to categorize log entry {message} with error {e}, trying again")
            tries += 1


def process_new_records():

    response = es_client.search(index="nginx-access", body=query_not_categorized)
    matches = response['hits']['total']['value']
    print(f"Found {matches} documents without a category field, overall.")
    hits = response['hits']['hits']
    print(f"  categorizing #: {len(hits)}")

    for hit in hits:
        print(f"\nDocument ID: {hit['_id']}")

        start_time = time.time()
        category = categorize_document(hit)
        duration_ms = (time.time() - start_time) * 1000
        print(f"  took {duration_ms:.1f} ms")

        if category is None:
            print(f"  Failed to categorize document after 3 tries")
            continue

        # patch the document with new "category" field
        document_id = hit['_id']
        update_body = {
            "doc": {"category": category}
        }
        es_client.update(index="nginx-access", id=document_id, body=update_body)


if __name__ == "__main__":

    while True:
        process_new_records()
        time.sleep(15) # every 15 seconds, check for new records
