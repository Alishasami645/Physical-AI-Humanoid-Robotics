import requests
import json

try:
    print("Testing LibreTranslate API...")
    r = requests.post(
        'https://libretranslate.de/translate',
        json={
            'q': 'Hello world',
            'source': 'en',
            'target': 'ur',
            'format': 'text'
        },
        timeout=10,
        headers={'Content-Type': 'application/json'}
    )
    print('Status:', r.status_code)
    print('Content-Type:', r.headers.get('Content-Type', 'unknown'))
    if 'application/json' in r.headers.get('Content-Type', ''):
        print('JSON Response:', r.json())
    else:
        print('Response text (first 500 chars):', r.text[:500])
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
