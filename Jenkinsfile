pipeline {
  agent any

  environment {
    // Remote deployment target (Linux host with Docker & Compose)
    DEPLOY_HOST   = 'deploy.example.com'   // <-- change me
    DEPLOY_USER   = 'ubuntu'               // <-- change me
    DEPLOY_PATH   = '/opt/student-registration-app' // <-- change me

    // Jenkins credentials ID for SSH to the server
    DEPLOY_SSH    = 'DEPLOY_SSH'           // <-- create this credential in Jenkins
  }

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Deploy (Build & Run on remote)') {
      steps {
        sshagent (credentials: [env.DEPLOY_SSH]) {
          sh '''
            set -eux
            # Prepare remote dir
            ssh -o StrictHostKeyChecking=no "$DEPLOY_USER@$DEPLOY_HOST" "mkdir -p '$DEPLOY_PATH'"
            # Sync repo to remote (tar stream is simple & fast)
            tar -czf - . | ssh -o StrictHostKeyChecking=no "$DEPLOY_USER@$DEPLOY_HOST" "tar -xzf - -C '$DEPLOY_PATH'"
            # Build & start on remote using Docker Compose (no registry involved)
            ssh -o StrictHostKeyChecking=no "$DEPLOY_USER@$DEPLOY_HOST" "bash -s" <<'EOSSH'
              set -eux
              cd "$DEPLOY_PATH"
              # Build updated images locally & (re)start in detached mode
              docker compose -f docker-compose.yml up -d --build
              docker compose ps
            EOSSH
          '''
        }
      }
    }
  }

  post {
    always {
      echo "Build finished: ${currentBuild.currentResult}"
    }
  }
}
