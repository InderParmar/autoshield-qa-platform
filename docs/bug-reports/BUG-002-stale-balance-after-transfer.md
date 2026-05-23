# BUG-002 — Account overview displays stale balance after fund transfer

## Summary
After a successful fund transfer, the account overview page continues to display the pre-transfer balance. The balance only reflects the change after a manual page refresh or re-navigation, indicating the UI is rendering cached data rather than fetching the updated state from the server.

---

## Metadata

| Field | Value |
|---|---|
| **Bug ID** | BUG-002 |
| **Status** | Open |
| **Severity** | Medium |
| **Priority** | P2 |
| **Component** | UI / Data Freshness |
| **Environment** | https://parabank.parasoft.com |
| **Browser** | Chromium, Firefox, WebKit (most pronounced on WebKit) |
| **Discovered During** | UI Testing |
| **Related Test** | `tests/test_transfer.py::test_transfer_updates_account_balance` |
| **Reported By** | Inderpreet Singh Parmar |
| **Date Reported** | 2026-05-22 |

---

## Steps to Reproduce

1. Log in to ParaBank with valid credentials.
2. Navigate to **Accounts Overview** and note the current balance for Account A.
3. Navigate to **Transfer Funds**.
4. Transfer any amount from Account A to Account B.
5. Confirm the transfer success message is displayed.
6. Navigate back to **Accounts Overview** without refreshing the page.
7. Observe the balance displayed for Account A.

---

## Expected Result
Account A's balance on the overview page should reflect the deducted transfer amount immediately after the successful transfer.

## Actual Result
Account A's balance displays the original pre-transfer value. The correct updated balance only appears after a hard refresh (`F5`) or navigating away from the page and returning.

---

## Evidence

- **Test file:** `tests/test_transfer.py::test_transfer_updates_account_balance`
- **Note:** This test experiences intermittent failures specifically on WebKit due to more aggressive page caching behaviour. The failure is reproducible manually. The test was not modified — the intermittent failure is accepted as a known application bug, not a test defect. Documented in `pytest.ini` via `--reruns 2 --reruns-delay 120`.

---

## Impact
Users performing transfers may believe the operation failed or resulted in a different amount because the displayed balance does not match the expected post-transfer state. This creates confusion and could cause duplicate transfer attempts.

---

## Suggested Fix
After a successful transfer, the application should either: (a) invalidate the cached account overview data and force a fresh fetch from the server before rendering the page, or (b) update the balance in the client-side state directly using the known transfer amount returned in the success response.