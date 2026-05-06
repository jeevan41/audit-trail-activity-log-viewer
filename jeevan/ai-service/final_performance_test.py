import requests
import json
import time
import hashlib

# Test configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_ITERATIONS = 5  # Test each endpoint multiple times to check caching

# Test data
test_logs = [
    "2024-01-15 10:30:45 - User 'john.doe' successfully logged in from IP 192.168.1.100",
    "2024-01-15 10:31:22 - User 'admin' accessed file '/etc/passwd' with read permissions",
    "2024-01-15 10:32:10 - Failed login attempt for user 'root' from IP 10.0.0.5"
]

def calculate_cache_key(text):
    """Calculate SHA256 cache key like the app does"""
    return hashlib.sha256(text.encode()).hexdigest()

def test_endpoint_performance(endpoint_name, method, url, payload=None, iterations=TEST_ITERATIONS):
    """Test endpoint performance and caching"""
    print(f"\n🔍 Testing {endpoint_name} ({iterations} iterations)")

    results = []
    cache_keys = []

    for i in range(iterations):
        start_time = time.time()

        try:
            if method == 'GET':
                response = requests.get(url, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=payload, timeout=30)
            else:
                return {"error": f"Unsupported method: {method}"}

            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)

            result = {
                "iteration": i + 1,
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "timestamp": time.strftime("%H:%M:%S", time.localtime(start_time))
            }

            # Calculate cache key for POST requests
            if method == 'POST' and payload:
                if 'log_entry' in payload:
                    cache_key = calculate_cache_key(f"{endpoint_name}:{payload['log_entry']}")
                elif 'logs' in payload:
                    logs_text = '\n'.join(payload['logs'])
                    cache_key = calculate_cache_key(f"report:{logs_text}")
                else:
                    cache_key = None
                cache_keys.append(cache_key)
                result["cache_key"] = cache_key

            if response.status_code == 200:
                try:
                    result["response"] = response.json()
                    result["is_fallback"] = result["response"].get("is_fallback", False)
                except:
                    result["response"] = response.text
            else:
                result["error"] = response.text

            results.append(result)
            status = "✅" if response.status_code == 200 else "❌"
            cache_indicator = " (cached)" if i > 0 and response_time < 100 else " (fresh)"
            print(f"  {status} Iteration {i+1}: {response_time}ms{cache_indicator}")

        except Exception as e:
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)
            results.append({
                "iteration": i + 1,
                "error": str(e),
                "response_time_ms": response_time,
                "timestamp": time.strftime("%H:%M:%S", time.localtime(start_time))
            })
            print(f"  ❌ Iteration {i+1}: Exception - {str(e)}")

        # Small delay between requests
        time.sleep(0.5)

    return results

def analyze_performance(results, endpoint_name):
    """Analyze performance results"""
    if not results:
        return {"error": "No results to analyze"}

    response_times = [r['response_time_ms'] for r in results if 'response_time_ms' in r]
    successful_requests = len([r for r in results if r.get('status_code') == 200])
    fallback_responses = len([r for r in results if r.get('is_fallback')])

    # Check for caching (significant time difference between first and subsequent requests)
    cache_working = False
    if len(response_times) >= 2:
        first_time = response_times[0]
        avg_subsequent = sum(response_times[1:]) / len(response_times[1:])
        cache_working = avg_subsequent < (first_time * 0.5)  # 50% faster indicates caching

    analysis = {
        "endpoint": endpoint_name,
        "total_requests": len(results),
        "successful_requests": successful_requests,
        "success_rate": round(successful_requests / len(results) * 100, 1) if results else 0,
        "fallback_responses": fallback_responses,
        "cache_working": cache_working,
        "avg_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0,
        "min_response_time_ms": min(response_times) if response_times else 0,
        "max_response_time_ms": max(response_times) if response_times else 0,
        "target_met": False  # Will be set based on targets
    }

    return analysis

