# ngrok Setup Guide - Expose Local Backend to Internet

## 🎯 What This Does

Exposes your local Flask backend (`http://localhost:5000`) to the internet so your deployed v0 frontend can access it.

---

## 📥 Step 1: Install ngrok

### Download ngrok:
1. Go to https://ngrok.com/download
2. Sign up for a free account
3. Download ngrok for Windows
4. Extract the ZIP file to a folder (e.g., `C:\ngrok\`)

### Add to PATH (Optional but Recommended):
1. Copy the path where you extracted ngrok (e.g., `C:\ngrok\`)
2. Search "Environment Variables" in Windows
3. Click "Environment Variables"
4. Under "System variables", find "Path"
5. Click "Edit" → "New"
6. Paste the ngrok folder path
7. Click OK

---

## 🔑 Step 2: Authenticate ngrok

1. Go to https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy your authtoken
3. Open PowerShell and run:

```powershell
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

---

## 🚀 Step 3: Start Your Flask Backend

**Terminal 1** (Keep this running):

```powershell
cd "D:\Alldata\Desktop\Celestral AI\Local MVP\backend"
python app.py
```

You should see:
```
✅ Deepgram API configured successfully
✅ OpenAI Whisper API configured successfully
✅ Claude 3 Opus API configured successfully
✅ ElevenLabs API configured successfully
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Step 4: Expose with ngrok

**Terminal 2** (New PowerShell window):

```powershell
ngrok http 5000
```

You'll see something like:

```
ngrok                                                                           

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def456.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the Forwarding URL**: `https://abc123def456.ngrok-free.app`

---

## 📡 Step 5: Update Your v0 Frontend

### Your API Endpoint:

```
https://abc123def456.ngrok-free.app/process-audio
```

**Replace `abc123def456.ngrok-free.app` with YOUR actual ngrok URL**

### In your v0 frontend code:

```typescript
// Replace this:
const API_URL = 'https://celestral-ai-webapp.vercel.app/process-audio';

// With this:
const API_URL = 'https://abc123def456.ngrok-free.app/process-audio';
```

---

## 🧪 Step 6: Test the Connection

### Test with Postman:

1. **Method**: `POST`
2. **URL**: `https://your-ngrok-url.ngrok-free.app/process-audio`
3. **Body**: form-data, `audio` (File)
4. **Send**

**Expected**: Same response as localhost (with speaker diarization working!)

---

## 📊 Monitor Requests

ngrok provides a web interface to see all requests:

**Open in browser**: http://localhost:4040

You'll see:
- All incoming requests
- Request/response details
- Timing information
- Errors

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ **URL changes** every time you restart ngrok
- ✅ **Random subdomain** (e.g., `abc123.ngrok-free.app`)
- ✅ **No custom domain**
- ✅ **Session expires** after 2 hours (need to restart)
- ✅ **Rate limits** apply

### Paid Tier Benefits ($8/mo):
- ✅ **Static domain** (same URL every time)
- ✅ **No session timeout**
- ✅ **Higher rate limits**
- ✅ **Custom domains**

---

## 🔄 Daily Workflow

### Every time you work on your project:

**Terminal 1**:
```powershell
cd "D:\Alldata\Desktop\Celestral AI\Local MVP\backend"
python app.py
```

**Terminal 2**:
```powershell
ngrok http 5000
```

**Copy the new ngrok URL** and update your v0 frontend if it changed.

---

## 🎯 Alternative: Use Static Domain (Paid)

If you upgrade to ngrok Pro ($8/mo):

```powershell
ngrok http 5000 --domain=your-custom-name.ngrok-free.app
```

Then your URL never changes! Update your v0 frontend once and forget about it.

---

## 🐛 Troubleshooting

### Issue: "command not found: ngrok"
**Solution**: 
- Ensure ngrok is in your PATH
- Or run it with full path: `C:\ngrok\ngrok.exe http 5000`

### Issue: "ERR_NGROK_108"
**Solution**: Run the authtoken command again

### Issue: Frontend can't connect
**Solution**: 
- Check CORS is enabled in Flask (already done ✅)
- Verify ngrok is running
- Check the URL is correct (including `https://`)

### Issue: "tunnel session expired"
**Solution**: Restart ngrok (free tier has 2-hour limit)

---

## 📝 Quick Reference

| Component | URL | Status |
|-----------|-----|--------|
| **Flask Backend** | http://localhost:5000 | Local only |
| **ngrok Tunnel** | https://abc123.ngrok-free.app | Public |
| **ngrok Dashboard** | http://localhost:4040 | Monitor requests |
| **v0 Frontend** | Your deployed URL | Uses ngrok URL |

---

## ✅ Final Setup

```
┌─────────────────────────────────────────┐
│  Your Computer                          │
│  ┌─────────────────────────────────┐   │
│  │ Flask Backend                   │   │
│  │ http://localhost:5000           │   │
│  └────────────┬────────────────────┘   │
│               │                         │
│  ┌────────────▼────────────────────┐   │
│  │ ngrok                           │   │
│  │ https://abc123.ngrok-free.app   │   │
│  └────────────┬────────────────────┘   │
└───────────────┼─────────────────────────┘
                │
                │ Internet
                │
┌───────────────▼─────────────────────────┐
│  v0 Frontend (Deployed on Vercel)       │
│  Calls: https://abc123.ngrok-free.app   │
└─────────────────────────────────────────┘
```

---

## 🎉 You're Ready!

Your local backend with full diarization support is now accessible to your deployed frontend!

**Benefits**:
- ✅ No Vercel timeout limits
- ✅ Full control and debugging
- ✅ All features working (diarization, long audio, etc.)
- ✅ See logs in real-time

**Start ngrok and give the URL to your v0 frontend!** 🚀

