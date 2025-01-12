import requests

# SerpApi API key (replace if needed for security)
api_key = "97c239f191e97b518fad0bf8c6a7ce4164eada43aca1a89346defbb514e088ed"  # Replace as necessary

def scrape_google_images(query, num_images=50):
    # Set up the request parameters
    search_url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "tbm": "isch",  # Specifies image search
        "ijn": 0,
        "api_key": api_key
    }

    try:
        # Send request to SerpApi
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for non-200 responses
        search_results = response.json()

        # Extract image URLs
        image_urls = [result["original"] for result in search_results.get("images_results", [])[:num_images]]
        
        # Return structured JSON response
        return {
            "status": "success",
            "image_urls": image_urls
        }

    except requests.exceptions.RequestException as e:
        # Handle network and HTTP errors
        print(f"Request error: {e}")
        return {
            "status": "error",
            "message": f"Request error: {e}"
        }

    except KeyError:
        # Handle case where 'images_results' is missing
        print("Error: 'images_results' key not found.")
        return {
            "status": "error",
            "message": "Unexpected response structure. 'images_results' key not found."
        }
