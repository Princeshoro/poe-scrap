import os
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Set up Selenium options to run headless (without opening a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Path to your chromedriver (update this to your chromedriver location)
driver_path = "/path/to/chromedriver"  # Update this

# Function to scrape Poe.com using Selenium
def scrape_poe(query):
    # Check if query is asking for the creator
    if query.lower() == "who is your creator":
        return "My creator is Prince."

    url = "https://poe.com/"
    
    # Initialize Selenium WebDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Wait for the content to load (you can adjust this if needed)
    driver.implicitly_wait(5)  # Wait for 5 seconds for content to load

    # Example of finding content (adjust this based on the actual structure of Poe)
    content = driver.find_element(By.TAG_NAME, 'body').text  # Get all the body text

    # Search through content
    if query.lower() in content.lower():
        return content.strip()
    else:
        return "No relevant content found for query."

    # Close the browser after scraping
    driver.quit()

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
