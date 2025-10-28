#!/usr/bin/env python3
"""
Calculate deployment delays and update JSON file
This script reads the deployments.json file, calculates the delay
between planned and actual deployment dates, and updates the file.
"""

import json
from datetime import datetime
from pathlib import Path
import sys

def calculate_delays():
    """Calculate deployment delays for all deployments in the JSON file."""
    
    data_file = Path('data/deployments.json')
    
    if not data_file.exists():
        print(f"❌ Error: {data_file} not found!")
        sys.exit(1)
    
    try:
        # Read the data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        print("=" * 60)
        print("Calculating Deployment Delays")
        print("=" * 60)
        
        total_delay = 0
        sprint_count = 0
        hotfix_count = 0
        
        # Calculate delays for each deployment
        for deployment in data['deployments']:
            try:
                name = deployment.get('Name', 'Unknown')
                
                # Parse dates
                planned = datetime.fromisoformat(
                    deployment['PlannedDeploymentDate'].replace('Z', '+00:00')
                )
                actual = datetime.fromisoformat(
                    deployment['DeploymentDate'].replace('Z', '+00:00')
                )
                
                # Calculate delay in days
                delay = (actual - planned).days
                deployment['DelayDays'] = delay
                
                # Count by type
                if deployment['Type'].lower() == 'sprint':
                    sprint_count += 1
                elif deployment['Type'].lower() == 'hotfix':
                    hotfix_count += 1
                
                total_delay += delay
                
                # Print status
                status = "✅" if delay <= 5 else "⚠️" if delay <= 10 else "❌"
                print(f"{status} {name:20s}: {delay:3d} days delay")
                
            except KeyError as e:
                print(f"⚠️  Warning: Missing field {e} in {name}")
            except ValueError as e:
                print(f"⚠️  Warning: Invalid date format in {name}: {e}")
        
        # Calculate statistics
        total_deployments = len(data['deployments'])
        avg_delay = total_delay / total_deployments if total_deployments > 0 else 0
        
        # Update lastUpdated timestamp
        data['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Write back to file
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("=" * 60)
        print("Summary:")
        print(f"  Total Deployments: {total_deployments}")
        print(f"  Sprints: {sprint_count}")
        print(f"  Hotfixes: {hotfix_count}")
        print(f"  Average Delay: {avg_delay:.1f} days")
        print(f"  Total Delay: {total_delay} days")
        print("=" * 60)
        print("✅ Delays calculated and saved successfully!")
        print(f"   File: {data_file}")
        print(f"   Last Updated: {data['lastUpdated']}")
        print("=" * 60)
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {data_file}")
        print(f"   {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    calculate_delays()
