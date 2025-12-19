#!/usr/bin/env python3
"""
Performance Testing Script for API vs Self-hosted Comparison
Run comprehensive tests to compare latency, cost, and scaling characteristics
"""

import requests
import time
import statistics
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.shared.utils import generate_test_documents, calculate_cost_breakeven, format_currency

class PerformanceTester:
    def __init__(self):
        self.api_url = "http://localhost:8001"
        self.selfhosted_url = "http://localhost:8002"
        self.results = {
            "api_service": {},
            "selfhosted_service": {},
            "comparison": {}
        }
    
    def wait_for_services(self, timeout=300):
        """Wait for both services to be ready"""
        print(" Waiting for services to be ready...")
        
        services = [
            ("API Service", f"{self.api_url}/health"),
            ("Self-hosted Service", f"{self.selfhosted_url}/health")
        ]
        
        for name, url in services:
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if name == "Self-hosted Service":
                            if data.get("ready", False):
                                print(f" {name} is ready")
                                break
                        else:
                            print(f" {name} is ready")
                            break
                except requests.exceptions.RequestException:
                    pass
                
                print(f" Waiting for {name}...")
                time.sleep(5)
            else:
                raise Exception(f" {name} did not become ready within {timeout} seconds")
    
    def test_single_request(self, service_url, text, service_name):
        """Test a single summarization request"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{service_url}/summarize",
                json={"text": text},
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "latency_ms": (end_time - start_time) * 1000,
                    "processing_time_ms": data.get("processing_time_ms", 0),
                    "service_type": service_name,
                    "summary_length": len(data.get("summary", "")),
                    "cost_estimate": data.get("cost_estimate", 0)
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "service_type": service_name
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "service_type": service_name
            }
    
    def test_latency_comparison(self):
        """Compare latency between API and self-hosted services"""
        print("\n Testing Latency Comparison...")
        
        test_docs = generate_test_documents()
        
        for doc in test_docs:
            print(f"\n Testing {doc['size']} document ({doc['word_count']} words)")
            
            # Test each service multiple times
            api_results = []
            selfhosted_results = []
            
            for i in range(5):
                print(f"  Round {i+1}/5")
                
                # Test API service
                api_result = self.test_single_request(
                    self.api_url, doc['text'], "api"
                )
                if api_result['success']:
                    api_results.append(api_result['latency_ms'])
                
                # Test self-hosted service
                selfhosted_result = self.test_single_request(
                    self.selfhosted_url, doc['text'], "selfhosted"
                )
                if selfhosted_result['success']:
                    selfhosted_results.append(selfhosted_result['latency_ms'])
                
                time.sleep(1)  # Brief pause between requests
            
            # Calculate statistics
            if api_results:
                api_stats = {
                    "avg": statistics.mean(api_results),
                    "min": min(api_results),
                    "max": max(api_results),
                    "median": statistics.median(api_results)
                }
            else:
                api_stats = {"error": "No successful API requests"}
            
            if selfhosted_results:
                selfhosted_stats = {
                    "avg": statistics.mean(selfhosted_results),
                    "min": min(selfhosted_results),
                    "max": max(selfhosted_results),
                    "median": statistics.median(selfhosted_results)
                }
            else:
                selfhosted_stats = {"error": "No successful self-hosted requests"}
            
            self.results[f"latency_{doc['size']}"] = {
                "api": api_stats,
                "selfhosted": selfhosted_stats
            }
            
            # Print results
            if "error" not in api_stats and "error" not in selfhosted_stats:
                print(f"    API Service: {api_stats['avg']:.1f}ms avg (min: {api_stats['min']:.1f}ms, max: {api_stats['max']:.1f}ms)")
                print(f"    Self-hosted: {selfhosted_stats['avg']:.1f}ms avg (min: {selfhosted_stats['min']:.1f}ms, max: {selfhosted_stats['max']:.1f}ms)")
                print(f"    Difference: {api_stats['avg'] - selfhosted_stats['avg']:.1f}ms ({((api_stats['avg'] / selfhosted_stats['avg'] - 1) * 100):+.1f}%)")
    
    def test_concurrent_load(self):
        """Test concurrent request handling"""
        print("\n Testing Concurrent Load Handling...")
        
        test_text = generate_test_documents()[1]['text']  # Medium document
        concurrent_requests = [2, 5, 10]
        
        for num_requests in concurrent_requests:
            print(f"\n Testing {num_requests} concurrent requests")
            
            for service_name, service_url in [("API", self.api_url), ("Self-hosted", self.selfhosted_url)]:
                print(f"  Testing {service_name} service...")
                
                start_time = time.time()
                results = []
                
                with ThreadPoolExecutor(max_workers=num_requests) as executor:
                    futures = [
                        executor.submit(self.test_single_request, service_url, test_text, service_name.lower())
                        for _ in range(num_requests)
                    ]
                    
                    for future in as_completed(futures):
                        results.append(future.result())
                
                end_time = time.time()
                total_time = (end_time - start_time) * 1000
                
                successful = [r for r in results if r['success']]
                failed = [r for r in results if not r['success']]
                
                if successful:
                    avg_latency = statistics.mean([r['latency_ms'] for r in successful])
                    print(f"    {service_name}: {len(successful)}/{num_requests} successful")
                    print(f"    Average latency: {avg_latency:.1f}ms")
                    print(f"    Total time: {total_time:.1f}ms")
                    print(f"    Requests/second: {len(successful) / (total_time / 1000):.1f}")
                
                if failed:
                    print(f"    Failed requests: {len(failed)}")
                
                time.sleep(2)  # Brief pause between service tests
    
    def calculate_cost_analysis(self):
        """Calculate cost comparison at different volumes"""
        print("\n Calculating Cost Analysis...")
        
        # Cost assumptions
        api_cost_per_request = 0.002  # $0.002 per request
        selfhosted_monthly_cost = 500  # $500/month infrastructure
        
        volumes = [100, 1000, 10000, 25000, 50000, 100000]
        
        print(f"Assumptions:")
        print(f"  API cost: {format_currency(api_cost_per_request)}/request")
        print(f"  Self-hosted: {format_currency(selfhosted_monthly_cost)}/month")
        
        print(f"\n{'Volume':<10} {'API Cost':<12} {'Self-hosted':<12} {'Cheaper':<15} {'Savings':<10}")
        print("-" * 65)
        
        for volume in volumes:
            api_monthly = volume * api_cost_per_request
            selfhosted_monthly = selfhosted_monthly_cost
            
            if api_monthly < selfhosted_monthly:
                cheaper = "API"
                savings = format_currency(selfhosted_monthly - api_monthly)
            else:
                cheaper = "Self-hosted"
                savings = format_currency(api_monthly - selfhosted_monthly)
            
            print(f"{volume:<10,} {format_currency(api_monthly):<12} {format_currency(selfhosted_monthly):<12} {cheaper:<15} {savings:<10}")
        
        # Calculate exact breakeven
        breakeven = calculate_cost_breakeven(api_cost_per_request, selfhosted_monthly_cost)
        print(f"\n Breakeven point: {breakeven['breakeven_requests_per_month']:,} requests/month")
        
        self.results['cost_analysis'] = {
            'breakeven_requests': breakeven['breakeven_requests_per_month'],
            'api_cost_per_request': api_cost_per_request,
            'selfhosted_monthly_cost': selfhosted_monthly_cost
        }
    
    def test_startup_behavior(self):
        """Test startup time differences"""
        print("\n Testing Startup Behavior...")
        print("Note: This test requires manual container restart")
        print("Run these commands in another terminal:")
        print("  docker-compose restart api-service")
        print("  docker-compose restart selfhosted-service")
        print("Then observe the logs with:")
        print("  docker-compose logs -f api-service")
        print("  docker-compose logs -f selfhosted-service")
    
    def generate_report(self):
        """Generate comprehensive comparison report"""
        print("\n" + "="*80)
        print(" PERFORMANCE COMPARISON REPORT")
        print("="*80)
        
        print("\n KEY FINDINGS:")
        
        # Latency findings
        if 'latency_medium' in self.results:
            medium_results = self.results['latency_medium']
            if 'error' not in medium_results.get('api', {}) and 'error' not in medium_results.get('selfhosted', {}):
                api_avg = medium_results['api']['avg']
                selfhosted_avg = medium_results['selfhosted']['avg']
                improvement = ((api_avg - selfhosted_avg) / api_avg) * 100
                
                print(f"  • Self-hosted is {improvement:.1f}% faster than API service")
                print(f"    - API: {api_avg:.1f}ms average")
                print(f"    - Self-hosted: {selfhosted_avg:.1f}ms average")
        
        # Cost findings
        if 'cost_analysis' in self.results:
            breakeven = self.results['cost_analysis']['breakeven_requests']
            print(f"  • Cost breakeven at {breakeven:,} requests/month")
            print(f"    - Below: API service is cheaper")
            print(f"    - Above: Self-hosted is cheaper")
        
        print("\n RECOMMENDATIONS:")
        print("  Choose API service when:")
        print("    - Volume < 25,000 requests/month")
        print("    - Variable/unpredictable load")
        print("    - Fast time-to-market needed")
        print("    - Limited DevOps resources")
        
        print("\n  Choose Self-hosted when:")
        print("    - Volume > 25,000 requests/month")
        print("    - Predictable load patterns")
        print("    - Data privacy requirements")
        print("    - Cost predictability needed")
        
        # Save results to file
        with open('test_results/performance_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n Detailed results saved to: test_results/performance_report.json")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print(" Starting Performance Comparison Tests")
        print("="*50)
        
        # Create results directory
        os.makedirs('test_results', exist_ok=True)
        
        try:
            self.wait_for_services()
            self.test_latency_comparison()
            self.test_concurrent_load()
            self.calculate_cost_analysis()
            self.test_startup_behavior()
            self.generate_report()
            
            print("\n All tests completed successfully!")
            
        except Exception as e:
            print(f"\n Test failed: {e}")
            return False
        
        return True

if __name__ == "__main__":
    tester = PerformanceTester()
    tester.run_all_tests()
