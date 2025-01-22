from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

LANGFLOW_API_URL = "http://gmc-platform0.eastus.cloudapp.azure.com:7860/api/v1/run/298f4a01-26eb-436c-bac3-4c1cbfcc9e67?stream=false"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    payload = {
        "input_value": user_message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {}
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(LANGFLOW_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Safely extract the chatbot's response
            try:
                # Navigate the JSON response structure
                reply = (
                    data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                )
            except (IndexError, KeyError, TypeError) as e:
                print(f"Error parsing Langflow response: {e}")
                print(f"Full response content: {data}")  # Log full response for debugging
                reply = "The Langflow API returned an unexpected response format."

            return jsonify({'reply': reply})
        else:
            return jsonify({'error': f'Langflow API returned status code {response.status_code}'}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error contacting Langflow API: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
