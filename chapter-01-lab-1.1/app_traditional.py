#!/usr/bin/env python3
"""
Traditional Rule-Based Sentiment Analysis API
- Instant startup (~3 seconds)
- Low memory usage (~50MB)
- Simple logic, fast responses
- Perfect for horizontal scaling
"""

from flask import Flask, request, jsonify
import time
import os
import logging
import threading

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Startup timer
startup_time = time.time()

# Simple rule-based sentiment analysis
POSITIVE_WORDS = [
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
    'love', 'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'awesome',
    'perfect', 'brilliant', 'outstanding', 'superb', 'marvelous'
]

NEGATIVE_WORDS = [
    'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry',
    'frustrated', 'disappointed', 'sad', 'upset', 'annoyed', 'disgusted',
    'worst', 'pathetic', 'useless', 'garbage', 'stupid'
]

def analyze_sentiment_traditional(text):
    """
    Rule-based sentiment analysis
    - Fast execution (<1ms)
    - Predictable results
    - No model loading required
    """
    text_lower = text.lower()
    
    positive_score = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative_score = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    if positive_score > negative_score:
        sentiment = "POSITIVE"
        confidence = min(0.9, 0.5 + (positive_score - negative_score) * 0.1)
    elif negative_score > positive_score:
        sentiment = "NEGATIVE"
        confidence = min(0.9, 0.5 + (negative_score - positive_score) * 0.1)
    else:
        sentiment = "NEUTRAL"
        confidence = 0.5
    
    return {
        "sentiment": sentiment,
        "confidence": round(confidence, 2),
        "method": "rule-based",
        "processing_time_ms": 1  # Always fast
    }

@app.route('/health')
def health():
    """Health check - always ready for traditional API"""
    uptime = time.time() - startup_time
    return jsonify({
        "status": "healthy",
        "api_type": "traditional",
        "uptime_seconds": round(uptime, 2),
        "memory_usage_mb": "~50MB",  # Estimated
        "startup_time": "~3 seconds"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze sentiment using rule-based approach"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        start_time = time.time()
        result = analyze_sentiment_traditional(data['text'])
        processing_time = (time.time() - start_time) * 1000
        
        result['processing_time_ms'] = round(processing_time, 2)
        
        logger.info(f"Processed request in {processing_time:.2f}ms")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        # 🚀 PAID version includes: retry logic, circuit breakers, fallback responses
        return jsonify({"error": "Processing failed"}), 500

@app.route('/metrics')
def metrics():
    """Basic metrics endpoint"""
    return jsonify({
        "api_type": "traditional",
        "requests_processed": "Manual counting only",  
        "avg_response_time": "~1ms",
        "memory_usage": "~50MB",
        "scaling_capability": "Excellent - stateless",
        # 🚀 PAID version includes: Prometheus metrics, detailed performance stats
        "upgrade_note": "PAID version includes full Prometheus integration"
    })

@app.route('/compare')
def compare():
    """Show operational differences vs ML API"""
    return jsonify({
        "traditional_api": {
            "startup_time": "3 seconds",
            "memory_usage": "50MB",
            "response_time": "1ms",
            "scaling": "Perfect horizontal scaling",
            "deployment": "Rolling updates work great"
        },
        "ml_api_challenges": {
            "startup_time": "30+ seconds (model loading)",
            "memory_usage": "1.2GB+ (model weights)", 
            "response_time": "100-500ms (inference)",
            "scaling": "Cold start problems",
            "deployment": "Blue-green needed for zero downtime"
        },
        "key_insight": "ML APIs require fundamentally different operational patterns"
    })

if __name__ == '__main__':
    logger.info("🚀 Starting Traditional API...")
    logger.info("📊 Expected: 3s startup, 50MB RAM, instant responses")
    logger.info("🔄 Scaling: Horizontal scaling works perfectly")
    
    app.run(host='0.0.0.0', port=8000, debug=False)