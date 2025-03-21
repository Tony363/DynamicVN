# Add this at the beginning of your script file (after the init -100 python block)
init:
    # Define transforms for different image types
    transform fullscreen_bg:
        size (config.screen_width, config.screen_height)
        xalign 0.5
        yalign 0.5
    
    # For character sprites or other elements that should maintain aspect ratio
    transform fit_width:
        xalign 0.5
        yalign 1.0
        fit "contain"
        size (config.screen_width, None) 

def get_image(path, is_background=True):
    if os.path.isabs(path):
        if os.path.exists(path) and path.startswith(config.gamedir):
            rel_path = os.path.relpath(path, config.gamedir)
        else:
            rel_path = "cache/images/placeholder.png"
    else:
        if renpy.loadable(path):
            rel_path = path
        else:
            rel_path = "cache/images/placeholder.png"
    
    # Apply fullscreen transform for backgrounds
    if is_background:
        return Transform(rel_path, size=(config.screen_width, config.screen_height))
    else:
        return rel_path

label start:
    $ home_bg = fetch_image("A cozy medieval cottage interior...")
    $ safe_path = get_image(home_bg, is_background=True)
    scene expression safe_path
    
    # ... rest of your code ... 