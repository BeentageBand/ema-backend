# User Guide

## Endpoints

EMA runs in http://127.0.0.1:8000

Endpoint documentation can be checked in
http://127.0.0.1:8000/doc

## Register as new User

In order to create a new User,
execute the following command with the right info.
This new user can look at `r'^user/$` path and only authenticated users are capable of using this APIs
```
POST api/user/register
```
Payload

```json
{
  "username": "string",
  "password": "string",
  "email": "user@example.com"
}
```

## Look for Events

User and Admin can look at all events.














