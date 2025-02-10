from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

LANGFLOW_API_URL = "http://gmc-platform0.eastus.cloudapp.azure.com:7860/api/v1/run/d560aad0-97ab-4df9-97b9-d298994e9516?stream=false"

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
            
            # Extract chatbot response with safe parsing
            try:
                raw_reply = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            except (IndexError, KeyError, TypeError) as e:
                print(f"Error parsing Langflow response: {e}")
                print(f"Full response content: {data}")  # Log full response for debugging
                return jsonify({'error': "The Langflow API returned an unexpected response format."}), 500
            
            # Format response with balanced spacing
            formatted_reply = format_response(raw_reply)

            return jsonify({'reply': formatted_reply})

        else:
            return jsonify({'error': f'Langflow API returned status code {response.status_code}'}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error contacting Langflow API: {e}'}), 500


def format_response(response_text):
    """
    Formats the Langflow response for readability while preventing excessive line breaks.
    """
    # Apply structured formatting with balanced spacing
    response_text = response_text.replace("### Summary of Key Metrics:", "**📊 Summary of Key Metrics**\n")
    response_text = response_text.replace("### Interesting Insights:", "\n**💡 Interesting Insights**\n")
    response_text = response_text.replace("### Recurring Accounts:", "\n**🔄 Recurring Accounts**\n")
    response_text = response_text.replace("### Additional Observations:", "\n**📌 Additional Observations**\n")

    # Properly space bullet points while avoiding excessive blank lines
    response_text = response_text.replace("- **", "\n✅ **")  # Major bullet points
    response_text = response_text.replace("- ", "\n🔹 ")  # Minor bullet points

    # Reduce excessive consecutive newlines while preserving paragraph breaks
    response_text = "\n".join([line.strip() for line in response_text.splitlines() if line.strip()])

    return response_text.strip()


if __name__ == '__main__':
    app.run(debug=True)
