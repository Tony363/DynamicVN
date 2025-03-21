# Define the loading screen
screen loading:
    text "Loading..." align (0.5, 0.5)

# Python block for API calls and caching
init python:
    import os
    import urllib.request
    import urllib.parse
    import json
    import ssl
    import base64
    import renpy
    import hashlib
    
    def init_settings():
        # Set the root directory relative to the game directory
        root_dir = os.path.join(renpy.config.gamedir, "cache")
        text_dir = os.path.join(root_dir, "text")
        images_dir = os.path.join(root_dir, "images")
        
        # Create directories if they don't exist
        if not os.path.exists(text_dir):
            os.makedirs(text_dir)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        # Define placeholder image path
        placeholder = os.path.join(images_dir, "placeholder.png")
        if not os.path.exists(placeholder):
            print(f"Warning: {placeholder} doesn't exist. Create a placeholder.png in the cache/images directory.")
        
        # Get API key from environment variable
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            print("Error: GEMINI_API_KEY environment variable not set.")
        
        # SSL context setup (unchanged)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        print("WARNING: SSL certificate verification disabled for development. This is not secure for production use.")
        
        return ssl_context, text_dir, images_dir, placeholder, API_KEY
    
    ssl_context, text_dir, images_dir, placeholder, API_KEY = init_settings()
    
    def get_hash(prompt):
        """Generate a consistent hash for a prompt using MD5."""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def fetch_text(prompt: str) -> str:
        """
        Generate text using the Gemini API and cache it.
        Returns the generated text content.
        """
        hash_value = get_hash(prompt)
        output_file = os.path.join(text_dir, f"text_{hash_value}.txt")
        
        # Check for cached version
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                return f.read()
        
        # Construct the API request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt}
                ]
            }]
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        
        # Send request and process response
        with urllib.request.urlopen(req, context=ssl_context) as response:
            response_data = response.read().decode('utf-8')
            response_json = json.loads(response_data)
            generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
            
            # Cache the text
            with open(output_file, 'w') as f:
                f.write(generated_text)
            print(f"Text saved as '{output_file}'")
        
        return generated_text
    
    def fetch_image(prompt: str) -> str:
        """
        Generate an image using the Gemini API and cache it.
        Returns the relative path to the image file.
        """
        hash_value = get_hash(prompt)
        output_file = os.path.join(images_dir, f"image_{hash_value}.png")
        relative_path = os.path.relpath(output_file, renpy.config.gamedir)
        
        # Check for cached version
        if os.path.exists(output_file):
            print(f"Using cached image: {relative_path}")
            return relative_path
        
        # Construct the API request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"
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
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        
        # Send request and process response
        with urllib.request.urlopen(req, context=ssl_context) as response:
            response_data = response.read().decode('utf-8')
            response_json = json.loads(response_data)
            image_data = response_json['candidates'][0]['content']['parts'][0]['inlineData']['data']
            
            # Cache the image
            with open(output_file, 'wb') as f:
                f.write(base64.b64decode(image_data))
            print(f"Image saved as '{output_file}'")
        
        return relative_path

# Define characters
define p = Character("Player")
define s = Character("Shopkeeper")
define v = Character("Villager")
define m = Character("Mysterious Stranger")

# Define inventory variable
default has_lantern = False

# Game start
label start:
    show screen loading
    $ home_bg = fetch_image("A cozy medieval cottage interior with a fireplace, wooden furniture, and a bed. Sunlight streams through a small window. Style: medieval fantasy, detailed illustration.")
    $ home_text = fetch_text("Generate a short description of a cozy medieval cottage where the player starts their adventure.")
    hide screen loading
    scene expression home_bg
    p "[home_text]"
    p "What would you like to do?"
    menu:
        "Go to the town square":
            jump town_square
        "Stay home":
            "You decide to rest a bit longer."
            jump start

label town_square:
    show screen loading
    $ town_bg = fetch_image("A bustling medieval town square with market stalls, a central fountain, and timber-framed houses with thatched roofs. Style: medieval fantasy, detailed illustration.")
    $ town_text = fetch_text("Generate a short description of a bustling medieval town square in an RPG setting.")
    hide screen loading
    scene expression town_bg
    p "[town_text]"
    p "You see a shop to your left and a forest path to your right. A villager stands nearby."
    menu:
        "Talk to the villager":
            jump talk_villager
        "Go to the shop":
            jump shop
        "Head to the forest":
            jump forest
        "Go back home":
            jump start

label talk_villager:
    show screen loading
    $ villager_text = fetch_text("Generate a short dialogue for a villager in a medieval RPG responding to a question about the forest.")
    hide screen loading
    v "[villager_text]"
    p "Interesting. Thanks for the info."
    jump town_square

label shop:
    show screen loading
    $ shop_bg = fetch_image("A medieval shop interior with shelves of goods, a wooden counter, and a merchant. Style: medieval fantasy, detailed illustration.")
    $ shop_text = fetch_text("Generate a short description of a medieval shop where the player can buy supplies.")
    hide screen loading
    scene expression shop_bg
    p "[shop_text]"
    if not has_lantern:
        s "Welcome, traveler! Care to see my fine goods? I've got just what you need!"
        menu:
            "Buy a lantern":
                p "I'd like a lantern."
                s "That'll be 10 gold coins. A fine choice!"
                $ has_lantern = True
                p "Thanks!"
            "Leave":
                p "Just looking, thanks."
    else:
        s "Welcome back! Need anything else?"
        p "Just browsing, thanks."
    jump town_square

label forest:
    show screen loading
    $ forest_bg = fetch_image("A dense medieval forest with tall trees, a winding path, and dappled sunlight. Style: medieval fantasy, detailed illustration.")
    $ forest_text = fetch_text("Generate a short description of a mysterious forest in an RPG setting.")
    hide screen loading
    scene expression forest_bg
    p "[forest_text]"
    if has_lantern:
        "Your lantern lights the way deeper into the forest."
        jump meet_stranger
    else:
        "It's too dark to go further. You need a light source."
        jump town_square

label meet_stranger:
    show screen loading
    $ stranger_text = fetch_text("Generate a mysterious dialogue for a cloaked stranger in a forest, hinting at a quest in a medieval RPG.")
    hide screen loading
    m "[stranger_text]"
    "The stranger vanishes, leaving you with a sense of purpose."
    "To be continued..."
    return