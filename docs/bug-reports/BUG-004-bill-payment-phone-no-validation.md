# BUG-004 — Bill payment phone number field accepts non-numeric and invalid format input

## Summary
The **Phone Number** field on the Bill Payment form applies no client-side or server-side format validation. Alphabetical characters, special characters, and arbitrarily short strings are accepted without error, allowing semantically invalid phone numbers to be stored against a payee record.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-004 |
| **Status** | Open |
| **Severity** | Low |
| **Priority** | P3 |
| **Component** | UI / Input Validation |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | Chromium, Firefox, WebKit |
| **Discovered During** | UI Testing |
| **Related Test** | `tests/test_bill_payment.py` |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Log in to ParaBank with valid credentials.
2. Navigate to **Bill Pay**.
3. In the **Phone** field, enter an invalid value such as `abc!!!xyz`.
4. Fill in the remaining required fields with valid data (payee name, address, account number, amount).
5. Click **Send Payment**.
6. Observe whether the submission is accepted or rejected.

---

## Expected Result
The form should reject the submission and display a validation error such as: *"Please enter a valid phone number"*. Only numeric characters (with optional standard formatting such as dashes or parentheses) should be accepted.

## Actual Result
The form accepts the submission with the invalid phone number. The payment is processed successfully and the payee record is stored with the invalid phone value (e.g., `abc!!!xyz`).

---

## Evidence

- **Test file:** `tests/test_bill_payment.py` — valid test data from `test_data/bill_payment_data.json` always passes. The absence of a rejection test for invalid phone numbers reflects the discovery that no such validation exists.
- The HTML `<input>` element for the phone field is of type `text` with no `pattern` attribute, confirming there is no browser-level constraint applied.

---

## Impact
Payee records can be stored with nonsensical phone numbers, corrupting data quality. In a production system this could cause failures in downstream processes such as SMS notifications, automated dialling systems, or third-party payment gateway integrations that expect a valid phone number format.

---

## Suggested Fix
Apply a `pattern` attribute on the input field (e.g., `pattern="[0-9]{10}"`) for client-side enforcement, and add server-side validation using a regular expression to reject non-numeric or improperly formatted phone numbers before persisting the payee record.