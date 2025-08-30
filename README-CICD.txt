CI/CD with Jenkins (Docker + Docker Compose)
===========================================

What this adds
--------------
- Jenkinsfile to build, push, and deploy the app image.
- docker-compose.deploy.override.yml that tells Compose to use the pushed image.
- Remote deploy via SSH to a Linux host with Docker & Docker Compose.

Prerequisites
-------------
1) Jenkins agent with Docker CLI available.
2) Credentials created in Jenkins:
   - ID: DOCKERHUB_CRED (Username + Password for Docker Hub or your registry)
   - ID: DEPLOY_SSH     (SSH private key for the deploy user on the remote host)
3) Remote host:
   - Docker and Docker Compose plugin installed.
   - SSH access for the deploy user.
   - The user is in the `docker` group or can run docker without sudo.

How it works
------------
- Build: `docker build -t REGISTRY/REPO:BUILD_NUMBER ./app`
- Push:  login to registry and push
- Deploy:
  - Copies compose files and db/init.sql to remote host
  - Creates `.env` with `APP_IMAGE=...`
  - Runs `docker compose up -d` using the override to pull & run the new image

Quick Setup
-----------
1) Edit the Jenkinsfile:
   - REGISTRY, IMAGE_REPO (e.g., docker.io/yourname/student-registration-app)
   - DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH
2) In Jenkins UI:
   - Create pipeline from SCM pointing to your repo
   - Set credentials IDs to match Jenkinsfile
3) Trigger a build:
   - On success, the new version is online on your remote host.

Rollback
--------
- Re-run the pipeline with `IMAGE_TAG` set to an older build number (use "Build With Parameters" if you parameterize it), or
- On the remote host: `docker compose -f docker-compose.yml -f docker-compose.deploy.override.yml up -d APP_IMAGE=<old-tag>`