def run_final_verification():
    """Run comprehensive final performance verification"""
    print("🚀 Final Performance Verification")
    print("=" * 60)
    print("Testing all endpoints for performance, caching, and fallback behavior")
    print(f"Each endpoint tested {TEST_ITERATIONS} times")
    print()

    all_results = {}
    analyses = {}

    # Start Flask app
    print("📍 Note: Ensure AI service is running on http://127.0.0.1:5000")
    print("📍 Note: GROQ_API_KEY should NOT be set to test fallback behavior")
    print()

    # Test Health endpoint
    health_results = test_endpoint_performance(
        "health", "GET", f"{BASE_URL}/health"
    )
    all_results["health"] = health_results
    analyses["health"] = analyze_performance(health_results, "health")

    # Test Describe endpoint
    describe_results = test_endpoint_performance(
        "describe", "POST", f"{BASE_URL}/describe",
        {"log_entry": test_logs[0]}
    )
    all_results["describe"] = describe_results
    analyses["describe"] = analyze_performance(describe_results, "describe")

    # Test Recommend endpoint
    recommend_results = test_endpoint_performance(
        "recommend", "POST", f"{BASE_URL}/recommend",
        {"log_entry": test_logs[1]}
    )
    all_results["recommend"] = recommend_results
    analyses["recommend"] = analyze_performance(recommend_results, "recommend")

    # Test Generate Report endpoint
    report_results = test_endpoint_performance(
        "generate-report", "POST", f"{BASE_URL}/generate-report",
        {"logs": test_logs}
    )
    all_results["generate-report"] = report_results
    analyses["generate-report"] = analyze_performance(report_results, "generate-report")

    # Performance targets (based on requirements)
    targets = {
        "health": {"max_avg_time": 1000, "min_success_rate": 100},  # 1s max
        "describe": {"max_avg_time": 8000, "min_success_rate": 100},  # 8s max
        "recommend": {"max_avg_time": 8000, "min_success_rate": 100},  # 8s max
        "generate-report": {"max_avg_time": 15000, "min_success_rate": 100}  # 15s max
    }

    # Check targets
    print("\n🎯 Performance Target Analysis")
    print("-" * 60)

    all_targets_met = True
    for endpoint, analysis in analyses.items():
        target = targets.get(endpoint, {})
        max_time = target.get("max_avg_time", 10000)
        min_success = target.get("min_success_rate", 95)

        time_met = analysis["avg_response_time_ms"] <= max_time
        success_met = analysis["success_rate"] >= min_success

        analysis["target_met"] = time_met and success_met
        if not analysis["target_met"]:
            all_targets_met = False

        status = "✅ PASS" if analysis["target_met"] else "❌ FAIL"
        print(f"{status} {endpoint}:")
        print(f"    Response Time: {analysis['avg_response_time_ms']}ms (target: ≤{max_time}ms) {'✅' if time_met else '❌'}")
        print(f"    Success Rate: {analysis['success_rate']}% (target: ≥{min_success}%) {'✅' if success_met else '❌'}")
        print(f"    Cache Working: {'✅' if analysis['cache_working'] else '❌'}")
        print(f"    Fallback Active: {'✅' if analysis['fallback_responses'] > 0 else '❌'}")
        print()

    # Overall assessment
    print("🏆 Final Assessment")
    print("-" * 60)

    cache_endpoints = ["describe", "recommend", "generate-report"]
    cache_working = all(analyses[ep]["cache_working"] for ep in cache_endpoints if ep in analyses)

    fallback_working = all(analyses[ep]["fallback_responses"] > 0 for ep in ["describe", "recommend", "generate-report"] if ep in analyses)

    print(f"Performance Targets: {'✅ ALL MET' if all_targets_met else '❌ SOME FAILED'}")
    print(f"Cache Working: {'✅ YES' if cache_working else '❌ NO'}")
    print(f"Fallback Working: {'✅ YES' if fallback_working else '❌ NO'}")

    overall_status = all_targets_met and cache_working and fallback_working
    print(f"\n🎉 Overall Status: {'✅ PRODUCTION READY' if overall_status else '❌ NEEDS ATTENTION'}")

    # Save detailed results
    output = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "test_configuration": {
            "base_url": BASE_URL,
            "iterations_per_endpoint": TEST_ITERATIONS,
            "groq_api_key_set": False  # Assuming not set for fallback testing
        },
        "performance_targets": targets,
        "detailed_results": all_results,
        "analyses": analyses,
        "overall_assessment": {
            "all_targets_met": all_targets_met,
            "cache_working": cache_working,
            "fallback_working": fallback_working,
            "production_ready": overall_status
        }
    }

    with open("final_performance_verification.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n💾 Detailed results saved to final_performance_verification.json")

    return output

if __name__ == "__main__":
    run_final_verification()