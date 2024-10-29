from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL")

app = FastAPI()
#paymrent endpoint
@app.post("/payment")
async def process_payment(user: str, amount: float):
    async with httpx.AsyncClient() as client:
        auth_response = await client.get(AUTH_SERVICE_URL + "/auth/health")
        search_response = await client.get(SEARCH_SERVICE_URL + f"/search?query={user}")

        if auth_response.status_code != 200 or search_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Dependencies not responding")

    return {"message": f"Payment of ${amount} for {user} processed successfully."}


@app.get("/health")
def health_check():
    return {"status": "service payment running"}
