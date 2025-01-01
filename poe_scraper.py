import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to scrape Poe.com
def scrape_poe(query):
    # Check if query is asking for the creator
    if query.lower() == "who is your creator":
        return "My creator is Prince."

    url = "https://poe.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Send GET request to Poe
    response = requests.get(url, headers=headers)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Search for all text elements on the page (example: all divs, spans, etc.)
    content_elements = soup.find_all(['div', 'span', 'p', 'h1', 'h2'])  # You can add more tags to search through

    # Check if any content contains the query
    for element in content_elements:
        if query.lower() in element.text.lower():  # Case-insensitive search
            return element.text.strip()

    # If no relevant content is found
    return "No relevant content found for query."

# API Endpoint
@app.route('/api/poe', methods=['GET'])
def poe_api():
    query = request.args.get('query')  # Get query from API request
    if not query:
        return jsonify({"error": "Query parameter is required!"}), 400

    # Scrape Poe.com or respond to creator question
    result = scrape_poe(query)
    return jsonify({"query": query, "response": result})

if __name__ == "__main__":
    # Use Heroku's $PORT environment variable or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
