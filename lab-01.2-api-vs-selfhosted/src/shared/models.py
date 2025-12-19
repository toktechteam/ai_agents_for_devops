"""
Shared data models for API and self-hosted services
Ensures consistent request/response formats
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, validator

class SummarizationRequest(BaseModel):
    """Request model for text summarization"""
    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 50
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()
    
    @validator('text')
    def text_length_check(cls, v):
        if len(v) < 50:
            raise ValueError('Text must be at least 50 characters long')
        if len(v) > 50000:
            raise ValueError('Text must be less than 50,000 characters')
        return v
    
    @validator('max_length')
    def validate_max_length(cls, v):
        if v and (v < 20 or v > 500):
            raise ValueError('max_length must be between 20 and 500')
        return v
    
    @validator('min_length')
    def validate_min_length(cls, v):
        if v and (v < 10 or v > 200):
            raise ValueError('min_length must be between 10 and 200')
        return v

class SummarizationResponse(BaseModel):
    """Response model for text summarization"""
    summary: str
    method: str  # 'openai-api' or 'local-bart'
    processing_time_ms: float
    model_info: str
    tokens_used: Optional[int] = None  # Only for API services
    cost_estimate: Optional[float] = None  # Only for API services
    metadata: Optional[Dict[str, Any]] = None
    
    def dict(self, **kwargs):
        """Override dict method to handle None values"""
        result = super().dict(**kwargs)
        # Remove None values for cleaner response
        return {k: v for k, v in result.items() if v is not None}

class PerformanceMetrics(BaseModel):
    """Performance comparison metrics"""
    service_type: str
    avg_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    memory_usage_mb: float
    startup_time_seconds: float
    requests_processed: int
    errors_count: int
    success_rate: float

class CostAnalysis(BaseModel):
    """Cost analysis for different request volumes"""
    requests_per_month: int
    api_cost_monthly: float
    selfhosted_cost_monthly: float
    breakeven_point: int
    recommendation: str
    
    @validator('requests_per_month')
    def validate_requests(cls, v):
        if v < 0:
            raise ValueError('Requests per month must be positive')
        return v
