# Celestral AI

Celestral AI is a conversational legacy keeper that turns everyday conversations into a rich personal archive.

## Project Overview

This project aims to build a web application with the following core features:
- Voice input from users.
- Transcription of voice input (using Deepgram).
- Understanding, summarization, and narrative generation (using Anthropic Claude 3 Sonnet).
- Text-to-speech for AI responses (using ElevenLabs).
- Smart archiving of conversations.
- Voice-to-story mode.
- Reflection prompts.
- Output features like timeline view, searchable memories, and life digests.

This `README.md` will be updated as the project progresses.

## Setup (Initial)

1.  **Backend**:
    - Navigate to the `backend` directory.
    - Create a virtual environment: `python -m venv venv`
    - Activate it:
        - Windows: `venv\Scripts\activate`
        - macOS/Linux: `source venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`
    - (Coming soon) Create a `.env` file in the `backend` directory and add your API keys:
      ```
      DEEPGRAM_API_KEY=your_deepgram_api_key
      ANTHROPIC_API_KEY=your_anthropic_api_key
      ELEVENLABS_API_KEY=your_elevenlabs_api_key
      ```
    - Run the Flask app: `flask run` (or `python app.py`)

2.  **Frontend**:
    - Open `frontend/index.html` in your web browser.

## Development Phases

- **Phase 1: Basic Structure (Current)**
    - Setup project directories.
    - Basic Flask backend.
    - Basic HTML/JS frontend for audio input and displaying (dummy) text output.
- **Phase 2: API Integrations**
    - Integrate Deepgram for transcription.
    - Integrate Anthropic Claude 3 Sonnet for NLU/NLG.
    - Integrate ElevenLabs for TTS.
- **Phase 3: Core Features**
    - Implement smart archiving (tagging).
    - Develop voice-to-story mode.
    - Add reflection prompts.
- **Phase 4: UI/UX Enhancements**
    - Implement timeline view, searchable memories, life digests.
    - Refine user interface. 