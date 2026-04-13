
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime
from typing import Optional

# Initialize FastAPI application
app = FastAPI()

# Enable CORS so external graders/frontend clients can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow requests from any origin
    allow_credentials=False,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all request headers
)

# External API endpoint
GENDERIZE_API_URL = "https://api.genderize.io"


@app.get("/api/classify")
async def classify_name(name: Optional[str] = Query(None)):
    """
    GET /api/classify?name=<name>

    Calls Genderize API, processes the response,
    and returns standardized output.
    """

    # Validate input:
    # Return 400 if name is missing or empty
    if name is None or name.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Name query parameter is required and cannot be empty"
            }
        )

    # Remove leading/trailing spaces
    clean_name = name.strip()

    try:
        # Call external Genderize API with 3-second timeout
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(
                GENDERIZE_API_URL,
                params={"name": clean_name}
            )
            response.raise_for_status()
            data = response.json()

        # Extract required fields from external response
        gender = data.get("gender")
        probability = float(data.get("probability") or 0)
        count = int(data.get("count") or 0)

        # Handle edge case:
        # If API cannot predict the gender
        if not gender or count <= 0:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "No prediction available for the provided name"
                }
            )

        # Rename count -> sample_size
        sample_size = count

        # Compute confidence logic
        # True only if both conditions are satisfied
        is_confident = (
            probability >= 0.7 and sample_size >= 100
        )

        # Return successful standardized response
        return {
            "status": "success",
            "data": {
                "name": clean_name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": datetime.utcnow().isoformat() + "Z"
            }
        }

    # Handle timeout from external API
    except httpx.TimeoutException:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "External API timeout"
            }
        )

    # Handle external API HTTP errors
    except httpx.HTTPStatusError:
        return JSONResponse(
            status_code=502,
            content={
                "status": "error",
                "message": "External API error"
            }
        )

    # Catch unexpected internal server errors
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error"
            }
        )
