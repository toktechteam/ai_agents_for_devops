#!/usr/bin/env python3
"""
Self-Hosted Document Summarization Service
- Uses local BART model for text summarization
- High memory usage (~2.5GB)
- Slow startup (~45 seconds)
- Fixed cost model (infrastructure)
- No network latency for processing
"""

from flask import Flask, request, jsonify
import time
import os
import logging
import yaml
import threading
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import torch
from shared.models import SummarizationRequest, SummarizationResponse
from shared.utils import validate_request, measure_time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Global variables
config = {}
summarizer_pipeline = None
model_ready = False
startup_time = time.time()
model_load_time = None

def load_config():
    """Load configuration from YAML file"""
    global config
    try:
        with open('/app/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        config = {
            'max_length': 150,
            'min_length': 50,
            'model_name': 'facebook/bart-large-cnn'
        }

def load_model():
    """
    Load summarization model - this is the expensive operation
    Takes 30-60 seconds and ~2.5GB RAM
    """
    global summarizer_pipeline, model_ready, model_load_time
    
    logger.info(" Loading local summarization model... (this takes ~45 seconds)")
    load_start = time.time()
    
    try:
        model_name = config.get('model_name', 'facebook/bart-large-cnn')
        
        logger.info(f" Loading model: {model_name}")
        logger.info(" Expected memory usage: ~2.5GB")
        
        # Load model with specific configuration
        summarizer_pipeline = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
            device=-1,  # CPU only in FREE version
            model_kwargs={"cache_dir": "/app/models"}
        )
        
        model_load_time = time.time() - load_start
        model_ready = True
        
        logger.info(f" Model loaded successfully in {model_load_time:.2f}s")
        logger.info(f" Memory usage: ~2.5GB (model weights)")
        logger.info(" Cold start problem: Each new instance takes 45s+")
        
        # Warm up the model with a small test
        logger.info(" Warming up model with test input...")
        test_summary = summarizer_pipeline("This is a test document for warming up the model.", 
                                          max_length=50, min_length=10)
        logger.info(" Model warmed up and ready for requests")
        
    except Exception as e:
        logger.error(f" Failed to load model: {e}")
        model_ready = False

# Start model loading in background thread
threading.Thread(target=lambda: (load_config(), load_model()), daemon=True).start()

@measure_time
def summarize_with_local_model(text: str) -> dict:
    """
    Summarize text using local BART model
    
    Performance characteristics:
    - No network latency
    - Processing: 50-200ms depending on text length
    - Memory intensive but fast once loaded
    """
    if not model_ready:
        raise Exception("Model not ready yet - still loading")
    
    try:
        logger.info(f"Summarizing {len(text)} characters with local model")
        
        # Configure summarization parameters
        max_length = min(config.get('max_length', 150), len(text.split()) // 2)
        min_length = config.get('min_length', 50)
        
        # Perform summarization
        result = summarizer_pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True
        )
        
        summary = result[0]['summary_text']
        
        return {
            'summary': summary,
            'method': 'local-bart',
            'model': config.get('model_name', 'facebook/bart-large-cnn'),
            'max_length': max_length,
            'min_length': min_length
        }
        
    except Exception as e:
        logger.error(f"Local summarization failed: {e}")
        raise

@app.route('/health')
def health():
    """
    Health check with model readiness status
    Critical: Container running ≠ service ready for self-hosted models
    """
    uptime = time.time() - startup_time
    
    status = "healthy" if model_ready else "loading"
    
    return jsonify({
        "status": status,
        "ready": model_ready,
        "service_type": "self-hosted",
        "uptime_seconds": round(uptime, 2),
        "model_load_time_seconds": round(model_load_time, 2) if model_load_time else None,
        "memory_usage_mb": "~2500MB",
        "startup_time": "~45 seconds",
        "dependencies": ["Local model files"],
        "cost_model": "fixed-infrastructure",
        "cold_start_challenge": "Each replica needs 45s+ warmup"
    })

