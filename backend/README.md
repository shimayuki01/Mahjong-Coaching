# backend

A small Flask backend that runs `mjai-reviewer` in Docker and returns HTML output.

## Requirements

- Python 3.10+
- Docker installed and usable by this user
- `mjai-reviewer:latest` or another OCI image available locally or pullable

## Install

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
cd backend
python app.py
```

The service listens on `http://0.0.0.0:8000`.

## Usage

### JSON body

```bash
curl -X POST http://localhost:8000/report?seat=0 \
  -H "Content-Type: application/json" \
  -d @../akochan-docker/mjai-reviewer/test.json > report.html
```

### File upload

```bash
curl -X POST http://localhost:8000/report?seat=0 \
  -F "file=@../akochan-docker/mjai-reviewer/test.json" > report.html
```

## Environment

- `MJAI_REVIEWER_IMAGE`: optional image name, default `mjai-reviewer:latest`
