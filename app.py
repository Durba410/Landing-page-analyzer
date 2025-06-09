import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')
CORS(app)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/audit', methods=['POST'])
def audit():
    try:
        data = request.get_json()
        url = data.get('url')
        description = data.get('description')

        if not api_key:
            return jsonify({'error': 'API key not found'}), 401

        prompt = f"""
        Perform a detailed CRO (Conversion Rate Optimization) audit for the following website:
        URL: {url}
        Description: {description}
        Provide actionable feedback on layout, CTA, copy, mobile experience, etc.
        """

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o",  # or "gpt-4o-mini", "gpt-3.5-turbo", etc.
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        return jsonify({'result': content})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)