@app.route('/ready')
def ready():
    """
    Separate readiness endpoint
    Kubernetes pattern: liveness ≠ readiness for ML services
    """
    if model_ready:
        return jsonify({"ready": True, "model_status": "loaded"})
    else:
        return jsonify({"ready": False, "model_status": "loading"}), 503

@app.route('/summarize', methods=['POST'])
def summarize():
    """Summarize text using local model"""
    if not model_ready:
        return jsonify({
            "error": "Model still loading, please wait",
            "estimated_ready_in": "45 seconds",
            "service_type": "self-hosted"
        }), 503
    
    start_time = time.time()
    
    try:
        # Validate request
        data = request.get_json()
        if not validate_request(data):
            return jsonify({"error": "Invalid request format"}), 400
        
        req = SummarizationRequest(**data)
        
        # Perform summarization
        result = summarize_with_local_model(req.text)
        processing_time = (time.time() - start_time) * 1000
        
        response = SummarizationResponse(
            summary=result['summary'],
            method=result['method'],
            processing_time_ms=round(processing_time, 2),
            model_info=result['model'],
            tokens_used=None,  # Not tracked for local models
            cost_estimate=0.0,  # Fixed infrastructure cost
            metadata={
                "service_type": "self-hosted",
                "network_dependent": False,
                "scaling": "manual",
                "max_length": result['max_length'],
                "min_length": result['min_length']
            }
        )
        
        logger.info(f"Local summarization completed in {processing_time:.2f}ms")
        return jsonify(response.dict())
        
    except Exception as e:
        logger.error(f"Self-hosted summarization failed: {e}")
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            "error": str(e),
            "processing_time_ms": round(processing_time, 2),
            "service_type": "self-hosted"
        }), 500

@app.route('/metrics')
def metrics():
    """Service metrics and characteristics"""
    return jsonify({
        "service_type": "self-hosted",
        "characteristics": {
            "startup_time": "45 seconds",
            "memory_usage": "2.5GB",
            "latency_breakdown": {
                "network": "0ms (local)",
                "processing": "50-200ms",
                "total": "50-200ms"
            },
            "cost_model": {
                "type": "fixed",
                "rate": "~$500/month infrastructure",
                "scaling": "economies of scale"
            },
            "scaling": {
                "horizontal": "5+ minutes (cold start)",
                "limitations": "memory intensive, slow startup"
            },
            "dependencies": ["Local compute resources"],
            "operational_complexity": "high"
        },
        "when_to_use": [
            "High volume (>25K requests/month)",
            "Predictable load patterns",
            "Data privacy requirements",
            "Cost predictability needed",
            "Custom model requirements"
        ],
        "trade_offs": {
            "pros": ["No network latency", "Fixed costs", "Data privacy"],
            "cons": ["High memory", "Slow startup", "Operational complexity"]
        }
    })

@app.route('/model-info')
def model_info():
    """Detailed model information"""
    if not model_ready:
        return jsonify({"error": "Model not loaded yet"}), 503
    
    return jsonify({
        "model_name": config.get('model_name', 'facebook/bart-large-cnn'),
        "model_type": "BART (Bidirectional and Auto-Regressive Transformers)",
        "parameters": "~400M parameters",
        "memory_usage": "~2.5GB",
        "optimal_input_length": "512-1024 tokens",
        "capabilities": ["Document summarization", "Text generation"],
        "limitations": ["CPU inference only", "English language only"],
        "performance": {
            "short_text": "50-100ms",
            "medium_text": "100-150ms", 
            "long_text": "150-200ms"
        }
    })

if __name__ == '__main__':
    logger.info(" Starting self-hosted summarization service...")
    logger.info(" Expected: 45s startup, 2.5GB RAM, 50-200ms responses")
    logger.info(" Cost model: Fixed infrastructure (~$500/month)")
    logger.info(" Warning: Cold start problem evident")
    logger.info(" Advantage: Data stays local, no network dependency")
    
    app.run(host='0.0.0.0', port=8000, debug=False)
