````markdown
# GenderizedAPI 

A serverless API built with **FastAPI** and deployed on **Vercel** that integrates with the **Genderize.io API**.

It processes the external response by:

- Renaming `count` → `sample_size`
- Adding `is_confident`
- Adding `processed_at`
- Returning standardized error responses

---

## Endpoint

### GET `/api/classify?name={name}`

Example:

```bash
https://your-app.vercel.app/api/classify?name=john
````

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
    "processed_at": "2026-04-13T12:34:56Z"
  }
}
```

---

## Error Responses

### 400 – Missing name

```json
{
  "status": "error",
  "message": "Name query parameter is required and cannot be empty"
}
```

### 404 – No prediction

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

### 502 – External API failure

```json
{
  "status": "error",
  "message": "External API timeout"
}
```

---

## Logic Used

```text
is_confident = probability >= 0.7 AND sample_size >= 100
```

---

## Run Locally

```bash
git clone https://github.com/yourusername/genderize-vercel.git
cd genderize-vercel

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
uvicorn api.index:app --reload --port 3000
```

Test:

```bash
http://localhost:3000/api/classify?name=john
```

---

## Deploy

```bash
vercel --prod
```

---

## Project Structure

```text
GenderizeAPI/
├── api/
│   └── index.py
├── requirements.txt
├── vercel.json
└── README.md
```

---

## Tech Stack

* Python
* FastAPI
* httpx
* Vercel

---

## Live URL

```bash
https://your-app.vercel.app
```

```
```
