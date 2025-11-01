# Vercel Deployment Guide - Adding Deepgram API Key

## ✅ Code Status
- ✅ All code changes committed and pushed to GitHub
- ✅ Commit: `0d3e349` - "Add Deepgram speaker diarization with parallel processing"
- ✅ Local testing successful (2 speakers detected)

---

## 🚀 Deploy to Vercel

### Step 1: Add Deepgram API Key to Vercel

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Navigate to your project: **celestral-ai-webapp**

2. **Open Project Settings**
   - Click on your project
   - Click **Settings** (top navigation)

3. **Add Environment Variable**
   - Click **Environment Variables** (left sidebar)
   - Click **Add New** button

4. **Configure the Variable**
   - **Key**: `DEEPGRAM_API_KEY`
   - **Value**: `c0f8d418026949c7e1ea38811dd76dcb74054546`
   - **Environment**: Select all (Production, Preview, Development)
   - Click **Save**

### Step 2: Verify All Environment Variables

Make sure you have all 4 API keys configured in Vercel:

| Variable | Status | Purpose |
|----------|--------|---------|
| `OPENAI_API_KEY` | ✅ Should exist | Whisper transcription |
| `ANTHROPIC_API_KEY` | ✅ Should exist | Claude 3 Opus LLM |
| `ELEVENLABS_API_KEY` | ✅ Should exist | Text-to-speech |
| `DEEPGRAM_API_KEY` | 🆕 **ADD THIS** | Speaker diarization |

### Step 3: Redeploy

**Option A - Automatic (Recommended)**:
- Vercel will automatically redeploy when you add the environment variable
- Wait 1-2 minutes for deployment to complete

**Option B - Manual**:
- Go to **Deployments** tab
- Click the **⋮** menu on the latest deployment
- Click **Redeploy**
- Select **Use existing Build Cache** (faster)
- Click **Redeploy**

### Step 4: Test Production Deployment

Once deployed, test with Postman:

**URL**: `https://celestral-ai-webapp.vercel.app/process-audio`

**Request**:
- Method: `POST`
- Body: `form-data`
- Key: `audio` (File type)
- Value: Upload your test audio

**Expected Response**:
```json
{
  "user_transcription": "...",
  "speaker_transcription": "Speaker 0: ...\nSpeaker 1: ...",
  "speaker_count": 2,
  "ai_response_text": "...",
  "ai_response_audio": "...",
  "message": "Processed with OpenAI Whisper, Deepgram diarization, Claude 3 Opus, and ElevenLabs"
}
```

---

## 🔍 Troubleshooting

### Issue: Deployment fails
**Solution**: Check Vercel deployment logs for errors

### Issue: `speaker_transcription` is still `null` in production
**Possible causes**:
1. Environment variable not saved correctly
2. Deployment didn't pick up the new variable
3. Need to redeploy after adding the variable

**Solution**:
- Verify the `DEEPGRAM_API_KEY` is visible in Vercel settings
- Trigger a manual redeploy
- Check deployment logs for "Deepgram API configured successfully"

### Issue: "quota_exceeded" error
**Solution**: 
- This is for ElevenLabs (TTS), not Deepgram
- Your ElevenLabs account has run out of credits
- Either add more credits or the system will work without TTS audio

---

## 📊 Deployment Checklist

- [ ] Add `DEEPGRAM_API_KEY` to Vercel environment variables
- [ ] Verify all 4 API keys are configured
- [ ] Wait for automatic redeploy (or trigger manual redeploy)
- [ ] Test production endpoint with Postman
- [ ] Verify `speaker_transcription` is not `null`
- [ ] Verify `speaker_count` > 0 for multi-speaker audio

---

## 🎯 Expected Behavior

### Local (Working Now):
```
✅ Deepgram API configured successfully
✅ Diarization complete: 2 speaker(s) detected
✅ Speaker diarization successful: 2 speaker(s)
```

### Production (After Adding Key):
```
✅ Same behavior as local
✅ speaker_transcription field populated
✅ speaker_count shows correct number
```

---

## 📝 Notes

- **Cost**: Deepgram adds ~$0.0043/minute to your processing cost
- **Performance**: No additional latency (parallel processing)
- **Fallback**: If Deepgram fails, system returns Whisper-only transcription
- **API Key**: Stored securely in Vercel environment variables (not in code)

---

**Next Step**: Go to Vercel dashboard and add the `DEEPGRAM_API_KEY` environment variable!

**Vercel Dashboard**: https://vercel.com/dashboard
**Project**: celestral-ai-webapp

