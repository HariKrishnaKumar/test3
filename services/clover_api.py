import httpx
import os
from fastapi import HTTPException

BASE_URL = os.getenv("CLOVER_BASE_URL", "https://apisandbox.dev.clover.com/v3/merchants")

async def make_clover_api_request(merchant_id: str, access_token: str, endpoint: str, params: dict = None):
    """
    A reusable function for making authenticated GET requests to the Clover API.
    """
    url = f"{BASE_URL}/v3/merchants/{merchant_id}/{endpoint}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises HTTPStatusError for 4XX/5XX responses
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"A network error occurred: {e}")
        except httpx.HTTPStatusError as e:
            # Pass the error up to be handled by the specific route
            raise HTTPException(status_code=e.response.status_code, detail=f"Clover API error: {e.response.text}")


async def get_clover_merchant_details(merchant_id: str, access_token: str):
    """Fetches details for a specific merchant."""
    return await make_clover_api_request(merchant_id, access_token, "")


async def get_clover_item_details(merchant_id: str, item_id: str, access_token: str):
    """Fetches details for a specific item, expanding variants."""
    return await make_clover_api_request(merchant_id, access_token, f"items/{item_id}", params={"expand": "variants"})


async def get_clover_categories(merchant_id: str, access_token: str):
    """Fetches all categories for a given merchant from the Clover API."""
    return await make_clover_api_request(merchant_id, access_token, "categories")


async def get_clover_items(merchant_id: str, access_token: str):
    """
    Fetches all items for a merchant, expanding to include variants and categories.
    """
    return await make_clover_api_request(merchant_id, access_token, "items", params={"expand": "variants,categories"})

class CloverAPI:
    def __init__(self, merchant_id: str, access_token: str):
        self.merchant_id = merchant_id
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    async def get_items(self, limit: int = 100, offset: int = 0, expand: str | None = None):
        url = f"{BASE_URL}/{self.merchant_id}/items"
        params = {"limit": limit, "offset": offset}
        if expand:
            params["expand"] = expand
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers, params=params)
            return r.json()

    async def get_categories(self, limit: int = 100, offset: int = 0):
        url = f"{BASE_URL}/{self.merchant_id}/categories"
        params = {"limit": limit, "offset": offset}
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers, params=params)
            return r.json()

    async def get_modifier_groups(self, limit: int = 100, offset: int = 0):
        url = f"{BASE_URL}/{self.merchant_id}/modifier_groups"
        params = {"limit": limit, "offset": offset}
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers=self.headers, params=params)
            return r.json()
