import http.client, json

conn = http.client.HTTPConnection('127.0.0.1', 8000, timeout=10)
body = json.dumps({
    "query": "artificial intelligence",
    "selected_text": "artificial intelligence",
    "conversation_history": []
})
headers = {"Content-Type": "application/json"}
conn.request("POST", "/api/chat", body, headers)
res = conn.getresponse()
print(res.status, res.reason)
print(res.read().decode())
