from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)


WINDOW_SIZE = 10
TIMEOUT = 0.5  
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQzNjAzOTc3LCJpYXQiOjE3NDM2MDM2NzcsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjUwMTdjMmE1LTg3MWUtNDlmMi04YzEzLTQyYjllNTgwOGUwZSIsInN1YiI6InNoYWhiaHVzaGFuNzNAZ21haWwuY29tIn0sImVtYWlsIjoic2hhaGJodXNoYW43M0BnbWFpbC5jb20iLCJuYW1lIjoiYmh1c2hhbiBzYWgiLCJyb2xsTm8iOiIyMjA1NDMyMSIsImFjY2Vzc0NvZGUiOiJud3B3cloiLCJjbGllbnRJRCI6IjUwMTdjMmE1LTg3MWUtNDlmMi04YzEzLTQyYjllNTgwOGUwZSIsImNsaWVudFNlY3JldCI6IlFUSHdNcXdhR1Zjcmp5cXEifQ.on2oYxaDy85tZhbuX-sdv5rP19dUNS7YQVJzytFmcDU"  # Replace with your actual API token


ENDPOINTS = {
    'p': "http://20.244.56.144/evaluation-service/primes",
    'f': "http://20.244.56.144/evaluation-service/fibo",
    'e': "http://20.244.56.144/evaluation-service/even",
    'r': "http://20.244.56.144/evaluation-service/rand"
}


windows = {
    'p': [],
    'f': [],
    'e': [],
    'r': []
}

def update_window(window, new_numbers):
    """
    Update the given window with new numbers ensuring:
      - Only unique numbers are stored (duplicates are ignored).
      - The window size is not exceeded. If it is, remove the oldest numbers.
    Returns the updated window.
    """
    window_prev = window.copy()

    for num in new_numbers:
        if num not in window:
            window.append(num)
            if len(window) > WINDOW_SIZE:
                window.pop(0)

    return window_prev, window

@app.route('/numbers/<numberid>', methods=['GET'])
def numbers_endpoint(numberid):
    if numberid not in ENDPOINTS:
        return jsonify({"error": "Invalid numberid. Allowed values are 'p', 'f', 'e', 'r'."}), 400

    url = ENDPOINTS[numberid]
    third_party_numbers = []
    start_time = time.time()

    try:
       
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        third_party_numbers = data.get("numbers", [])
    except Exception as e:
        print(f"Error calling third-party API for {numberid}: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        return jsonify({"error": "Request timed out"}), 504

    current_window = windows[numberid]
    window_prev, window_curr = update_window(current_window, third_party_numbers)
    windows[numberid] = window_curr

    if window_curr:
        avg = sum(window_curr) / len(window_curr)
    else:
        avg = 0.0

    result = {
        "windowPrevState": window_prev,
        "windowCurrState": window_curr,
        "numbers": third_party_numbers,
        "avg": round(avg, 2)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)