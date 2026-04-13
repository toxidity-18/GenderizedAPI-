# Genderized API

A backend API built with **FastAPI** and deployed on **Vercel** for the Stage 0 Backend Assessment.

This API integrates with the **Genderize.io API**, processes the raw response, and returns a standardized enriched result.

---

## Live API

Base URL:

```text
https://genderized-api.vercel.app
````

Endpoint:

```text
GET /api/classify?name=<name>
```

Example:

```text
https://genderized-api.vercel.app/api/classify?name=john
```

---

## Features

* Calls the external Genderize API
* Renames `count` → `sample_size`
* Computes `is_confident`
* Adds `processed_at` timestamp (UTC ISO 8601)
* Handles edge cases and errors
* Includes CORS support
* Deployed publicly on Vercel

---

## Success Response

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-13T20:40:00Z"
  }
}
```

---

## Error Responses

### Missing or empty name (400)

```json
{
  "status": "error",
  "message": "Name query parameter is required and cannot be empty"
}
```

### No prediction available (404)

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

### External API timeout (502)

```json
{
  "status": "error",
  "message": "External API timeout"
}
```

---

## Confidence Logic

```text
is_confident = probability >= 0.7 AND sample_size >= 100
```

If either condition fails, `is_confident` returns `false`.

---

## Local Development

Clone the repository:

```bash
git clone https://github.com/toxidity-18/GenderizedAPI-.git
cd GenderizedAPI-
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
uvicorn api.index:app --reload --port 3000
```

Test locally:

```text
http://localhost:3000/api/classify?name=john
```

---

## Project Structure

```text
GenderizedAPI-/
├── api/
│   └── index.py
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

---

## Tech Stack

* Python
* FastAPI
* httpx
* Vercel

---

## GitHub Repository

* **GitHub Repo:** https://github.com/toxidity-18/GenderizedAPI-
* **Live API:** https://genderized-api.vercel.app


