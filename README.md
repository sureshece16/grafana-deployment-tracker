# Grafana Deployment Tracker

Automated deployment tracking dashboard for monitoring Sprint and Hotfix deployments with Jenkins CI/CD integration.

## 📊 Features

- **Real-time Dashboard**: Visualize deployment metrics in Grafana
- **Automated Delays Calculation**: Automatically calculates delays between planned and actual deployment dates
- **CI/CD Integration**: Jenkins pipeline for automated deployment
- **Git Version Control**: Track all changes in Git repository
- **REST API**: Serve deployment data via HTTP API

## 🏗️ Architecture
```
Git Repository → Jenkins Pipeline → Grafana Dashboard
     ↓                  ↓                    ↓
  Data JSON      Calculate Delays      Visualizations
  Dashboard      Deploy to Server      Interactive Tables
```

## 📁 Repository Structure
```
grafana-deployment-tracker/
├── Jenkinsfile                    # Jenkins pipeline configuration
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── data/
│   └── deployments.json          # Deployment data (auto-updated)
├── dashboards/
│   └── deployment-dashboard.json # Grafana dashboard definition
├── scripts/
│   ├── calculate_delays.py       # Calculate deployment delays
│   ├── deploy_dashboard.py       # Deploy dashboard to Grafana
│   └── serve_data.py            # HTTP server for data (optional)
└── docs/
    └── setup-guide.md            # Detailed setup instructions
```

## 🚀 Quick Start

### Prerequisites

- Jenkins server with Pipeline plugin
- Grafana instance (https://igotkarmayogi.gov.in/grafana)
- Python 3.7+
- Git

### Setup Steps

1. **Clone this repository:**
```bash
   git clone https://github.com/YOUR_USERNAME/grafana-deployment-tracker.git
   cd grafana-deployment-tracker
```

2. **Install Python dependencies:**
```bash
   pip3 install requests flask flask-cors
```

3. **Configure Jenkins credentials:**
   - `grafana-url`: https://igotkarmayogi.gov.in/grafana
   - `grafana-api-key`: Your Grafana API key
   - `data-url`: URL where deployments.json is hosted

4. **Create Jenkins pipeline job pointing to this repository**

5. **Run the pipeline to deploy dashboard**

## 📝 Adding New Deployments

Edit `data/deployments.json` and add new entries:
```json
{
  "Type": "Sprint",
  "Name": "Sprint 31",
  "PlannedDeploymentDate": "2025-06-01T00:00:00Z",
  "DeploymentDate": "2025-06-05T00:00:00Z",
  "Description": "https://your-documentation-url"
}
```

Then commit and push:
```bash
git add data/deployments.json
git commit -m "Add Sprint 31 deployment"
git push origin main
```

Jenkins will automatically:
1. ✅ Calculate delays
2. ✅ Update the JSON file
3. ✅ Deploy data to server
4. ✅ Update Grafana dashboard

## 📊 Dashboard Panels

- **Total Deployments**: Count of all deployments
- **Average Delay**: Mean delay across all deployments
- **Max Delay**: Highest delay recorded
- **Sprint vs Hotfix**: Distribution pie chart
- **On-Time vs Delayed**: Performance metrics
- **Detailed Table**: Full deployment history with documentation links
- **Delay Timeline**: Bar chart of delays by release
- **Trend Chart**: Time-series visualization of deployment delays

## 🔧 Scripts

### calculate_delays.py
Calculates delay between planned and actual deployment dates.
```bash
python3 scripts/calculate_delays.py
```

### deploy_dashboard.py
Deploys dashboard to Grafana via API.
```bash
export GRAFANA_URL="https://igotkarmayogi.gov.in/grafana"
export GRAFANA_API_KEY="your-api-key"
export DATA_URL="http://your-server/deployments.json"
python3 scripts/deploy_dashboard.py
```

### serve_data.py (Optional)
Runs HTTP server to host deployment data.
```bash
python3 scripts/serve_data.py
# Access at http://localhost:8080/deployments.json
```

## 🔐 Security

- Never commit API keys to Git
- Use Jenkins credentials for sensitive data
- Rotate API keys periodically
- Use HTTPS for all communications

## 🐛 Troubleshooting

### Pipeline fails at "Deploy to Grafana"
- Check Grafana URL is correct
- Verify API key has Editor or Admin permissions
- Ensure Grafana is accessible from Jenkins server

### Data not updating
- Check Jenkins credentials are set correctly
- Verify deployments.json format is valid
- Check file permissions on web server

### Dashboard not showing data
- Verify DATA_URL is accessible
- Check Infinity data source is installed in Grafana
- Ensure CORS is enabled on data server

## 📚 Documentation

- [Jenkins Setup Guide](docs/jenkins-setup.md)
- [Grafana Configuration](docs/grafana-setup.md)
- [API Documentation](docs/api-docs.md)

## 👥 Contributors

- Your Name <your.email@igotkarmayogi.gov.in>

## 📄 License

MIT License - feel free to use and modify as needed.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues and questions:
- Create an issue in this repository
- Contact: your.email@igotkarmayogi.gov.in

---

**Last Updated**: October 2025
**Grafana URL**: https://igotkarmayogi.gov.in/grafana
