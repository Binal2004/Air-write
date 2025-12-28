# AirWrite - Air Writing Recognition System

AirWrite is a web-based application that recognizes handwritten letters and numbers drawn in the air using your webcam and hand tracking technology powered by MediaPipe Hands and a hybrid LSTM + Template Matching recognition system.

## Features

- **Real-time Hand Tracking**: Uses MediaPipe Hands for accurate fingertip detection
- **Gesture-Based Control**: Natural gestures to write, predict, and control the interface
- **Letter & Number Recognition**: Recognizes A-Z letters and 0-9 numbers using hybrid recognition
- **Training Mode**: Train custom templates for improved accuracy
- **Visual Template Viewer**: Review and manage your trained templates
- **Export/Import**: Backup and restore your trained templates as JSON

---

## How It Works

### Input Pipeline
1. **Webcam Capture**: Real-time video feed captured via browser's getUserMedia API
2. **Hand Detection**: MediaPipe Hands ML model detects hand landmarks (21 points per hand)
3. **Gesture Recognition**: System identifies gestures based on finger positions:
   - **Open Palm** → Idle state (system ready)
   - **Index Finger Extended** → Writing state (recording stroke)
   - **Thumbs Up** → Predict state (triggers recognition)
4. **Stroke Recording**: Index fingertip coordinates are recorded as the user "writes" in the air
5. **Normalization**: Strokes are normalized to a fixed-length sequence (32 points) with coordinates scaled to 0-1 range

### Recognition Process
The system uses a **hybrid recognition approach** combining two methods:

1. **LSTM Neural Network**: Deep learning model trained on letter/number patterns
2. **Template Matching**: Traditional pattern matching against stored templates

**Prediction Fusion Logic**:
- If LSTM confidence > 70% → Use LSTM prediction
- Otherwise → Use template matching result
- If both methods agree → Confidence boosted by 10%

---

## Model Used

### Dual Recognition System

#### 1. LSTM Neural Network
A recurrent neural network designed for sequential data:

```
Architecture:
├── Input Layer: [32 timesteps × 2 features (x, y)]
├── LSTM Layer: 32 units, dropout 0.1
├── Dense Layer: 36 units (A-Z + 0-9)
└── Softmax Activation: Probability distribution
```

**Training Configuration**:
- Optimizer: Adam (learning rate: 0.001)
- Loss Function: Categorical Cross-Entropy
- Epochs: 15
- Batch Size: 16
- Backend: CPU (to avoid GPU contention with MediaPipe)
- Training Trigger: Deferred until camera stops (non-blocking)

#### 2. Template Matching
- Compares normalized input strokes against stored templates
- Uses Euclidean distance for similarity measurement
- User-trained templates receive priority (1.2x weight boost)
- Confidence = inverse of minimum distance, normalized

---

## Training Datasets

### Default Templates
- **Source**: `src/data/defaultTemplates.json`
- **Content**: ~168 pre-recorded samples for A-Z letters and 0-9 numbers
- **Format**: Normalized coordinate arrays (32 points each)

### Data Augmentation
To improve model robustness, training data is augmented:
- **Horizontal Mirroring**: Flips strokes horizontally
- **Total Training Samples**: ~336 (168 original + 168 mirrored)

### User-Trained Templates
- Stored in browser's `localStorage`
- Users can train multiple samples per character
- Receives priority boost in template matching
- Can be exported/imported as JSON for backup

---

## Technologies Used

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | React 18.3 | UI framework and component architecture |
| **Language** | TypeScript | Type-safe JavaScript development |
| **Build Tool** | Vite | Fast development server and bundler |
| **ML Framework** | TensorFlow.js 4.22 | In-browser LSTM model training/inference |
| **Hand Tracking** | MediaPipe Hands | Real-time hand landmark detection |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | Shadcn UI | Accessible React components |
| **Graphics** | HTML5 Canvas | Stroke visualization and hand skeleton |
| **Storage** | localStorage | Persistent template storage |
| **Performance** | requestIdleCallback | Non-blocking deferred training |

