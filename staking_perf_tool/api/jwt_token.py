
import boto3
from botocore.exceptions import ClientError
from config import properties
import base64
import json
import hashlib
import uuid
import time
import jwt

def base64url_encode(data):
    return  base64.urlsafe_b64encode(data).replace(b"=", b"")


def sign_with_private_key(data):
    private_key = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0Tskp/Of4Epqe
K1gI+wtWkoDJL/ump6xDGm/me/gAldDdKUoBx/tnsvxZgPTPSjSbzr+X8vVhncof
SQ4cpQErFogFf2mgabz7NYCHcqtWXYRCp0GfAE0OtHqYX2IygnZsczQDvmn/LUgg
flJ0dKAfvDfcZCQvWQIiZDYvr8fiFmuRsw+CTs2SQXFA9gpYcqfi55WQUrrFVSWD
NKz+23WRkH3nh7Hcl6P8a5WWK+p8gWyTSejjm38/G1XfFRSnqhFzHwfo/TMBHdrX
QAqNsGkrAahBTFbD6PIriFtd7fEbvm6Gf7ok8MfwdBzntv7M3sv2MxSxvSVuJ0a0
qVM/0I5VAgMBAAECggEAIhotn3ijOg7wuf4qLCapJhJW89ZUsxhO8zEenXnwddHg
G1hKFEyp3triMh57DvKywQ5JO/i6kuAoYKLtXZsSvb7I8rs+s9WT5fJgUR3tzIuq
7n1aYrOIn4Ggl02hEbsNoWTnn1amDxqWI/koaLi/KUlsyk0Rb/gWeIE6I2pMdJTl
E5bT/Jsaf4I61M6QDmHy7/04/aYKlKPJP8bgPjFEL5O8q0EZUEl/wSJwyGvpgFq+
qIe35QIpfDU8JNK1iO3exCtjz8eivtTwaah4aeKg57xmeeI4heqwGsiYFFDvDhhT
kAHUAjJlnYw6esehAPtRamHISS8uE4vXoEQvgIYVEQKBgQD92Y38lLUKUmJ99Qzx
xQMv3QgDjd22vepHPsUBhxz0XeImRDtoX8opUynHnoujpPWp2xyHK30Jf8wU2aKa
7d+6G9KkuH3WdAz7bTwNtk6VlsrX9rq/Cl4j6D7d3dk8gdcYMJ5vH8CB0/ODVJyz
WCUZQDQz7xKm7JX+qYyIvtTMUQKBgQC11cNna9SR9rp+77UDA+bQ+29feWRuhyjS
bouU/uxp8H413stBbhS0oFyjx/RrP3JLjPqPrDtifF+j3Z2XepLDz2SNTCx4S0BG
27KaTaf/5zuwRJsywmc3AWei37hGenjdqbqG40nbSNJn+eFnuPol64JA/SqhejjL
gM1/k0kUxQKBgQCYe8F9kro5LAm7zaJr7EMg0i3JLMOczPHYwAzJASdUZry87cmd
xcSDFFCJd2Q79ZAX6uV1EJt4REsLzzuMwwzcF3Btv+DfHDDcKt6jAfqsgrrwBWZh
8VFhUlXJIkUmwnu5LSNObw1NL0scfYvvcyg9xcJV2+shWAY1xhUD41WiMQKBgHrS
xYbaQ1/E9PxBFlfPDt4iuHwZF0nBakWZ/hbKiw6UL+xbbZfor3vCxlCrA+JdnOqD
c8wQXpyLvl6Fl6l2ViSFtjnrNi6bRfOW+vFXex9UJfFOpjaHMgjpngNacrLIj1PL
Df+HD6BbdCRfmW3ieLWcewNC/sTMNgjgG+8ModSxAoGAeStSUufvfkhMLnViqbV4
DL8Dq55U4HFH8Wx90tIvp9OnWYsFGARd/bsshh37KuyRRbf4PiJ4Ss2I4iBrW1z7
fUPhlcIo+rCUxiLGeZ4u7dvh8lo7HEj9JM5S79V+pexCmp0FZzahzjRv9kEYQULu
5mg9ZSUaveHaJ+Em1PTgRYs=
-----END PRIVATE KEY-----
        """
    
    return jwt.encode(data, private_key, algorithm='RS256')

def sign_with_kms(message:bytes):
    kms_client = boto3.client('kms', region_name=properties.SIGNING_KEY_REGION)
    try:
        response = kms_client.sign(
            KeyId=properties.SIGNING_KEY_ID,
            Message=message,
            MessageType='RAW',
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
        )
        return base64url_encode(response['Signature'])
    except ClientError as e:
        print(f"Error during signing: {e}")
        return None


def create_jwt_token(data:dict, url_path:str)->str:
    header = {
    "alg": "RS256",
    "typ": "JWT"
    }
    json_string = json.dumps(data, separators=(',', ':'))
    json_hash = hashlib.sha256(json_string.encode('utf-8')).hexdigest()
    nonce = str(uuid.uuid4())
    iat = int(time.time())
    exp= iat+ 18000
    jwt_body = {
        'urlPath': url_path,
        'bodyHash': json_hash,
        'iat': iat,
        'exp': exp,
        'nonce': nonce, 
        'sub': 'perf_test'
    }
    
    encoded_header = base64url_encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = base64url_encode( json.dumps(
            jwt_body,
            separators=(",", ":"),
        ).encode("utf-8"))
    message = encoded_header + b'.' + encoded_payload
    signature = sign_with_kms(message)
    jwt_token = message.decode("utf-8") + '.' + signature.decode("utf-8")
    return jwt_token


def verify_token(token:str, public_key:str):
    return jwt.decode(token, public_key, algorithms=["RS256"])
