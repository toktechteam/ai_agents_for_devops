#!/usr/bin/env python3
"""
ML Model-Based Sentiment Analysis API
- Slow startup (~30 seconds for model loading)
- High memory usage (~1.2GB for model weights)
- Better accuracy but operational complexity
- Horizontal scaling challenges (cold start problem)
"""

from flask import Flask, request, jsonify
import time
import os
import logging
import threading
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Global variables for model and readiness
model_pipeline = None
model_ready = False
startup_time = time.time()
model_load_time = None

def load_model():
    """
    Load ML model - this is where the 30s startup time comes from
    In production, this is a major operational challenge
    """
    global model_pipeline, model_ready, model_load_time
    
    logger.info("🤖 Loading ML model... (this takes ~30 seconds)")
    load_start = time.time()
    
    try:
        model_name = os.getenv('MODEL_NAME', 'distilbert-base-uncased-finetuned-sst-2-english')
        
        # This is the expensive part - loading model weights
        logger.info(f"📥 Downloading/loading model: {model_name}")
        model_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,
            device=-1,  # CPU only in FREE version
            # 🚀 PAID version includes: GPU support, model quantization, caching
        )
        
        model_load_time = time.time() - load_start
        model_ready = True
        
        logger.info(f"✅ Model loaded successfully in {model_load_time:.2f}s")
        logger.info(f"💾 Memory usage: ~1.2GB (model weights)")
        logger.info("🚨 Cold start problem: Each new instance takes 30s+")
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model_ready = False

# Start model loading in background thread
threading.Thread(target=load_model, daemon=True).start()

def analyze_sentiment_ml(text):
    """
    ML-based sentiment analysis using transformer model
    - Higher accuracy than rule-based
    - Slower processing (100-500ms)
    - Requires significant compute resources
    """
    if not model_ready:
        raise Exception("Model not ready yet")
    
    start_time = time.time()
    
    try:
        # Inference using transformer model
        result = model_pipeline(text)[0]
        processing_time = (time.time() - start_time) * 1000
        
        # Convert HuggingFace format to consistent format
        sentiment = result['label']
        confidence = result['score']
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "method": "transformer-ml",
            "processing_time_ms": round(processing_time, 2),
            "model_info": "DistilBERT (CPU only in FREE version)"
        }
        
    except Exception as e:
        logger.error(f"ML inference failed: {e}")
        # 🚀 PAID version includes: fallback to simpler model, retry logic
        raise

@app.route('/health')
def health():
    """
    Health check with separate readiness
    ML APIs need different health check patterns
    """
    uptime = time.time() - startup_time
    
    return jsonify({
        "status": "healthy" if model_ready else "starting",
        "ready": model_ready,
        "api_type": "ml",
        "uptime_seconds": round(uptime, 2),
        "model_load_time_seconds": round(model_load_time, 2) if model_load_time else None,
        "memory_usage_mb": "~1200MB",
        "startup_time": "~30 seconds",
        "operational_challenge": "Cold start problem - each replica needs 30s warmup"
    })

@app.route('/ready')
def ready():
    """
    Separate readiness endpoint
    Critical for ML APIs - liveness != readiness
    """
    if model_ready:
        return jsonify({"ready": True, "model_status": "loaded"})
    else:
        return jsonify({"ready": False, "model_status": "loading"}), 503

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze sentiment using ML model"""
    if not model_ready:
        # 🚀 PAID version includes: queueing system, fallback models
        return jsonify({
            "error": "Model still loading, please wait",
            "estimated_ready_in": "30 seconds",
            "upgrade_note": "PAID version includes request queueing during startup"
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        result = analyze_sentiment_ml(data['text'])
        
        logger.info(f"ML processed request in {result['processing_time_ms']:.2f}ms")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing ML request: {e}")
        # 🚀 PAID version includes: circuit breakers, fallback to rule-based
        return jsonify({
            "error": "ML inference failed",
            "upgrade_note": "PAID version includes fallback mechanisms"
        }), 500

@app.route('/metrics')
def metrics():
    """ML-specific metrics"""
    return jsonify({
        "api_type": "ml",
        "model_ready": model_ready,
        "model_load_time": model_load_time,
        "memory_usage": "~1200MB (model weights)",
        "inference_time": "100-500ms per request",
        "scaling_challenge": "Cold start problem",
        "cost_implication": "High memory usage = expensive cloud bills",
        # 🚀 PAID version includes: GPU metrics, batch processing stats, model performance
        "upgrade_note": "PAID version includes comprehensive ML metrics"
    })

@app.route('/performance-comparison')
def performance_comparison():
    """Show why ML APIs are operationally different"""
    return jsonify({
        "startup_comparison": {
            "traditional_api": "3 seconds",
            "ml_api_free": "30 seconds",
            "ml_api_paid": "8 seconds (optimized)",
            "problem": "Cold start kills auto-scaling"
        },
        "memory_comparison": {
            "traditional_api": "50MB",
            "ml_api_free": "1200MB", 
            "ml_api_paid": "400MB (quantized)",
            "problem": "Memory costs scale linearly with replicas"
        },
        "scaling_strategies": {
            "traditional": "Horizontal scaling works perfectly",
            "ml_naive": "Each replica = 30s delay + 1.2GB RAM",
            "ml_optimized": "Warm pools, model sharing, smart scheduling",
            "key_insight": "ML requires fundamentally different scaling patterns"
        },
        "real_world_impact": {
            "scenario": "Traffic spike 10x",
            "traditional_response": "Scale out in 30 seconds",
            "ml_response_naive": "Users wait 30s+ for new capacity",
            "ml_response_optimized": "Pre-warmed pools handle spike"
        }
    })

if __name__ == '__main__':
    logger.info("🤖 Starting ML API...")
    logger.info("⏳ Expected: 30s startup, 1.2GB RAM, 100-500ms responses")  
    logger.info("🚨 Warning: Cold start problem evident")
    logger.info("💰 Note: High memory usage = expensive scaling")
    
    app.run(host='0.0.0.0', port=8000, debug=False)