init -10 python:
    import os
    from PIL import Image as PILImage
    import io
    
    # Create placeholder image directory if it doesn't exist
    placeholder_dir = os.path.join(config.gamedir, "cache", "images")
    if not os.path.exists(placeholder_dir):
        os.makedirs(placeholder_dir)
        
    # Create a single placeholder image we can reuse
    placeholder_path = os.path.join(placeholder_dir, "placeholder.png")
    if not os.path.exists(placeholder_path):
        img = PILImage.new('RGBA', (512, 512), (128, 128, 128, 255))
        img.save(placeholder_path)
    
    # Path conversion function
    def get_image(path):
        # If path is absolute, convert to a relative path that Ren'Py can use
        if os.path.isabs(path):
            # Check if path is within the game directory
            rel_path = os.path.relpath(path, config.gamedir) if path.startswith(config.gamedir) else None
            
            # If image doesn't exist or is outside game directory, use placeholder
            if not rel_path or not renpy.loadable(rel_path):
                # Return the placeholder image (using relative path)
                return "cache/images/placeholder.png"
            else:
                # Return the relative path
                return rel_path
        else:
            # For relative paths, check if they exist
            if renpy.loadable(path):
                return path
            else:
                return "cache/images/placeholder.png" 

label some_label:
    $ image_path = fetch_image(prompt)
    $ safe_image_path = get_image(image_path)
    show expression safe_image_path 