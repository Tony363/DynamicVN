import os
import requests
import urllib
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables with optional fallback
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

# Get cache directory from environment variables or use default
CACHE_DIR = os.environ.get("CACHE_DIR", "cache")

# Create cache directory if it doesn't exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

import ssl
# Create an SSL context that doesn't verify certificates (for development only)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

import urllib.request
import json
import base64


import urllib.request
import json

def fetch_text(prompt: str) -> str:
    """
    Generate text using the Gemini 2.0 Flash API and save it to a file.

    Parameters:
    - prompt (str): The text prompt for generating the text.

    Returns:
    - str: The path to the file where the generated text is saved.
    """
    # Define the output file path using the prompt's hash
    output_file = f"game/cache/text_{hash(prompt)}.txt"
    
    # Construct the URL with the API key for the text generation model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Create the JSON payload for text generation
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }]
    }
    
    # Convert payload to JSON string and encode to bytes
    data = json.dumps(payload).encode('utf-8')
    
    # Create the request object
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    # Send the request and get the response
    with urllib.request.urlopen(req) as response:
        # Read and decode the response
        response_data = response.read().decode('utf-8')
        
        # Parse the JSON response and extract the generated text
        response_json = json.loads(response_data)
        generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Save the generated text to a file
        with open(output_file, 'w') as f:
            f.write(generated_text)
        print(f"Text saved as '{output_file}'")
    
    return generated_text
def generate_and_save_image(
    prompt:str, 
    output_file:str='gemini-native-image.png'
)->None:
    """
    Generate an image using the Gemini API and save it to a file.

    Parameters:
    - api_key (str): The API key for accessing the Gemini API.
    - prompt (str): The text prompt for generating the image.
    - output_file (str): The name of the file to save the image to. Default is 'gemini-native-image.png'.
    """
    # Construct the URL with the API key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"
    
    # Create the JSON payload
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    # Convert payload to JSON string and encode to bytes
    data = json.dumps(payload).encode('utf-8')
    
    # Create the request object
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    # Send the request and get the response
    with urllib.request.urlopen(req) as response:
        # Read and decode the response
        response_data = response.read().decode('utf-8')
        
        # Parse the JSON response
        response_json = json.loads(response_data)
        response_json_data = response_json['candidates'][0]['content']['parts'][0]['inlineData']['data']
       
        image_data = response_json_data
        # Decode base64 and save to file
        with open(output_file, 'wb') as f:
            f.write(base64.b64decode(image_data))
        print(f"Image saved as '{output_file}'")

def fetch_image(prompt=None):
    """Generate an image using Gemini API client."""
    # Configure the Gemini client with the API key
    client = genai.Client(api_key=API_KEY)

    # Use provided prompt or default
    contents = prompt if prompt else 'Female AI influencer'
    print(f"Generating image with prompt: {contents}")

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )

    # Process and save the response
    output_path = None
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            
            # Use the prompt to name the file, or use default name
            if prompt:
                safe_name = ''.join(c if c.isalnum() else '_' for c in prompt[:30])
                output_path = f"generated_{safe_name}.png"
            else:
                output_path = 'gemini-native-image.png'
            
            image.save(output_path)
            print(f"Image saved to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    # Example usage
    prompt = "A medieval knight in full armor, standing on a hill overlooking a battlefield."
    # generate_and_save_image(prompt)

    # Option 2: Use the default prompt
    fetch_text("Generate a short description of a cozy medieval cottage where the player starts their adventure.")