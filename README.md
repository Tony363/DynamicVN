# DynamicVN - AI-Powered Visual Novel

DynamicVN is an interactive visual novel powered by AI that generates dynamic storylines, character interactions, and images in real-time.

## Features

- **Dynamic Storytelling**: Stories adapt based on your choices and character interactions
- **AI-Generated Content**: Uses OpenAI's GPT models for text and Gemini for image generation
- **Character Attributes**: Characters have attributes that change based on your interactions
- **Visual Experience**: Displays character avatars and scene images to enhance immersion

## How to Play

1. **Setup**:
   - Ensure you have [Ren'Py](https://www.renpy.org/) installed (version 7.4 or higher recommended)
   - Set the following environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key for text generation
     - `GEMINI_API_KEY`: Your Google Gemini API key for image generation

2. **Launch the Game**:
   - Open the project in Ren'Py Launcher
   - Click "Launch Project" to start the game

3. **Gameplay**:
   - **Initial Story**: The game starts with a basic setup where you can explore different areas
   - **Character Interaction**: Talk to characters and make choices that affect your relationship
   - **Auto-Generated Content**: After meeting the mysterious stranger, the game transitions to the auto-generated content
   - **Decision Making**: Choose from menu options or input your own text to influence the story
   - **Attribute Changes**: Your choices affect character attributes, which can lead to different story paths and endings

4. **Controls**:
   - **Left Click/Enter**: Advance dialogue
   - **Space**: Skip dialogue (hold)
   - **Escape**: Access game menu
   - **S**: Save game
   - **L**: Load game

## Story Themes

The game includes several story themes that can be selected:
- Fantasy adventures
- Cyberpunk hacker's quest
- Corporate tycoon simulation
- And more!

Each theme has unique character attributes and ending conditions.

## Technical Details

- **Image Generation**: Scene images and character avatars are generated using Google's Gemini API
- **Text Generation**: Story content is generated using OpenAI's GPT models
- **Caching**: Generated images are cached to improve performance and reduce API calls
- **Attribute System**: Characters have dynamic attributes that change based on player choices

## Tips for Best Experience

1. **API Keys**: Make sure your API keys are valid and have sufficient quota
2. **Internet Connection**: The game requires an active internet connection for AI generation
3. **Patience**: Image generation may take a few seconds, especially on first run
4. **Exploration**: Try different choices to see how the story adapts
5. **Custom Input**: Use the "Input your own text" option for more personalized interactions

## Troubleshooting

- **Missing Images**: If images don't appear, check your Gemini API key and internet connection
- **Text Generation Issues**: Verify your OpenAI API key is valid
- **Performance**: Close other applications to ensure smooth gameplay
- **Cache Issues**: If you encounter strange behavior, try clearing the cache folder

Enjoy your dynamic visual novel experience!
