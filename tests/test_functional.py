import json
import requests
from pathlib import Path

def load_scenarios():
    """Load test scenarios from JSON file"""
    scenarios_path = Path(__file__).parent / "scenarios.json"
    with open(scenarios_path) as f:
        return json.load(f)

def test_api_functionality():
    """Test API functionality against scenarios"""
    scenarios = load_scenarios()
    api_url = "http://0.0.0.0:8081/predict"
    
    for case in scenarios["test_cases"]:
        print(f"\nTesting scenario: {case['name']}")
        
        # Send request to API
        response = requests.post(api_url, json=case["input"])
        
        # Check response status
        assert response.status_code == 200, f"API return status code {response.status_code}"
        
        # Get prediction result
        result = response.json()
        
        # Check prediction
        assert result["prediction"] == case["expected"]["prediction"], \
            f"Prediction mismatch for {case['name']}. Expected {case['expected']['prediction']}, got {result['prediction']}"
        
        # Check probability (with some tolerance)
        expected_prob = case["expected"]["probability"]
        actual_prob = result["probability"]
        assert abs(expected_prob - actual_prob) < 0.1, \
            f"Probability mismatch for {case['name']}. Expected {expected_prob}, got {actual_prob}"
        
        print(f"✓ Test passed: {case['name']}")
        print(f"  Input: {case['input']}")
        print(f"  Expected: {case['expected']}")
        print(f"  Got: {result}")

if __name__ == "__main__":
    test_api_functionality() 