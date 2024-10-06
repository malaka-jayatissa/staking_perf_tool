import state as state
from config import properties
import requests
import json
import httpx


def send_staking_request( data: dict, jwt_token: str):
    staking_request_url = f'{properties.BASE_URL}/v1/ethereum/validators'
   
   
    headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
    }

 
    response = requests.post(staking_request_url, data=json.dumps(data), headers=headers )
    return (response.status_code, response.json())


async def send_staking_request_async(data: dict, jwt_token: str):
    staking_request_url = f'{properties.BASE_URL}/v1/ethereum/validators'
   
   
    headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
    }
    timeout = httpx.Timeout(600.0, connect=5.0) 

    async with httpx.AsyncClient() as client:
        response = await client.post(staking_request_url, json=data, headers=headers, timeout=timeout)
        return response.status_code, response.json()
