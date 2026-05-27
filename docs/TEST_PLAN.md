# AutoShield QA Test Plan

**Project:** AutoShield — QA Automation Platform
**Target Application:** ParaBank Demo Banking Application (https://parabank.parasoft.com)
**Author:** Inderpreet Singh Parmar
**Version:** 1.1
**Date:** May 2026
**Repository:** https://github.com/InderParmar/autoshield-qa-platform
**Live Test Results:** https://inderparmar.github.io/autoshield-qa-platform/

---

## 1. Introduction

### 1.1 Purpose
This test plan describes the testing strategy, scope, approach, and coverage for the AutoShield QA Automation Platform. It documents what is tested, why it is tested, how it is tested, and what tools and frameworks are used.

This document is intended to demonstrate the ability to plan, design, and execute a multi-layered QA strategy across UI, API, BDD, and performance testing disciplines.

### 1.2 Project Overview
AutoShield is a five-layer QA automation platform built against ParaBank, a publicly available demo banking application. ParaBank exposes a full web UI and a REST API, making it suitable for demonstrating real-world testing across multiple testing approaches.

The platform covers:
- UI functional testing via Playwright with Page Object Model
- API testing via Python requests and Postman
- Behaviour-Driven Development (BDD) via pytest-bdd 8.x and Gherkin
- Performance baseline testing via Locust
- Continuous integration and live reporting via GitHub Actions and GitHub Pages

---

## 2. Scope

### 2.1 In Scope

**Functional areas under test:**
- User registration (new account creation)
- User authentication (login and logout)
- Account overview and balance display
- Fund transfer between accounts
- Bill payment
- End-to-end user journeys combining the above
- REST API endpoints for authentication, accounts, and transactions

**Test types included:**
- UI functional tests (Playwright + pytest)
- API tests (Python requests + Postman)
- BDD scenario tests (pytest-bdd + Gherkin)
- Performance baseline (Locust)

**Browsers under test:**
- Chromium
- Firefox
- WebKit (Safari engine)

### 2.2 Out of Scope
- Loan request functionality
- Admin panel
- Security penetration testing (bugs noted only — see `docs/bug-reports/`)
- Accessibility testing
- Mobile browser testing
- Database-level testing
- ParaBank backend internals

---

## 3. Test Objectives

1. Verify all critical user journeys complete successfully across three browsers
2. Validate REST API endpoints return correct status codes, response structures, and data
3. Confirm business scenarios are readable and executable in plain English via BDD
4. Establish a performance baseline showing ParaBank handles 50 concurrent users with acceptable response times
5. Ensure the test suite runs automatically on every code push via CI/CD with results published to GitHub Pages

---

## 4. Test Environment

| Component | Details |
|---|---|
| Target URL | https://parabank.parasoft.com |
| API Base URL | https://parabank.parasoft.com/parabank/services/bank |
| OS (CI) | Ubuntu (GitHub Actions — azure runner) |
| OS (local) | macOS / Linux |
| Python version | 3.14 |
| Browser automation | pytest-playwright 0.7.2 / Playwright 1.59.0 |
| Test framework | pytest 9.0.3 |
| BDD framework | pytest-bdd 8.1.0 |
| Performance tool | Locust 2.43.4 |
| CI platform | GitHub Actions |
| Results hosting | GitHub Pages (gh-pages branch) |

### 4.1 Test Data Strategy
- Each test run registers a unique user with a UUID suffix (e.g. `johnwilliam7d631c`) to avoid username conflicts on the shared demo environment
- Registration data stored in `test_data/registration_data.json`
- Bill payment data stored in `test_data/bill_payment_data.json`
- Login data stored in `test_data/login_data.json`
- Transfer data stored in `test_data/transfer_data.json`
- A session-scoped `registered_user` fixture handles user creation once per test run and shares credentials across all test types

### 4.2 Known Environment Constraints
- ParaBank is a shared public demo site — it is not under our control
- The server throttles sustained request sequences, causing intermittent page load delays of 30+ seconds
- The transfer page (`transfer.htm`) is particularly susceptible to throttling
- ParaBank returns HTTP 400 (not 401) for invalid credentials — this is documented as BUG-001 and all assertions reflect actual observed behaviour
- Account balance data on the overview page is served from cache and may not reflect a transfer immediately — documented as BUG-002

---

## 5. Test Approach

### 5.1 Testing Layers

**Layer 1 — UI Functional Tests (`tests/`)**
Playwright automates real browser interactions through the Page Object Model (POM). Each page of the application has a corresponding page class encapsulating its selectors and actions. Tests interact with pages through these classes, never directly with raw selectors. This ensures maintainability — if a selector changes, only the page object requires updating.

**Layer 2 — API Tests (`api_tests/`)**
The `ParaBankClient` class wraps Python's `requests.Session` with pre-configured headers and one method per endpoint. Tests call these methods and assert on response status codes, response structure, and field values. A Postman collection mirrors the Python suite for manual exploration and demonstration.

**Layer 3 — BDD Tests (`bdd/`)**
Business scenarios are written in Gherkin (Given/When/Then) and stored as `.feature` files. Step definitions connect each sentence to the existing POM layer — no duplicate browser logic. This layer demonstrates that tests can be written in a format readable by non-technical stakeholders.

Note on pytest-bdd 8.x: `scenarios()` path resolution changed in version 8.x — paths are now resolved relative to the test file, not the project root. Feature file paths are written as `"../features/login.feature"` from the steps directory.

**Layer 4 — Performance Baseline (`performance/`)**
Locust simulates 50 concurrent users performing login, account retrieval, and transaction queries. The test runs for 60 seconds and produces an HTML report documenting response times and failure rates. This is run manually and the report is committed to the repository. See Section 11 for baseline results.

**Layer 5 — CI/CD Pipeline (`.github/workflows/test_pipeline.yml`)**
GitHub Actions runs the full suite on every push to main across two jobs:
- `ui-bdd-tests`: runs `tests/` and `bdd/` across Chromium, Firefox, and WebKit in a parallel matrix. Each browser deploys its report to `gh-pages/{browser}/`
- `api-tests`: runs after `ui-bdd-tests` completes. Isolated to prevent Cloudflare rate limiting from parallel browser jobs hitting the same origin. Deploys to `gh-pages/api/`

### 5.2 Test Design Approach
- Equivalence partitioning: valid inputs, invalid inputs, boundary inputs (empty fields, wrong credentials, zero amounts)
- Happy path coverage for all critical user journeys
- Negative path coverage for error handling and validation
- Observed behaviour assertions: assertions are written against what the application actually returns, not what HTTP convention suggests
- Soft coupling between layers: BDD step definitions reuse POM classes; API tests reuse the `registered_user` fixture from root conftest

### 5.3 Fixture Architecture

```
conftest.py (root)
├── browser_instance    — session-scoped Playwright browser
├── context             — browser context per session
├── page                — page object per session
├── registered_user     — registers unique user via UI, opens second account
├── base_url            — reads from config.ini
└── test_data           — loads JSON test data files

tests/conftest.py
└── logged_in_page      — navigates to login, logs in as registered_user

api_tests/conftest.py
├── api_client          — ParaBankClient instance
├── authenticated_session — logged-in API session
└── account_ids         — fetches account IDs for registered user

bdd/steps/conftest.py
├── login_page          — LoginPage instance
├── registration_page   — RegistrationPage instance
├── transfer_page       — TransferPage instance
└── accounts_page       — AccountsPage instance
```

**Key implementation detail — `registered_user` fixture:**
After calling Open New Account, the fixture waits explicitly for `select#fromAccountId option` to be present before proceeding. Skipping this wait causes a silent backend failure where the new account is created but not yet reflected in the dropdown. This race condition is documented as BUG-005.

---

## 6. Test Cases

### 6.1 UI — Login (3 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| UI-LOG-01 | `test_valid_login_redirects_to_account` | Valid credentials submitted | Redirected to accounts overview page |
| UI-LOG-02 | `test_invalid_login_shows_error` | Invalid credentials submitted | Error message displayed |
| UI-LOG-03 | `test_empty_credentials_shows_error` | Empty credentials submitted | Error message displayed |

### 6.2 UI — Registration (3 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| UI-REG-01 | `test_valid_registration_shows_welcome` | Valid registration form submitted | Welcome message shown with username |
| UI-REG-02 | `test_duplicate_username_shows_error` | Duplicate username submitted | Duplicate username error shown |
| UI-REG-03 | `test_missing_fields_shows_error` | Required fields left empty | Validation errors shown for missing fields |

### 6.3 UI — Accounts (3 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| UI-ACC-01 | `test_accounts_page_loads_after_login` | Navigate to accounts overview | Page loads with account list visible |
| UI-ACC-02 | `test_account_list_is_not_empty` | Accounts overview rendered | Account list contains at least one entry |
| UI-ACC-03 | `test_total_balance_is_displayed` | Accounts overview rendered | Balance figure is visible and non-empty |

### 6.4 UI — Transfer (3 tests)

| Test ID | Test Name | Scenario | Expected Result | Notes |
|---|---|---|---|---|
| UI-TRF-01 | `test_valid_transfer_shows_success` | Valid transfer between two accounts | Transfer Complete confirmation shown | Known flaky — ParaBank throttling |
| UI-TRF-02 | `test_transfer_zero_amount_shows_error` | Transfer submitted with $0.00 amount | Error message shown | Known flaky — throttling; also documents BUG-003 |
| UI-TRF-03 | `test_transfer_page_loads` | Navigate to transfer funds page | Transfer form with amount input displayed | Known flaky — throttling |

### 6.5 UI — Bill Payment (3 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| UI-BILL-01 | `test_bill_payment_page_loads` | Navigate to bill payment page | Bill payment form is displayed |
| UI-BILL-02 | `test_valid_bill_payment_shows_success` | Valid bill payment submitted | Bill payment success confirmation shown |
| UI-BILL-03 | `test_missing_payee_name_shows_error` | Bill payment submitted with missing payee name | Validation error shown |

### 6.6 UI — End-to-End (2 tests)

| Test ID | Test Name | Scenario | Expected Result | Notes |
|---|---|---|---|---|
| UI-E2E-01 | `test_transfer_updates_account_balance` | Transfer funds and verify balance change | Updated balance reflects transferred amount | Intermittently flaky on WebKit — BUG-002 |
| UI-E2E-02 | `test_full_user_journey` | Login → view accounts → transfer → pay bill | All steps complete without error | |

### 6.7 API — Authentication (3 tests)

| Test ID | Test Name | Scenario | Expected Result | Notes |
|---|---|---|---|---|
| API-AUTH-01 | `test_login_valid_credentials` | Login with valid credentials | 200 response, customer ID returned as integer | |
| API-AUTH-02 | `test_login_invalid_credentials` | Login with invalid credentials | 400 response | ParaBank does not return 401 — see BUG-001 |
| API-AUTH-03 | `test_login_response_time` | Login response timing | Response received under 3000ms | |

### 6.8 API — Accounts (4 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| API-ACC-01 | `test_get_accounts_returns_list` | Fetch all accounts for valid customer | 200 response, non-empty list returned |
| API-ACC-02 | `test_account_schema_validation` | Account object structure | Each account contains id, customerId, balance, type |
| API-ACC-03 | `test_get_single_account` | Fetch single account by ID | 200 response, returned ID matches requested ID |
| API-ACC-04 | `test_get_account_invalid_id` | Fetch account with invalid ID | 400 response |

### 6.9 API — Transactions (3 tests)

| Test ID | Test Name | Scenario | Expected Result |
|---|---|---|---|
| API-TXN-01 | `test_get_transactions_returns_list` | Fetch transactions after a transfer | 200 response, non-empty list returned |
| API-TXN-02 | `test_transaction_schema_validation` | Transaction object structure | Each transaction contains id, amount, date, description |
| API-TXN-03 | `test_transfer_creates_transaction` | Transfer and verify transaction record | Transfer succeeds, transaction appears in history |

### 6.10 BDD — Login (3 scenarios)

| Scenario ID | Test Name | Gherkin Summary | Notes |
|---|---|---|---|
| BDD-LOG-01 | `test_valid_credentials_redirect_to_accounts_overview` | Valid credentials redirect to accounts overview | Known flaky — ParaBank throttling on overview redirect |
| BDD-LOG-02 | `test_invalid_credentials_show_an_error_message` | Invalid credentials show an error message | Stable |
| BDD-LOG-03 | `test_empty_credentials_show_an_error_message` | Empty credentials show an error message | Stable |

### 6.11 BDD — Registration (2 scenarios)

| Scenario ID | Test Name | Gherkin Summary |
|---|---|---|
| BDD-REG-01 | `test_valid_registration_shows_welcome_message` | Valid registration shows welcome message |
| BDD-REG-02 | `test_duplicate_username_shows_an_error` | Duplicate username shows an error |

### 6.12 BDD — Transfer (2 scenarios)

| Scenario ID | Test Name | Gherkin Summary | Notes |
|---|---|---|---|
| BDD-TRF-01 | `test_valid_transfer_shows_success_confirmation` | Valid transfer shows success confirmation | Known flaky — ParaBank throttling |
| BDD-TRF-02 | `test_transfer_page_loads_correctly` | Transfer page loads correctly | Known flaky — ParaBank throttling |

---

## 7. Test Summary

| Layer | Test Count | Location |
|---|---|---|
| UI Functional | 17 | `tests/` |
| API | 10 | `api_tests/` |
| BDD | 7 | `bdd/` |
| **Total automated** | **34** | |
| **CI executions per run** | **102** | 34 tests × 3 browsers |

---

## 8. Known Flaky Tests

The following tests are known to fail intermittently due to ParaBank server throttling. These are **not automation defects** — the underlying test logic is correct. Failures present as `TimeoutError` (30s exceeded) on page load or navigation, not as assertion failures.

| Test | Affected Browsers | Root Cause |
|---|---|---|
| `test_valid_transfer_shows_success` | All | Transfer page throttling |
| `test_transfer_zero_amount_shows_error` | All | Transfer page throttling |
| `test_transfer_page_loads` | All | Transfer page throttling |
| `test_transfer_updates_account_balance` | WebKit most | Balance caching — BUG-002 |
| `test_valid_credentials_redirect_to_accounts_overview` (BDD) | All | Overview redirect throttling |
| `test_valid_transfer_shows_success_confirmation` (BDD) | All | Transfer page throttling |
| `test_transfer_page_loads_correctly` (BDD) | All | Transfer page throttling |

**Mitigation:** `--reruns 2 --reruns-delay 120` in `pytest.ini` retries failed tests twice with a 120-second delay, allowing the server to recover between attempts.

**Typical CI pass rates (when ParaBank is not heavily loaded):**
- Firefox: 24/24
- Chromium: 22–24/24
- WebKit: 22–24/24

---

## 9. Entry and Exit Criteria

### 9.1 Entry Criteria
- Target application (ParaBank) is accessible at `https://parabank.parasoft.com`
- Python dependencies installed from `requirements.txt`
- Playwright browsers installed via `playwright install`
- Valid test user credentials available (registered on ParaBank)
- CI pipeline configured with `contents: write` and `pages: write` permissions for GitHub Pages deployment

### 9.2 Exit Criteria
- All 34 tests collected without import errors
- No test failures caused by automation code defects (throttling-related `TimeoutError` failures are accepted)
- HTML reports generated for all three browsers and API suite
- Reports accessible at `https://inderparmar.github.io/autoshield-qa-platform/`
- Performance baseline report committed at `reports/performance_report.html`
- `--reruns 2 --reruns-delay 120` retry strategy active for throttling resilience

---

## 10. Defect Management

Bugs discovered during test development are documented in `docs/bug-reports/` using the standard template at `docs/bug-reports/BUG_TEMPLATE.md`.

| Bug ID | Title | Severity | Component |
|---|---|---|---|
| BUG-001 | REST API returns HTTP 400 instead of 401 for invalid credentials | Medium | REST API |
| BUG-002 | Account overview displays stale balance after fund transfer | Medium | UI / Caching |
| BUG-003 | Fund transfer form accepts $0.00 as a valid amount | Medium | UI / Validation |
| BUG-004 | Bill payment phone number field accepts non-numeric characters | Low | UI / Validation |
| BUG-005 | Newly opened account not available in transfer dropdown immediately | Medium | UI / Race Condition |
| BUG-006 | Sequential integer IDs enable IDOR (OWASP API1:2023) | High | REST API / Security |
| BUG-007 | Authenticated pages accessible via browser back button after logout | Medium | Session Management |

Each report includes: Bug ID, severity, priority, component, steps to reproduce, expected vs actual behaviour, related test file, impact, and suggested fix.

---

## 11. Performance Baseline Results

**Tool:** Locust 2.43.4
**Configuration:** 50 concurrent users, 5 users/second spawn rate, 60-second duration
**Report:** `reports/performance_report.html`

**Endpoints tested:**
- Login (`on_start` — runs once per user)
- GET accounts for customer (weight 3 — most frequent)
- GET single account details (weight 2)
- GET account transactions (weight 1 — heaviest response)

**Results:**

| Metric | Result |
|---|---|
| Total Requests | 1,408 |
| Total Failures | 0 |
| Failure Rate | **0%** |
| Average Response Time | **83ms** |
| Median (50th percentile) | 81ms |
| 95th Percentile | 92ms |
| 99th Percentile | 110ms |
| Max Response Time | 422ms |
| Requests / Second | ~24 |

**Task distribution (matches weights):**
- viewAccounts: 50%
- getAccountDetails: 33.3%
- getTransactions: 16.7%

All endpoints responded within acceptable thresholds. The login endpoint (422ms max) is the slowest due to session initialisation — this is expected behaviour.

---

## 12. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| ParaBank is a shared demo site and may be throttled | Page loads time out, tests fail | `--reruns 2 --reruns-delay 120` in `pytest.ini` |
| ParaBank parallel browser jobs cause Cloudflare 429 | All API tests rate-limited | API tests isolated in a separate CI job (`needs: ui-bdd-tests`) |
| Parallel gh-pages deployments conflict | Reports not deployed | `keep_files: true` and `continue-on-error: true` on all deploy steps |
| Balance caching causes E2E assertion to fail | `test_transfer_updates_account_balance` fails on WebKit | Accepted known flaky — polling loop checks balance up to 10 times before asserting |
| ParaBank returns 400 not 401 for invalid credentials | Assertions fail if written to HTTP spec | All assertions written against observed actual behaviour — documented as BUG-001 |
| New account AJAX creation race condition | Second account missing from transfer dropdown, silent failure | `registered_user` fixture waits for `select#fromAccountId option` before proceeding |
| pytest-bdd 8.x path resolution change | Feature files not found, import error | `scenarios()` path written as relative to test file: `"../features/login.feature"` |

---

## 13. Tools and Frameworks

| Tool | Purpose | Version |
|---|---|---|
| Python | Primary language | 3.14 |
| Playwright | Browser automation | 1.59.0 |
| pytest-playwright | pytest plugin for Playwright | 0.7.2 |
| pytest | Test runner and framework | 9.0.3 |
| pytest-bdd | BDD layer | 8.1.0 |
| pytest-html | HTML report generation | 4.2.0 |
| pytest-rerunfailures | Flaky test retry | 16.2 |
| Locust | Performance testing | 2.43.4 |
| requests | HTTP client for API tests | 2.33.1 |
| Postman | Manual API exploration | latest |
| GitHub Actions | CI/CD pipeline | — |
| GitHub Pages | Live results hosting | — |

---

## 14. Deliverables

| Deliverable | Location | Status |
|---|---|---|
| UI test suite | `tests/` | ✅ Complete — 17 tests |
| API test suite | `api_tests/` | ✅ Complete — 10 tests |
| BDD test suite | `bdd/` | ✅ Complete — 7 tests |
| Page Object Model | `pages/` | ✅ Complete — 6 page classes |
| API client | `api_tests/api_utils/api_helper.py` | ✅ Complete |
| BDD feature files | `bdd/features/` | ✅ Complete — 3 feature files |
| Postman collection | `postman/` | ✅ Complete |
| Performance test | `performance/locustfile.py` | ✅ Complete |
| Performance baseline report | `reports/performance_report.html` | ✅ Complete |
| CI/CD pipeline | `.github/workflows/test_pipeline.yml` | ✅ Complete |
| Live results dashboard | https://inderparmar.github.io/autoshield-qa-platform/ | ✅ Live |
| Bug reports (7 bugs) | `docs/bug-reports/` | ✅ Complete |
| README | `README.md` | ✅ Complete |
| This test plan | `docs/TEST_PLAN.md` | ✅ Complete |