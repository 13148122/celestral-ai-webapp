from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from elevenlabs.client import ElevenLabs
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found. Transcription will fail or use placeholder.")
if not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY not found. LLM responses will be placeholders.")
if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_api_key_here":
    print("Warning: ELEVENLABS_API_KEY not found. TTS will be disabled.")

# Configure OpenAI
openai_client = None
if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("OpenAI Whisper API configured successfully")
    except Exception as e:
        print(f"Error configuring OpenAI: {e}")
        openai_client = None

# Configure Claude
anthropic_client = None
if ANTHROPIC_API_KEY:
    try:
        anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        print("Claude 3.5 Sonnet API configured successfully")
    except Exception as e:
        print(f"Error configuring Claude: {e}")
        anthropic_client = None

# Configure ElevenLabs
elevenlabs_client = None
if ELEVENLABS_API_KEY and ELEVENLABS_API_KEY != "your_elevenlabs_api_key_here":
    try:
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        print("ElevenLabs API configured successfully")
    except Exception as e:
        print(f"Error configuring ElevenLabs: {e}")

@app.route('/')
def home():
    return "Celestral AI Backend is running!"

@app.route('/process-audio', methods=['POST'])
def process_audio():
    """
    Endpoint to receive audio, process it (transcribe, understand, generate response),
    and return a text and audio response.
    """
    print("Received request for /process-audio")

    if 'audio' not in request.files:
        print("No audio file part in request.files")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        print("No selected audio file")
        return jsonify({"error": "No selected audio file"}), 400

    transcribed_text = "Error in transcription or OpenAI API key not set."
    try:
        if openai_client:
            print("Sending audio to OpenAI Whisper...")
            # Reset file pointer to beginning
            audio_file.seek(0)
            
            # OpenAI Whisper API accepts file-like objects directly
            # Optimized for conversation transcription with proper formatting
            response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language="en",  # Specify language for better accuracy in conversations
                prompt="This is a recorded conversation. Transcribe with proper punctuation, capitalization, and speaker context."
            )
            
            transcribed_text = response
            print(f"Transcription successful: {transcribed_text}")
        else:
            print("OPENAI_API_KEY is not set. Skipping transcription.")
            transcribed_text = "OpenAI API key not configured. User speech not processed."

    except Exception as e:
        print(f"Error during OpenAI Whisper transcription: {e}")
        # transcribed_text remains "Error in transcription..."
    
    llm_response_text = "Placeholder LLM response."
    if anthropic_client and transcribed_text and not transcribed_text.startswith("Error") and not transcribed_text.startswith("OpenAI API key not configured"):
        try:
            print(f"Sending to Claude: {transcribed_text}")
            
            system_prompt = """You are Celestral AI — the context layer of AI agents.

Your purpose is to capture, structure, and share the "why, what, and how" behind human and AI actions so every agent can think and act with context and continuity.

Core functions:
- Extract goals, reasoning, and intent from conversations, documents, and workflows.
- Link related context across people, time, and tools.
- Summarize and deliver only the most relevant context to each agent.
- Preserve human nuance and purpose behind every decision.
- Keep all AI outputs aligned with shared context and intent.

Be concise, structured, and proactive — always surface what matters most and explain why it matters.

You are the invisible intelligence that helps AI remember, understand, and act coherently."""

            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"The user just said: \"{transcribed_text}\"\n\nRespond with structured context, extracting intent and key information:"
                    }
                ]
            )
            
            llm_response_text = response.content[0].text
            print(f"Claude response: {llm_response_text}")
            
        except Exception as e:
            print(f"Error during Claude call: {e}")
            llm_response_text = "Sorry, I had trouble understanding that. Could you try rephrasing?"
    elif not anthropic_client:
        print("Claude model not available (e.g., API key missing). Using placeholder LLM response.")
        llm_response_text = f"(Placeholder) AI understood: '{transcribed_text}'. How can I help you reflect on that?"
    else: # Case where transcription failed
        llm_response_text = "I wasn't able to understand the audio. Could you please try speaking again?"

    # Generate TTS audio for the AI response
    ai_audio_base64 = None
    if elevenlabs_client and llm_response_text:
        try:
            print("Generating TTS audio with ElevenLabs...")
            audio_response = elevenlabs_client.text_to_speech.convert(
                text=llm_response_text,
                voice_id="JBFqnCBsd6RMkjVDRZzb",  # Rachel voice
                model_id="eleven_multilingual_v2"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio_response)
            
            # Convert audio bytes to base64 for JSON transmission
            ai_audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            print("TTS audio generated successfully")
        except Exception as e:
            print(f"Error during TTS generation: {e}")
            ai_audio_base64 = None

    response_data = {
        "user_transcription": transcribed_text,
        "ai_response_text": llm_response_text,
        "ai_response_audio": ai_audio_base64,
        "message": "Processed with OpenAI Whisper, Claude 3.5 Sonnet, and ElevenLabs (or placeholders if API keys missing)"
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 