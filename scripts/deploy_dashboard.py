#!/usr/bin/env python3
"""
Deploy Grafana dashboard via API
This script reads the dashboard JSON and deploys it to Grafana
using the REST API.
"""

import os
import json
import requests
import sys
from pathlib import Path

def deploy_dashboard():
    """Deploy dashboard to Grafana using API."""
    
    # Get environment variables
    grafana_url = os.environ.get('GRAFANA_URL', 'https://igotkarmayogi.gov.in/grafana')
    api_key = os.environ.get('GRAFANA_API_KEY')
    data_url = os.environ.get('DATA_URL', '')
    
    # Validation
    if not api_key:
        print("❌ Error: GRAFANA_API_KEY environment variable must be set")
        print("   Set it in Jenkins credentials")
        sys.exit(1)
    
    # Remove trailing slash from Grafana URL
    grafana_url = grafana_url.rstrip('/')
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("=" * 60)
    print("Deploying Dashboard to Grafana")
    print("=" * 60)
    print(f"Grafana URL: {grafana_url}")
    print(f"Data URL: {data_url if data_url else 'Not set'}")
    print("=" * 60)
    
    # Read dashboard JSON
    dashboard_file = Path('dashboards/deployment-dashboard.json')
    
    if not dashboard_file.exists():
        print(f"❌ Error: Dashboard file not found: {dashboard_file}")
        sys.exit(1)
    
    try:
        with open(dashboard_file, 'r') as f:
            dashboard_config = json.load(f)
        print(f"✅ Dashboard JSON loaded: {dashboard_file}")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in dashboard file")
        print(f"   {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading dashboard file: {e}")
        sys.exit(1)
    
    # Update data source URL in dashboard if DATA_URL is provided
    if data_url:
        print(f"🔄 Updating data URL in dashboard...")
        dashboard_json = json.dumps(dashboard_config)
        dashboard_json = dashboard_json.replace('YOUR_DATA_URL_HERE', data_url)
        dashboard_config = json.loads(dashboard_json)
        print(f"✅ Data URL updated to: {data_url}")
    
    # Deploy to Grafana
    api_endpoint = f"{grafana_url}/api/dashboards/db"
    print(f"📤 Deploying to: {api_endpoint}")
    print("   Please wait...")
    
    try:
        response = requests.post(
            api_endpoint,
            json=dashboard_config,
            headers=headers,
            timeout=30,
            verify=True  # Set to False if SSL certificate issues
        )
        
        if response.status_code == 200:
            result = response.json()
            print("=" * 60)
            print("✅ Dashboard Deployed Successfully!")
            print("=" * 60)
            print(f"   Dashboard URL: {grafana_url}{result.get('url', '')}")
            print(f"   Status: {result.get('status', 'deployed')}")
            print(f"   Version: {result.get('version', 'N/A')}")
            print(f"   UID: {result.get('uid', 'N/A')}")
            
            if result.get('slug'):
                print(f"   Slug: {result.get('slug')}")
            
            print("=" * 60)
            print("🎉 You can now view your dashboard in Grafana!")
            print("=" * 60)
            
        elif response.status_code == 401:
            print("=" * 60)
            print("❌ Authentication Failed (401 Unauthorized)")
            print("=" * 60)
            print("   Possible causes:")
            print("   1. Invalid or expired API key")
            print("   2. API key doesn't have sufficient permissions")
            print("   3. API key is for a different organization")
            print("")
            print("   Solution:")
            print("   1. Generate a new API key with Editor or Admin role")
            print("   2. Update GRAFANA_API_KEY in Jenkins credentials")
            print("=" * 60)
            sys.exit(1)
            
        elif response.status_code == 403:
            print("=" * 60)
            print("❌ Permission Denied (403 Forbidden)")
            print("=" * 60)
            print("   Your API key doesn't have permission to create/update dashboards")
            print("   Generate a new API key with Editor or Admin role")
            print("=" * 60)
            sys.exit(1)
            
        elif response.status_code == 404:
            print("=" * 60)
            print("❌ Not Found (404)")
            print("=" * 60)
            print(f"   URL: {api_endpoint}")
            print("   Check if Grafana URL is correct")
            print("=" * 60)
            sys.exit(1)
            
        else:
            print("=" * 60)
            print(f"❌ Deployment Failed: HTTP {response.status_code}")
            print("=" * 60)
            print(f"   Response: {response.text}")
            print("=" * 60)
            sys.exit(1)
            
    except requests.exceptions.SSLError as e:
        print("=" * 60)
        print("❌ SSL Certificate Error")
        print("=" * 60)
        print(f"   {e}")
        print("")
        print("   Solutions:")
        print("   1. Fix SSL certificate on Grafana server")
        print("   2. Set verify=False in script (not recommended for production)")
        print("=" * 60)
        sys.exit(1)
        
    except requests.exceptions.ConnectionError as e:
        print("=" * 60)
        print("❌ Connection Error")
        print("=" * 60)
        print(f"   Cannot connect to: {grafana_url}")
        print(f"   {e}")
        print("")
        print("   Check:")
        print("   1. Grafana URL is correct")
        print("   2. Grafana server is running")
        print("   3. Network/firewall allows connection from Jenkins")
        print("=" * 60)
        sys.exit(1)
        
    except requests.exceptions.Timeout:
        print("=" * 60)
        print("❌ Request Timeout")
        print("=" * 60)
        print("   Grafana server took too long to respond")
        print("   Try again or increase timeout value")
        print("=" * 60)
        sys.exit(1)
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Unexpected Error")
        print("=" * 60)
        print(f"   {type(e).__name__}: {e}")
        print("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    deploy_dashboard()
