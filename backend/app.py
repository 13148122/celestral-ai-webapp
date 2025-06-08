from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API keys from environment variables
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not DEEPGRAM_API_KEY:
    print("Warning: DEEPGRAM_API_KEY not found. Transcription will fail or use placeholder.")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found. LLM responses will be placeholders.")
if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_api_key_here":
    print("Warning: ELEVENLABS_API_KEY not found. TTS will be disabled.")

# Configure Gemini
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("Gemini 1.5 Flash Latest API configured successfully")
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        model = None

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

    transcribed_text = "Error in transcription or Deepgram API key not set."
    try:
        if DEEPGRAM_API_KEY:
            deepgram = DeepgramClient(DEEPGRAM_API_KEY)
            buffer_data = audio_file.read()
            payload = {"buffer": buffer_data}
            options = PrerecordedOptions(model="nova-2", smart_format=True)
            
            print("Sending audio to Deepgram...")
            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
            transcribed_text = response.results.channels[0].alternatives[0].transcript
            print(f"Transcription successful: {transcribed_text}")
        else:
            print("DEEPGRAM_API_KEY is not set. Skipping transcription.")
            transcribed_text = "Deepgram API key not configured. User speech not processed."

    except Exception as e:
        print(f"Error during Deepgram transcription: {e}")
        # transcribed_text remains "Error in transcription..."
    
    llm_response_text = "Placeholder LLM response."
    if model and transcribed_text and not transcribed_text.startswith("Error") and not transcribed_text.startswith("Deepgram API key not configured"):
        try:
            print(f"Sending to Gemini: {transcribed_text}")
            
            prompt = f"""You are Celestral AI, a friendly and empathetic conversational legacy keeper. Your goal is to help users turn their everyday conversations into a rich personal archive, blending journaling, storytelling, and reflection.

Listen carefully to what the user says and respond in a way that encourages them to share more, reflect, or tell stories. Keep your responses relatively concise and conversational.

The user just said: "{transcribed_text}"

Based on this, what is a thoughtful and encouraging response? If they mentioned an event, ask a follow-up question. If they mentioned a feeling, acknowledge it. If they mentioned a memory, perhaps ask for more detail or how it made them feel."""

            response = model.generate_content(prompt)
            llm_response_text = response.text
            print(f"Gemini response: {llm_response_text}")
            
        except Exception as e:
            print(f"Error during Gemini call: {e}")
            llm_response_text = "Sorry, I had trouble understanding that. Could you try rephrasing?"
    elif not model:
        print("Gemini model not available (e.g., API key missing). Using placeholder LLM response.")
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
        "message": "Processed with Deepgram, Gemini, and ElevenLabs (or placeholders if API keys missing)"
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 