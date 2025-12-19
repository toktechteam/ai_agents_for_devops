#!/usr/bin/env python3
"""
API-Based Document Summarization Service
- Uses OpenAI API for text summarization
- Low memory usage (~100MB)
- Fast startup (~3 seconds)
- Variable cost model (pay per request)
- Network latency dependent
"""

from flask import Flask, request, jsonify
import openai
import time
import os
import logging
import yaml
from shared.models import SummarizationRequest, SummarizationResponse
from shared.utils import validate_request, measure_time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Global configuration
config = {}
startup_time = time.time()

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
            'max_tokens': 150,
            'temperature': 0.3,
            'model': 'gpt-3.5-turbo'
        }

def setup_openai():
    """Initialize OpenAI client"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY not found!")
        return False
    
    openai.api_key = api_key
    logger.info("OpenAI client configured")
    return True

@measure_time
def summarize_with_api(text: str) -> dict:
    """
    Summarize text using OpenAI API
    
    Performance characteristics:
    - Network latency: 100-300ms
    - API processing: 100-500ms  
    - Total: 200-800ms typically
    """
    try:
        logger.info(f"Summarizing {len(text)} characters via OpenAI API")
        
        prompt = f"""Summarize the following text in a concise manner:

{text}

Summary:"""

        response = openai.ChatCompletion.create(
            model=config.get('model', 'gpt-3.5-turbo'),
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.get('max_tokens', 150),
            temperature=config.get('temperature', 0.3)
        )
        
        summary = response.choices[0].message.content.strip()
        
        return {
            'summary': summary,
            'method': 'openai-api',
            'tokens_used': response.usage.total_tokens,
            'model': config.get('model', 'gpt-3.5-turbo'),
            'cost_estimate': response.usage.total_tokens * 0.000002  # Rough estimate
        }
        
    except openai.error.RateLimitError:
        logger.error("OpenAI rate limit exceeded")
        raise Exception("Rate limit exceeded - try again later")
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise Exception("API service temporarily unavailable")
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise

@app.route('/health')
def health():
    """Health check endpoint"""
    uptime = time.time() - startup_time
    
    # Test API connectivity
    api_status = "healthy"
    try:
        # Simple API test (doesn't count toward usage)
        openai.Model.list()
    except Exception as e:
        api_status = f"api_error: {str(e)[:50]}"
    
    return jsonify({
        "status": "healthy",
        "service_type": "api-based",
        "uptime_seconds": round(uptime, 2),
        "memory_usage_mb": "~100MB",
        "startup_time": "~3 seconds",
        "api_status": api_status,
        "dependencies": ["OpenAI API"],
        "cost_model": "pay-per-request"
    })

@app.route('/summarize', methods=['POST'])
def summarize():
    """Summarize text using OpenAI API"""
    start_time = time.time()
    
    try:
        # Validate request
        data = request.get_json()
        if not validate_request(data):
            return jsonify({"error": "Invalid request format"}), 400
        
        req = SummarizationRequest(**data)
        
        # Perform summarization
        result = summarize_with_api(req.text)
        processing_time = (time.time() - start_time) * 1000
        
        response = SummarizationResponse(
            summary=result['summary'],
            method=result['method'],
            processing_time_ms=round(processing_time, 2),
            model_info=result['model'],
            tokens_used=result.get('tokens_used'),
            cost_estimate=result.get('cost_estimate'),
            metadata={
                "service_type": "api",
                "network_dependent": True,
                "scaling": "instant"
            }
        )
        
        logger.info(f"API summarization completed in {processing_time:.2f}ms")
        return jsonify(response.dict())
        
    except Exception as e:
        logger.error(f"Summarization request failed: {e}")
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            "error": str(e),
            "processing_time_ms": round(processing_time, 2),
            "service_type": "api",
            "retry_suggested": True
        }), 500

@app.route('/metrics')
def metrics():
    """Service metrics and characteristics"""
    return jsonify({
        "service_type": "api-based",
        "characteristics": {
            "startup_time": "3 seconds",
            "memory_usage": "100MB",
            "latency_breakdown": {
                "network": "100-300ms",
                "api_processing": "100-500ms",
                "total": "200-800ms"
            },
            "cost_model": {
                "type": "variable",
                "rate": "$0.002/request (approx)",
                "scaling": "linear with usage"
            },
            "scaling": {
                "horizontal": "instant (handled by OpenAI)",
                "limitations": "rate limits, API quotas"
            },
            "dependencies": ["OpenAI API", "Internet connectivity"],
            "operational_complexity": "low"
        },
        "when_to_use": [
            "Low volume (<10K requests/month)",
            "Variable/unpredictable load", 
            "Fast MVP development",
            "Access to latest models",
            "Limited DevOps resources"
        ],
        "trade_offs": {
            "pros": ["No infrastructure", "Latest models", "Instant scaling"],
            "cons": ["Network latency", "Variable costs", "External dependency"]
        }
    })

@app.route('/compare')
def compare():
    """Comparison with self-hosted approach"""
    return jsonify({
        "api_service": {
            "startup": "3 seconds",
            "memory": "100MB",
            "latency": "200-800ms (network + processing)",
            "cost_1k": "$2/month",
            "cost_100k": "$200/month", 
            "scaling": "Instant",
            "complexity": "Low"
        },
        "self_hosted_service": {
            "startup": "45 seconds",
            "memory": "2.5GB", 
            "latency": "50-150ms (processing only)",
            "cost_1k": "$500/month (fixed)",
            "cost_100k": "$500/month (fixed)",
            "scaling": "5+ minutes",
            "complexity": "High"
        },
        "breakeven_analysis": {
            "requests_per_month": "~25,000",
            "note": "Above this volume, self-hosted becomes cheaper"
        },
        "decision_factors": [
            "Request volume and growth",
            "Latency requirements", 
            "Cost predictability needs",
            "Data privacy requirements",
            "Operational capacity"
        ]
    })

if __name__ == '__main__':
    logger.info(" Starting API-based summarization service...")
    logger.info(" Expected: 3s startup, 100MB RAM, 200-800ms responses")
    logger.info(" Cost model: Pay per request (~$0.002/request)")
    logger.info(" Scaling: Instant (handled by OpenAI)")
    
    load_config()
    if not setup_openai():
        logger.error("Failed to setup OpenAI - check API key!")
        exit(1)
    
    app.run(host='0.0.0.0', port=8000, debug=False)
