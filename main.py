from dotenv import load_dotenv
import os
import requests
import jwt
import json

load_dotenv()


def __get_public_keys():
    public_keys = {}
    response = requests.get(
        f"https://cognito-idp.{os.environ['COGNITO_REGION']}.amazonaws.com/{os.environ['COGNITO_USER_POOL_ID']}/.well-known/jwks.json"
    )
    if response.status_code == 200:
        jwks = response.json()
        for jwk in jwks["keys"]:
            kid = jwk["kid"]
            key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            public_keys[kid] = key

    return public_keys


def __jwt_decode(access_token, public_keys):
    jwt_header = jwt.get_unverified_header(access_token)
    alg = jwt_header["alg"]
    kid = jwt_header["kid"]
    key = public_keys[kid]
    return jwt.decode(
        access_token, key=key, algorithms=[alg], options={"verify_iat": False}
    )


def main():
    client_id = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")
    client_secret = os.environ.get("COGNITO_USER_POOL_CLIENT_SECRET")
    cognito_oauth2_token_url = os.environ["COGNITO_OAUTH2_TOKEN_URL"]
    public_keys = __get_public_keys()
    response = requests.post(
        cognito_oauth2_token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        jwt_payload = __jwt_decode(access_token, public_keys)
        print(jwt_payload)

if __name__ == "__main__":
    main()
