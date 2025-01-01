import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to scrape Poe.com
def scrape_poe(query):
    url = "https://poe.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Send GET request to Poe
    response = requests.get(url, headers=headers)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Implement scraping logic here
    # For now, let's return the query as a placeholder
    return f"Response for: {query}"

# API Endpoint
@app.route('/api/poe', methods=['GET'])
def poe_api():
    query = request.args.get('query')  # Get query from API request
    if not query:
        return jsonify({"error": "Query parameter is required!"}), 400

    # Scrape Poe.com
    result = scrape_poe(query)
    return jsonify({"query": query, "response": result})

if __name__ == "__main__":
    # Use Heroku's $PORT environment variable or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
