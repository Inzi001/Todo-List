from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Regular expression pattern to extract emails
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

@app.route('/extract-emails', methods=['POST'])
def extract_emails():
    try:
        # Get URL from the request
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text and search for emails
        text = soup.get_text()
        emails = re.findall(EMAIL_REGEX, text)

        # Return unique emails
        return jsonify({"emails": list(set(emails))})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching the URL: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
