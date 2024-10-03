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

    public_key = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtSmz0SOwWVmMeCUpxPCu
rF1ZuuUSrT0f/EtRconUbHrW4XmwvW8SdjveaJRaJir/Eh/SMx+mAWFNEMBcoB5Y
XKntGl805lMWkbNpqrMM9DpAcKqFlX9oOLbIeoNQyBaen9kGCrguOWMczuNW7cDA
CUtTinEtTKu++qprzUhHE+iKWUqwagsps/TDh6bsnBceC7m4RaFp1BcajC6vAtg2
zE/rUk//dqbtOBBm0gNOion4veEEjsiEwaqhUUBmLO5aat8XCeVRgbp5CacXmiKE
H3LQcKMx8X4iLWL5joOqRBy+c8lOGxau48OZK7iQi7cWlR216cg0qEdzWVwsjqtG
rH+98/kWSx9qBfdvysrpStRhZC5l9LMTHzcBMu92ZBYuSN9GmeXrnL6M5vVDwRl+
wBmy//cRW6xFl7hQ8A5kv5lqrpYsV2vASaQ49Q8BPNuRuSM4CYnI+sL6cHzqYKsK
bQn6zx/XjeUPoz+HKrUmwKk3dLq8L1W4QZTss7Jq7T0kHfE5+x25pfL//prhS/v1
arGYMX8vMXhttm0cuyEy2W4dEkoOmQX89NgKWk0xtCYohSqyUtdmEYgjplScBJIT
bMSCyXfNVlPLJD630m0orDQv30cGVnFM/29u3wahiIB92SXN2ezVyvOQ4lqkmDqZ
+Q+XuTZp3zRHDhtO6y/KF/MCAwEAAQ==
-----END PUBLIC KEY-----
"""
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