---

## User Outputs

When using AirWrite, users see the following information:

| Output | Description |
|--------|-------------|
| **Predicted Character** | The recognized letter (A-Z) or number (0-9) |
| **Confidence Score** | Percentage indicating prediction certainty |
| **LSTM Status** | "Training LSTM..." or "LSTM Model Ready" |
| **Gesture State** | Current state: idle, ready, writing, predicting |
| **Hand Skeleton** | Visual overlay of detected hand landmarks |
| **Stroke Trail** | Real-time visualization of the drawn path |
| **Stroke Preview** | Miniature preview of the recorded stroke |

---

## Prerequisites

Before running this project, ensure you have:

- **Node.js** (v18 or higher) - [Install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- **npm** or **bun** package manager
- A modern web browser (Chrome, Firefox, Edge)
- A webcam for hand tracking

## Installation

### Step 1: Clone the Repository

```bash
git clone <YOUR_GIT_URL>
cd <YOUR_PROJECT_NAME>
```

### Step 2: Install Dependencies

```bash
npm install
# or
bun install
```

### Step 3: Start the Development Server

```bash
npm run dev
# or
bun run dev
```

### Step 4: Open in Browser

Navigate to: `http://localhost:8080`

---

## How to Use

### Recognition Mode

1. Click **"Start Camera"** to begin hand tracking
2. Extend your **index finger** to start drawing letters in the air
3. Show a **thumbs up** gesture to trigger letter prediction
4. View the predicted letter and confidence score on screen

### Training Mode

1. Switch to the **"Train Model"** tab
2. Select the letter you want to train from the alphabet grid
3. Draw the letter using your index finger
4. Click **"Save Template"** to store it
5. Repeat 3-5 times per letter for better accuracy
6. Use the **Template Viewer** to review saved templates

### Gesture Reference

| Gesture | State | Action |
|---------|-------|--------|
| Open Palm | Idle | System ready, not recording |
| Index Finger Extended | Writing | Drawing strokes in the air |
| Thumbs Up | Predict | Triggers letter recognition |

---

## Building for Production

```bash
npm run build
```

The output will be in the `dist` folder, ready for deployment.

---

## Conclusions

### Strengths
- **In-Browser Processing**: No server required, all ML runs client-side
- **Real-Time Performance**: Smooth hand tracking with optimized LSTM training
- **Hybrid Recognition**: Combines neural network with template matching for accuracy
- **Personalization**: Users can train custom templates for their handwriting
- **Non-Blocking Training**: LSTM trains during idle time, no camera lag
- **Offline Capable**: Works without internet after initial load

### Limitations
- **Lighting Dependent**: Requires good lighting for hand detection
- **Single-Stroke Only**: Each character must be drawn in one continuous stroke
- **Limited Dataset**: LSTM trained on ~336 samples (small for deep learning)
- **Characters Only**: Supports A-Z and 0-9, no special characters or words

### Performance Optimizations Applied
- CPU backend for TensorFlow.js (avoids GPU contention)
- Deferred LSTM training via `requestIdleCallback`
- Smaller LSTM architecture (32 units, single layer)
- Minimal data augmentation (horizontal mirroring only)
- `yieldEvery: 'batch'` for main thread responsiveness

### Future Improvements
- Multi-stroke character support
- Word and sentence recognition
- Larger pre-trained dataset
- WebGL backend toggle for high-end devices
- Mobile device support

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not working | Check browser permissions and ensure no other app is using the camera |
| Hand not detected | Improve lighting and keep hand clearly visible |
| Poor recognition accuracy | Train more samples (3-5) for each letter in Training Mode |
| Slow performance | Close other browser tabs and applications |
| LSTM not training | Stop camera to trigger deferred training |

---

## License

MIT License
