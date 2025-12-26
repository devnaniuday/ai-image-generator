from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Get HuggingFace token from environment variable
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Hugging Face Inference API endpoint for Flux Dev model
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query_hf_api(payload):
    """
    Query Hugging Face Inference API
    This uses HuggingFace's free inference API - no local GPU needed!
    """
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    return response

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate image from prompt using Flux Dev model via HuggingFace API"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        width = data.get('width', 1024)
        height = data.get('height', 1024)
        steps = data.get('steps', 28)
        
        # Validation
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if not HF_TOKEN or HF_TOKEN == "your_hf_token_here":
            return jsonify({
                'error': 'HuggingFace token not configured. Please set HF_TOKEN environment variable.',
                'help': 'Get your token from https://huggingface.co/settings/tokens'
            }), 401
        
        print(f"Generating image: {prompt[:60]}...")
        print(f"Parameters: {width}x{height}, steps={steps}")
        
        # Query the Hugging Face Inference API
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": width,
                "height": height,
                "num_inference_steps": steps,
                "guidance_scale": 3.5
            }
        }
        
        response = query_hf_api(payload)
        
        # Check if request was successful
        if response.status_code == 503:
            return jsonify({
                'error': 'Model is loading',
                'message': 'The model is currently loading. Please try again in 20-30 seconds.'
            }), 503
        
        if response.status_code == 401:
            return jsonify({
                'error': 'Invalid HuggingFace token',
                'message': 'Please check your HF_TOKEN is valid and has access to the model.'
            }), 401
        
        if response.status_code != 200:
            error_msg = f"API Error: {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except:
                pass
            return jsonify({'error': error_msg}), response.status_code
        
        # Get image bytes
        image_bytes = response.content
        
        # Convert to base64 for sending to frontend
        img_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        print("✓ Image generated successfully!")
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'message': 'Image generated successfully'
        })
    
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'message': 'The request took too long. Try reducing steps or image size.'
        }), 504
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'FLUX.1-dev by Black Forest Labs',
        'api': 'HuggingFace Inference API (Free)',
        'token_configured': bool(HF_TOKEN and HF_TOKEN != "your_hf_token_here"),
        'note': 'No local GPU required - runs on HuggingFace servers'
    })

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('views', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('views', filename)

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" 🎨 FLUX DEV IMAGE GENERATOR SERVER")
    print("="*70)
    print(f" Server running at: http://localhost:5000")
    print(f" Model: black-forest-labs/FLUX.1-dev")
    print(f" API: HuggingFace Inference (Free - No GPU needed!)")
    print("="*70)
    
    if not HF_TOKEN or HF_TOKEN == "your_hf_token_here":
        print("\n ⚠️  WARNING: HuggingFace token not configured!")
        print(" Please set HF_TOKEN environment variable or create .env file:")
        print(" 1. Get token from: https://huggingface.co/settings/tokens")
        print(" 2. Create .env file with: HF_TOKEN=your_token_here")
        print(" 3. Make sure you have access to FLUX.1-dev model\n")
    else:
        print(f"\n ✓ HuggingFace token configured")
        print(" ✓ Ready to generate images!\n")
    
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)