# Joke-Witter

# Introduction
An API to simulate a recommendation engine using generated pickled data.

# Table of content
1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Error Handling](#error-handling)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- Basic understanding of HTTP requests

### Installation

To start using the API, you need to install the necessary dependencies:

For Python:
```bash
$ pip install requests
```

From the cli/curl:
_curl comes preinstalled on most linux distributions_
_if not installed, you can get it from your distribution's package manager_
```
# Arch
$ sudo pacman -S curl

# Ubuntu
$ sudo apt install curl
```

### Making Your First Request

Here's an example of how to make a request to the API:

For Python:
```
import requests

url = "https://api.yourservice.com/v1/endpoint"
headers = {"Authorization": "Bearer <TOKEN>"}
response = requests.get(url, headers=headers)
print(response.json())
```

For Curl:
```
$ curl -X GET "http://127.0.0.1:5000/api/v1/user/main/populate" -H "accept: application/json" -H "Authorization: Bearer <TOKEN>"
```

## Authentication

Authentication is required for selected endpoints. You must include the token in the `Authorization` header of each request:

```
Authorization: Bearer <TOKEN>
```

## Endpoints

Visit [Api Docs](http://127.0.0.1:5000/api/v1/apidocs) to see full documentation on endpoints

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of an API request. 

- `200 OK`: The request was successful.
- `201 CREATED`: The request successfully created an item in the server.
- `400 Bad Request`: The request could not be understood or was missing required parameters.
- `401 Unauthorized`: Authentication failed or user does not have permissions for the requested operation.
- `403 Forbidden`: Authentication succeeded but authenticated user does not have access to the requested resource.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred on the server.
