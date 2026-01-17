# Fast-Translit Backend

![Alt text](Static/sample.png)

This project is a **FastAPI-based backend service** that accepts user input (name and address), transliterates the text using **AI4Bharat’s Indic Transliteration Engine**, and stores the processed records in PostgreSQL for retrieval. The system is designed to be simple, deterministic, and production-aligned, with a clear separation of concerns between API, database, business logic, and AI processing.

---

## High-Level Flow

1. Client sends a `POST` request to the API with `name` and `address`
2. Backend receives the request via FastAPI
3. Text is passed to the AI4Bharat transliteration engine
4. Transliteration output is generated
5. Transliterated data is persisted in PostgreSQL
6. Saved record is returned as API response

---

## Project Structure

```
Fast-Translit/
├── Backend/
│   ├── main.py          # FastAPI app entry point
│   ├── db.py            # Database engine & session management
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud_helper.py   # Database CRUD + transliteration logic
│   ├── translit.py      # AI4Bharat transliteration wrapper
│   ├── create_db.py     # One-time DB table creation
│   ├── rabbitmq.py      # (Optional) async messaging support
│   └── __init__.py
├── requirements.txt
├── README.md
└── .env                 # Environment variables (not committed)
```

---

## Transliteration Logic

- The project uses **AI4Bharat XlitEngine**.
- All input text is transliterated (no script detection checks).
- Hindi (`hi`) is used as the language code by default.
- Beam search is enabled for better transliteration quality.

![Alt text](Static/output.png)

Example:

```
नमस्ते → namaste
दिल्ली भारत → dilli bhaarat
```

---

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **AI Transliteration**: AI4Bharat Indic Transliteration
- **ASGI Server**: Uvicorn
- **Python Version**: 3.10 (strictly recommended)

---

## Version Requirements (IMPORTANT)

To avoid runtime issues, use the exact versions below where possible.

### Python

```
Python 3.10.x
```

> AI4Bharat transliteration is known to be unstable on Python 3.12 and may fail silently.

---

## Installation & Local Setup

This section describes how to set up the project locally on Linux/macOS and Windows.

Prerequisites:
- Python 3.10.x installed
- PostgreSQL installed and running
- git
- (Optional) build tools for some Python wheels (e.g., `build-essential`, `python3-dev` on Linux)

1. Clone the repository

```bash
git clone https://github.com/mradulnatani/Fast-Translit.git
cd Fast-Translit
```

2. Create and activate a virtual environment

Linux / macOS:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Upgrade pip and install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Note: The transliteration dependencies (and `torch` if used) can be large and sometimes require system-specific wheels or CUDA packages. If you encounter issues installing `torch`, consult the official PyTorch installation guide: https://pytorch.org/get-started/locally/

4. Create `.env` file in the project root

Create a `.env` file (this file is not committed to the repo):

```
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/user_data
```

Replace `<password>` with your PostgreSQL password. If you use a different user/host/port/dbname, update accordingly.

5. PostgreSQL: create the database

Start PostgreSQL if it is not running, then create the database:

Using psql (Unix):

```bash
psql -U postgres
postgres=# CREATE DATABASE user_data;
postgres=# \q
```

Or from shell (if you have permissions):

```bash
createdb -U postgres user_data
```

6. Create DB tables

Run the one-time DB creation script:

```bash
python Backend/create_db.py
```

This script will use the `DATABASE_URL` from your `.env` and create the required tables (check `Backend/create_db.py` for the exact behavior).

If you prefer to inspect with psql:

```sql
\c user_data
SELECT * FROM user_submissions;
```

---

## Running the Application (Development)

1. Make sure your virtualenv is activated and `.env` is present.
2. Start the server with uvicorn:

```bash
uvicorn Backend.main:app --reload --host 127.0.0.1 --port 8000
```

- `--reload` enables auto-reload during development.
- The API will be available at: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

Example request using curl:

```bash
curl -X POST "http://127.0.0.1:8000/submit" \
  -H "Content-Type: application/json" \
  -d '{"name":"नमस्ते","address":"दिल्ली भारत"}'
```

Expected response:

```json
{
  "id": 9,
  "name_trans": "namaste",
  "address_trans": "dilli bhaarat"
}
```

---

## Running in Production (Recommendations)

- Use a process manager (systemd, supervisor) or containerization (Docker).
- Serve with multiple worker processes for better concurrency:

Example (uvicorn workers):

```bash
uvicorn Backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use Gunicorn with uvicorn workers:

```bash
gunicorn -k uvicorn.workers.UvicornWorker Backend.main:app -w 4 -b 0.0.0.0:8000
```

- Ensure you secure your database credentials and connection.
- For large-scale deployments, use managed databases, GPU-enabled instances if transliteration inference needs acceleration, and configure proper logging and monitoring.

---

## Environment Variables Reference

- `DATABASE_URL` — SQLAlchemy-compatible PostgreSQL connection string (example above).

If you add more env variables (for messaging, alternate DB, or secrets), list them here.

---

## Troubleshooting

- DB connection issues:
  - Verify `.env` is present and `DATABASE_URL` is correct.
  - Ensure PostgreSQL is running and the database `user_data` exists.
  - Check logs for connection errors.

- Python dependency issues:
  - Use Python 3.10 as recommended.
  - If `pip install -r requirements.txt` fails on `torch` or other heavy libs, consult their official installation docs and install the appropriate wheel for your platform.

- Silent transliteration failures:
  - Ensure `torch` and AI4Bharat dependencies are installed for the correct Python version.
  - Run the server with DEBUG logs: `uvicorn Backend.main:app --reload --log-level debug`

- Permission errors on create_db.py:
  - Run with a DB user that has CREATE TABLE privileges or use a DBA to initialize the schema.

---

## Example API Request

### POST `/submit`

**Request Body**

```json
{
  "name": "नमस्ते",
  "address": "दिल्ली भारत"
}
```

**Response**

```json
{
  "id": 9,
  "name_trans": "namaste",
  "address_trans": "dilli bhaarat"
}
```

---

## Notes & Constraints

- Transliteration quality depends on the AI4Bharat model output.
- Mixed-script input may produce partial transliteration.
- This backend assumes single-language Hindi transliteration by default.
- RabbitMQ integration is optional and currently unused.

---

## Future Enhancements

- Language auto-detection
- Async transliteration via message queue
- Batch submission support
- REST pagination & filtering
- Admin dashboard

