pipeline {
  agent any

  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Start DB Only') {
      steps {
        sh '''
          set -eux
          docker compose -f docker-compose.yml up -d db
          for i in $(seq 1 30); do
            state=$(docker inspect -f '{{json .State.Health.Status}}' sr_mysql || echo "null")
            if [ "$state" = "\"healthy\"" ]; then
              echo "DB is healthy"; break
            fi
            echo "Waiting for DB to be healthy... ($i/30)"; sleep 2
          done
        '''
      }
    }

    stage('DB Migrate (Idempotent)') {
      steps {
        sh '''
          set -eux
          docker exec -i sr_mysql mysql -uappuser -papppass training_center < db/init.sql
        '''
      }
    }

    stage('Build & Deploy App') {
      steps {
        sh '''
          set -eux
          docker compose -f docker-compose.yml up -d --build app
          docker compose ps
        '''
      }
    }
  }

  post {
    always { echo "Pipeline finished: ${currentBuild.currentResult}" }
  }
}
