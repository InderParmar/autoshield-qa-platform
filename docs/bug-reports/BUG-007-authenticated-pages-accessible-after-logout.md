# BUG-007 — Authenticated pages accessible via browser back button after logout

## Summary
After a user logs out of ParaBank, navigating back using the browser's back button renders previously visited authenticated pages (such as Accounts Overview and Transfer Funds) from the browser cache without redirecting to the login page. The application does not set appropriate cache-control headers to prevent authenticated page content from being stored and re-served after session termination.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-007 |
| **Status** | Open |
| **Severity** | Medium |
| **Priority** | P2 |
| **Component** | Session Management / Security |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | Chromium, Firefox, WebKit |
| **Discovered During** | Exploratory Testing |
| **Related Test** | `tests/test_login.py::test_logout` |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Log in to ParaBank with valid credentials.
2. Navigate to **Accounts Overview** — allow the page to fully load.
3. Navigate to **Transfer Funds** — allow the page to fully load.
4. Click **Log Out**.
5. Confirm the logout success message is displayed and you are on the login page.
6. Click the browser **Back** button once or twice.
7. Observe which page is rendered and whether account data is visible.

---

## Expected Result
Clicking the browser back button after logout should either:
- Redirect the user to the login page immediately, or
- Display an empty / expired page with no authenticated content visible.

The user's account data must not be visible after logout under any navigation method.

## Actual Result
The browser renders the cached version of the previously visited authenticated page (e.g., Accounts Overview showing account balances, or Transfer Funds). The account data is visible without re-authentication. This occurs because the server does not send `Cache-Control: no-store` or equivalent headers on authenticated pages, allowing the browser to serve them from its local cache after the session has ended.

---

## Evidence

- **Test file:** `tests/test_login.py::test_logout` — the current logout test verifies that the logout action lands on the correct page, but does not assert the back-navigation behaviour. This gap was identified during manual exploratory testing following the automated test run.

---

## Impact
On a shared or public device (library computer, shared workstation), a subsequent user can press the back button after the original user logs out and view the previous user's full account information — balances, account numbers, and transaction history — without any credentials. This is a session data exposure risk that disproportionately affects users on shared devices.

This maps to **OWASP Web Security Testing Guide — WSTG-SESS-006: Testing for Logout Functionality**.

---

## Suggested Fix
All responses serving authenticated page content should include the following HTTP headers to prevent browser caching:

```
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Expires: 0
```

Additionally, the application should implement a client-side navigation guard that checks session state on page load and redirects to the login page if no valid session exists, providing a second layer of defence independent of cache headers.