# Auth

A small FastAPI service that handles login once and issues short-lived codes other local apps can exchange for a user's identity, in the shape of an OAuth authorization-code flow. Currently used by [`pr-agent`](https://github.com/Vainius2002/local-agent).

## How it works

- `/login` shows a username/password form. Passwords are hashed with Argon2.
- On success, it opens a session (cookie plus a row in `sessions`) valid for 7 days.
- `/authorize?redirect_uri=...` checks the session, verifies the redirect URI against an allowlist, issues a one-time code valid for 3 minutes, and redirects back to the caller with it.
- `/token` exchanges a valid code for the user's id and username, then deletes the code so it can't be reused.
- `/` is a simple endpoint other apps can hit to check whether a session is still valid.

## Setup

1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your own values.
4. `alembic upgrade head`
5. Start the app, then hit `GET /login-creation` once to create the first user from the `USERNAME`/`PASSWORD` in `.env`.
6. Generate a self-signed cert if you don't already have one: `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes`
7. `uvicorn app.main:app --host 0.0.0.0 --port 6969 --ssl-keyfile=key.pem --ssl-certfile=cert.pem`

Browsers will flag the self-signed certificate as untrusted; that's expected for local use.

## Used by

Other apps redirect unauthenticated users here and exchange the resulting code for a user identity through `/token`. See [`pr-agent`](<link-to-pr-agent-repo>) for a working example of that flow.
