# Cognito Client Credentials

## Getting started

First creat a `.env` file with the following content:

```sh
COGNITO_USER_POOL_ID=<your-pool-id>
COGNITO_USER_POOL_CLIENT_ID=<your-client-id>
COGNITO_USER_POOL_CLIENT_SECRET=<your-client-secret>
COGNITO_OAUTH2_TOKEN_URL=https://yourdomain.us-west-2.amazoncognito.com/oauth2/token
COGNITO_REGION=us-west-2
```

Then install modules:

```sh
pip install requirements.txt
```

Finally run the `main.py` script:

```sh
python main.py
```
