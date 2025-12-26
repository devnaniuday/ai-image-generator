# Flux Dev Image Generator

A modern, beautiful web application for generating AI images using the Flux Dev model via HuggingFace Inference API.

## Features

✨ Clean, modern UI with gradient design  
🎨 Real-time image generation using Flux Dev model  
⚡ No local GPU required - uses HuggingFace's free inference API  
📱 Fully responsive design  
🎯 Customizable parameters (width, height, steps)  
💾 Download generated images  
🔄 Settings persistence with localStorage  

## Project Structure

```
python/
├── app.py              # Flask backend server
├── views/
│   ├── index.html     # Main HTML page
│   ├── styles.css     # Modern CSS styling
│   └── script.js      # Frontend JavaScript
├── .env.example       # Environment variables template
└── requirements.txt   # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install flask flask-cors requests python-dotenv
```

### 2. Get HuggingFace Token

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a new access token (with "read" access)
3. Copy your token

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
HF_TOKEN=your_huggingface_token_here
```

### 4. Run the Application

```bash
python app.py
```

The server will start at: `http://localhost:5000`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a detailed prompt describing the image you want
3. Adjust parameters if needed:
   - **Width/Height**: Image dimensions (256-2048px)
   - **Steps**: Number of inference steps (1-50, higher = better quality but slower)
4. Click "Generate Image"
5. Wait for the AI to create your image
6. Download or create a new image!

## Example Prompts

- "A futuristic cityscape at sunset with flying cars, neon lights reflecting on wet streets, cyberpunk style"
- "A serene mountain landscape with a crystal clear lake reflection, autumn colors, golden hour"
- "A magical forest with glowing mushrooms and fireflies at night, fantasy art style"
- "An astronaut exploring a colorful alien planet with multiple moons in the sky"

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **AI Model**: FLUX.1-dev by Black Forest Labs
- **API**: HuggingFace Inference API
- **Icons**: Font Awesome 6.5
- **Fonts**: Google Fonts (Inter)

## API Endpoints

- `GET /` - Serve the main application
- `POST /generate` - Generate image from prompt
- `GET /health` - Health check endpoint

## Notes

- First generation may take longer as the model loads on HuggingFace servers
- The free tier has rate limits - wait a few seconds between requests if needed
- For faster generation, consider using a paid HuggingFace plan or running locally with GPU

## Troubleshooting

**Model loading error**: Wait 20-30 seconds and try again  
**Token error**: Make sure your HF_TOKEN is valid and has model access  
**Timeout**: Reduce the number of steps or image dimensions  
**CORS errors**: Make sure flask-cors is installed  

## License

MIT License - Feel free to use and modify for your projects!

## Credits

- Flux Dev Model: Black Forest Labs
- UI Design: Custom modern gradient design
- Icons: Font Awesome
