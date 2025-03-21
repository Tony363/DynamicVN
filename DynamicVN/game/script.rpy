﻿# Define the loading screen
screen loading:
    text "Loading..." align (0.5, 0.5)

# Add player avatar screen
screen player_avatar:
    fixed:
        xalign 0.95  # Position at right side of screen
        yalign 0.1   # Position near top
        image avatar_files.get("Player", "cache/images/placeholder.png")

# Python block for API calls, caching, and custom character class
init python:
    import os
    import urllib.request
    import urllib.parse
    import json
    import ssl
    import base64

    def init_settings()->None:
        # Set API key directly
        API_KEY = os.getenv("GEMINI_API_KEY")
        root_dir = '/home/tony/Desktop/DynamicVN/DynamicVN/game/cache'

        text_dir = os.path.join(root_dir, "text")
        if not os.path.exists(text_dir):
            os.makedirs(text_dir)

        images_dir = os.path.join(root_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        # For testing or if errors occur, use placeholder
        placeholder = os.path.join(root_dir, "images", "placeholder.png")
        if not os.path.exists(placeholder):
            print(f"Warning: {placeholder} doesn't exist. Create an images/placeholder.png file.")

        # Create an SSL context that doesn't verify certificates (for development only)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        print("WARNING: SSL certificate verification disabled for development. This is not secure for production use.")
        return ssl_context, text_dir, images_dir, placeholder, API_KEY
    
    ssl_context, text_dir, images_dir, placeholder, API_KEY = init_settings()
    
    # Dictionary to store avatar file paths, populated at runtime
    avatar_files = {}
    
    # Define avatar prompts for each character
    avatar_prompts = {
        "player": "A portrait of a brave adventurer with a sword and leather armor. Style: medieval fantasy, detailed illustration.",
        "shopkeeper": "A portrait of a friendly shopkeeper with an apron and a welcoming smile. Style: medieval fantasy, detailed illustration.",
        "villager": "A portrait of a simple villager wearing peasant clothes and a hat. Style: medieval fantasy, detailed illustration.",
        "stranger": "A portrait of a cloaked figure with a hood, casting a shadow over their face. Style: medieval fantasy, detailed illustration."
    }
    
    def fetch_text(prompt: str) -> str:
        """
        Generate text using the Gemini 2.0 Flash API and save it to a file.

        Parameters:
        - prompt (str): The text prompt for generating the text.

        Returns:
        - str: The path to the file where the generated text is saved.
        """
        # Define the output file path using the prompt's hash
        output_file = os.path.join(text_dir, f"text_{'_'.join(prompt.split(' ')[:2])}.txt")
        
        # Check for cached version
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                return f.read()
        
        # Construct the URL with the API key for the text generation model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        
        # Create the JSON payload for text generation
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt + "Keep it short and concise."}
                ]
            }]
        }
        
        # Convert payload to JSON string and encode to bytes
        data = json.dumps(payload).encode('utf-8')
        
        # Create the request object
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        
        # Send the request and get the response - WITH SSL CONTEXT
        with urllib.request.urlopen(req, context=ssl_context) as response:
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

    def fetch_image(prompt:str)->str:
        """
        Generate an image using the Gemini API and save it to a file.

        Parameters:
        - prompt (str): The text prompt for generating the image.

        Returns:
        - str: The path to the generated image file.
        """
        output_file = os.path.join(images_dir, f"image_{'_'.join(prompt.split(' ')[:2])}.png")
        
        # Check for cached version
        if os.path.exists(output_file):
            print(f"Using cached image: {output_file}")
            return output_file
        
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

        
        # Send the request and get the response - WITH SSL CONTEXT
        with urllib.request.urlopen(req, context=ssl_context) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                return placeholder
            
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
            return output_file

    # Function to convert absolute paths to relative paths for Ren'Py
    def get_image(path):
        import renpy
        if os.path.isabs(path):
            if os.path.exists(path) and path.startswith(renpy.config.gamedir):
                return os.path.relpath(path, renpy.config.gamedir)
            else:
                return "cache/images/placeholder.png"
        else:
            if renpy.loadable(path):
                return path
            else:
                return "cache/images/placeholder.png"
    
    # Callback function to show/hide avatars
    def avatar_callback(event, interact=True, **kwargs):
        character = kwargs.get("who", None)
        if character and character.name in avatar_files:
            avatar_path = avatar_files[character.name]
            avatar_tag = "avatar_" + character.name.lower().replace(" ", "_")
            if event == "begin":
                renpy.show(avatar_path, at_list=[center], layer="screens", tag=avatar_tag)
            elif event == "end":
                renpy.hide(avatar_tag, layer="screens")

