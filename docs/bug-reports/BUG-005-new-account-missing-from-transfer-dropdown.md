# BUG-005 — Newly opened account not immediately available in Transfer Funds dropdown

## Summary
After successfully opening a new account via the **Open New Account** page, the new account does not appear in the source or destination dropdowns on the **Transfer Funds** page if the user navigates there immediately. The UI renders a stale account list, omitting the just-created account until the page is reloaded or sufficient time has passed for the backend to complete the account creation.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-005 |
| **Status** | Open |
| **Severity** | Medium |
| **Priority** | P2 |
| **Component** | UI / Race Condition / Data Freshness |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | Chromium, Firefox, WebKit |
| **Discovered During** | UI Testing / E2E Testing |
| **Related Test** | `conftest.py::registered_user`, `tests/test_e2e.py`, `tests/test_transfer.py` |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Log in to ParaBank with valid credentials.
2. Navigate to **Open New Account**.
3. Select account type (e.g., Savings) and click **Open New Account**.
4. Observe the success confirmation showing the new account number.
5. **Immediately** navigate to **Transfer Funds**.
6. Inspect the **From Account** and **To Account** dropdown options.

---

## Expected Result
The newly created account should appear in both dropdowns on the Transfer Funds page, since it was successfully created and confirmed by the server in the previous step.

## Actual Result
The new account is absent from the dropdown list. Only the original account(s) that existed before the new account was opened are present. The new account only becomes available after a full page reload or waiting several seconds before navigating to Transfer Funds.

---

## Evidence

- **Test file:** `conftest.py::registered_user` fixture
- **Root cause identified during test development:** The Open New Account page uses an AJAX call to create the account. The confirmation is displayed before the account is fully committed and reflected in the accounts list endpoint. A programmatic workaround — explicitly waiting for the new account's `<option>` element to appear in the `select#fromAccountId` dropdown using `page.wait_for_selector("select#fromAccountId option[value]")` — was required to make the test suite reliable. Without this wait, the test suite experienced silent failures where the downstream transfer step operated without a valid second account.
- The workaround is in place in the test suite but the underlying UI bug is unfixed.

---

## Impact
Users who open a new account and immediately attempt to use it for a transfer will not find it in the dropdown and may believe the account creation failed. This creates a poor user experience and potential for duplicate account creation attempts. It is a particularly disruptive race condition because the creation success message has already been shown to the user.

---

## Suggested Fix
The Transfer Funds page (or the component that populates the account dropdowns) should fetch the account list fresh from the server each time the page is loaded, rather than relying on a cached or pre-loaded list. Alternatively, the Open New Account flow should not display the success state until the account is fully available in the accounts endpoint — confirmed by a follow-up GET request before rendering the confirmation message.