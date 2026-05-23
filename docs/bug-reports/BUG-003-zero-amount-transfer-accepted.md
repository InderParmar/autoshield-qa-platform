# BUG-003 — Fund transfer form accepts $0.00 as a valid transfer amount

## Summary
The Transfer Funds form performs no validation against a zero-dollar transfer amount. Submitting a transfer of `0` is accepted by both the UI and the backend, which creates a transaction record with a $0.00 value — a meaningless operation that pollutes transaction history with no business value.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-003 |
| **Status** | Open |
| **Severity** | Medium |
| **Priority** | P3 |
| **Component** | UI / Validation |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | Chromium, Firefox, WebKit |
| **Discovered During** | Exploratory Testing |
| **Related Test** | `tests/test_transfer.py` (boundary condition — not currently in test suite) |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Log in to ParaBank with valid credentials.
2. Navigate to **Transfer Funds**.
3. Enter `0` in the **Amount** field.
4. Select a valid source account and a different destination account.
5. Click **Transfer**.
6. Observe the response and check the transaction history for the source account.

---

## Expected Result
The form should reject the submission with a validation error such as: *"Amount must be greater than $0.00"*. No transaction record should be created.

## Actual Result
The transfer is accepted. A confirmation message is displayed and a $0.00 transaction entry is created in the source account's transaction history.

---

## Evidence

- **Test file:** `tests/test_transfer.py` — boundary case identified during exploratory testing while writing the transfer test suite.
- The transfer API endpoint also accepts a zero-value `amount` parameter when called directly, confirming there is no server-side guard either.

---

## Impact
$0 transactions pollute account transaction histories with meaningless entries. In a production system this could also be exploited to probe account relationships or trigger downstream processes (notifications, audit logs, fee calculations) without moving any real funds. It also indicates a gap in boundary-value validation across both the UI and API layers.

---

## Suggested Fix
Add a minimum amount validation rule on both the client (form field) and server (API layer) requiring that `amount > 0`. The UI should display a clear inline error message before submission. The API should return `400 Bad Request` with a descriptive error if a zero or negative amount is submitted.