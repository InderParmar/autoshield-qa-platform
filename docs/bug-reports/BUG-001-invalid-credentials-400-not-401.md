# BUG-001 — REST API returns HTTP 400 instead of HTTP 401 for invalid login credentials

## Summary
The ParaBank REST API login endpoint returns `400 Bad Request` when credentials are invalid, instead of the semantically correct `401 Unauthorized`. This violates the HTTP specification and misleads API consumers about the nature of the failure.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-001 |
| **Status** | Open |
| **Severity** | Medium |
| **Priority** | P2 |
| **Component** | REST API |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | N/A |
| **Discovered During** | API Testing |
| **Related Test** | `api_tests/test_auth.py::test_login_invalid_credentials` |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Send a GET request to the ParaBank login endpoint with invalid credentials:
   ```
   GET https://parabank.parasoft.com/parabank/services/bank/login/invaliduser/wrongpassword
   Accept: application/json
   ```
2. Observe the HTTP response status code.

---

## Expected Result
The server should return `401 Unauthorized`, indicating that authentication failed — the request was understood but the credentials were rejected.

## Actual Result
The server returns `400 Bad Request` with an error body. HTTP 400 indicates a malformed or invalid request (client syntax error), which is factually incorrect — the request is well-formed, the credentials are simply wrong.

```
HTTP/1.1 400 Bad Request
{"error": "could not find login details with username: invaliduser"}
```

---

## Evidence

- **Test file:** `api_tests/test_auth.py`
- **Note:** Both the Python test suite and Postman collection were updated to assert `400` after confirming this is the actual server behaviour, not a test error. The expected status code was initially written as `401` and then corrected when the real response was observed.

---

## Impact
Any API consumer or automated test that follows the HTTP specification and expects `401` for failed authentication will incorrectly treat this as a bad-request error rather than an authentication failure. This also complicates generic error-handling middleware that branches on standard HTTP status codes.

---

## Suggested Fix
The login controller should return `401 Unauthorized` (with a `WWW-Authenticate` header where applicable) when credentials are not found or do not match, and reserve `400` for genuinely malformed requests such as missing or improperly structured parameters.