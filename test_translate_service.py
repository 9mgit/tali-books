#!/usr/bin/env python3
import requests
import json

# Test Gemini
url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=YOUR_GEMINI_API_KEY"
data = {
    "contents": [{"parts": [{"text": "Translate to Bisaya: Hello, how are you?"}]}]
}

try:
    resp = requests.post(url, json=data, timeout=30)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"Result: {result['candidates'][0]['content']['parts'][0]['text']}")
    else:
        print(f"Error: {resp.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")