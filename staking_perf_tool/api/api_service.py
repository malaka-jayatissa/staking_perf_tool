import state as state
from config import properties
import requests
from .jwt_token import create_jwt_token, verify_token, sign_with_private_key
import json

def send_staking_request(validator_count: int):
    staking_request_url = f'{properties.BASE_URL}/v1/ethereum/validators'
    data = {
        'network': properties.NETWORK,
        'fee_recipient_address': properties.FEE_RECIPIENT_ADDRESS,
        'withdrawal_address': properties.WITHDRAWAL_ADDRESS,
        'region': properties.REGION,
        'validator_count': validator_count,
        'client_req_id': 'perf_1'
    }
    jwt_token = create_jwt_token(data, 'v1/ethereum/validators')
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
    print(verify_token(jwt_token,public_key))
    print()
    #response = requests.post(staking_request_url, data=json.dumps(data), headers=headers )
    #print(response.status_code)
    #print(response.json())
    state.hello()