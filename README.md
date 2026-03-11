# ✍️ AirWrite — Air Writing Recognition System

A browser-based application that lets you write letters and numbers **in the air using your webcam**. AirWrite tracks your fingertip in real time using MediaPipe Hands and recognises characters through a hybrid **LSTM neural network + template matching** system — entirely in-browser, no server required.

---

## ✨ Features

- **Real-time hand tracking** via MediaPipe Hands (21 landmark points per hand)
- **Gesture-controlled interface** — write with your index finger, predict with a thumbs up
- **Hybrid recognition** — LSTM neural network fused with template matching for A–Z and 0–9
- **Training mode** — draw and save your own templates per character for personalised accuracy
- **Template manager** — review, delete, export, and import templates as JSON
- **Fully offline-capable** — all ML inference runs client-side via TensorFlow.js
- **Non-blocking training** — LSTM trains during idle time using `requestIdleCallback`, no camera lag
- **Streamlit wrapper** — `app.py` serves the production React build inside a Streamlit iframe for easy sharing

---

## 🧠 How It Works

### Input Pipeline

```
Webcam Feed
    │
    ▼
MediaPipe Hands  →  21 hand landmarks detected per frame
    │
    ▼
Gesture Classifier
    ├── Open Palm          →  Idle (ready)
    ├── Index Finger Up    →  Writing (recording stroke)
    └── Thumbs Up          →  Predict (trigger recognition)
    │
    ▼
Stroke Recorder  →  Fingertip (x, y) coordinates captured
    │
    ▼
Normalizer  →  Resampled to 32 points, scaled to [0, 1]
```

### Recognition — Hybrid Fusion

The system runs two recognition methods in parallel and fuses their results:

**1. LSTM Neural Network** (TensorFlow.js, in-browser)
```
Input:  [32 timesteps × 2 features (x, y)]
  → LSTM Layer (32 units, dropout 0.1)
  → Dense (36 units — A–Z + 0–9)
  → Softmax
```
- Optimizer: Adam (lr = 0.001), Loss: Categorical Cross-Entropy
- Trained on ~336 samples (168 default + 168 horizontally mirrored for augmentation)
- 15 epochs, batch size 16, CPU backend (avoids GPU contention with MediaPipe)
- Training is deferred until the camera stops so it never blocks the UI

**2. Template Matching**
- Compares normalised stroke against stored templates using Euclidean distance
- User-trained templates receive a **1.2× weight boost** for personalised priority
- Confidence = inverse of minimum distance, normalised to a percentage

**Fusion Logic:**
```
if LSTM confidence > 70%  →  use LSTM result
else                       →  use template matching result
if both methods agree      →  confidence boosted by +10%
```

---

## 🖐️ Gesture Reference

| Gesture | State | Action |
|---|---|---|
| Open Palm | Idle | System ready, not recording |
| Index Finger Extended | Writing | Records fingertip path as stroke |
| Thumbs Up | Predict | Triggers recognition on recorded stroke |

---

## 📊 What You See On-Screen

| Output | Description |
|---|---|
| Predicted Character | Recognised letter (A–Z) or number (0–9) |
| Confidence Score | Prediction certainty as a percentage |
| LSTM Status | "Training LSTM..." or "LSTM Model Ready" |
| Gesture State | Current state: idle / writing / predicting |
| Hand Skeleton | Live overlay of detected hand landmarks |
| Stroke Trail | Real-time path of your fingertip |
| Stroke Preview | Miniature preview of the completed stroke |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | React 18.3 + TypeScript |
| Build Tool | Vite |
| ML (In-Browser) | TensorFlow.js 4.22 |
| Hand Tracking | MediaPipe Hands |
| Styling | Tailwind CSS + Shadcn UI |
| Canvas Rendering | HTML5 Canvas |
| Template Storage | Browser localStorage |
| Python Wrapper | Streamlit (`app.py`) |

---

## 🚀 Getting Started

### Prerequisites
- Node.js v18+ (install via [nvm](https://github.com/nvm-sh/nvm))
- npm or bun
- A modern browser (Chrome recommended)
- A webcam

### Install & Run (Development)

```bash
git clone https://github.com/Binal2004/Air-write.git
cd Air-write

npm install       # or: bun install
npm run dev       # or: bun run dev
```

Open **http://localhost:8080** in your browser.

### Build for Production

```bash
npm run build
```

Output goes to the `dist/` folder.

### Run via Streamlit

```bash
pip install streamlit
npm run build     # must build first
streamlit run app.py
```

> `app.py` inlines the compiled React bundle into a Streamlit component, making it easy to share or demo without a separate web host.

---

## 🎓 How to Use

### Recognition Mode
1. Click **"Start Camera"** to begin hand tracking
2. Extend your **index finger** and draw a letter in the air
3. Show a **thumbs up** to trigger prediction
4. The recognised character and confidence score appear on screen

### Training Mode
1. Switch to the **"Train Model"** tab
2. Select a character from the alphabet grid
3. Draw it in the air with your index finger
4. Click **"Save Template"** — repeat 3–5 times per character for best results
5. Use the **Template Viewer** to review or delete saved templates
6. **Export** your templates as JSON to back them up, or **import** them on another device

---

## ⚠️ Known Limitations

- Requires good lighting for reliable hand detection
- Each character must be drawn in a **single continuous stroke**
- LSTM is trained on a small dataset (~336 samples) — custom training improves accuracy significantly
- Supports A–Z and 0–9 only (no special characters or multi-character words)
- Best experienced on desktop Chrome; mobile support is limited

---

## 🔭 Future Improvements

- Multi-stroke character support
- Word and sentence-level recognition
- WebGL backend toggle for higher-end devices
- Larger pre-trained dataset
- Mobile / touch device support

---

## 🛟 Troubleshooting

| Issue | Fix |
|---|---|
| Camera not working | Check browser permissions; ensure no other app is using the webcam |
| Hand not detected | Improve lighting and keep your hand clearly in frame |
| Poor recognition | Train 3–5 samples per character in Training Mode |
| Slow performance | Close other browser tabs; ensure hardware acceleration is enabled |
| LSTM not training | Stop the camera — training is deferred until camera stops |

---


