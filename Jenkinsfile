pipeline {
  agent any

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Deploy Locally') {
      steps {
        sh '''
          set -eux
          # Build images and start containers locally
          docker compose -f docker-compose.yml up -d --build
          docker compose ps
        '''
      }
    }
  }

  post {
    always {
      echo "Pipeline finished: ${currentBuild.currentResult}"
    }
  }
}
