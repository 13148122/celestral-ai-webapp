# Celestral AI

**The context layer of AI agents** — Celestral AI turns everyday conversations into a rich personal archive with intelligent context extraction.

## 🎯 Project Overview

Celestral AI is a voice-powered conversational AI that:
- **Captures** multi-speaker conversations with accurate transcription
- **Understands** context, intent, and meaning using advanced AI
- **Responds** with natural voice synthesis
- **Archives** conversations for future reference

### Current Features ✅

- **Voice Input**: Record conversations in real-time
- **Dual Transcription**: 
  - OpenAI Whisper for accurate transcription
  - Deepgram Nova-2 for speaker diarization (who said what)
- **AI Understanding**: Claude 3 Opus for context extraction and intelligent responses
- **Voice Output**: ElevenLabs for natural text-to-speech
- **Parallel Processing**: Whisper and Deepgram run simultaneously for maximum speed

### Planned Features 🚀

- Smart archiving with automatic tagging
- Voice-to-story mode
- Reflection prompts
- Timeline view, searchable memories, and life digests

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Transcription** | OpenAI Whisper API |
| **Diarization** | Deepgram Nova-2 |
| **LLM** | Anthropic Claude 3 Opus |
| **TTS** | ElevenLabs |
| **Deployment** | Vercel (Serverless) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- API Keys for:
  - OpenAI (Whisper)
  - Anthropic (Claude)
  - ElevenLabs (TTS)
  - Deepgram (Diarization) - optional but recommended

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/13148122/celestral-ai-webapp.git
   cd celestral-ai-webapp
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```
   
   Server will start at `http://localhost:5000`

5. **Test the API**
   
   Use Postman or curl:
   ```bash
   curl -X POST http://localhost:5000/process-audio \
     -F "audio=@your_audio_file.mp3"
   ```

---

## 📡 API Endpoints

### `POST /process-audio`

Process audio with transcription, diarization, and AI response.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `audio` (file, max 25MB)

**Response:**
```json
{
  "user_transcription": "Raw transcription text",
  "speaker_transcription": "Speaker 0: Hello\nSpeaker 1: Hi there",
  "speaker_count": 2,
  "ai_response_text": "AI's contextual response",
  "ai_response_audio": "base64_encoded_audio",
  "message": "Processing status"
}
```

---

## 🔧 Configuration

### Audio Optimization

The backend automatically optimizes audio for faster processing:
- Converts to mono
- Reduces sample rate to 16kHz
- Compresses with lower bitrate
- Removes silence from beginning/end

### Whisper Settings

```python
model="whisper-1"
response_format="verbose_json"  # For word timestamps
language="en"
temperature=0  # Deterministic output
```

### Deepgram Settings

```python
model="nova-2"  # Most accurate
diarize=True    # Speaker detection
language="en"
```

---

## 🌐 Deployment

### Vercel Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - Vercel will auto-detect the Flask app

3. **Set environment variables**
   
   In Vercel dashboard, add:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `ELEVENLABS_API_KEY`
   - `DEEPGRAM_API_KEY`

4. **Deploy**
   
   Vercel will automatically deploy on every push to `main`

**Live URL**: https://celestral-ai-webapp.vercel.app

---

## 📚 Documentation

- **[Diarization Setup Guide](DIARIZATION_SETUP.md)** - Complete guide for speaker diarization
- **[Whisper Optimizations](WHISPER_OPTIMIZATIONS.md)** - Audio processing optimizations

---

## 💰 Cost Estimates

Per minute of audio:
- OpenAI Whisper: ~$0.006/min
- Deepgram Nova-2: ~$0.0043/min
- Claude 3 Opus: ~$0.015/request (varies by response length)
- ElevenLabs: ~$0.18/1000 characters

**Total**: ~$0.02-0.05 per conversation (depending on length)

---

## 🐛 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Ensure `.env` file exists in `backend/` directory
   - Restart Flask server after adding keys

2. **"Audio file too large"**
   - Max file size: 25MB
   - Use compressed formats (MP3, M4A)

3. **"Deepgram diarization failed"**
   - Check Deepgram API key is valid
   - Verify account has credits
   - System will fallback to Whisper-only transcription

4. **"Failed to fetch"**
   - Ensure Flask server is running
   - Check CORS is enabled
   - Verify frontend is using correct backend URL

---

## 🤝 Contributing

This is a private project for Celestral AI. For questions or issues, contact the development team.

---

## 📄 License

Proprietary - All rights reserved

---

## 🔗 Links

- **GitHub**: https://github.com/13148122/celestral-ai-webapp
- **Live Demo**: https://celestral-ai-webapp.vercel.app
- **Deepgram Console**: https://console.deepgram.com/
- **OpenAI Platform**: https://platform.openai.com/
- **Anthropic Console**: https://console.anthropic.com/
- **ElevenLabs**: https://elevenlabs.io/

---

**Status**: ✅ Production Ready (MVP)
**Last Updated**: October 31, 2025 