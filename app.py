import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/audit', methods=['POST'])
def audit():
    try:
        data = request.get_json()
        url = data.get('url')
        description = data.get('description')

        if not api_key:
            return jsonify({'error': 'API key not found'}), 401

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""Perform a detailed CRO (Conversion Rate Optimization) audit for the following website:

URL: {url}
Description: {description}

Provide actionable feedback and highlight problem areas. Cover the hero section, layout, CTA placement, copy clarity, and mobile responsiveness."""

        payload = {
            "model": "gpt-4o",  # This is the actual model name
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return jsonify({'result': content})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)