# Define characters using the callback
define p = Character("Player", callback=avatar_callback)
define s = Character("Shopkeeper", callback=avatar_callback)
define v = Character("Villager", callback=avatar_callback)
define m = Character("Mysterious Stranger", callback=avatar_callback)

# Define inventory variable
default has_lantern = False

# Game start
label start:
    # Use the placeholder path we defined in the init block
    show screen loading
    
    # Generate avatars BEFORE assigning to avatar_files
    $ player_avatar_path = fetch_image(avatar_prompts["player"])
    $ shopkeeper_avatar_path = fetch_image(avatar_prompts["shopkeeper"])
    $ villager_avatar_path = fetch_image(avatar_prompts["villager"])
    $ stranger_avatar_path = fetch_image(avatar_prompts["stranger"])
    
    # Store avatar files in the dictionary
    $ avatar_files["Player"] = get_image(player_avatar_path)
    $ avatar_files["Shopkeeper"] = get_image(shopkeeper_avatar_path)
    $ avatar_files["Villager"] = get_image(villager_avatar_path)
    $ avatar_files["Mysterious Stranger"] = get_image(stranger_avatar_path)
    
    # Show player avatar using the screen we defined (not the variable name)
    show screen player_avatar
    
    # Load initial scene
    $ home_bg_path = fetch_image("A cozy medieval cottage interior with a fireplace, wooden furniture, and a bed. Sunlight streams through a small window. Style: medieval fantasy, detailed illustration.")
    $ home_bg_file = get_image(home_bg_path)
    $ home_bg = im.Scale(home_bg_file, config.screen_width, config.screen_height)
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
    $ town_bg_path = fetch_image("A bustling medieval town square with market stalls, a central fountain, and timber-framed houses with thatched roofs. Style: medieval fantasy, detailed illustration.")
    $ town_bg_file = get_image(town_bg_path)
    $ town_bg = im.Scale(town_bg_file, config.screen_width, config.screen_height)
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
        "Explore a new area":
            jump explore_new_area
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
    $ shop_bg_path = fetch_image("A medieval shop interior with shelves of goods, a wooden counter, and a merchant. Style: medieval fantasy, detailed illustration.")
    $ shop_bg_file = get_image(shop_bg_path)
    $ shop_bg = im.Scale(shop_bg_file, config.screen_width, config.screen_height)
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
    $ forest_bg_path = fetch_image("A dense medieval forest with tall trees, a winding path, and dappled sunlight. Style: medieval fantasy, detailed illustration.")
    $ forest_bg_file = get_image(forest_bg_path)
    $ forest_bg = im.Scale(forest_bg_file, config.screen_width, config.screen_height)
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

label explore_new_area:
    show screen loading
    $ area_type = renpy.random.choice(["forest", "cave", "mountain", "village", "ruins", "lake", "desert"])
    $ features = {
        "forest": ["dense", "sparse", "enchanted", "dark"],
        "cave": ["spooky", "crystal", "underground", "lava"],
        "mountain": ["snowy", "rocky", "misty", "volcanic"],
        "village": ["bustling", "abandoned", "coastal", "mountain"],
        "ruins": ["ancient", "crumbling", "overgrown", "desert"],
        "lake": ["serene", "misty", "frozen", "volcanic"],
        "desert": ["sandy", "rocky", "oasis", "dune"]
    }
    $ times = ["daytime", "nighttime", "dawn", "dusk"]
    $ weathers = ["clear", "rainy", "foggy", "snowy"]
    $ feature = renpy.random.choice(features.get(area_type, ["mysterious"]))
    $ time = renpy.random.choice(times)
    $ weather = renpy.random.choice(weathers)
    $ image_prompt = f"A {feature} {area_type} at {time} with {weather} weather. Style: medieval fantasy, detailed illustration."
    $ new_area_bg_path = fetch_image(image_prompt)
    $ new_area_bg_file = get_image(new_area_bg_path)
    $ new_area_bg = im.Scale(new_area_bg_file, config.screen_width, config.screen_height)
    $ text_prompt = f"Describe a {feature} {area_type} at {time} with {weather} weather in a medieval fantasy setting."
    $ new_area_text = fetch_text(text_prompt)
    $ area_name = "The " + feature.capitalize() + " " + area_type.capitalize()
    hide screen loading
    scene expression new_area_bg with dissolve
    p "You venture into [area_name]."
    p "[new_area_text]"
    p "What would you like to do?"
    menu:
        "Explore further":
            "You decide to explore this area more, but for now, you return to the town square."
            jump town_square
        "Return to town square":
            jump town_square

label meet_stranger:
    show screen loading
    $ stranger_text = fetch_text("Generate a mysterious dialogue for a cloaked stranger in a forest, hinting at a quest in a medieval RPG.")
    hide screen loading
    m "[stranger_text]"
    "The stranger vanishes, leaving you with a sense of purpose."
    "To be continued..."
    return