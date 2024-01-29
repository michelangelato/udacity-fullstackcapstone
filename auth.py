# Libraries
import os
import json
from flask import request, jsonify
from functools import wraps
import jwt
from urllib.request import urlopen
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ['API_AUDIENCE']


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
'''
get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    return parts[1]

'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True

# Convert base64 to int
def base64url_to_int(value):
    # Decode Base64 URL and convert to integer
    padded_value = value + '=' * (4 - len(value) % 4)  # Add padding if necessary
    decoded_bytes = base64.urlsafe_b64decode(padded_value.encode('utf-8'))
    return int.from_bytes(decoded_bytes, 'big')

# Convert the key from JWK to PEM
def jwk_to_pem(jwk):
    if jwk['kty'] != 'RSA':
        raise ValueError("Unsupported key type. Only RSA keys are supported.")

    public_numbers = rsa.RSAPublicNumbers(
        base64url_to_int(jwk['e']),
        base64url_to_int(jwk['n'])
    )

    public_key = public_numbers.public_key(default_backend())
    pem_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_key.decode('utf-8')

# Get public key from Auth0
def get_public_key(jwks_url, kid):
    # Fetch JWKS from the well-known JWKS endpoint
    jwks_response = urlopen(jwks_url)
    jwks_data = json.loads(jwks_response.read())

    # Find the public key associated with the given 'kid' (Key ID)
    for key in jwks_data['keys']:
        if key['kid'].strip() == kid.strip():
            key_type = key.get('kty')
            return jwk_to_pem(key)

    return None

'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # Prepare auth0 url
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

    try:
        # Decode the header of the token to get the 'kid' (Key ID)
        header = jwt.get_unverified_header(token)
        kid = header['kid']

        # Get the public key using the 'kid'
        public_key = get_public_key(jwks_url, kid)

        if public_key:
            # Verify the token using the retrieved public key
            payload = jwt.decode(
                token,
                public_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            print("Token verification successful")
            return payload
        else:
            print("Public key not found for the specified 'kid'")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)

    except jwt.ExpiredSignatureError as e:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token has expired.'
        }, 401)
    except jwt.InvalidTokenError as e:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Please, check the audience and issuer.'
        }, 401)
    except Exception as e:
        print(f'e: {e}')
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 401)

'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                #return f(payload, *args, **kwargs)
                return f(*args, **kwargs)
            except AuthError as auth_error:
                # Handle AuthError and return the appropriate HTTP response
                return jsonify({
                    'success': False,
                    'error': auth_error.status_code,
                    'message': auth_error.error,
                }), auth_error.status_code

        return wrapper

    return requires_auth_decorator
