init -10 python:
    import os
    import io
    import renpy.display.image
    from renpy.display.imagelike import Solid
    
    # Create placeholder image directory if it doesn't exist
    placeholder_dir = os.path.join(config.gamedir, "cache", "images")
    if not os.path.exists(placeholder_dir):
        os.makedirs(placeholder_dir)
        
    # Define placeholder path
    placeholder_path = os.path.join(placeholder_dir, "placeholder.png")
    
    # Check if placeholder exists, if not we'll use Ren'Py's built-in solid color
    has_placeholder = os.path.exists(placeholder_path)
    
    # Path conversion function
    def get_image(path):
        # If path is absolute, convert to a relative path that Ren'Py can use
        if os.path.isabs(path):
            # Check if path is within the game directory
            rel_path = os.path.relpath(path, config.gamedir) if path.startswith(config.gamedir) else None
            
            # If image doesn't exist or is outside game directory, use placeholder
            if not rel_path or not renpy.loadable(rel_path):
                # Use placeholder if it exists, otherwise use a solid color
                if has_placeholder and renpy.loadable("cache/images/placeholder.png"):
                    return "cache/images/placeholder.png"
                else:
                    return Solid("#808080")  # Gray solid color as fallback
            else:
                # Return the relative path
                return rel_path
        else:
            # For relative paths, check if they exist
            if renpy.loadable(path):
                return path
            else:
                # Use placeholder if it exists, otherwise use a solid color
                if has_placeholder and renpy.loadable("cache/images/placeholder.png"):
                    return "cache/images/placeholder.png"
                else:
                    return Solid("#808080")  # Gray solid color as fallback

label some_label:
    $ image_path = fetch_image(prompt)
    $ safe_image_path = get_image(image_path)
    show expression safe_image_path
