# DynamicVN - AI-Generated Visual Novel Game

DynamicVN is an interactive visual novel game built with Ren'Py that uses Google's Gemini API to dynamically generate images and text for a unique gameplay experience each time you play.

## Game Overview

Embark on a medieval fantasy adventure where you'll explore a cozy cottage, town square, forests, and other procedurally generated locations. Interact with characters, collect items, and uncover a mysterious quest. The game features AI-generated backgrounds, descriptions, and dialogues that create a unique experience with each playthrough.

## Prerequisites

- [Ren'Py 8.3.0+](https://www.renpy.org/latest.html) - Visual Novel Engine
- Google Gemini API Key (for image and text generation)
- Python 3.6 or higher
- Python packages:
  - Pillow (PIL)

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/DynamicVN.git
   cd DynamicVN
   ```

2. Set up your Gemini API key as an environment variable:
   ```bash
   # On Linux/macOS
   export GEMINI_API_KEY="your-api-key-here"
   
   # On Windows (Command Prompt)
   set GEMINI_API_KEY=your-api-key-here
   
   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="your-api-key-here"
   ```

3. Make sure you have the required Python packages installed:
   ```
   pip install pillow
   ```

## Running the Game

1. Start the Ren'Py launcher
2. From the launcher, select "DynamicVN" from your projects list
3. Click "Launch Project" to start the game

Alternatively, you can run the game directly from the Ren'Py SDK:
```bash
# Navigate to your Ren'Py SDK directory
cd path/to/renpy-sdk

# Run the game (replace with your actual path)
./renpy.sh /home/tony/Desktop/DynamicVN/DynamicVN
```

## How to Play

### Game Controls
- **Left mouse button** - Advance dialogue, make choices
- **Space/Enter** - Advance dialogue
- **Esc** - Access game menu
- **Ctrl** - Skip dialogue
- **Tab** - Toggle skip mode
- **A** - Auto-advance text
- **S** - Screenshot
- **Back/Mouse 4** - Roll back to previous choice

### Gameplay Guide

1. **Start at your cottage**: The game begins in a cozy medieval cottage. You'll be presented with options to go to the town square or stay home.

2. **Explore the town square**: Here you can:
   - Talk to villagers for information
   - Visit the shop to buy items (like a lantern)
   - Head to the forest for adventure
   - Explore new randomly generated areas
   - Return to your cottage

3. **Visit the shop**: You can purchase a lantern which is required to explore deeper into the forest.

4. **Explore the forest**: With a lantern, you can venture deeper into the forest and encounter a mysterious stranger with a potential quest.

5. **Discover new areas**: Use the "Explore a new area" option to discover procedurally generated locations with unique descriptions and visuals.

## Features

- **Dynamic content generation**: AI-generated images and text create a unique experience each playthrough
- **Exploration system**: Visit various locations with contextual interactions
- **Inventory system**: Collect and use items that affect gameplay options
- **Procedural area generation**: Discover new locations with varying features, times of day, and weather conditions

## Troubleshooting

- If images don't load properly, check that:
  - Your Gemini API key is set correctly
  - You have an active internet connection
  - The game's cache directories exist (they're created automatically on first run)

- If you encounter any errors related to the Gemini API, check the console output for details.

## License

[Include your license information here]

## Acknowledgements

- Built with [Ren'Py](https://www.renpy.org/), a visual novel engine
- Uses Google's [Gemini API](https://ai.google.dev/gemini-api) for dynamic content generation
