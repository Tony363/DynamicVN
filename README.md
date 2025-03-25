# DynamicVN - AI-Generated Visual Novel Game

DynamicVN is an interactive visual novel game built with Ren'Py that uses Google's Gemini API for image generation and OpenAI's GPT models for dynamic story generation, creating a unique gameplay experience each time you play.

## Game Overview

Embark on a medieval fantasy adventure where you'll explore a cozy cottage, town square, forests, and other procedurally generated locations. Interact with characters, collect items, and uncover a mysterious quest. The game features AI-generated backgrounds, descriptions, and dialogues that create a unique experience with each playthrough.

After completing the initial adventure, you'll transition to the AutoScriptPlugin which generates a completely dynamic storyline based on your choices and interactions.

## Prerequisites

- [Ren'Py 8.3.0+](https://www.renpy.org/latest.html) - Visual Novel Engine
- Google Gemini API Key (for image generation)
- OpenAI API Key (for dynamic story generation)
- Python 3.6 or higher
- Python packages:
  - Pillow (PIL)
  - requests

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/DynamicVN.git
   cd DynamicVN
   ```

2. Set up your API keys as environment variables:
   ```bash
   # On Linux/macOS
   export GEMINI_API_KEY="your-gemini-api-key-here"
   export OPENAI_API_KEY="your-openai-api-key-here"
   
   # On Windows (Command Prompt)
   set GEMINI_API_KEY=your-gemini-api-key-here
   set OPENAI_API_KEY=your-openai-api-key-here
   
   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="your-gemini-api-key-here"
   $env:OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. Make sure you have the required Python packages installed:
   ```
   pip install pillow requests
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

6. **Transition to AutoScriptPlugin**: After meeting the mysterious stranger in the forest, you'll transition to the AutoScriptPlugin which generates a dynamic storyline based on your choices.

### AutoScriptPlugin Features

The AutoScriptPlugin is a powerful addition that takes over after the initial adventure, providing:

- **Dynamic character creation**: The game will generate a unique character with their own personality, background, and attributes.

- **Adaptive storytelling**: The story adapts to your choices and interactions, creating a unique narrative path each time you play.

- **Character attributes**: Characters have various attributes that change based on your interactions, affecting the story's progression.

- **Real-time image generation**: Background images are generated in real-time based on the current scene description, providing visual context for the story.

- **Character status tracking**: View your character's status and attributes through the in-game interface.

- **Save/Load functionality**: Save your progress and continue your adventure later.

#### AutoScript Interface

During the AutoScript portion of the game, you'll have access to several interface options:

- **Reset Game**: Resets the game and starts a new story.
- **Save Game**: Saves your current progress.
- **Character Info**: View information about your character.
- **Character Status**: Check your character's current attributes and status.

## Features

- **Dynamic content generation**: AI-generated images and text create a unique experience each playthrough
- **Exploration system**: Visit various locations with contextual interactions
- **Inventory system**: Collect and use items that affect gameplay options
- **Procedural area generation**: Discover new locations with varying features, times of day, and weather conditions
- **Dynamic storytelling**: The AutoScriptPlugin generates a unique storyline based on your choices and interactions
- **Character development**: Characters evolve based on your interactions, with changing attributes and relationships

## Troubleshooting

- If images don't load properly, check that:
  - Your Gemini API key is set correctly
  - You have an active internet connection
  - The game's cache directories exist (they're created automatically on first run)

- If the dynamic story generation doesn't work, check that:
  - Your OpenAI API key is set correctly
  - The API key has sufficient credits/quota
  - You're using a supported OpenAI model (default is gpt-4o-mini)

- If you encounter HTTP 401 errors:
  - This usually means your API key is invalid or has expired
  - Check that your environment variables are set correctly
  - Verify that your API keys have the necessary permissions

- If you see "None" for image prompts:
  - This is normal and just means the system couldn't extract a specific image prompt
  - The game will still generate appropriate images based on the context

## Customizing the Experience

You can customize various aspects of the AutoScriptPlugin by editing the following files:

- **Story themes**: Modify or create new story themes in `DynamicVN/game/RenPy-AutoScriptPlugin/Stories/`
- **Character attributes**: Edit character attributes in the respective story folder's `character_attributes.json`
- **End conditions**: Change how the story can end in `end_conditions.json`
- **Model selection**: Change the OpenAI model in `main.rpy` by modifying the `MODEL_NAME` variable

## License

[Include your license information here]

## Acknowledgements

- Built with [Ren'Py](https://www.renpy.org/), a visual novel engine
- Uses Google's [Gemini API](https://ai.google.dev/gemini-api) for image generation
- Uses OpenAI's [GPT models](https://openai.com/api/) for dynamic story generation
