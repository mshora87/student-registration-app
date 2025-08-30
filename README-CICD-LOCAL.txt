CI/CD with Jenkins (Local Docker Build on Server)
=================================================

Summary
-------
This pipeline deploys by copying the repo to your server over SSH and running:
  docker compose up -d --build
on the server. No Docker Hub (or any registry) is used.

Prerequisites
-------------
- Jenkins with SSH Agent plugin.
- Jenkins credential (ID: DEPLOY_SSH) = SSH private key for the deploy user.
- Remote server:
  - Linux with Docker + Docker Compose v2 installed.
  - Deploy user can run Docker (be in 'docker' group or use sudo and adjust commands).

Configure
---------
Edit these in Jenkinsfile:
  DEPLOY_HOST, DEPLOY_USER, DEPLOY_PATH, DEPLOY_SSH

Typical Jenkins job
-------------------
- Pipeline from SCM (point to your Git repo).
- No parameters required.
- Trigger on Git push (optional webhook).

Rollback
--------
- Re-run an older Git commit through the pipeline, or on the server:
    cd /opt/student-registration-app
    git checkout <old-commit>
    docker compose up -d --build

Notes
-----
- If sudo is required for Docker on the server, change commands to 'sudo docker ...'.
- Add a 'Test' stage before Deploy if you want linting/test gates.
