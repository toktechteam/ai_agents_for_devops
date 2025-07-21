"""
Shared utilities for API and self-hosted services
Common functions for validation, timing, and analysis
"""

import time
import functools
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def measure_time(func):
    """Decorator to measure function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = (time.time() - start_time) * 1000
            logger.debug(f"{func.__name__} completed in {execution_time:.2f}ms")
            return result
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"{func.__name__} failed after {execution_time:.2f}ms: {e}")
            raise
    return wrapper

def validate_request(data: Dict[str, Any]) -> bool:
    """Validate incoming request data"""
    if not data:
        return False
    
    if 'text' not in data:
        return False
    
    text = data.get('text', '').strip()
    if not text or len(text) < 50:
        return False
    
    return True

def calculate_cost_breakeven(api_cost_per_request: float = 0.002, 
                           selfhosted_monthly_cost: float = 500) -> Dict[str, Any]:
    """
    Calculate the breakeven point between API and self-hosted costs
    
    Args:
        api_cost_per_request: Cost per API request (default: $0.002)
        selfhosted_monthly_cost: Monthly infrastructure cost (default: $500)
    
    Returns:
        Dictionary with breakeven analysis
    """
    breakeven_requests = selfhosted_monthly_cost / api_cost_per_request
    
    return {
        "breakeven_requests_per_month": int(breakeven_requests),
        "api_cost_per_request": api_cost_per_request,
        "selfhosted_monthly_cost": selfhosted_monthly_cost,
        "analysis": {
            "below_breakeven": f"API cheaper (< {int(breakeven_requests):,} req/month)",
            "above_breakeven": f"Self-hosted cheaper (> {int(breakeven_requests):,} req/month)"
        }
    }

def analyze_latency_components(total_latency_ms: float, 
                             service_type: str) -> Dict[str, float]:
    """
    Break down latency components by service type
    
    Args:
        total_latency_ms: Total measured latency
        service_type: 'api' or 'selfhosted'
    
    Returns:
        Dictionary with latency breakdown
    """
    if service_type == 'api':
        # API services have network + processing latency
        estimated_network = min(total_latency_ms * 0.4, 300)  # Max 300ms network
        estimated_processing = total_latency_ms - estimated_network
        
        return {
            "total_ms": total_latency_ms,
            "network_ms": round(estimated_network, 2),
            "processing_ms": round(estimated_processing, 2),
            "network_percentage": round((estimated_network / total_latency_ms) * 100, 1)
        }
    else:
        # Self-hosted has only processing latency
        return {
            "total_ms": total_latency_ms,
            "network_ms": 0,
            "processing_ms": total_latency_ms,
            "network_percentage": 0
        }

def generate_test_documents() -> List[Dict[str, str]]:
    """Generate test documents of various sizes for performance testing"""
    
    short_doc = """
    Artificial Intelligence (AI) has become a transformative force in modern technology. 
    Machine learning algorithms can now process vast amounts of data to identify patterns 
    and make predictions. This technology is being applied across industries from healthcare 
    to finance, revolutionizing how we approach complex problems. The development of neural 
    networks has particularly advanced the field, enabling computers to perform tasks that 
    were once thought to be exclusively human capabilities.
    """
    
    medium_doc = """
    Cloud computing has fundamentally changed how organizations approach IT infrastructure. 
    Instead of maintaining physical servers on-premises, companies can now leverage scalable, 
    on-demand computing resources from cloud providers. This shift has enabled greater 
    flexibility, reduced capital expenditure, and improved disaster recovery capabilities.
    
    The three main service models - Infrastructure as a Service (IaaS), Platform as a Service 
    (PaaS), and Software as a Service (SaaS) - offer different levels of abstraction and control. 
    IaaS provides basic compute, storage, and networking resources, while PaaS adds application 
    development and deployment tools. SaaS delivers complete applications over the internet.
    
    DevOps practices have evolved alongside cloud adoption, emphasizing automation, continuous 
    integration, and continuous deployment. These methodologies enable faster development cycles 
    and more reliable software delivery. Container technologies like Docker and orchestration 
    platforms like Kubernetes have further streamlined application deployment and management.
    
    Security in the cloud requires a shared responsibility model, where cloud providers secure 
    the infrastructure while customers protect their data and applications. This has led to 
    new security practices and tools specifically designed for cloud environments.
    """
    
    long_doc = """
    The evolution of software development methodologies has been driven by the need for faster, 
    more reliable delivery of software products. Traditional waterfall approaches, while providing 
    structure and documentation, often struggled with changing requirements and long development cycles.
    
    Agile methodologies emerged as a response to these challenges, emphasizing iterative development, 
    customer collaboration, and responding to change. The Agile Manifesto, published in 2001, 
    outlined core values that prioritized individuals and interactions over processes and tools, 
    working software over comprehensive documentation, customer collaboration over contract negotiation, 
    and responding to change over following a plan.
    
    Scrum, one of the most popular Agile frameworks, introduced concepts like sprints, daily standups, 
    and retrospectives. These practices helped teams maintain focus, improve communication, and 
    continuously adapt their processes. The role of the Scrum Master became crucial in facilitating 
    these processes and removing impediments to the team's progress.
    
    DevOps emerged as an extension of Agile principles, focusing on the collaboration between 
    development and operations teams. This cultural shift emphasized automation, monitoring, and 
    continuous improvement throughout the software delivery lifecycle. Tools like Jenkins, Git, 
    and various cloud platforms became essential components of modern DevOps toolchains.
    
    Continuous Integration and Continuous Deployment (CI/CD) pipelines automated the process of 
    code integration, testing, and deployment. This automation reduced human error, increased 
    deployment frequency, and provided faster feedback on code changes. Automated testing became 
    a critical component, ensuring that code changes didn't introduce regressions.
    
    Infrastructure as Code (IaC) brought software development practices to infrastructure management. 
    Tools like Terraform, Ansible, and CloudFormation allowed teams to version control their 
    infrastructure definitions and deploy consistent environments across development, testing, 
    and production stages.
    
    The rise of microservices architecture further transformed how applications are designed and 
    deployed. Instead of monolithic applications, systems are broken down into smaller, independently 
    deployable services. This approach provides greater flexibility and scalability but introduces 
    new challenges in service discovery, communication, and data consistency.
    """
    
    return [
        {"size": "short", "text": short_doc.strip(), "word_count": len(short_doc.split())},
        {"size": "medium", "text": medium_doc.strip(), "word_count": len(medium_doc.split())},
        {"size": "long", "text": long_doc.strip(), "word_count": len(long_doc.split())}
    ]

def format_currency(amount: float) -> str:
    """Format currency values for display"""
    if amount < 0.01:
        return f"${amount:.4f}"
    elif amount < 1:
        return f"${amount:.3f}"
    else:
        return f"${amount:.2f}"

def format_memory(bytes_value: int) -> str:
    """Format memory values for display"""
    if bytes_value < 1024:
        return f"{bytes_value}B"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.1f}KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.1f}MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.1f}GB"
