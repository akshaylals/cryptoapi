## API Docs

- get authentication token  
`POST /auth/login`

    Basic Authentication:
    ```http
        Username: <username>
        Password: <password>
    ```

    Response:
    ```js
    {
        "token": <token>
    }
    ```

- Generate RSA certificate  
`POST /certificate`

    Http header:
    ```http
    x-access-tokens: <token>
    ```

    Request body:
    ```js
    {
        "filename": String,
        "algorithm": "RSA",
        "public_exponent": Number, // optional, default 65537
        "key_size": Number, // optional, default 2048
    }
    ```

- Generate Ed25519 certificate  
`POST /certificate`

    Http header:
    ```http
    x-access-tokens: <token>
    ```

    Request body:
    ```js
    {
        "filename": String,
        "algorithm": "Ed25519"
    }
    ```

- Generate Ed448 certificate  
`POST /certificate`

    Http header:
    ```http
    x-access-tokens: <token>
    ```

    Request body:
    ```js
    {
        "filename": String,
        "algorithm": "Ed448"
    }
    ```

- Generate ECC certificate  
`POST /certificate`

    Http header:
    ```http
    x-access-tokens: <token>
    ```

    Request body:
    ```js
    {
        "filename": String,
        "algorithm": "ECC",
        "curve": String
    }
    ```

    valid values for curve: 
    ```js
    "SECP256R1"
    "SECP384R1"
    "SECP521R1"
    "SECP224R1"
    "SECP192R1"
    "SECP256K1"
    "BrainpoolP256R1"
    "BrainpoolP384R1"
    "BrainpoolP512R1"
    "SECT571K1"
    "SECT409K1"
    "SECT283K1"
    "SECT233K1"
    "SECT163K1"
    "SECT571R1"
    "SECT409R1"
    "SECT283R1"
    "SECT233R1"
    "SECT163R2"
    ```

- Get certificate  
`GET /certificate`

    Http header:
    ```http
    x-access-tokens: <token>
    ```

    parameters:
    ```http
    public: <filename>
    private: <filename>
    ````