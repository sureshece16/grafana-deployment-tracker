pipeline {
    agent any
    
    environment {
        GRAFANA_URL = credentials('grafana-url')
        GRAFANA_API_KEY = credentials('grafana-api-key')

        // Local filesystem path where Grafana can read
        GRAFANA_DATA_PATH = '/var/lib/grafana/data'
        DATA_FILE_NAME = 'deployments.json'

        // File URL for Grafana to access
        DATA_URL = "file://${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}"

        // If Grafana is on different server, set this
        GRAFANA_SERVER = 'localhost'  // Change to actual hostname if remote
        GRAFANA_USER = 'grafana'       // User that Grafana runs as
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔄 Checking out code from repository..."
                }
                checkout scm
            }
        }

        stage('Validate JSON') {
            steps {
                script {
                    echo "✔️  Validating JSON format..."
                }
                sh '''
                    # Validate JSON syntax
                    python3 -m json.tool data/deployments.json > /dev/null

                    if [ $? -eq 0 ]; then
                        echo "✅ JSON is valid"
                    else
                        echo "❌ Invalid JSON format"
                        exit 1
                    fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "📦 Installing Python dependencies..."
                }
                sh '''
                    python3 -m pip install --user requests --quiet || true
                '''
            }
        }

        stage('Calculate Deployment Delays') {
            steps {
                script {
                    echo "🧮 Calculating deployment delays..."
                }
                sh '''
                    python3 scripts/calculate_delays.py
                '''
            }
        }

        stage('Commit Updated Data') {
            when {
                expression {
                    return sh(
                        script: 'git status --porcelain data/deployments.json',
                        returnStdout: true
                    ).trim() != ''
                }
            }
            steps {
                script {
                    echo "💾 Committing updated data back to repository..."
                }
                sh '''
                    git config user.email "jenkins@igotkarmayogi.gov.in"
                    git config user.name "Jenkins CI"

                    git add data/deployments.json
                    git commit -m "Jenkins: Auto-calculate deployment delays [skip ci]"

                    echo "✅ Changes committed locally"
                    echo "⚠️  Note: Push to remote if needed"
                '''
            }
        }

        stage('Deploy Data to Local Filesystem') {
            steps {
                script {
                    echo "📂 Deploying data to local filesystem..."
                    echo "   Target: ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}"
                }
                sh '''
                    # Create directory if it doesn't exist
                    sudo mkdir -p ${GRAFANA_DATA_PATH}

                    # Copy the data file
                    sudo cp -f data/${DATA_FILE_NAME} ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}

                    # Set ownership to grafana user
                    sudo chown ${GRAFANA_USER}:${GRAFANA_USER} ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}

                    # Set read permissions
                    sudo chmod 644 ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}

                    # Verify the file
                    if [ -f "${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}" ]; then
                        echo "✅ File deployed successfully"
                        echo "   Location: ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}"
                        echo "   Size: $(ls -lh ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME} | awk '{print $5}')"
                        echo "   Permissions: $(ls -l ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME} | awk '{print $1}')"
                    else
                        echo "❌ File deployment failed"
                        exit 1
                    fi
                '''
            }
        }

        stage('Create Backup') {
            steps {
                script {
                    echo "💾 Creating backup of previous data..."
                }
                sh '''
                    # Create backup directory
                    BACKUP_DIR="${GRAFANA_DATA_PATH}/backups"
                    sudo mkdir -p ${BACKUP_DIR}

                    # Create backup with timestamp
                    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                    BACKUP_FILE="${BACKUP_DIR}/deployments_${TIMESTAMP}.json"

                    if [ -f "${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}" ]; then
                        sudo cp ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME} ${BACKUP_FILE}
                        echo "✅ Backup created: ${BACKUP_FILE}"

                        # Keep only last 10 backups
                        sudo ls -t ${BACKUP_DIR}/deployments_*.json | tail -n +11 | xargs -r sudo rm
                        echo "   Retained last 10 backups"
                    fi
                '''
            }
        }

        stage('Deploy Dashboard to Grafana') {
            steps {
                script {
                    echo "📊 Deploying dashboard to Grafana..."
                }
                sh '''
                    python3 scripts/deploy_dashboard.py
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    echo "✔️  Verifying deployment..."
                }
                sh '''
                    # Verify file exists and is readable
                    if [ -r "${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}" ]; then
                        echo "✅ File is readable by current user"
                    else
                        echo "⚠️  File may not be readable by Grafana"
                    fi

                    # Verify JSON is valid
                    sudo cat ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME} | python3 -m json.tool > /dev/null

                    if [ $? -eq 0 ]; then
                        echo "✅ Deployed JSON is valid"
                    else
                        echo "❌ Deployed JSON is invalid"
                        exit 1
                    fi

                    # Count deployments
                    DEPLOYMENT_COUNT=$(sudo cat ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME} | python3 -c "import sys, json; print(len(json.load(sys.stdin)['deployments']))")
                    echo "✅ Total deployments in file: ${DEPLOYMENT_COUNT}"

                    # Verify Grafana is reachable
                    curl -s -k -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
                         "${GRAFANA_URL}/api/health" > /dev/null

                    if [ $? -eq 0 ]; then
                        echo "✅ Grafana is reachable"
                    else
                        echo "⚠️  Cannot reach Grafana"
                    fi

                    echo ""
                    echo "=" * 60
                    echo "Deployment Summary:"
                    echo "  Data Path: ${GRAFANA_DATA_PATH}/${DATA_FILE_NAME}"
                    echo "  Grafana URL: ${DATA_URL}"
                    echo "  Dashboard: ${GRAFANA_URL}"
                    echo "=" * 60
                '''
            }
        }
    }

    post {
        success {
            script {
                def buildDuration = currentBuild.durationString.replace(' and counting', '')

                echo '✅ =============================================='
                echo '✅ Pipeline completed successfully!'
                echo '✅ =============================================='
                echo "   Build Duration: ${buildDuration}"
                echo "   Data Location: ${env.GRAFANA_DATA_PATH}/${env.DATA_FILE_NAME}"
                echo "   Grafana Dashboard: ${env.GRAFANA_URL}"
                echo '✅ =============================================='
            }
        }

        failure {
            echo '❌ =============================================='
            echo '❌ Pipeline failed!'
            echo '❌ =============================================='
            echo "   Check the logs above for details"
            echo '❌ =============================================='
        }

        always {
            script {
                echo '🧹 Cleaning up workspace...'
            }
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: '**/*.pyc', type: 'INCLUDE'],
                    [pattern: '**/__pycache__', type: 'INCLUDE']
                ]
            )
        }
    }
}