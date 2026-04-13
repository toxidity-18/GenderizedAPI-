from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_API_URL = "https://api.genderize.io"

@app.get("/api/classify")
async def classify_name(name: Optional[str] = Query(None)):
    
    # 400 missing or empty
    if name is None or name.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Name query parameter is required and cannot be empty"
            }
        )

    clean_name = name.strip()

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(
                GENDERIZE_API_URL,
                params={"name": clean_name}
            )
            response.raise_for_status()
            data = response.json()

        gender = data.get("gender")
        probability = float(data.get("probability") or 0)
        count = int(data.get("count") or 0)

        # edge case
        if gender is None or count == 0:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No prediction available for the provided name"
                }
            )

        sample_size = count
        is_confident = (
            probability >= 0.7 and sample_size >= 100
        )

        processed_at = datetime.utcnow().isoformat() + "Z"

        return {
            "status": "success",
            "data": {
                "name": clean_name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }

    except httpx.TimeoutException:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "External API timeout"
            }
        )

    except httpx.HTTPStatusError:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "External API error"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )