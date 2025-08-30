Student Registration App (Flask + MySQL + Docker)
=================================================

What you get
------------
- A simple HTML app to register students for IT courses and store them in MySQL.
- A reporting page to view/search registrations.
- Fully containerized with Docker Compose (app + MySQL).

Quick start
-----------
1) Prerequisites: Docker Desktop (or Docker Engine) with Compose v2.
2) Extract this folder.
3) In a terminal, cd into the folder and run:
   docker compose up -d --build

4) Open the app:
   http://localhost:8000       -> Registration form
   http://localhost:8000/report -> Reporting page

5) Stop everything:
   docker compose down

Default DB creds (for demo only)
--------------------------------
- Host: db (inside Compose network), 127.0.0.1:3307 from your machine
- Database: training_center
- User: appuser
- Password: apppass
- Root password: rootpass

You can change these in docker-compose.yml and the `app` service environment variables.

Files
-----
- docker-compose.yml
- db/init.sql
- app/Dockerfile
- app/requirements.txt
- app/app.py
- app/templates/{base.html, index.html, report.html}
- app/static/style.css

Notes
-----
- For production, set a strong FLASK_SECRET_KEY and use non-default DB credentials.
- Backups: the MySQL data is persisted in a named Docker volume `db_data`.
- The app listens on port 8000 on your machine (maps to Flask 5000).

Troubleshooting
---------------
- If the app page shows a DB error, make sure the `db` container is healthy:
  docker compose ps
  docker compose logs db

- To inspect the DB from your host:
  mysql -h 127.0.0.1 -P 3307 -u appuser -papppass training_center
